#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Forschung Rev. D — Schema-Nachzug fuer factions.<F>.research.

deltav-game-master v3.10 ersetzt das Forschungsmodell. Der research-Block der
Vorlage traegt fuenf Felder, die unser Stand nicht hat: ration, vorbescheide,
marken, club, level2/level3. Ohne sie kann weder eine Ration gebucht noch ein
Vorbescheid abgelegt werden.

ADDITIV. Kein vorhandener Wert wird angefasst; completedL1/L2/L3 bleiben, wie
sie sind. Fehlende Felder werden aus der Vorlage ergaenzt, die Beispielzeile
in vorbescheide wird NICHT mitkopiert.

    python3 zug6/skripte/research_revD_migration.py [--schreiben]
"""
import json, os, sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GS = os.path.join(W, "stand", "gamestate.json")

NEU = {
    "level2": False,
    "level3": False,
    "ration": {"jahr": None, "stufe": None, "verbraucht_durch": None,
               "_hinweis": "eine Ration je Fraktion und Jahr, nicht ansparbar, "
                           "nicht uebertragbar (research.md Rev. D §1.1)"},
    "vorbescheide": [],
    "marken": [],
    "club": {"projekte": [], "durchsetzung_genutzt": []},
    "_weltuhr": "L1 einmalig 2030, Luecke 2031-2034, ab 2035 jaehrlich; L2 ab "
                "2046; L3/AG ab 2058 oder nach S-01 Stufe C (research.md §1.2)",
    "_budget": "Budget ist KEIN Forschungshebel (§1.3). Das Ratenmodell FO-01 "
               "ist im Grundmodell NICHT in Kraft; der Block gamestate.forschung "
               "liegt still, bis der Tisch FO-01 als Hausregel einschaltet.",
}


def main(schreiben):
    g = json.load(open(GS, encoding="utf-8"))
    zeilen = []
    for f, v in g["factions"].items():
        r = v.setdefault("research", {})
        fehlte = [k for k in NEU if k not in r]
        for k, w in NEU.items():
            r.setdefault(k, json.loads(json.dumps(w)))
        zeilen.append(f"{f:5} ergaenzt: {', '.join(fehlte) if fehlte else '(nichts)'}")
    print("\n".join(zeilen))
    if schreiben:
        json.dump(g, open(GS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\ngebucht nach", GS)


if __name__ == "__main__":
    main("--schreiben" in sys.argv)
