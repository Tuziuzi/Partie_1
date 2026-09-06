#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Militaerpunkte fuer das Earth-Surface-Scoring, Zug 5 (2030).

Regelgrundlage, woertlich:
  scoring.md, »Earth Surface Scoring — Best-of-Three«:
    »1. Militaerpunkte: Wer mehr konventionelle Staerkepunkte hat«
  zeughaus-gm/references/regeln.md Z-2d, Tafel »Art | Dauer | Kategorie -> BD-01 §8«:
    Modernisierung -> `modern`, q 1,00 · Advanced -> `advanced`, q 1,15 ·
    Future -> `future`, q 1,40   (Legacy ist die Grundstufe, q 1,00)
  bodenbruecke-gm/skripte/bd01_rechner.py, Kopf:
    »Delta V fuehrt die Bodenverbaende einer Fraktion als Punktepool
     (Heer/Luft/SAM/See je 100 nach BL-01)«

Staerkepunkte: Ausgabe von deltav-game-master/scripts/bodenlage.py, woertlich
uebernommen (Pruefsumme 19f83738f9e34f86, alpha=0.5, n=5, Ziel je TSK 500).
Qualitaetsstufen je Teilstreitkraft: UEBERGABE_ZUG5.md §4 »Stand je Fraktion«.
Omega: 0 (kein Skalenschnitt im vorliegenden Material vermerkt) -> keine
Renormierung, WN-02 §4.3 nicht beruehrt.
"""
import json

# BL-01 tabelle --fraktionen=USA,CHN,RUS,EU,IND,REST  (woertliche Uebernahme)
SP = {
    "USA": {"heer": 159, "luft": 177, "sam": 157, "see": 185},
    "CHN": {"heer": 105, "luft": 105, "sam": 116, "see": 114},
    "EU":  {"heer":  93, "luft":  97, "sam":  86, "see":  94},
    "RUS": {"heer":  79, "luft":  67, "sam":  90, "see":  57},
    "IND": {"heer":  64, "luft":  54, "sam":  51, "see":  50},
}
# UEBERGABE §4 »Qualitaet«
QUAL = {
    "USA": {"heer": "legacy",  "luft": "legacy", "sam": "modern", "see": "legacy"},
    "CHN": {"heer": "future",  "luft": "legacy", "sam": "future", "see": "future"},
    "EU":  {"heer": "legacy",  "luft": "legacy", "sam": "legacy", "see": "legacy"},
    "RUS": {"heer": "future",  "luft": "legacy", "sam": "legacy", "see": "legacy"},
    "IND": {"heer": "future",  "luft": "legacy", "sam": "legacy", "see": "legacy"},
}
Q = {"legacy": 1.00, "modern": 1.00, "advanced": 1.15, "future": 1.40}   # Z-2d / BD-01 §8
# Zug-5-Kauf laut Blatt 3: Indien 9 Future-SP, Ziel-TSK heer (Feld bf_z_future=9, bf_z_zieltsk=heer)
ZUKAUF = {"IND": {"heer": 9}}

def punkte(f, mit_zukauf):
    ges, zeile = 0.0, []
    for tsk in ("heer", "luft", "sam", "see"):
        sp = SP[f][tsk] + (ZUKAUF.get(f, {}).get(tsk, 0) if mit_zukauf else 0)
        q = Q[QUAL[f][tsk]]
        ges += sp * q
        zeile.append(f"{tsk} {sp:3d}x{q:.2f}={sp*q:7.2f}")
    return ges, "  ".join(zeile)

print("=" * 78)
print("MILITAERPUNKTE Zug 5 — Earth-Surface Best-of-3, Teilkategorie 1")
print("=" * 78)
for stand, mit in (("vor dem Zug-5-Kauf", False), ("nach dem Zug-5-Kauf", True)):
    print(f"\nStand: {stand}")
    erg = {f: punkte(f, mit) for f in SP}
    for f, (p, z) in sorted(erg.items(), key=lambda x: -x[1][0]):
        print(f"  {f:4s} {p:8.2f}   {z}")
    rang = sorted(erg.items(), key=lambda x: -x[1][0])
    sieger = [f for f, (p, _) in rang if abs(p - rang[0][1][0]) < 1e-9]
    print(f"  -> mehr konventionelle Staerkepunkte: {', '.join(sieger)} "
          f"({rang[0][1][0]:.2f} gegen {rang[1][1][0]:.2f} des Zweiten)")

print("\n" + "-" * 78)
print("NICHT GERECHNET, gemeldet statt gefuellt:")
print("  · REST fuehrt in BL-01 keine Tafelzeile ('UNBEKANNT ... uebersprungen').")
print("    HE-19 laesst aber alle sechs Fraktionen an den Vergleichen teilnehmen.")
print("    -> Befund B-27 an BL-01, Rueckfrage an den Tisch.")
print("  · SAM ist in den LW-01-Teilkonten nicht als eigener Rohbestand gefuehrt;")
print("    die SAM-Spalte stammt aus der BL-01-Verteilung, nicht aus Waffenzahlen.")
print("  · Verluste der Zuege 1-4 sind nicht gebucht (kein groundForces im Material).")
print("    Gerechnet wird auf der BL-01-Startaufstellung plus dem belegten Qualitaetsstand.")
erg = {f: round(punkte(f, True)[0], 2) for f in SP}
open("zug5/ausgabe/militaerpunkte.json", "w", encoding="utf-8").write(
    json.dumps({"militaerpunkte_nach_kauf": erg, "sp_basis": SP, "qualitaet": QUAL,
                "q_faktoren": Q, "omega": 0}, ensure_ascii=False, indent=2))
print("\ngeschrieben: zug5/ausgabe/militaerpunkte.json")
