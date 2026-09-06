#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSFIX B-38 — der Leser laesst unbekannte Felder des Kopierblocks fallen.

Befund: zh01_blattlesen.py baut aus blatt["felder"] eine FESTE Struktur; jedes
Feld, das dort keinen Platz hat, verschwindet ersatzlos. Freitext kennt der
Leser nur in zwei Slots, z_text1 und z_text2 — und beide sind auf Blatt 3
bereits belegt. Der fuenfte Reiter »FREITEXT« (Feld f_freitext) reist im
Kopierblock zwar mit — werte() sammelt woertlich $$("[id^=f_]") —, kommt aber
im Leserergebnis nicht an.

Dieser Wrapper aendert die Skilldatei nicht. Er ruft den Originalleser auf und
reicht den Freitext zusaetzlich durch, damit nichts verloren geht. Die
Kampagnenregel »stille Kuerzungen sind verboten« gilt fuer Spielertext zuerst.

Aufruf: python3 zh01_kopie_freitext.py --skill <S> <kopie.txt> [...] [--json]
"""
import sys, os, json, argparse, importlib.util, re

vor = argparse.ArgumentParser(add_help=False)
vor.add_argument("--skill", required=True)
eigen, rest = vor.parse_known_args()

BL = os.path.join(eigen.skill, "zeughaus-gm", "scripts", "zh01_blattlesen.py")
spec = importlib.util.spec_from_file_location("zh01_bl_haus", BL)
mod = importlib.util.module_from_spec(spec); sys.modules["zh01_bl_haus"] = mod
spec.loader.exec_module(mod)

original = mod.lies_kopie

def lies_kopie_mit_freitext(text, gamestate=None, *a, **kw):
    m = original(text, gamestate, *a, **kw) if a or kw else original(text, gamestate)
    try:
        roh = re.search(r"--- ZH01-BLATT ANFANG ---\s*(\{.*?\})\s*--- ZH01-BLATT ENDE ---",
                        text, re.S)
        if roh:
            felder = (json.loads(roh.group(1)).get("felder") or {})
            ft = (felder.get("freitext") or "").strip()
            if ft and isinstance(m, dict) and not m.get("fehler"):
                m["freitext"] = ft
                vor_a = (m.get("anmerkung") or "").strip()
                m["anmerkung"] = (vor_a + "\n\n" if vor_a else "") + ft
                m.setdefault("_hausfix", []).append(
                    "B-38: felder.freitext aus dem Kopierblock nachgereicht "
                    "(Reiter 5); der Originalleser kennt das Feld nicht.")
    except Exception as e:
        print(f"[HAUSFIX B-38] Freitext nicht lesbar: {type(e).__name__}: {e}", file=sys.stderr)
    return m

mod.lies_kopie = lies_kopie_mit_freitext
sys.argv = [BL] + rest
sys.exit(mod.main() if hasattr(mod, "main") else 0)
