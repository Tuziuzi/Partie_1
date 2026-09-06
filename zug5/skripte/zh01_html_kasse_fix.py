#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSFIX B-36 — zh01_blatt.py --html ignoriert --konto-t / --tranche-t.

Befund: Der PDF-Weg nimmt die Kasse aus feldklasse_s() und ehrt die
CLI-Setzung (Zeile 156-182). Der HTML-Weg baut die Feldklasse S dagegen in
Zeile 1396 aus `zh.sitrep_daten(...)` und sieht a.konto_t nie an. Folge: das
HTML-Blatt druckt eine selbst gerechnete Kasse als VORGABE — in dieser
Kampagne 1675,3 t statt der gebuchten 1660,5 t. Die Kampagnenregel lautet
»VORGABE ist Befund, nie Schaetzung« (Z-8.3), also darf das Blatt so nicht
an den Tisch.

Der Fix greift nicht in die Skilldatei ein: er laedt zh01_blatt als Modul und
legt sich VOR zh.sitrep_daten, ueberschreibt in der Rueckgabe genau zwei
Zahlen und laesst alles andere — auch die Standmarke, die danach ueber dem
korrigierten Stand gebildet wird — vom Original rechnen.

Aufruf:
  python3 zh01_html_kasse_fix.py --fraktion EU --zug 5 --konto-t 1660.5 \
      --tranche-t 249.1 [weitere Argumente wie zh01_blatt.py]
"""
import sys, os, argparse, importlib.util

def lade(pfad, name):
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

vor = argparse.ArgumentParser(add_help=False)
vor.add_argument("--skill", required=True)
vor.add_argument("--konto-t", type=float, required=True, dest="konto_t")
vor.add_argument("--tranche-t", type=float, required=True, dest="tranche_t")
eigen, rest = vor.parse_known_args()

BL = os.path.join(eigen.skill, "zeughaus-gm", "scripts", "zh01_blatt.py")
mod = lade(BL, "zh01_blatt_haus")

zh = mod._zh()
original = zh.sitrep_daten

def sitrep_daten_korrigiert(*a, **kw):
    stand = original(*a, **kw)
    k = stand.get("kasse") or {}
    alt_k, alt_t = k.get("bodenkonto_t"), k.get("tranche_t")
    k["bodenkonto_t"] = eigen.konto_t
    k["tranche_t"] = eigen.tranche_t
    for feld, wert in (("transfer_deckel_t", eigen.konto_t * 0.20),):
        if feld in k: k[feld] = round(wert, 1)
    stand["kasse"] = k
    print(f"  [HAUSFIX B-36] Kasse ersetzt: {alt_k} -> {eigen.konto_t} t · "
          f"Tranche {alt_t} -> {eigen.tranche_t} t", file=sys.stderr)
    return stand

zh.sitrep_daten = sitrep_daten_korrigiert
mod.zh01 = zh

sys.argv = [BL, "--html", "--konto-t", str(eigen.konto_t),
            "--tranche-t", str(eigen.tranche_t)] + rest
sys.exit(mod.main() if hasattr(mod, "main") else 0)
