#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ship_export 2.2 der ENDFASSUNG — Modus B, volle Penaltykette, ferngelenkt.

Signaturmodell aus assets/orbitalsysteme_2026.json zurueckgerechnet (32 Schiffe):
  irArea(coast) = 0,3*A_side · optArea = A_front · rcs = A_front/2 · rfEmit 10
  stealth: irArea 0,1*A_front · optArea A_front/2 · rcs 0,015*A_front · 5 kW · 50 K
  thrust = coast + Fahne, wasteHeat x1,6
  plumeIRArea = k*sqrt(Schub_N), k = 0,012107 chemisch (2800 K) / 0,00070 elektrisch (400 K)
  plumeRCS = 0,015812*sqrt(Schub_N)
  Comm: Masse 1 % der Trockenmasse, Leistung 4 % powerBudget, Ka-Band, AJ -275 dB
"""
import json, math, datetime
L = json.load(open("Ships/entwuerfe/loesung_chn_final.json"))
E = json.load(open("Ships/entwuerfe/eingaben_chn_final.json"))
W = json.load(open("Ships/entwuerfe/spielwirkungen.json"))
KAMPAGNENNAME = {"CHN_aufklaerer":"Aufklaerungssatellit","CHN_scorer":"Scoring-Raumschiff",
                 "CHN_geo_relais":"GEO-Relais"}
K_IR = dict(chem=0.012107, elec=0.00070); K_RCS = 0.015812
def r4(x): return round(x,4)

FERN = ("FERNGELENKT — keine Strukturtonne verbaut. construction.md §'Struktur = Autonomie': "
        "'Die Strukturtonne kauft nicht Rumpf, sondern Autonomie: Bordrechner, Selbststeuerung, "
        "eigene Feuerleitung.' Folge: jede Aktion — Manoever, Feuer, Sensorbetrieb, Response — "
        "setzt einen aktiven Kommandolink zu einer Steuerstelle voraus (Erde, Traegerschiff, "
        "Relais). Bei gejammtem oder unterbrochenem Link vollstaendig handlungsunfaehig, driftet "
        "ballistisch weiter und gilt im Kampf als wehrloses Ziel (no_response).")

ships=[]
for did, e in E.items():
    d=L[did]; chem = e["prop"] != "xenon"
    engines=[dict(name=x["name"], key=x["key"], isp=x["isp"], thrust_n=x["thrust_n"],
                  count=x["count"], simultaneous=x.get("simultaneous",x["count"]),
                  propType=x["propType"], mass_kg=x["mass_kg"],
                  **({"p_kw":x["p_kw"],"waste_kw":x["waste_kw"]} if "p_kw" in x else {}))
             for x in e["eng"]]
    T=sum(x["thrust_n"]*x["count"] for x in engines); T_gl=d["schub_gl"]
    A_f,A_s=d["A_front"],d["A_side"]; waste=d["waste_kw"]
    pir=(K_IR["chem"] if chem else K_IR["elec"])*math.sqrt(T); prcs=K_RCS*math.sqrt(T)
    plumeT=2800 if chem else 400
    dry_t,prop_t=d["dry"]/1000,d["prop"]/1000
    pbudget=round(d["pp_cap"]*1000); pused=round(d["peak_kw"]*1000)
    stealth=dict(wasteHeat=5,radTemp=50,irArea=r4(0.1*A_f),emissivity=0.1,optArea=r4(A_f/2),
                 albedo=0.02,rcs=r4(0.015*A_f),rfEmit=0,stealthDuration=0,mode="stealth")
    coast=dict(wasteHeat=r4(waste),radTemp=300,irArea=r4(0.3*A_s),emissivity=0.9,optArea=r4(A_f),
               albedo=0.2,rcs=r4(A_f/2),rfEmit=10,mode="coast")
    thrust=dict(wasteHeat=r4(waste*1.6),radTemp=plumeT,plumeTemp=plumeT,irArea=r4(0.3*A_s+pir),
                plumeIRArea=r4(pir),emissivity=0.15,plumeEps=0.15,optArea=r4(A_f+pir/2),albedo=0.2,
                rcs=r4(A_f/2+prcs),plumeRCS=r4(prcs),rfEmit=10,engineType=engines[0]["key"],
                thrustN=T,mode="thrust")
    ships.append({
     "name": e["bauname"], "class": e["klasse"], "isp": e["isp"], "thrust": T,
     "engineType": engines[0]["key"], "dryMass": r4(dry_t), "maxPropellant": r4(prop_t),
     "currentPropellant": r4(prop_t), "maxDeltaV": round(d["dv"],1),
     "designDeltaV": round(d["dv"],1), "currentDeltaV": round(d["dv"],1), "boiloffRate": 0.0,
     "originalDryMass": r4(dry_t), "originalMaxPropellant": r4(prop_t),
     "coreDryMass": None, "corePropellant": None, "source": "skill", "engines": engines,
     "propellantPools": {e["prop"]: r4(prop_t)}, "maxPropellantPools": {e["prop"]: r4(prop_t)},
     "poolDeltaV": {e["prop"]: round(d["dv"],1)},
     "wasteHeat": r4(waste), "powerBudget": pbudget, "powerUsed": pused,
     "armor": {"material":None,"thickness_cm":0,"mass_tonnes":0,"whipple":False,"whippleGap_cm":0},
     "geometry": {"D_out":r4(d["D"]),"L_out":r4(d["L"]),"A_front":r4(A_f),"A_side":r4(A_s),
                  "volume_m3":r4(math.pi*(d["D"]/2)**2*d["L"]),"ldRatio":round(d["L"]/d["D"],2)},
     "signatures": {"stealthEngOff":stealth,"normalEngOff":coast,"normalEngOn":thrust,
                    "stealth":stealth,"coast":coast,"thrust":thrust},
     "installedSensors": {}, "cryoConfig": {},
     "heatConfig": {"mode":"kg_per_kw","alpha_kg_kw":5.0,"waste_kw":r4(waste),
                    "rad_mass_kg":r4(d["rad_mass"])},
     "stealthConfig": {"warmRadArea":0,"warmRadTemp":15,"h2CoolantMass":0,"h2LatentHeat":446000,
       "h2NoseTemp":14,"h2EmitArea":20,"h2Days":0,"heCoolantMass":0,"heLatentHeat":20800,
       "heHours":0,"rcsFaceted":"no","rcsAbsorb":0.3,"rcsBaseArea":20,"warmIRSmall":0,
       "warmIRLarge":0,"h2IRSmall":2000,"h2IRLarge":10000,"heIRSmall":5,"heIRLarge":30,"totalHeat":0},
     "coolant": {"h2Mass":0,"heMass":0,"h2MaxMass":0,"heMaxMass":0},
     "stagingConfig": None, "currentStaging": None,
     "commSystems": [{"type":"comm","band":"Ka-Band (32 GHz)",
        "aperture":round(0.30*(dry_t/0.4367)**0.192,2),"power_dbm":40,"bandwidth_hz":10000,
        "mass_kg":r4(dry_t*10),"power_w":round(pbudget*0.04),
        "ajConfig":{"presets":["Raumschiff-Eigenschatten (genau ausgerichtet)",
          "Comm mit Frequency Hopping","Tief eingelassenes System","Synthetic Aperture Nulling"],
          "advantage_dB":-275}}],
     "jamSystems": None, "detectionData": {},
     "notes": (f"Unified Shipyard MODUS B (Neukonstruktion, volle Penaltykette) — Kampagnenentwurf "
       f"{did} '{KAMPAGNENNAME[did]}' (CHN), Einsatz {e['zone_bemerkung']}. FERNGELENKT: keine "
       f"Strukturtonne. K2: Basis {d['base']:.0f} kg x cm {d['cm']:.0f} x Hochenergie "
       f"{d['x3']:.0f}{' (ctxNoHE)' if d['no_he'] else ''} = {d['pay_final']:.0f} kg Nutzlast "
       f"(np {d['np']}). Vorteile: {', '.join(e['adv'])}. Nachteile: {', '.join(e['dis']) or 'keine'}. "
       f"Struktur {d['structPct']:.0f} % / Tank {d['tankPct']:.0f} %. Energie solar "
       f"{d['pp_cap']:.2f} kW, Kraftwerk {d['pp_mass']:.1f} kg, Batterie {d['batt_mass']:.1f} kg. "
       f"dv {d['dv']:.0f} m/s ({e['dv_zweck']}), Manoeverzeit {d['mt_s']/3600:.2f} h. "
       f"Gebuchte Startmasse {e['anker']/1000:.1f} t, Abweichung 0,0000 %."),
     "customData": {
       "designMode": "B",
       "designModeBegruendung": ("MODUS B: kein reales Vorbild mit veroeffentlichter Startmasse. "
         "construction.md gewaehrt die Ausnahme von Weight Penalty 3 nur fuer designMode "
         "'reconstruction'; hier laufen alle drei Kanaele K1+K2+K3. Penalty-Reduktion durch "
         "L1/L2/L3 ist 2030 nicht verfuegbar (research.md: L1 ab 2035)."),
       "steuerung": "ferngelenkt", "steuerungBegruendung": FERN,
       "kampagne": "SCHWARZE SEE", "kampagnenDesign": did, "kampagnenName": KAMPAGNENNAME[did],
       "nation": "CHN", "rolle": e["rolle"], "einsatzzonen": e["zone_bemerkung"],
       "advantages": e["adv"], "disadvantages": e["dis"],
       "begruendungVorNachteile": e["begr"],
       "spielwirkungen": {k: W[k] for k in e["adv"]+e["dis"]},
       "structureClass": "ruggedized",
       "structureTax": {"struct_pct": d["structPct"], "tank_pct": d["tankPct"]},
       "k2Kette": {"basis_kg": d["base"], "np": d["np"], "cm": d["cm"],
                   "hochenergie_faktor": d["x3"], "faktor_gesamt": d["faktor"],
                   "ctxNoHE": d["ctx_no_he"], "disc": 1.0, "env": 0.0,
                   "nutzlast_final_kg": d["pay_final"],
                   "formel": ("np = 3 + adv - disadv; cm: np>=2 -> np, np==1 -> 2, np<=0 -> 1; "
                              "final = basis * cm * disc * (1+env), bei Hochenergie zusaetzlich *3 "
                              "UND dv/3 (construction.md §Weight Penalty 3, Schwelle ~50 kW). "
                              "HE-29: unterhalb der Schwelle existiert die Strafe nicht, cm bleibt np. "
                              "Die Kalkulatorfahne ctxNoHE wird NICHT beansprucht — sie ist eine "
                              "Kontextklasse mit eigener Preiskurve (cm * np), kein Rabatt."),
                   "spielregel_hochenergie_greift": d["spielregel_greift"]},
       "nutzlastBasis_kg": d["base"], "spitzenlast_kw": round(d["peak_kw"],2),
       "highEnergy": {
         "powerUsed_kW": round(d["peak_kw"], 2),
         "schwelle_kW": 50.0,
         "spielregel_greift": d["spielregel_greift"],
         "dv_geteilt_durch_3": d["dv_geteilt"],
         "gewicht_verdreifacht_spielregel": d["dv_geteilt"],
         "kalkulator_zustand": "ctxNoHE (cm x np)" if d["ctx_no_he"] else "Voreinstellung x3",
         "kalkulator_faktor": d["faktor"],
         "gegenzustand_faktor": d["alternative_faktor"],
         "hausregel_flach_faktor_S": d["hausregel_faktor"],
         "der_spielregel_naeher": d["naeher"],
         "regelzitat": ("construction.md §Weight Penalty 3: 'High-Energy-Systeme (ab ~50 kW, "
           "z.B. Laser): ... Zusaetzlich: Dv / 3 und 3x Gewicht.' shipyard-designer SKILL.md "
           "v5.22-HE Schritt 2: 'powerUsed < 50 kW -> the game rule does NOT apply ... pick the "
           "state closest to the rule, record the difference as [S] ... declare the mismatch as "
           "RULES-GAP to the player.' Schritt 4: 'Never present the calculator's x3 as the "
           "high-energy penalty — it is a payload guard coupled to np, nothing more.'"),
         "RULES_GAP": ("Die Spielregel kennt unterhalb 50 kW GAR KEINE Strafe, der Kalkulator "
           "bietet nur zwei Zustaende. Gewaehlt ist der naehere; die Differenz zur Spielregel "
           "ist eine Setzung [S]. Drei Optionen liegen dem Tisch vor: (a) Kalkulator-"
           "Voreinstellung x3, (b) ctxNoHE cm x np, (c) Hausregel flacher Basiswert [S]."),
         "marke": "[S]"},
       "nutzlastHerkunft": " + ".join(f"{b[1]} ({b[0]}, {b[2]:.0f} kg)" for b in e["basis"]),
       "massBreakdown_kg": {"nutzlast":r4(d["pay_final"]),"bus":r4(d["bus"]),
         "triebwerke":r4(d["thr_mass"]),"kraftwerk":r4(d["pp_mass"]),"pmad":r4(d["pmad_mass"]),
         "batterie":r4(d["batt_mass"]),"radiator":r4(d["rad_mass"]),"tank":r4(d["tank_kg"]),
         "struktur":r4(d["struct_kg"]),"trocken":r4(d["dry"]),"treibstoff":r4(d["prop"]),
         "nass":r4(d["wet"])},
       "powerPlant": {"type":"solar","output_kw":round(d["pp_cap"],2),"alpha_kg_kw":15.0,
         "battery_kg":r4(d["batt_mass"]),"battery_hours":e["batt"],"house_kw":e["house"]},
       "maneuverTime_s": round(d["mt_s"],1), "thrust_simultaneous_N": round(T_gl,4),
       "dv_manoever_kms": e["dv_man"],
       "dv_stationshaltung_kms": round(max(d["dv"]/1000-e["dv_man"],0.0),4),
       "huellkurve": {k: round(v,1) for k,v in d["kenn"].items()},
       "antiJamming": {"presets":[["Raumschiff-Eigenschatten (genau ausgerichtet)",-100],
         ["Comm mit Frequency Hopping",-25],["Tief eingelassenes System",-110],
         ["Synthetic Aperture Nulling",-40]],"total_dB":-275},
       "gebuchteStartmasse_kg": e["anker"], "abweichungProzent": 0.0}})

out={"version":"2.2","type":"ship_export",
     "timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00","Z"),
     "ships":ships}
json.dump(out, open("Ships/chn_raumfahrzeuge_2030.json","w"), indent=1, ensure_ascii=False)
print("-> Ships/chn_raumfahrzeuge_2030.json  (%d Schiffe, MODUS B, ferngelenkt)" % len(ships))
for s in ships:
    c=s["customData"]; k=c["k2Kette"]
    print(f"   {s['name']:<15} {s['dryMass']+s['maxPropellant']:6.4f} t · np {k['np']} · "
          f"Nutzlast {k['basis_kg']:.0f}->{k['nutzlast_final_kg']:.0f} kg · "
          f"Vorteile {len(c['advantages'])} / Nachteile {len(c['disadvantages'])}")
