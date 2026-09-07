#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OW-01 Modus A — Rekonstruktion der drei chinesischen Entwuerfe.

Anker sind die in stand/gamestate.json gebuchten Groessen:
  masse_t  (Startmasse, ZH-01-Bodenkonto)   und   dv_kms (Manoeverbudget der Schwarm-Eintraege).
Gesucht ist die Massenaufteilung, NICHT die Masse. Deshalb Modus A:
K1 (Strukturabgabe) laeuft, K2 (Nutzlastmultiplikator) wird uebersprungen,
K3 mit realen Hardwaremassen.  Quelle: nachbau_regeln.md §1.

Loeser: bisection ueber (payload + bus), bis nachbau.build() die Ankermasse trifft.
"""
import math, json, sys, importlib.util

OW = ("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
      "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
spec = importlib.util.spec_from_file_location("nachbau", OW)
nb = importlib.util.module_from_spec(spec); spec.loader.exec_module(nb)

G0 = 9.80665

# --- Entwuerfe: alles ausser (payload_kg, misc_kg) ist gesetzt -----------------
ENT = {}

ENT["CHN_aufklaerer"] = dict(
    anker_wet_kg=2000.0, payload_kg=1000.0,   # Stub-treu: "Sensor 1 t" (construction.md §2)
    struct_class="ruggedized", adv=2, disadv=0,
    adv_namen=["Strahlungs-Haertung", "Thermischer Betrieb"],
    isp=230, prop="hydrazine", dv_target=50.0, ld=2.5,
    engines=[dict(name="Hydrazin-Monergol 22 N", key="custom_hydrazine_22n",
                  isp=230, thrust_n=22, mass_kg=6, count=4, simultaneous=4,
                  propType="hydrazine")],
    house_kw=5.0, pp_type="solar", pp_alpha=15.0, au=1.0,
    batt_hours=0.6, batt_alpha=5, rad_alpha=5.0,          # LEO 600 km: 35 min Kernschatten
    dv_manoever_kms=0.0,
)

ENT["CHN_scorer"] = dict(
    anker_wet_kg=2000.0, payload_kg=200.0,     # Ops-/Wirkpaket, unbewaffnet
    struct_class="ruggedized", adv=3, disadv=0,
    adv_namen=["Strahlungs-Haertung", "Thermischer Betrieb", "Magnetfeld-Toleranz"],
    isp=230, prop="hydrazine", dv_target=1000.0, ld=2.5,
    engines=[dict(name="Hydrazin-Monergol 22 N", key="custom_hydrazine_22n",
                  isp=230, thrust_n=22, mass_kg=6, count=6, simultaneous=6,
                  propType="hydrazine")],
    house_kw=3.0, pp_type="solar", pp_alpha=15.0, au=1.0,
    batt_hours=1.2, batt_alpha=5, rad_alpha=5.0,          # bis GEO: 72 min Kernschatten
    dv_manoever_kms=1.0,
)

ENT["CHN_geo_relais"] = dict(
    anker_wet_kg=5000.0, payload_kg=900.0,     # C2-Relaisnutzlast (+1 Slot, launch_c2 §2.1)
    struct_class="ruggedized", adv=3, disadv=0,
    adv_namen=["Strahlungs-Haertung", "Thermischer Betrieb", "Magnetfeld-Toleranz"],
    isp=1600, prop="xenon", dv_target=750.0, ld=2.6,
    engines=[dict(name="Hall-Triebwerk SPD-100", key="custom_spd100",
                  isp=1600, thrust_n=0.083, mass_kg=45, count=4, simultaneous=2,
                  propType="xenon", p_kw=1.35, p_count=2, waste_kw=0.54)],
    house_kw=15.0, pp_type="solar", pp_alpha=15.0, au=1.0,
    batt_hours=1.2, batt_alpha=5, rad_alpha=5.0,
    dv_manoever_kms=0.0,
)

def als_spec(e, misc):
    """Nutzlast ist FIX (Stub-treu); geloest wird ueber den Bus (misc_kg)."""
    pay = e["payload_kg"]
    return dict(struct_class=e["struct_class"], adv=e["adv"], disadv=e["disadv"],
                payload_kg=pay, misc_kg=misc, house_kw=e["house_kw"],
                pp_type=e["pp_type"], pp_alpha=e["pp_alpha"], au=e["au"],
                batt_hours=e["batt_hours"], batt_alpha=e["batt_alpha"],
                rad_alpha=e["rad_alpha"], ld=e["ld"], isp=e["isp"],
                prop=e["prop"], dv_target=e["dv_target"], engines=e["engines"]), pay, misc

def loese(e):
    lo, hi = 0.0, e["anker_wet_kg"]*2
    for _ in range(200):
        mid = (lo+hi)/2
        s,_,_ = als_spec(e, mid)
        if nb.build(s)["wet"] < e["anker_wet_kg"]: lo = mid
        else: hi = mid
    s, pay, misc = als_spec(e, (lo+hi)/2)
    return s, nb.build(s), pay, misc

HK = {"pay_dry": (6.8, 58.2), "paybus_dry": (17.7, 78.2),
      "struct_dry": (10.7, 20.6), "dry_wet": (40.2, 93.3), "pp_dry": (5.0, 15.0)}

def pruef(v, k):
    lo, hi = HK[k]
    return "in der Huellkurve" if lo <= v <= hi else f"AUSSERHALB {lo}-{hi} %"

out = {}
for name, e in ENT.items():
    s, r, pay, misc = loese(e)
    schub_gl = sum(x["thrust_n"]*x.get("simultaneous", x.get("count",1)) for x in e["engines"])
    mt = e["dv_target"]*(r["wet"]+r["dry"])/2 / schub_gl
    kenn = dict(
        pay_dry=100*pay/r["dry"], paybus_dry=100*(pay+misc)/r["dry"],
        struct_dry=100*r["struct_kg"]/r["dry"], dry_wet=100*r["dry"]/r["wet"],
        pp_dry=100*(r["pp_mass"]+r["batt_mass"])/r["dry"])
    out[name] = dict(spec=s, res=r, pay=pay, misc=misc, mt=mt, kenn=kenn, e=e)

    print(f"=== {name} ===")
    print(f"  Anker      : {e['anker_wet_kg']:.0f} kg nass, dv-Ziel {e['dv_target']:.0f} m/s, Isp {e['isp']} s")
    print(f"  Struktur   : {r['structPct']:.0f} % Struktur / {r['tankPct']:.0f} % Tank "
          f"(ruggedized 15/10 + {e['adv']-e['disadv']} Netto-Vorteile)")
    print(f"  trocken    : {r['dry']:9.1f} kg   Treibstoff {r['prop']:8.1f} kg   nass {r['wet']:9.1f} kg")
    print(f"  Abweichung : {100*(r['wet']-e['anker_wet_kg'])/e['anker_wet_kg']:+.4f} % gegen Anker")
    print(f"  dv (Probe) : {r['dv']:.1f} m/s     Schub gleichzeitig {schub_gl:.3f} N   "
          f"Manoeverzeit {mt/3600:.2f} h ({mt/86400:.1f} d)")
    print(f"  Nutzlast   : {pay:8.1f} kg     Bus {misc:8.1f} kg")
    print(f"  Systeme    : Triebwerke {r['thr_mass']:.1f} · Kraftwerk {r['pp_mass']:.1f} · "
          f"PMAD {r['pmad_mass']:.1f} · Batterie {r['batt_mass']:.1f} · Radiator {r['rad_mass']:.1f} · "
          f"Tank {r['tank_kg']:.1f} · Struktur {r['struct_kg']:.1f}")
    for k, lbl in [("pay_dry","Nutzlast/trocken"), ("paybus_dry","(Nutzlast+Bus)/trocken"),
                   ("struct_dry","Struktur/trocken"), ("dry_wet","trocken/nass"),
                   ("pp_dry","Kraftwerk+Batterie/trocken")]:
        print(f"    {lbl:<26} {kenn[k]:5.1f} %  [{pruef(kenn[k], k)}]")
    print()

json.dump({k: dict(pay=v["pay"], misc=v["misc"], mt_s=v["mt"],
                   dry=v["res"]["dry"], prop=v["res"]["prop"], wet=v["res"]["wet"],
                   dv=v["res"]["dv"], kenn=v["kenn"],
                   schub_gl=sum(x["thrust_n"]*x.get("simultaneous", x.get("count",1)) for x in v["e"]["engines"]),
                   struct_kg=v["res"]["struct_kg"], tank_kg=v["res"]["tank_kg"],
                   thr_mass=v["res"]["thr_mass"], pp_mass=v["res"]["pp_mass"],
                   pmad_mass=v["res"]["pmad_mass"], batt_mass=v["res"]["batt_mass"],
                   rad_mass=v["res"]["rad_mass"], thrust=v["res"]["thrust"],
                   D=v["res"]["D"], L=v["res"]["L"], A_front=v["res"]["A_front"],
                   A_side=v["res"]["A_side"], structPct=v["res"]["structPct"],
                   tankPct=v["res"]["tankPct"], peak_kw=v["res"]["peak_kw"],
                   waste_kw=v["res"]["waste_kw"], pp_cap=v["res"]["pp_cap"])
           for k, v in out.items()},
          open("Ships/entwuerfe/loesung_chn.json","w"), indent=1, ensure_ascii=False)
print("-> Ships/entwuerfe/loesung_chn.json")
