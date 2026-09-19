#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die drei HTML-Befehlsblaetter fuer Zug 6 (2031) in einem Lauf.

Kette (jede Stufe ist ein benannter Hausfix oder Hausbaustein):
  0  gamestate_computepfad_adapter.py   B-37  computeConfig -> economy.resources.compute
  1  zh01_html_kasse_fix.py             B-36  --konto-t/--tranche-t im HTML-Weg
     mit --c9                           B-39  Raumfahrtquote (Selbsterkennung greift nicht)
  2  blatt_innenlage_reiter.py          B-31  Reiter 5 »Innenlage« (A-6/A-7)
  3  blatt_werft_reiter.py                    Reiter 6 »Werft« (PW-01, BZ-01
                                             Rev. B, Forschung Rev. D)
  4  blatt_freitext_reiter.py                 Reiter 7 »Freitext«

Kontowerte aus zh01.py konto, Zug 6 (Journal Z5): CHN 2659,0 / 398,9 ·
EU 1670,6 / 250,6 · IND 764,0 / 114,6.
"""
import os, shutil, subprocess, sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = ("/root/.claude/skills/synced/"
     "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773")
AUS = os.path.join(W, "zug6", "blaetter")
TMP = os.path.join(W, "zug6", "skripte", "_arbeit")

FRAKTIONEN = [
    # Kuerzel, Staat,   Spieler,  konto_t, tranche_t, Doktrin
    ("IND", "indien", "JAKOB_INDIEN", 764.0, 114.6, "de_eskalationsschlag"),
    ("CHN", "china",  "ANDI_CHINA",  2659.0, 398.9, "ambiguitaet"),
    ("EU",  "eu",     "ROMAN_EU",    1670.6, 250.6, None),
]


def lauf(cmd, erwarte=None, **kw):
    """erwarte: Datei, deren Vorhandensein den Erfolg belegt.

    Noetig, weil zh01_html_kasse_fix.py mit `sys.exit(mod.main())` endet und
    main() den Dateipfad zurueckgibt — sys.exit(<Zeichenkette>) heisst Rueckgabe-
    code 1, obwohl das Blatt sauber geschrieben wurde. Der Pfad ist der Beleg,
    nicht der Code."""
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    ok = (r.returncode == 0) or (erwarte and os.path.exists(erwarte))
    if not ok:
        print(r.stdout); print(r.stderr, file=sys.stderr)
        raise SystemExit(f"FEHLGESCHLAGEN: {' '.join(cmd[:4])} …")
    return r


def main():
    os.makedirs(TMP, exist_ok=True); os.makedirs(AUS, exist_ok=True)
    gs = os.path.join(TMP, "gamestate_compute.json")
    print("0  B-37 Computepfad spiegeln")
    r = lauf(["python3", os.path.join(W, "zug5", "skripte",
                                      "gamestate_computepfad_adapter.py"),
              os.path.join(W, "stand", "gamestate.json"), gs])
    print("   " + r.stdout.strip().replace("\n", "\n   "))

    for kurz, staat, spieler, konto, tranche, doktrin in FRAKTIONEN:
        print(f"\n{kurz} — {spieler}")
        cmd = ["python3", os.path.join(W, "zug5", "skripte", "zh01_html_kasse_fix.py"),
               "--skill", S, "--konto-t", str(konto), "--tranche-t", str(tranche),
               "--fraktion", kurz, "--staat", staat, "--zug", "6",
               "--gamestate", gs,
               "--lagewerk", os.path.join(S, "lagewerk", "daten", "konventionell_2026.json"),
               "--erde01", os.path.join(S, "erde01-gm"),
               "--c2", "NORMATIV", "--w-index", "1.0", "--c9",
               "--aus", TMP, "--praefix", "roh"]
        if doktrin:
            cmd += ["--doktrin", doktrin]
        roh = os.path.join(TMP, f"Befehlsblatt_{kurz}_Zug6.html")
        if os.path.exists(roh):
            os.remove(roh)
        r = lauf(cmd, erwarte=roh)
        for l in (r.stdout + r.stderr).splitlines():
            if l.strip():
                print("   " + l.strip())

        if not os.path.exists(roh):
            raise SystemExit(f"   Erzeuger hat {roh} nicht geschrieben.")
        for bau in ("zug6/skripte/blatt_innenlage_reiter.py",
                    "zug6/skripte/blatt_werft_reiter.py",
                    "zug5/skripte/blatt_freitext_reiter.py"):
            r = lauf(["python3", os.path.join(W, bau), roh])
            for l in r.stdout.splitlines():
                if l.strip():
                    print("   " + l.strip())
        ziel = os.path.join(AUS, f"Befehlsblatt_{spieler}_Zug6.html")
        shutil.copyfile(roh, ziel)
        print(f"   -> {os.path.relpath(ziel, W)}  "
              f"({os.path.getsize(ziel)/1024:.1f} KiB)")

    shutil.rmtree(TMP, ignore_errors=True)
    print("\nfertig.")


if __name__ == "__main__":
    main()
