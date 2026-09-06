#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSFIX B-37 — Pfadadapter fuer den DW-01-Computeblock.

Befund: dw01.py liest den Rechenbestand aus
    factions.<F>.economy.resources.compute   (Zeile 634-635, 645)
Die Kampagne SCHWARZE SEE fuehrt ihn seit dem Setup unter
    factions.<F>.computeConfig
Folge: das neue HTML-Blatt 4 meldet »Die Fraktion fuehrt keinen compute-Block
im Spielstand«, obwohl 8,0 RP gebucht sind — das Hausformular
work/blatt4_rechenwerk.py liest denselben Bestand korrekt.

Dieser Adapter aendert KEINEN Wert. Er spiegelt den vorhandenen Block an die
Stelle, an der dw01.py ihn sucht, und schreibt eine Arbeitskopie. Der echte
Spielstand bleibt unberuehrt.
"""
import json, sys, copy

quelle, ziel = sys.argv[1], sys.argv[2]
gs = json.load(open(quelle, encoding="utf-8"))
neu = copy.deepcopy(gs)
gespiegelt = []
for fid, fak in (neu.get("factions") or {}).items():
    cc = fak.get("computeConfig")
    if not cc:
        continue
    eco = fak.setdefault("economy", {})
    res = eco.setdefault("resources", {})
    if res.get("compute"):
        continue
    res["compute"] = copy.deepcopy(cc)
    res["compute"]["_adapter"] = ("HAUSFIX B-37: gespiegelt aus factions.%s.computeConfig; "
                                  "kein Wert geaendert" % fid)
    gespiegelt.append(f"{fid} stock_rp={cc.get('stock_rp')}")
json.dump(neu, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Arbeitskopie:", ziel)
print("gespiegelt:", " · ".join(gespiegelt) if gespiegelt else "nichts")
