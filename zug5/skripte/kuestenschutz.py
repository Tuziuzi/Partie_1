#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wirkung des Kuestenschutzes (Anpassung) nach G-2 — Rechen-Gate.

Regelgrundlage, woertlich:
  erde01-gm/references/ereignisse.md §Schadensfunktion (G-2):
    »Aktive Regel: Default `Schaden = 1,2 % · dT^2` des BIP. ...
     Regional: arm x1,7 · reich x0,4. Anpassung halbiert den Grenzschaden [QG-13].«
  erde01-gm/assets/erde01_regeln.json:
    klima.schaden.anpassung_halbiert_grenzschaden = true

Grenzschaden = Ableitung der Schadensfunktion nach der Temperatur:
    d/dT (1,2 % · T^2) = 2,4 % · T   je Grad weiterer Erwaermung
Mit Anpassung: die Haelfte davon.

Eingaben aus dem Spielstand (erde01_state_schwarzesee.json), nicht gesetzt:
  T_ist_C = 1,4131 · Regionalvektor aus erde01_engine.py klima --regional
BIP-Werte nach der rueckwirkenden E-1-Buchung (HE-24).
"""
T = 1.4131                      # module.erde01.daten.T_ist_C
PCT_JE_C2 = 1.2 / 100           # G-2 Default
REGIONAL = {"usa": 0.7672, "china": 0.7737, "eu": 0.8419,
            "indien": 1.6092, "russland": 1.5584, "rest": 1.1235}
BIP = {"china": 17.2064, "eu": 19.8234, "indien": 4.9524}   # Bio USD, E-1 rueckwirkend

def schaden_pct(T, f):  return PCT_JE_C2 * T * T * f * 100
def grenz_pct(T, f):    return 2 * PCT_JE_C2 * T * f * 100

print("=" * 76)
print(f"G-2 KLIMASCHADEN bei T = {T} C — Wirkung des Kuestenschutzes (Anpassung)")
print("=" * 76)
print(f"\nGlobales Niveau: 1,2 % x {T}^2 = {PCT_JE_C2*T*T*100:.3f} % des BIP\n")
print(f"{'Block':10s}{'Faktor':>8s}{'Schaden %':>11s}{'Grenzschaden':>14s}{'mit Anpassung':>15s}")
for b, f in REGIONAL.items():
    print(f"  {b:8s}{f:8.4f}{schaden_pct(T,f):11.3f}{grenz_pct(T,f):13.3f}/C{grenz_pct(T,f)/2:13.3f}/C")

print("\n" + "-" * 76)
print("In Geld, fuer die beiden Empfaenger der Technologie:")
for b in ("china", "indien"):
    s = schaden_pct(T, REGIONAL[b]) / 100
    g = grenz_pct(T, REGIONAL[b]) / 100
    print(f"  {b:8s} BIP {BIP[b]:8.4f} Bio -> Schaden heute {BIP[b]*s*1000:7.1f} Mrd USD/a")
    print(f"           je weiterem Grad zusaetzlich {BIP[b]*g*1000:7.1f} Mrd -> mit Anpassung {BIP[b]*g/2*1000:7.1f} Mrd")

print("\n" + "-" * 76)
print("Beispielrechnung: Erwaermung steigt von 1,4131 auf 2,0 C")
for b in ("china", "indien"):
    f = REGIONAL[b]
    alt = PCT_JE_C2 * T*T * f
    neu = PCT_JE_C2 * 2.0*2.0 * f
    zuwachs = neu - alt
    print(f"  {b:8s} ohne Anpassung {alt*100:6.3f} % -> {neu*100:6.3f} %  (+{zuwachs*100:.3f} Pp = {BIP[b]*zuwachs*1000:6.1f} Mrd/a)")
    print(f"           mit  Anpassung {alt*100:6.3f} % -> {(alt+zuwachs/2)*100:6.3f} %  (+{zuwachs/2*100:.3f} Pp = {BIP[b]*zuwachs/2*1000:6.1f} Mrd/a)")
    print(f"           ersparnis {BIP[b]*zuwachs/2*1000:6.1f} Mrd USD/a")

print("\n" + "-" * 76)
print("NICHT GERECHNET, gemeldet (B-35): erde01_engine.py klima() kennt KEINEN")
print("Anpassungsparameter. Die Regel steht in den Daten und im Referenztext, hat")
print("aber weder eine Erwerbsregel (Kosten, Dauer, Voraussetzung) noch einen")
print("Codepfad. Die Halbierung ist hier von Hand nach dem Regeltext gerechnet.")
