#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scharfe Buchung Zug 5 (2030) — SCHWARZE SEE.

Jede Zahl stammt aus einem Skriptlauf, der im Journal steht. Diese Datei
SCHREIBT nur, sie rechnet nicht neu.
Snapshots liegen in snapshots/*_vor_zug5_BUCHUNG.json.
"""
import json, sys

GS, ES = "gamestate.json", "erde01_state_schwarzesee.json"
gs = json.load(open(GS, encoding="utf-8"))
es = json.load(open(ES, encoding="utf-8"))

# ------------------------------------------------------------------ E-1 ---
# HE-24: Basiswachstumspfad rueckwirkend ab 2026 (zug5/skripte/e1_basispfad.py,
# Gegenprobe gegen KB-02 §7 und WK-01 tafel bestanden).
E1_2029 = {"china": 17.2064, "eu": 19.8234, "indien": 4.9524}
# 2030 = 2029 * (1 + Summe der Terme). Terme einzeln belegt, siehe Journal Z5-044.
WACHSTUM_2030_PP = {"china": 4.151, "eu": 0.641, "indien": 6.500}
BIP_2030 = {k: round(E1_2029[k] * (1 + WACHSTUM_2030_PP[k] / 100), 4) for k in E1_2029}

res = es["truth"]["ressourcen"]
for blk in E1_2029:
    res[blk]["bip_bio_usd_2029_ist"] = res[blk].get("bip_bio_usd")
    res[blk]["bip_bio_usd_2029_e1"] = E1_2029[blk]
    res[blk]["bip_bio_usd"] = BIP_2030[blk]

# --------------------------------------------------------- Zug und Uhr ---
gs["state"]["turnNumber"] = 5
gs["state"]["currentYear"] = 2031
gs["state"]["currentPhase"] = "setup"
es["kopf"]["zug"] = 5
es["kopf"]["uhr"]["datum_ingame"] = "2030-12-31"
es["kopf"]["seed_registry"] = {
    "zug_seed": 20300101,
    "stufen_seeds": {k: 20300100 + i for i, k in enumerate(
        ["validierung", "aufloesung", "sensorfilter", "regime_bias", "rendering",
         "kipppunkte", "coup", "attribution", "schicksal"], start=2)}
}
for i, blk in enumerate(("usa", "china", "eu", "indien", "russland", "rest")):
    es["kopf"]["seed_registry"]["stufen_seeds"][f"regime_bias_{blk}"] = 20300200 + i

# ------------------------------------------------------------- ZEUGHAUS ---
zh = gs["zeughaus"]["fraktionen"]
KONTO_Z5 = {"CHN": (2503.1, 375.5), "EU": (1660.5, 249.1), "IND": (719.3, 107.9)}
for fid, (k, t) in KONTO_Z5.items():
    zh[fid].setdefault("bodenkonto", {})
    zh[fid]["bodenkonto"]["zug5_t"] = k
    zh[fid]["bodenkonto"]["zug5_tranche_t"] = t
    zh[fid]["bodenkonto"]["zug5_quelle"] = "HE-24 (E-1 rueckwirkend), Blatt 3 neu gedruckt"

zh["IND"]["dienste"] = {"pct": 85.0, "kosten_t": 611.4, "slots": 8,
                        "beleg": "Blatt 3 bf_z_intel_frei=85 · zh01.py dienste --pct 85 --konto 719.3"}
zh["IND"]["aufwertung_zug5"] = {"ziel_tsk": "heer", "modernisierung_t": 0.0, "advanced_t": 0.0,
                                "hochtechnologie": {"future_sp": {"stueck": 9, "t": 90.0}},
                                "kategorie_neu": "future", "q_bd01": 1.4,
                                "tranche_rest_verfallen_t": round(107.9 - 90.0, 1),
                                "beleg": "Blatt 3 bf_z_future=9, bf_z_zieltsk=heer · zh01.py aufwertung"}
zh["EU"]["aufwertung_zug5"] = {"ziel_tsk": None, "modernisierung_t": 0.0, "advanced_t": 0.0,
                               "hochtechnologie": {}, "tranche_rest_verfallen_t": 249.1,
                               "bodenkonto_verfallen_t": 1660.5,
                               "beleg": "B-34: Blatt 3 traegt keinen Einsatz und keine Stueckzahl; "
                                        "Z-1.4 'Was im Zug nicht gebucht ist, verfaellt'"}
zh["EU"]["transfer_zug5"] = {"status": "ZURUECKGEWIESEN", "code": "V13", "regel": "Z-5",
                             "text": "Transfer 'nukleare Teilhabe' mit Ziel EU = eigene Fraktion, "
                                     "Posten 'advanced' passt nicht zur Teilhabe (Z-5.2 handelt in "
                                     "Sprengkoepfen), Menge leer. Rueckfrage an den Spieler."}

# -------------------------------------------------- Forschung / Praemie ---
fo = gs.setdefault("forschung", {}).setdefault("fraktionen", {})
fo.setdefault("CHN", {})["freie_forschung_zug5"] = {
    "quelle": "Siegbedingung 'Krieg gewonnen', scoring.md §Auszahlung bei Serie = 3",
    "stufe": "L1", "projekt": "Kuestenschutz (Klimaanpassung)",
    "sofort_timelinefrei": True, "zusaetzlich_zur_jahresration": True, "ansparbar": False,
    "wirkung": "G-2: Anpassung halbiert den Grenzschaden (erde01_regeln.json "
               "klima.schaden.anpassung_halbiert_grenzschaden = true)",
    "vorbehalt": "RG-Z5-12 — Kuestenschutz steht nicht im L1-Katalog von research.md; "
                 "als Hausentscheidung gebucht. B-35 — die Anpassungsregel hat weder "
                 "Erwerbsregel noch Codepfad."}
fo.setdefault("IND", {})["lizenz_zug5"] = {
    "geber": "CHN", "gegenstand": "Kuestenschutz (Klimaanpassung)", "vektor": "FO-01 S-6 HANDEL/LIZENZ",
    "kosten_jb": 0.15, "decke_e0": 0.7, "ertrag_jb": 0.175, "entdeckung": False,
    "politischer_preis": "Buendnisbindung, Auflagen, Sichtbarkeit",
    "beschraenkung": "nur Indien; Weitergabe an Dritte durch Lizenzauflage untersagt"}
fo.setdefault("EU", {})["projekt_zug5"] = {
    "name": "Yoda-Inspektoren (Inspektorsatellit)", "stufe": "L1", "einsatz_jb": 1.0,
    "p_erfolg": 0.75, "erwartete_zuege": 1.33, "p_in_4_zuegen": 0.99609,
    "beleg": "HE-26 Redaktion Blatt 4 · fo01_rechner.py rate --einsatz 1.0 --stufe L1",
    "hinweis": "Das Geraet selbst braucht keine L-Stufe (BS-01 §9 / NW-01); die "
               "Forschungszeile bildet die Entwicklungsarbeit ab."}
# Anpassungsmarke fuer G-2
for fid in ("CHN", "IND"):
    gs["factions"][fid].setdefault("klima", {})["anpassung"] = {
        "aktiv": True, "seit_zug": 5, "quelle": "Kuestenschutz L1 (CHN Siegpraemie, IND Lizenz)",
        "wirkung": "Grenzschaden halbiert (G-2 / QG-13)"}

# ------------------------------------------------------------- Compute ---
# EU: Zuteilung aus Zug 4 fortgeschrieben (HE-26, Teil der Redaktion)
gs["factions"]["EU"]["computeConfig"]["zuteilung_zug5"] = {
    "T": 0, "F": 3, "O": 1, "Z": 4, "D": 0,
    "beleg": "HE-26: Blatt 4 trug keine Zuteilung; Zug-4-Verteilung fortgeschrieben, "
             "Rueckfrage an Roman (RG-Z5-10: leeres Feld = 0 oder unveraendert?)"}

# ------------------------------------------------------------- GZ-01 ---
es.setdefault("module", {}).setdefault("gz01", {}).setdefault("daten", {}) \
  .setdefault("druck", {}).setdefault("indien", {})["eu"] = {
    "stand": 29.3, "stufe": "G2", "stufe_name": "Kampagne",
    "zufluesse_zug5": {"sabotage": 8.0, "einfluss": 6.0, "desinformation": 15.3},
    "wirkung_innenunterstuetzung": -1.213, "z_zuschlag_b2": 0.103,
    "befund": "diffuser Druck ohne Urheber",
    "beleg": "gz01_calc.py druck indien eu --stand=0 --zufluss=sabotage:1,einfluss:1,desinformation:15.3"}

json.dump(gs, open(GS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(es, open(ES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("GEBUCHT")
print(f"  Zug {gs['state']['turnNumber']} · gamestate currentYear {gs['state']['currentYear']} · "
      f"erde01 zug {es['kopf']['zug']} · {es['kopf']['uhr']['datum_ingame']}")
print(f"  warsWon: {gs['scoring']['warsWon']}")
for b in E1_2029:
    print(f"  {b:7s} 2029 Ist {res[b]['bip_bio_usd_2029_ist']} -> E-1 {E1_2029[b]} -> "
          f"2030 {BIP_2030[b]} Bio USD  ({WACHSTUM_2030_PP[b]:+.3f} Pp)")
