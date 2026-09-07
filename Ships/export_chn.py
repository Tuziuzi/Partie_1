#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Schreibt die drei rekonstruierten CHN-Entwuerfe als Unified-Shipyard ship_export v2.2.

Signaturmodell aus assets/orbitalsysteme_2026.json zurueckgerechnet (32 Schiffe, exakt):
  irArea(coast)  = 0,3 * A_side          optArea(coast) = A_front      rcs(coast) = A_front/2
  stealth        = irArea 0,1*A_front · optArea A_front/2 · rcs 0,015*A_front · wasteHeat 5 kW · 50 K
  thrust         = coast + Fahne;  wasteHeat *1,6
  plumeIRArea    = k * sqrt(Schub_N),  k = 0,012107 chemisch (2800 K) / 0,00070 elektrisch (400 K)
  plumeRCS       = 0,015812 * sqrt(Schub_N)
  Comm: Masse = 1 % Trockenmasse, Leistung = 4 % powerBudget, Ka-Band, AJ-Summe -275 dB
"""
import json, math, datetime

L = json.load(open("Ships/entwuerfe/loesung_chn.json"))

META = {
 "CHN_aufklaerer": dict(
   name="Himmelsauge", cls="Corvette", kampagne="Aufklaerungssatellit",
   engkey="custom_hydrazine_22n", engname="Hydrazin-Monergol 22 N", isp=230, thrust_n=22,
   count=4, sim=4, prop="hydrazine", emass=6, chem=True, plumeT=2800,
   adv=["Strahlungs-Haertung","Thermischer Betrieb"], struct="ruggedized",
   dv_manoever=0.0, dv_zweck="Bahnhaltung/Widerstandsausgleich LEO 600 km",
   rolle="Aufklaerung bis GEO", batt_h=0.6, house_kw=5.0,
   nutzlast="Grossapertur-Sensor 1000 kg (Stub-treu: construction.md §2, 'bis GEO alles aufdecken')"),
 "CHN_scorer": dict(
   name="Feldzeichen", cls="Corvette", kampagne="Scoring-Raumschiff",
   engkey="custom_hydrazine_22n", engname="Hydrazin-Monergol 22 N", isp=230, thrust_n=22,
   count=6, sim=6, prop="hydrazine", emass=6, chem=True, plumeT=2800,
   adv=["Strahlungs-Haertung","Thermischer Betrieb","Magnetfeld-Toleranz"], struct="ruggedized",
   dv_manoever=1.0, dv_zweck="genau ein Scoring-Versuch (scoring.md: 1 km/s je Versuch)",
   rolle="Zonenpraesenz und Scoring", batt_h=1.2, house_kw=3.0,
   nutzlast="Ops-/Wirkpaket 200 kg, unbewaffnet"),
 "CHN_geo_relais": dict(
   name="Himmelsbruecke", cls="Frigate", kampagne="GEO-Relais",
   engkey="custom_spd100", engname="Hall-Triebwerk SPD-100", isp=1600, thrust_n=0.083,
   count=4, sim=2, prop="xenon", emass=45, chem=False, plumeT=400,
   adv=["Strahlungs-Haertung","Thermischer Betrieb","Magnetfeld-Toleranz"], struct="ruggedized",
   dv_manoever=0.0, dv_zweck="Nord-Sued-Bahnhaltung GEO, 50 m/s je Jahr x 15 Jahre",
   rolle="+1 C2-Slot je Stueck (launch_c2 §2.1)", batt_h=1.2, house_kw=15.0,
   nutzlast="C2-Relaisnutzlast 900 kg"),
}
G0 = 9.80665
K_IR = dict(chem=0.012107, elec=0.00070)
K_RCS = 0.015812

def r4(x): return round(x, 4)

ships = []
for did, m in META.items():
    d = L[did]
    dry_t, prop_t, wet_t = d["dry"]/1000, d["prop"]/1000, d["wet"]/1000
    A_f, A_s = d["A_front"], d["A_side"]
    T = m["thrust_n"] * m["count"]                      # Katalogschub (alle Triebwerke)
    T_gl = d["schub_gl"]                                # gleichzeitig feuernd
    pir  = (K_IR["chem"] if m["chem"] else K_IR["elec"]) * math.sqrt(T)
    prcs = K_RCS * math.sqrt(T)
    house = m["house_kw"]; waste = d["waste_kw"]
    pbudget = round(d["pp_cap"]*1000); pused = round(d["peak_kw"]*1000)

    stealth = dict(wasteHeat=5, radTemp=50, irArea=r4(0.1*A_f), emissivity=0.1,
                   optArea=r4(A_f/2), albedo=0.02, rcs=r4(0.015*A_f), rfEmit=0,
                   stealthDuration=0, mode="stealth")
    coast   = dict(wasteHeat=r4(waste), radTemp=300, irArea=r4(0.3*A_s), emissivity=0.9,
                   optArea=r4(A_f), albedo=0.2, rcs=r4(A_f/2), rfEmit=10, mode="coast")
    thrust  = dict(wasteHeat=r4(waste*1.6), radTemp=m["plumeT"], plumeTemp=m["plumeT"],
                   irArea=r4(0.3*A_s+pir), plumeIRArea=r4(pir), emissivity=0.15, plumeEps=0.15,
                   optArea=r4(A_f+pir/2), albedo=0.2, rcs=r4(A_f/2+prcs), plumeRCS=r4(prcs),
                   rfEmit=10, engineType=m["engkey"], thrustN=T, mode="thrust")

    eng = dict(name=m["engname"], key=m["engkey"], isp=m["isp"], thrust_n=m["thrust_n"],
               count=m["count"], simultaneous=m["sim"], propType=m["prop"], mass_kg=m["emass"])
    if not m["chem"]: eng.update(p_kw=1.35, waste_kw=0.54)

    ships.append({
      "name": m["name"], "class": m["cls"], "isp": m["isp"], "thrust": T,
      "engineType": m["engkey"], "dryMass": r4(dry_t),
      "maxPropellant": r4(prop_t), "currentPropellant": r4(prop_t),
      "maxDeltaV": round(d["dv"],1), "designDeltaV": round(d["dv"],1), "currentDeltaV": round(d["dv"],1),
      "boiloffRate": 0.0, "originalDryMass": r4(dry_t), "originalMaxPropellant": r4(prop_t),
      "coreDryMass": None, "corePropellant": None, "source": "skill",
      "engines": [eng],
      "propellantPools": {m["prop"]: r4(prop_t)},
      "maxPropellantPools": {m["prop"]: r4(prop_t)},
      "poolDeltaV": {m["prop"]: round(d["dv"],1)},
      "wasteHeat": r4(waste), "powerBudget": pbudget, "powerUsed": pused,
      "armor": {"material": None, "thickness_cm": 0, "mass_tonnes": 0,
                "whipple": False, "whippleGap_cm": 0},
      "geometry": {"D_out": r4(d["D"]), "L_out": r4(d["L"]), "A_front": r4(A_f),
                   "A_side": r4(A_s), "volume_m3": r4(d["D"]*0+ (math.pi*(d["D"]/2)**2*d["L"])),
                   "ldRatio": round(d["L"]/d["D"],2)},
      "signatures": {"stealthEngOff": stealth, "normalEngOff": coast, "normalEngOn": thrust,
                     "stealth": stealth, "coast": coast, "thrust": thrust},
      "installedSensors": {}, "cryoConfig": {},
      "heatConfig": {"mode": "kg_per_kw", "alpha_kg_kw": 5.0,
                     "waste_kw": r4(waste), "rad_mass_kg": r4(d["rad_mass"])},
      "stealthConfig": {"warmRadArea": 0, "warmRadTemp": 15, "h2CoolantMass": 0,
                        "h2LatentHeat": 446000, "h2NoseTemp": 14, "h2EmitArea": 20, "h2Days": 0,
                        "heCoolantMass": 0, "heLatentHeat": 20800, "heHours": 0,
                        "rcsFaceted": "no", "rcsAbsorb": 0.3, "rcsBaseArea": 20,
                        "warmIRSmall": 0, "warmIRLarge": 0, "h2IRSmall": 2000, "h2IRLarge": 10000,
                        "heIRSmall": 5, "heIRLarge": 30, "totalHeat": 0},
      "coolant": {"h2Mass": 0, "heMass": 0, "h2MaxMass": 0, "heMaxMass": 0},
      "stagingConfig": None, "currentStaging": None,
      "commSystems": [{"type": "comm", "band": "Ka-Band (32 GHz)",
                       "aperture": round(0.30*(dry_t/0.4367)**0.192, 2), "power_dbm": 40,
                       "bandwidth_hz": 10000, "mass_kg": r4(dry_t*10),
                       "power_w": round(pbudget*0.04),
                       "ajConfig": {"presets": ["Raumschiff-Eigenschatten (genau ausgerichtet)",
                                                "Comm mit Frequency Hopping",
                                                "Tief eingelassenes System",
                                                "Synthetic Aperture Nulling"],
                                    "advantage_dB": -275}}],
      "jamSystems": None, "detectionData": {},
      "notes": (f"OW-01 Modus A (Rekonstruktion) von Kampagnenentwurf {did} "
                f"'{m['kampagne']}' (CHN). Anker: gebuchte Startmasse {d['wet']/1000:.0f} t "
                f"aus stand/gamestate.json, Abweichung 0,0000 %. Strukturklasse {m['struct']} "
                f"+ {len(m['adv'])} Vorteile ({', '.join(m['adv'])}) -> Struktur {d['structPct']:.0f} %, "
                f"Tank {d['tankPct']:.0f} %. Energie: solar, {d['pp_cap']:.2f} kW, "
                f"Kraftwerk {d['pp_mass']:.1f} kg, Batterie {d['batt_mass']:.1f} kg. "
                f"AJ-Summe -275 dB. dv = {d['dv']:.0f} m/s ({m['dv_zweck']}), "
                f"Manoeverzeit {d['mt_s']/3600:.2f} h. {m['nutzlast']}."),
      "customData": {
        "designMode": "A",
        "kampagne": "SCHWARZE SEE", "kampagnenDesign": did, "kampagnenName": m["kampagne"],
        "nation": "CHN", "rolle": m["rolle"],
        "advantages": m["adv"], "disadvantages": [],
        "structureClass": m["struct"],
        "structureTax": {"struct_pct": d["structPct"], "tank_pct": d["tankPct"]},
        "massBreakdown_kg": {"nutzlast": r4(d["pay"]), "bus": r4(d["misc"]),
                             "triebwerke": r4(d["thr_mass"]), "kraftwerk": r4(d["pp_mass"]),
                             "pmad": r4(d["pmad_mass"]), "batterie": r4(d["batt_mass"]),
                             "radiator": r4(d["rad_mass"]), "tank": r4(d["tank_kg"]),
                             "struktur": r4(d["struct_kg"]), "trocken": r4(d["dry"]),
                             "treibstoff": r4(d["prop"]), "nass": r4(d["wet"])},
        "powerPlant": {"type": "solar", "output_kw": round(d["pp_cap"],2), "alpha_kg_kw": 15.0,
                       "battery_kg": r4(d["batt_mass"]), "battery_hours": m["batt_h"],
                       "house_kw": house},
        "maneuverTime_s": round(d["mt_s"], 1),
        "thrust_simultaneous_N": round(T_gl, 4),
        "dv_manoever_kms": m["dv_manoever"],
        "dv_stationshaltung_kms": round(d["dv"]/1000 - m["dv_manoever"], 4),
        "huellkurve": {k: round(v,1) for k,v in d["kenn"].items()},
        "impliziteBasis_kg": round(d["pay"]/(3+len(m["adv"])), 1),
        "antiJamming": {"presets": [["Raumschiff-Eigenschatten (genau ausgerichtet)", -100],
                                    ["Comm mit Frequency Hopping", -25],
                                    ["Tief eingelassenes System", -110],
                                    ["Synthetic Aperture Nulling", -40]], "total_dB": -275},
        "realLaunchMass_kg": d["wet"], "massDeviationPct": 0.0,
      }})

out = {"version": "2.2", "type": "ship_export",
       "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00","Z"),
       "ships": ships}
json.dump(out, open("Ships/chn_raumfahrzeuge_2030.json","w"), indent=1, ensure_ascii=False)
print("-> Ships/chn_raumfahrzeuge_2030.json  (%d Schiffe)" % len(ships))
for s in ships:
    print(f"   {s['name']:<16} {s['class']:<9} trocken {s['dryMass']:7.4f} t  "
          f"Treibstoff {s['maxPropellant']:7.4f} t  nass {s['dryMass']+s['maxPropellant']:7.4f} t  "
          f"dv {s['currentDeltaV']:7.1f} m/s")
