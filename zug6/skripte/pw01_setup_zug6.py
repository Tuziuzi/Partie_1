#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PW-01 »PRIVATWERK« — Erstaufsetzung fuer alle sechs Fraktionen.

Regelinstanz ist pw01_calc.py; dieses Skript ruft nur auf und legt ab.

WICHTIG, und auf dem Blatt genauso benannt: der Privatsektor ist ein ANTEIL
der nationalen Startkapazitaet, kein Zuschlag (Riegel PW-01:S1). Die Zahl in
launch.capacity_t_year enthielt ihn seit Spielbeginn stillschweigend; das
Setup macht ihn sichtbar. Fuer China heisst das: von 400 t/a sind 60 t/a
privat, 340 t/a bleiben staatlich verfuegbar. Wirksam ab Zug 6, ruecksichtslos
NICHT rueckwirkend auf die Zuege 1-5.

    python3 zug6/skripte/pw01_setup_zug6.py            Tafel
    python3 zug6/skripte/pw01_setup_zug6.py --schreiben  in den Stand buchen
"""
import json, os, subprocess, sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773")
CALC = os.path.join(SK, "pw01-privatwerk", "scripts", "pw01_calc.py")
GS = os.path.join(W, "stand", "gamestate.json")
BLOECKE = ["USA", "CHN", "EU", "IND", "RUS", "REST"]
ARB = os.path.join(W, "zug6", "skripte", "_pw01")
os.makedirs(ARB, exist_ok=True)


def setup():
    g = json.load(open(GS, encoding="utf-8"))
    erg = {}
    for f in BLOECKE:
        l = g["factions"][f]["economy"]["resources"]["launch"]["capacity_t_year"]
        aus = os.path.join(ARB, f"pw01_{f}.json")
        r = subprocess.run(["python3", CALC, "setup", "--fraktion", f,
                            "--launch", str(l), "--bodensegment", "1.0",
                            "--stand", aus], capture_output=True, text=True)
        if r.returncode or not os.path.exists(aus):
            raise SystemExit(f"{f}: {(r.stderr or r.stdout)[:300]}")
        erg[f] = {"stand": json.load(open(aus, encoding="utf-8")),
                  "protokoll": [z for z in r.stdout.splitlines()
                                if z[:1].isalpha() and ":" in z],
                  "launch_national_t_a": l}
    return g, erg


def tafel(erg):
    z = [f"{'F':5} {'national':>9} {'privat':>8} {'Anteil':>7} {'staatl.':>9} "
         f"{'Lager':>7} {'RG':>12} {'Linien':>7}", "-" * 68]
    for f in BLOECKE:
        e = erg[f]; s = e["stand"]
        z.append(f"{f:5} {e['launch_national_t_a']:9.1f} {s['capacity_t_year']:8.1f} "
                 f"{s['anteil_2026']:7.2f} "
                 f"{e['launch_national_t_a']-s['capacity_t_year']:9.1f} "
                 f"{s['stockpile_t']:7.1f} {s['rg']:>12} {len(s['linien']):7d}")
    return "\n".join(z)


def schreiben(g, erg):
    for f in BLOECKE:
        g["factions"][f]["private"] = dict(
            erg[f]["stand"],
            _herkunft="pw01_calc.py setup, Zug 6 (2031)",
            _wirksam_ab="Zug 6",
            _nicht_rueckwirkend="Zuege 1-5 bleiben unberuehrt",
            _riegel=("PW-01:S1 — privat + staatlich <= national x boost. Der "
                     "Privatsektor ist ein ANTEIL, kein Zuschlag; die nationale "
                     "Zahl enthielt ihn bereits."),
            _staatlich_verfuegbar_t_a=round(
                erg[f]["launch_national_t_a"] - erg[f]["stand"]["capacity_t_year"], 2),
            _tischvorbehalt=("Setup gebucht, damit das Modul spielbar ist. Es "
                             "verschiebt keine Tonne, es macht die Aufteilung "
                             "sichtbar — aber die staatlich frei verfuegbare "
                             "Startmasse sinkt dadurch ab Zug 6. Ruecknahme: "
                             "factions.<F>.private loeschen."))
    json.dump(g, open(GS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return GS


if __name__ == "__main__":
    g, erg = setup()
    print(tafel(erg))
    if "--schreiben" in sys.argv:
        print("\ngebucht nach", schreiben(g, erg))
