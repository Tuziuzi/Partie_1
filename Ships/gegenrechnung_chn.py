#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unabhaengige Gegenrechnung der drei CHN-Entwuerfe.

Baut das Massenmodell aus atomic_shipyard.md ein ZWEITES Mal auf, ohne
nachbau.build() zu benutzen, und stellt es gegen den erzeugten ship_export.
Jede Konstante hier stammt aus dem Regeltext, nicht aus dem ersten Skript.
"""
import json, math
G0 = 9.80665                                   # SKILL.md Schritt 4
TAX = {"ruggedized": (15, 10)}                 # atomic_shipyard.md Strukturklassen
ALPHA_SOLAR = 15.0                             # nachbau_regeln.md §3.3, kg/kW bei 1 AU
PMAD_ALPHA  = 2.05
BATT_ALPHA  = 5.0                              # kg/kWh
RAD_ALPHA   = 5.0                              # kg/kW
MARGE       = 0.10
ZF = {"LEO":1,"SSO":1,"MEO":2,"HEO":3,"GEO":4} # launch_c2.md §1.1
HK = {"pay_dry":(6.8,58.2),"paybus_dry":(17.7,78.2),"struct_dry":(10.7,20.6),
      "dry_wet":(40.2,93.3),"pp_dry":(5.0,15.0)}   # nachbau_regeln.md §6

def k2_faktor(np_, zustand):
    """payload_catalog.md + HE-30. (a) cm x 3 · (b) cm x np · (c) cm."""
    cm = 1.0 if np_ <= 0 else (2.0 if np_ == 1 else float(np_))
    if np_ <= 0: return cm, cm
    return cm, {"a": cm*3.0, "b": cm*np_, "c": cm}[zustand]

def masse(pay, bus, adv, dis, house_kw, batt_h, thr_kg, isp, dv, waste_extra=0.0,
          thr_kw=0.0):
    """Konvergenzschleife nach atomic_shipyard.md, hier eigenstaendig."""
    sP, tP = TAX["ruggedized"]
    auf = max(0, adv - dis)
    sF, tF = (sP+auf)/100.0, (tP+auf)/100.0
    # nachbau_regeln.md §4.1: nur GLEICHZEITIG feuernde Triebwerke zaehlen zur Last
    spitze_kw = house_kw + thr_kw
    gesamt_kw = spitze_kw * (1 + MARGE)
    pp   = gesamt_kw * ALPHA_SOLAR
    pmad = gesamt_kw * PMAD_ALPHA
    batt = gesamt_kw * batt_h * BATT_ALPHA
    rad  = (house_kw + waste_extra) * RAD_ALPHA
    basis = pay + bus + thr_kg + pp + pmad + batt + rad
    dry = basis * (1 + sF); prop = 0.0
    for _ in range(200):
        wet  = dry * math.exp(dv / (isp * G0))
        prop = wet - dry
        neu  = (basis + prop * tF) * (1 + sF)
        if abs(neu - dry) < 1e-12: dry = neu; break
        dry = neu
    return dict(dry=dry, prop=prop, wet=dry+prop, sP=sP+auf, tP=tP+auf,
                pp=pp, batt=batt, struct=(basis + prop*tF)*sF,
                dv=isp*G0*math.log((dry+prop)/dry))

FALL = {
 "Feldzeichen":   dict(base=50.0,   adv=2, dis=0, zustand="c", isp=315,  dv=1000.0,
                       house=3.6,  batt=1.2, thr=16+4*6, anker=2000.0, zonen=["LEO","MEO","HEO","SSO","GEO"]),
 "Himmelsauge":   dict(base=1000.0, adv=2, dis=3, zustand="c", isp=230,  dv=50.0,
                       house=11.0, batt=0.6, thr=4*6,    anker=3600.0, zonen=["LEO","LEO"]),
 "Himmelsbruecke":dict(base=150.0,  adv=3, dis=0, zustand="c", isp=1600, dv=750.0,
                       house=15.0, batt=1.2, thr=4*45,   anker=5000.0, zonen=["GEO","GEO"],
                       waste=4*0.54, thr_kw=1.35*2),   # SPD-100: 2 von 4 feuern gleichzeitig
}
E = {s["name"]: s for s in json.load(open("Ships/chn_raumfahrzeuge_2030.json"))["ships"]}

print("GEGENRECHNUNG — zweite, unabhaengige Umsetzung des Massenmodells\n")
alles_gleich = True
for name, f in FALL.items():
    s = E[name]; c = s["customData"]; k = c["k2Kette"]; mb = c["massBreakdown_kg"]
    np_ = 3 + f["adv"] - f["dis"]
    cm, fak = k2_faktor(np_, f["zustand"])
    pay = f["base"] * fak
    r = masse(pay, mb["bus"], f["adv"], f["dis"], f["house"], f["batt"], f["thr"],
              f["isp"], f["dv"], f.get("waste", 0.0), f.get("thr_kw", 0.0))
    kenn = dict(pay_dry=100*pay/r["dry"], paybus_dry=100*(pay+mb["bus"])/r["dry"],
                struct_dry=100*r["struct"]/r["dry"], dry_wet=100*r["dry"]/r["wet"],
                pp_dry=100*(r["pp"]+r["batt"])/r["dry"])
    proben = [
      ("np",            np_,                      k["np"]),
      ("cm",            cm,                       k["cm"]),
      ("K2-Faktor",     fak,                      c["highEnergy"]["kalkulator_faktor"]),
      ("Nutzlast kg",   pay,                      k["nutzlast_final_kg"]),
      ("Struktur %",    r["sP"],                  c["structureTax"]["struct_pct"]),
      ("Tank %",        r["tP"],                  c["structureTax"]["tank_pct"]),
      ("trocken kg",    r["dry"],                 mb["trocken"]),
      ("Treibstoff kg", r["prop"],                mb["treibstoff"]),
      ("nass kg",       r["wet"],                 mb["nass"]),
      ("dv m/s",        r["dv"],                  s["currentDeltaV"]),
      ("Anker kg",      f["anker"],               c["gebuchteStartmasse_kg"]),
      ("Spitzenlast kW", f["house"]+f.get("thr_kw",0.0), c["highEnergy"]["powerUsed_kW"]),
    ] + [(f"HK {n}", kenn[n], c["huellkurve"][n]) for n in HK]
    print(f"=== {name} ===")
    for lbl, mein, export in proben:
        ok = abs(mein - export) <= max(0.06, abs(export)*0.0005)
        alles_gleich &= ok
        print(f"  {'OK ' if ok else 'ABWEICHUNG'} {lbl:<16} eigen {mein:12.4f} · Export {export:12.4f}")
    aus = [n for n,(lo,hi) in HK.items() if not lo <= kenn[n] <= hi]
    print(f"  Huellkurve: {5-len(aus)}/5 innen" + (f" · draussen: {', '.join(aus)}" if aus else ""))
    print()

print("=== Startkapazitaet und Werft, unabhaengig ===")
start = sum(FALL[n]["anker"]/1000 * ZF[z] for n in FALL for z in FALL[n]["zonen"])
werft = sum(FALL[n]["anker"]/1000 * len(FALL[n]["zonen"]) * 4.0 for n in FALL)
print(f"  Startmasse gewichtet {start:.1f} t von 400,0 t  ({100*start/400:.0f} %)")
print(f"  Werftdurchsatz       {werft:.1f} t von 120,0 t  ({100*werft/120:.0f} %)")
g = json.load(open("stand/gamestate.json"))
bp = [e for e in g["bz01"]["bauplan"] if e["fraktion"] == "CHN"]
w_stand = sum(e["werft_gebucht_t"] for e in bp)
v_stand = g["factions"]["CHN"]["economy"]["resources"]["launch"]["_vortrag_beleg"]["gestartet_gewichtet_t_2029"]
print(f"  gegen Zustand: Werft {w_stand:.1f} t ({'gleich' if abs(w_stand-werft)<0.05 else 'ABWEICHUNG'}) · "
      f"Start {v_stand:.1f} t ({'gleich' if abs(v_stand-start)<0.05 else 'ABWEICHUNG'})")
alles_gleich &= abs(w_stand-werft) < 0.05 and abs(v_stand-start) < 0.05
print("\nERGEBNIS:", "DECKUNGSGLEICH" if alles_gleich else "ABWEICHUNGEN GEFUNDEN")
