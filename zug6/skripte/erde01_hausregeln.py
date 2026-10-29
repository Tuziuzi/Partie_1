#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hausregeln dieser Partie, die der ERDE-01-Motor nicht aus dem Stand liest.

HINTERGRUND. `erde01_engine.py` laedt seine Regeln beim Import fest aus
`assets/erde01_regeln.json` des Skillbundles (Zeile 153) und bietet weder ein
Zustandsfeld noch ein CLI-Flag, um
`innenpolitik.korruption.regimewirkung_wachstum.aktive_regel` umzuschalten —
obwohl der Regelort A-6.3 genau diesen Schalter als vorgesehenen Weg nennt.
Das Asset selbst darf nicht geaendert werden: es wird beim naechsten
Bundle-Abgleich ueberschrieben.

Darum wird der Schalter hier nach dem Import gesetzt. Jedes Kampagnenskript,
das A-6 rechnet, importiert dieses Modul VOR dem ersten Motoraufruf:

    import erde01_hausregeln as HR
    HR.anwenden()

Wer den Motor als Unterprozess ueber die CLI aufruft, bekommt SAHA NICHT —
dort gilt weiter die Bundle-Vorgabe. Deshalb meldet `pruefen()` die Abweichung,
und `anwenden()` gibt zurueck, was es umgestellt hat.

HAUSENTSCHEIDUNGEN
  Z6-006 / RG-A6-VORZEICHEN (Tisch, 28.10.2026): SAHA aktiv statt GRUENDLER.
          Regelort korruption_terror.md A-6.3, Quelle QK-06 Saha/Sen 2020.
"""
import os
import sys

SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/"
      "erde01-gm")
if os.path.join(SK, "scripts") not in sys.path:
    sys.path.insert(0, os.path.join(SK, "scripts"))

HAUSREGELN = {
    "innenpolitik.korruption.regimewirkung_wachstum.aktive_regel": {
        "soll": "SAHA",
        "bundle_vorgabe": "GRUENDLER",
        "entscheidung": "Z6-006 / RG-A6-VORZEICHEN — Tisch, 28.10.2026",
        "regelort": "erde01-gm:references/korruption_terror.md A-6.3",
    },
}


def _block():
    import erde01_engine as E
    return E.REGELN["innenpolitik"]["korruption"]["regimewirkung_wachstum"]


def pruefen():
    """Was das Bundle derzeit fuehrt, gegen die Hausentscheidung. Aendert nichts."""
    rw = _block()
    ist = rw.get("aktive_regel")
    soll = HAUSREGELN[
        "innenpolitik.korruption.regimewirkung_wachstum.aktive_regel"]["soll"]
    return {"ist_im_bundle": ist, "soll_haus": soll,
            "deckungsgleich": ist == soll,
            "SAHA_vorhanden": isinstance(rw.get("SAHA"), dict),
            "GRUENDLER_vorhanden": isinstance(rw.get("GRUENDLER"), dict)}


def anwenden():
    """Setzt die Hausregeln im importierten Motor. Gibt die Umstellungen zurueck."""
    rw = _block()
    e = HAUSREGELN[
        "innenpolitik.korruption.regimewirkung_wachstum.aktive_regel"]
    soll = e["soll"]
    if not isinstance(rw.get(soll), dict):
        raise RuntimeError(
            f"Hausregel nicht anwendbar: das Bundle fuehrt keinen Block "
            f"{soll!r} in innenpolitik.korruption.regimewirkung_wachstum. "
            f"Vorhanden: {sorted(k for k in rw if isinstance(rw[k], dict))}")
    vorher = rw.get("aktive_regel")
    rw["aktive_regel"] = soll
    return [{"pfad": "innenpolitik.korruption.regimewirkung_wachstum.aktive_regel",
             "vorher": vorher, "nachher": soll,
             "entscheidung": e["entscheidung"], "regelort": e["regelort"],
             "f_autokratie_vorher": (rw.get(vorher) or {}).get("autokratie"),
             "f_autokratie_nachher": rw[soll]["autokratie"]}]


if __name__ == "__main__":
    import json
    print("PRUEFUNG vor dem Anwenden:")
    print(json.dumps(pruefen(), ensure_ascii=False, indent=1))
    print()
    print("ANWENDEN:")
    print(json.dumps(anwenden(), ensure_ascii=False, indent=1))
    print()
    print("PRUEFUNG danach:")
    print(json.dumps(pruefen(), ensure_ascii=False, indent=1))
