#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ENDFASSUNG der chinesischen Entwuerfe — Spielerentscheid vom Tisch.

Entscheid: die Strukturtonne ist Nutzlast (comps shipframe 1000 kg) und wird
WEGGELASSEN. construction.md §"Struktur = Autonomie (Kernregel)":

  "Die Strukturtonne kauft nicht Rumpf, sondern Autonomie: Bordrechner,
   Selbststeuerung, eigene Feuerleitung. Sie ist ein Bauentscheid und muss
   explizit verbaut sein — ab 10 t gratis (Synergieregel unten), darunter 1 t."
  "Ferngelenkt | Strukturtonne fehlt | Permanenter Kommandolink zu einer
   Steuerstelle (Erde, Traegerschiff, Relais) zwingend"

Damit sinkt die K2-Basis um 1000 kg — genug, um beide Schiffe mit voller
Haertung (Strahlungs-Haertung + Thermischer Betrieb) innerhalb der Werft-
kapazitaet zu bauen. Der Preis ist die Abhaengigkeit vom Kommandolink.

Modus B, alle drei Kanaele: K1 Strukturabgabe, K2 Nutzlastmultiplikator,
K3 Hardwaremassen. Keine Penalty-Reduktion durch Forschung (L1 erst ab 2035).
"""
import importlib.util, json, math
OW=("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
    "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
sp=importlib.util.spec_from_file_location("nb",OW); nb=importlib.util.module_from_spec(sp)
sp.loader.exec_module(nb)

def k2(base, adv, dis, no_he=False):
    """K2 nach nachbau_regeln.md §1 und construction.md — HAUSENTSCHEIDUNG HE-29.

    nachbau_regeln.md §1, Zeile K2, woertlich:
      "np = 3 + adv - disadv, Raumfahrzeug cm = np, dann final = base x cm x disc x (1+env),
       bei High-Energy zusaetzlich x3"
    construction.md §Weight Penalty 3:
      "High-Energy-Systeme (ab ~50 kW, z.B. Laser): ... Zusaetzlich: Dv / 3 und 3x Gewicht"

    Ohne Hochenergie-System gilt also cm = np, sonst nichts.

    REGELLUECKE: payload_catalog.md beschreibt fuer ctxNoHE ein anderes Kalkulatorverhalten —
    "the x3 is cancelled but cm is additionally multiplied by np" — also cm = np x np. Das ist
    ab np 4 TEURER als mit Hochenergie (np 6: Faktor 36 statt 18) und bestraft damit das FEHLEN
    eines 50-kW-Systems staerker als sein Vorhandensein. Das kann keine Regel sein. Gewaehlt
    wird die Lesart von construction.md und nachbau_regeln.md, die untereinander uebereinstimmen.
    """
    np_ = 3 + adv - dis
    if np_ <= 0: return dict(np=np_, cm=1.0, x3=1.0, final=base, no_he=no_he)
    cm = 2.0 if np_ == 1 else float(np_)
    if no_he: return dict(np=np_, cm=cm, x3=1.0, final=base*cm, no_he=True)
    return dict(np=np_, cm=cm, x3=3.0, final=base*cm*3.0, no_he=False)

WIRKUNG = {
 "Strahlungs-Haertung": "x10 Strahlungsbelastung tragbar (construction.md Tax-Tabelle, Stufe 1)",
 "Thermischer Betrieb": "Betrieb ueber der Basis von -200 C (Tax-Tabelle T1)",
 "Hoher EM-Abdruck":    "+1 auf gegnerische Aufklaerung gegen dieses Schiff",
 "Doktrinaer gebunden": "-1 Initiative oder Begleitschutz noetig",
 "Single-Use":          "einmal einsatzfaehig; nicht betankbar, nicht wartbar",
 "Fragile Radiatoren":  "+50 % Ausfall bei Kuehlungstreffer",
}

ENT = {
"CHN_scorer": dict(
  bauname="Feldzeichen", anker=2000.0, klasse="Corvette", zone_bemerkung="LEO/MEO/HEO/SSO/GEO",
  basis=[("custom_opspaket","Ops-Paket: Transponder, Nahbereichssensor, Praesenznachweis",50.0)],
  adv=["Strahlungs-Haertung","Thermischer Betrieb"], dis=[], no_he=True,
  begr={"Strahlungs-Haertung":"Die fuenf Scorer stehen in LEO 600, MEO 20 000, HEO 39 000, SSO 700 "
          "und GEO 35 786 km. MEO liegt im Kern des aeusseren Strahlungsguertels, HEO und GEO im "
          "Feld solarer Teilchenereignisse. 27 von 32 realen Systemen im OW-01-Katalog tragen "
          "diesen Vorteil, Chinas eigene GEO-Systeme TJS und Shijian-21/25 ebenfalls.",
        "Thermischer Betrieb":"Bis zu 72 min Kernschatten gegen volle Sonne, jeden Tag ueber die "
          "Einsatzdauer. Die Basis der Tax-Tabelle (-200 C) deckt das nicht ab.",
        "Doktrinaer gebunden":"Vorgeplanter Scoring-Korridor, bodengefuehrt, unbewaffnet — das "
          "Schiff fuehrt kein eigenstaendiges Gefecht und braucht Begleitschutz."},
  isp=315, prop="mmh_nto", dv=1000.0, ld=2.5, house=3.6, batt=1.2,
  eng=[dict(name="Bipropellant MMH/NTO 490 N", key="custom_490n_bipro", isp=315, thrust_n=490,
            mass_kg=16, count=1, simultaneous=1, propType="mmh_nto"),
       dict(name="Lageregelung MMH/NTO 22 N", key="custom_bipro_22n", isp=315, thrust_n=22,
            mass_kg=6, count=4, simultaneous=4, propType="mmh_nto")],
  dv_man=1.0, dv_zweck="genau ein Scoring-Versuch (scoring.md: 1 km/s je Versuch)",
  rolle="Zonenpraesenz und Scoring"),

"CHN_aufklaerer": dict(
  bauname="Himmelsauge", anker=3600.0, klasse="Corvette", zone_bemerkung="LEO 600 km",
  basis=[("sensor_geo","comps 'Sensor: to GEO' — construction.md §2 'Bis GEO alles aufdecken'",1000.0)],
  adv=["Strahlungs-Haertung","Thermischer Betrieb"],
  dis=["Hoher EM-Abdruck","Doktrinaer gebunden","Single-Use"], no_he=True,
  begr={"Strahlungs-Haertung":"LEO 600 km, mehrjaehrige Auslegung, Suedatlantische Anomalie und "
          "Polarpassagen. Auch Indiens SPADEX in LEO traegt ihn.",
        "Thermischer Betrieb":"35 min Kernschatten je Umlauf gegen volle Sonne, rund 15 Zyklen "
          "am Tag. Die Basis (-200 C) deckt das nicht ab.",
        "Hoher EM-Abdruck":"Eine Grossapertur, die 'bis GEO alles aufdeckt', ist ein aktiver "
          "Hochleistungs-Emitter. payload_catalog.md §Suite coupling nennt die Buchung dieses "
          "Nachteils neben einem aktiven Sensor ausdruecklich als empfohlene Praxis.",
        "Doktrinaer gebunden":"Fester Aufklaerungsorbit, bodengefuehrte Auftragssteuerung, kein "
          "eigenstaendiges Manoever — deckt sich mit dem gebuchten Manoeverbudget 0,0 km/s.",
        "Single-Use":"Nicht betankbar, nicht wartbar, nicht bergbar — eine Aussetzung.",
        "Fragile Radiatoren":"Minimaler, ungeschuetzter Radiator an einem Serienbau."},
  isp=230, prop="hydrazine", dv=50.0, ld=2.5, house=11.0, batt=0.6,
  eng=[dict(name="Hydrazin-Monergol 22 N", key="custom_hydrazine_22n", isp=230, thrust_n=22,
            mass_kg=6, count=4, simultaneous=4, propType="hydrazine")],
  dv_man=0.0, dv_zweck="Bahnhaltung/Widerstandsausgleich LEO 600 km",
  rolle="Aufklaerung bis GEO"),

"CHN_geo_relais": dict(
  bauname="Himmelsbruecke", anker=5000.0, klasse="Frigate", zone_bemerkung="GEO",
  basis=[("custom_c2relais","C2-Relaisnutzlast: Antennen, Transponder, Kreuzverbindung",150.0)],
  adv=["Strahlungs-Haertung","Thermischer Betrieb","Magnetfeld-Toleranz"],
  dis=[], no_he=True,
  begr={"Strahlungs-Haertung":"GEO im aeusseren Guertel, 15 Jahre Auslegungsdauer.",
        "Thermischer Betrieb":"72 min Kernschatten gegen volle Sonne.",
        "Magnetfeld-Toleranz":"Aufladung und Entladung im GEO-Plasma — das klassische "
          "Ausfallmuster geostationaerer Nachrichtensatelliten.",
        "Hoher EM-Abdruck":"Ein Nachrichtenrelais ist ein dauerhafter, starker Sender. Es zu "
          "verbergen ist unmoeglich und auch nicht beabsichtigt.",
        "Doktrinaer gebunden":"Fester GEO-Platz, unbewaffnete Infrastruktur ohne eigenstaendige "
          "Handlung."},
  isp=1600, prop="xenon", dv=750.0, ld=2.6, house=15.0, batt=1.2,
  eng=[dict(name="Hall-Triebwerk SPD-100", key="custom_spd100", isp=1600, thrust_n=0.083,
            mass_kg=45, count=4, simultaneous=2, propType="xenon", p_kw=1.35, p_count=2,
            waste_kw=0.54)],
  dv_man=0.0, dv_zweck="Nord-Sued-Bahnhaltung GEO, 50 m/s je Jahr x 15 Jahre",
  rolle="+1 C2-Slot je Stueck (launch_c2 §2.1) · zugleich Steuerstelle der ferngelenkten Schiffe"),
}
ENT["CHN_geo_relais"]["begr"]["Magnetfeld-Toleranz"]=ENT["CHN_geo_relais"]["begr"]["Magnetfeld-Toleranz"]
WIRKUNG["Magnetfeld-Toleranz"]="Aufladung/Entladung im GEO-Plasma beherrscht"

def spec(e, pay, bus):
    return dict(struct_class="ruggedized", adv=len(e["adv"]), disadv=len(e["dis"]),
        payload_kg=pay, misc_kg=bus, house_kw=e["house"], pp_type="solar", pp_alpha=15.0,
        au=1.0, batt_hours=e["batt"], batt_alpha=5, rad_alpha=5.0, ld=e["ld"],
        isp=e["isp"], prop=e["prop"], dv_target=e["dv"], engines=e["eng"])

erg={}
for did,e in ENT.items():
    base=sum(b[2] for b in e["basis"])
    m=k2(base, len(e["adv"]), len(e["dis"]), e["no_he"])
    lo,hi=-e["anker"]*4, e["anker"]*4
    for _ in range(200):
        mid=(lo+hi)/2
        if nb.build(spec(e,m["final"],max(mid,0.0) if mid>=0 else mid))["wet"]<e["anker"]: lo=mid
        else: hi=mid
    bus=(lo+hi)/2
    r=nb.build(spec(e,m["final"],max(bus,0.0)))
    schub=sum(x["thrust_n"]*x.get("simultaneous",x.get("count",1)) for x in e["eng"])
    mt=e["dv"]*(r["wet"]+r["dry"])/2/schub
    kenn=dict(pay_dry=100*m["final"]/r["dry"], paybus_dry=100*(m["final"]+max(bus,0))/r["dry"],
              struct_dry=100*r["struct_kg"]/r["dry"], dry_wet=100*r["dry"]/r["wet"],
              pp_dry=100*(r["pp_mass"]+r["batt_mass"])/r["dry"])
    erg[did]=dict(base=base, np=m["np"], cm=m["cm"], x3=m["x3"], no_he=m["no_he"],
        pay_final=m["final"], bus=max(bus,0.0), passt=bus>=0, dry=r["dry"], prop=r["prop"],
        wet=r["wet"], dv=r["dv"], mt_s=mt, schub_gl=schub, kenn=kenn,
        structPct=r["structPct"], tankPct=r["tankPct"], struct_kg=r["struct_kg"],
        tank_kg=r["tank_kg"], thr_mass=r["thr_mass"], pp_mass=r["pp_mass"],
        pmad_mass=r["pmad_mass"], batt_mass=r["batt_mass"], rad_mass=r["rad_mass"],
        pp_cap=r["pp_cap"], peak_kw=r["peak_kw"], waste_kw=r["waste_kw"],
        D=r["D"], L=r["L"], A_front=r["A_front"], A_side=r["A_side"],
        ferngelenkt=("shipframe" not in [b[0] for b in e["basis"]]))

    print(f"=== {did}  «{e['bauname']}»  ({e['zone_bemerkung']}) ===")
    print(f"  Steuerung  : FERNGELENKT — keine Strukturtonne verbaut" if erg[did]["ferngelenkt"]
          else "  Steuerung  : autonom")
    print(f"  Basis      : " + " + ".join(f"{b[1]} {b[2]:.0f} kg" for b in e["basis"]))
    print(f"  Vorteile ({len(e['adv'])}): {', '.join(e['adv'])}")
    print(f"  Nachteile({len(e['dis'])}): {', '.join(e['dis']) or '— keine —'}")
    print(f"  K2  np {m['np']} · cm {m['cm']:.0f} · Hochenergie x{m['x3']:.0f}"
          f"{' (ctxNoHE deklariert)' if m['no_he'] else ''} -> {base:.0f} -> {m['final']:.0f} kg")
    print(f"  K1  Struktur {r['structPct']:.0f} % / Tank {r['tankPct']:.0f} %")
    print(f"  trocken {r['dry']:8.1f} + Treibstoff {r['prop']:7.1f} = nass {r['wet']:8.1f} kg "
          f"(Anker {e['anker']:.0f}, Abweichung {r['wet']-e['anker']:+.4f})")
    print(f"  Bus {max(bus,0):.1f} kg · dv {r['dv']:.1f} m/s · Schub {schub:.3f} N · "
          f"Manoeverzeit {mt/3600:.2f} h")
    print()

json.dump(erg, open("Ships/entwuerfe/loesung_chn_final.json","w"), indent=1, ensure_ascii=False)
json.dump({k:dict(bauname=v["bauname"], anker=v["anker"], klasse=v["klasse"], basis=v["basis"],
                  adv=v["adv"], dis=v["dis"], no_he=v["no_he"], begr=v["begr"], isp=v["isp"],
                  prop=v["prop"], dv=v["dv"], ld=v["ld"], house=v["house"], batt=v["batt"],
                  eng=v["eng"], dv_man=v["dv_man"], dv_zweck=v["dv_zweck"], rolle=v["rolle"],
                  zone_bemerkung=v["zone_bemerkung"])
           for k,v in ENT.items()}, open("Ships/entwuerfe/eingaben_chn_final.json","w"),
          indent=1, ensure_ascii=False)
json.dump(WIRKUNG, open("Ships/entwuerfe/spielwirkungen.json","w"), indent=1, ensure_ascii=False)
print("-> Ships/entwuerfe/loesung_chn_final.json")
