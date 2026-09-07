#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NEUBERECHNUNG der drei chinesischen Entwuerfe — OW-01/Shipyard MODUS B.

Warum Modus B und nicht A:
  construction.md §"Weight Penalty 3": "Jede Konstruktion bekommt automatisch
  Weight Penalty 3 fuer zusaetzliche Systeme." Die Ausnahme gilt nur fuer
  "ein Schiff mit customData.designMode: 'reconstruction' (veroeffentlichte
  Startmasse eines realen Systems)". Diese drei Entwuerfe sind Kampagnenentwuerfe
  ohne reales Vorbild — die Ausnahme steht ihnen NICHT zu.

Die drei Kanaele laufen daher vollstaendig (design_modes.md §1):
  K1 Strukturabgabe   +(adv-disadv) Prozentpunkte, Boden 0 bei adv <= disadv
  K2 Nutzlastmultiplikator  np = 3 + adv - disadv
                            cm: np>=2 -> np ; np==1 -> 2 ; np<=0 -> 1 (geklemmt)
                            final = base * cm * disc * (1+env), dann *3 ausser ctxNoHE
                            (ctxNoHE: *3 entfaellt, dafuer cm zusaetzlich *np)
  K3 Hardwaremassen   reale Massen aus dem Katalog

Penalty-Reduktion durch Forschung (construction.md "Penalty reduzieren":
L1/L2/L3 = -1/-2/-3) ist 2030 NICHT verfuegbar: research.md schaltet L1
fruehestens 2035 frei, und factions.*.research.completedL1/L2/L3 sind leer.
Es bleiben nur benannte Nachteile (je -1).
"""
import math, json, importlib.util

OW = ("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
      "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
spec = importlib.util.spec_from_file_location("nachbau", OW)
nb = importlib.util.module_from_spec(spec); spec.loader.exec_module(nb)
G0 = 9.80665

def k2(base_kg, adv, disadv, disc=1.0, env=0.0, no_he=False):
    """Nutzlastmultiplikator, Raumfahrzeug-Kontext (payload_catalog.md §Multiplier chain)."""
    np_ = 3 + adv - disadv
    if np_ <= 0:  cm, x3 = 1.0, 1.0            # geklemmt: kein *3
    elif np_ == 1: cm, x3 = 2.0, (1.0 if no_he else 3.0)
    else:          cm, x3 = float(np_), (1.0 if no_he else 3.0)
    if no_he and np_ >= 1: cm *= np_
    return dict(np=np_, cm=cm, x3=x3, final=base_kg*cm*disc*(1+env)*x3)

# ---------------------------------------------------------------- Entwuerfe
ENT = {}
ENT["CHN_aufklaerer"] = dict(
  bauname="Himmelsauge", anker_wet_kg=2000.0,
  basis=[("sensor_geo", "Sensor: to GEO (comps)", 1000.0)],
  adv=[], disadv=["Hoher EM-Abdruck", "Doktrinaer gebunden", "Single-Use"],
  begruendung={
    "Hoher EM-Abdruck": "Der Sensor 'bis GEO alles aufdecken' ist ein aktiver Hochleistungs-Emitter. "
        "payload_catalog.md §Suite coupling: einen aktiven Sensor ohne diesen Nachteil zu buchen ist "
        "regelwidrig-nah. Spielwirkung: +1 auf gegnerische Aufklaerung gegen dieses Schiff.",
    "Doktrinaer gebunden": "Fester Aufklaerungsorbit, bodengefuehrte Auftragssteuerung, kein "
        "eigenstaendiges Manoever. Deckt sich mit dem gebuchten dv_kms 0,0. Spielwirkung: -1 Initiative "
        "oder Begleitschutz noetig.",
    "Single-Use": "Nicht betankbar, nicht wartbar, nicht bergbar — eine Aussetzung. "
        "Spielwirkung: einmal einsatzfaehig."},
  struct_class="ruggedized", isp=230, prop="hydrazine", dv_target=50.0, ld=2.5,
  engines=[dict(name="Hydrazin-Monergol 22 N", key="custom_hydrazine_22n", isp=230,
                thrust_n=22, mass_kg=6, count=4, simultaneous=4, propType="hydrazine")],
  house_kw=6.0, batt_hours=0.6, dv_manoever=0.0,
  dv_zweck="Bahnhaltung/Widerstandsausgleich LEO 600 km")

ENT["CHN_scorer"] = dict(
  bauname="Feldzeichen", anker_wet_kg=2000.0,
  basis=[("shipframe", "Spaceship frame (comps)", 1000.0)],
  adv=[], disadv=["Single-Use", "Doktrinaer gebunden", "Fragile Radiatoren"],
  begruendung={
    "Single-Use": "scoring.md: 1 km/s je Scoring-Versuch. Mit 1,0 km/s an Bord ist nach EINEM "
        "Versuch das gesamte Budget fort — das Schiff ist danach traege Masse. Der Nachteil "
        "beschreibt genau den gebuchten Zustand.",
    "Doktrinaer gebunden": "Vorgeplanter Scoring-Korridor, keine eigenstaendige Gefechtsfuehrung; "
        "unbewaffnet. Spielwirkung: -1 Initiative oder Begleitschutz noetig.",
    "Fragile Radiatoren": "Minimaler, ungeschuetzter Radiator an einem billigen Wegwerftraeger. "
        "Spielwirkung: +50 % Ausfall bei Kuehlungstreffer."},
  struct_class="ruggedized", isp=315, prop="mmh_nto", dv_target=1000.0, ld=2.5,
  engines=[dict(name="Bipropellant MMH/NTO 490 N", key="custom_490n_bipro", isp=315,
                thrust_n=490, mass_kg=16, count=1, simultaneous=1, propType="mmh_nto"),
           dict(name="Lageregelung MMH/NTO 22 N", key="custom_bipro_22n", isp=315,
                thrust_n=22, mass_kg=6, count=4, simultaneous=4, propType="mmh_nto")],
  house_kw=3.6, batt_hours=1.2, dv_manoever=1.0,
  dv_zweck="genau ein Scoring-Versuch (scoring.md: 1 km/s je Versuch)")

ENT["CHN_geo_relais"] = dict(
  bauname="Himmelsbruecke", anker_wet_kg=5000.0,
  basis=[("custom_c2relais", "C2-Relaisnutzlast (Antennen, Transponder, Kreuzverbindung)", 150.0)],
  adv=["Strahlungs-Haertung", "Thermischer Betrieb", "Magnetfeld-Toleranz"], disadv=[],
  begruendung={
    "Strahlungs-Haertung": "GEO liegt im aeusseren Strahlungsguertel und im Feld solarer "
        "Teilchenereignisse; 15 Jahre Auslegungsdauer. construction.md Tax-Tabelle: x10 Belastung.",
    "Thermischer Betrieb": "72 min Kernschatten taeglich gegen volle Sonne — die Basis "
        "(-200 C) deckt das nicht ab.",
    "Magnetfeld-Toleranz": "Aufladung und Entladung im GEO-Plasma, das klassische Ausfallmuster "
        "geostationaerer Nachrichtensatelliten."},
  struct_class="ruggedized", isp=1600, prop="xenon", dv_target=750.0, ld=2.6,
  engines=[dict(name="Hall-Triebwerk SPD-100", key="custom_spd100", isp=1600, thrust_n=0.083,
                mass_kg=45, count=4, simultaneous=2, propType="xenon", p_kw=1.35,
                p_count=2, waste_kw=0.54)],
  house_kw=15.0, batt_hours=1.2, dv_manoever=0.0,
  dv_zweck="Nord-Sued-Bahnhaltung GEO, 50 m/s je Jahr x 15 Jahre")

def spec_of(e, pay_final, misc):
    return dict(struct_class=e["struct_class"], adv=len(e["adv"]), disadv=len(e["disadv"]),
                payload_kg=pay_final, misc_kg=misc, house_kw=e["house_kw"],
                pp_type="solar", pp_alpha=15.0, au=1.0, batt_hours=e["batt_hours"],
                batt_alpha=5, rad_alpha=5.0, ld=e["ld"], isp=e["isp"], prop=e["prop"],
                dv_target=e["dv_target"], engines=e["engines"])

def loese_bus(e, pay_final):
    """Bus so, dass die Nassmasse den Anker trifft. Negativ = passt nicht hinein."""
    lo, hi = -e["anker_wet_kg"]*4, e["anker_wet_kg"]*4
    for _ in range(200):
        mid=(lo+hi)/2
        if nb.build(spec_of(e, pay_final, max(mid,0.0) if mid>=0 else mid))["wet"] < e["anker_wet_kg"]:
            lo=mid
        else: hi=mid
    return (lo+hi)/2

HK = {"pay_dry":("Nutzlast / trocken",6.8,58.2), "paybus_dry":("(Nutzlast+Bus) / trocken",17.7,78.2),
      "struct_dry":("Struktur / trocken",10.7,20.6), "dry_wet":("trocken / nass",40.2,93.3),
      "pp_dry":("Kraftwerk+Batterie / trocken",5.0,15.0)}

erg={}
for did,e in ENT.items():
    base = sum(b[2] for b in e["basis"])
    m  = k2(base, len(e["adv"]), len(e["disadv"]))
    m0 = k2(base, 0, 0)     # Vergleich: reine Weight Penalty 3, nichts geheilt
    bus = loese_bus(e, m["final"])
    r_min = nb.build(spec_of(e, m["final"], 0.0))          # Untergrenze: Bus = 0
    r     = nb.build(spec_of(e, m["final"], max(bus,0.0)))
    passt = bus >= 0
    r_ist = r if passt else r_min
    schub_gl = sum(x["thrust_n"]*x.get("simultaneous",x.get("count",1)) for x in e["engines"])
    mt = e["dv_target"]*(r_ist["wet"]+r_ist["dry"])/2/schub_gl
    kenn = dict(pay_dry=100*m["final"]/r_ist["dry"],
                paybus_dry=100*(m["final"]+max(bus,0.0))/r_ist["dry"],
                struct_dry=100*r_ist["struct_kg"]/r_ist["dry"],
                dry_wet=100*r_ist["dry"]/r_ist["wet"],
                pp_dry=100*(r_ist["pp_mass"]+r_ist["batt_mass"])/r_ist["dry"])
    erg[did]=dict(e=e, base=base, m=m, m0=m0, bus=bus, passt=passt, r=r_ist,
                  mt=mt, schub_gl=schub_gl, kenn=kenn)

    print(f"=== {did}  «{e['bauname']}» ===")
    print(f"  Basisnutzlast : " + " + ".join(f"{b[1]} {b[2]:.0f} kg" for b in e['basis']))
    print(f"  Vorteile ({len(e['adv'])}): {', '.join(e['adv']) or '— keine —'}")
    print(f"  Nachteile({len(e['disadv'])}): {', '.join(e['disadv']) or '— keine —'}")
    print(f"  K2  np = 3 + {len(e['adv'])} - {len(e['disadv'])} = {m['np']}"
          f"   cm = {m['cm']:.0f}   Hochenergie x{m['x3']:.0f}"
          f"   -> Nutzlast {base:.0f} -> {m['final']:.0f} kg")
    print(f"      zum Vergleich ohne geheilte Penalty (np=3): {m0['final']:.0f} kg")
    print(f"  K1  Struktur {r_ist['structPct']:.0f} % / Tank {r_ist['tankPct']:.0f} % "
          f"({e['struct_class']} 15/10, Aufschlag {max(0,len(e['adv'])-len(e['disadv']))} Pp)")
    print(f"  trocken {r_ist['dry']:9.1f} kg  Treibstoff {r_ist['prop']:8.1f} kg  "
          f"nass {r_ist['wet']:9.1f} kg   dv {r_ist['dv']:.1f} m/s")
    if passt:
        print(f"  PASST in den Anker {e['anker_wet_kg']:.0f} kg — freier Bus {bus:8.1f} kg")
    else:
        print(f"  PASST NICHT: Untergrenze bei Bus = 0 ist {r_min['wet']:.1f} kg, "
              f"Anker {e['anker_wet_kg']:.0f} kg -> Fehlbetrag {r_min['wet']-e['anker_wet_kg']:+.1f} kg "
              f"({100*(r_min['wet']-e['anker_wet_kg'])/e['anker_wet_kg']:+.1f} %)")
    print(f"  Schub gleichzeitig {schub_gl:.3f} N   Manoeverzeit {mt/3600:.2f} h ({mt/86400:.1f} d)")
    for k,(lbl,lo,hi) in HK.items():
        v=kenn[k]; print(f"    {lbl:<28} {v:6.1f} %  [{'in der Huellkurve' if lo<=v<=hi else f'AUSSERHALB {lo}-{hi} %'}]")
    print()

json.dump({k:dict(base=v["base"], np=v["m"]["np"], cm=v["m"]["cm"], x3=v["m"]["x3"],
                  pay_final=v["m"]["final"], pay_np3=v["m0"]["final"], bus=v["bus"],
                  passt=v["passt"], dry=v["r"]["dry"], prop=v["r"]["prop"], wet=v["r"]["wet"],
                  dv=v["r"]["dv"], mt_s=v["mt"], schub_gl=v["schub_gl"], kenn=v["kenn"],
                  structPct=v["r"]["structPct"], tankPct=v["r"]["tankPct"],
                  struct_kg=v["r"]["struct_kg"], tank_kg=v["r"]["tank_kg"],
                  thr_mass=v["r"]["thr_mass"], pp_mass=v["r"]["pp_mass"],
                  pmad_mass=v["r"]["pmad_mass"], batt_mass=v["r"]["batt_mass"],
                  rad_mass=v["r"]["rad_mass"], pp_cap=v["r"]["pp_cap"], peak_kw=v["r"]["peak_kw"],
                  waste_kw=v["r"]["waste_kw"], D=v["r"]["D"], L=v["r"]["L"],
                  A_front=v["r"]["A_front"], A_side=v["r"]["A_side"])
           for k,v in erg.items()},
          open("Ships/entwuerfe/loesung_chn_modusB.json","w"), indent=1, ensure_ascii=False)
print("-> Ships/entwuerfe/loesung_chn_modusB.json")
