#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-6 Niveauabschlag unter GRUENDLER und unter SAHA — Tischentscheidungen
Z6-006 (RG-A6-VORZEICHEN) und Z6-005 (RG-A6-NIVEAU), 28.10.2026.

Regelinstanz ist ausschliesslich erde01-gm/scripts/erde01_engine.py. Dieses
Skript setzt KEINE eigene Formel (CLAUDE.md §3); es schaltet nur den vom
Regelort selbst vorgesehenen Schalter
`innenpolitik.korruption.regimewirkung_wachstum.aktive_regel`
(korruption_terror.md A-6.3) und ruft den Motor zweimal.

    python3 zug6/skripte/a6_niveau_saha.py
"""
import json, os, sys

SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/"
      "erde01-gm")
sys.path.insert(0, os.path.join(SK, "scripts"))
import erde01_engine as E          # noqa: E402
import hybrid01 as H               # noqa: E402

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ST = os.path.join(W, "stand", "erde01_state_schwarzesee.json")

BLOECKE = ["usa", "eu", "indien", "china", "russland", "rest"]
KK = E.REGELN["innenpolitik"]["korruption"]
RW = KK["regimewirkung_wachstum"]
# Blockname im Stand -> Schluessel in truth.ressourcen (nur drei Bloecke gefuehrt)
RES = {"china": "china", "eu": "eu", "indien": "indien"}


def lauf(regel):
    """Ein Motorlauf je Block unter der genannten Regel. Der Schalter wird
    gesetzt, der Motor rechnet — nichts wird nachgebaut."""
    RW["aktive_regel"] = regel
    out = {}
    for b in BLOECKE:
        regime = H.regime_fuer(b)
        K = KK["startwerte_je_regime"][regime]
        kor = E._still(E.korruption, K, regime, ferne=0.0, dK=0.0, jahre_je_zug=1)
        out[b] = {"regime": regime, "K": K,
                  "aktive_regel": kor["aktive_regel"],
                  "niveau_abschlag_pct": kor["niveau_abschlag_pct"],
                  "niveau_bezug": kor["niveau_bezug"],
                  "f_korruption_coup": kor["f_korruption_coup"],
                  "kaskade_z_zuschlag": kor["kaskade_z_zuschlag"],
                  "wahre_zustimmung_pp": kor.get("wahre_zustimmung_pp")}
    return out


def main():
    urzustand = RW["aktive_regel"]
    g = lauf("GRUENDLER")
    s = lauf("SAHA")
    RW["aktive_regel"] = urzustand

    res = json.load(open(ST))["truth"]["ressourcen"]

    print("A-6.2 NIVEAUABSCHLAG — niveau_abschlag_pct = -17 * (K - 0,45) / 0,30 * f_regime")
    print("Regelort: korruption_terror.md A-6.2 / A-6.3 · Motor: erde01_engine.korruption")
    print()
    print(f"{'Block':10} {'Regimetyp':18} {'K':>5} {'GRUENDLER':>11} {'SAHA':>9} {'f_reg G':>8} {'f_reg S':>8}")
    print("-" * 76)
    for b in BLOECKE:
        demo = E._ist_demokratie(g[b]["regime"])
        fg = RW["GRUENDLER"]["demokratie" if demo else "autokratie"]
        fs = RW["SAHA"]["demokratie" if demo else "autokratie"]
        print(f"{b.upper():10} {g[b]['regime']:18} {g[b]['K']:>5} "
              f"{g[b]['niveau_abschlag_pct']:>10.3f}% {s[b]['niveau_abschlag_pct']:>8.3f}% "
              f"{fg:>8} {fs:>8}")
    print()
    print("BIP-Reihe im Stand (truth.ressourcen.<block>.bip_bio_usd) — nur drei Bloecke gefuehrt:")
    print(f"{'Block':10} {'BIP ist':>12} {'* GRUENDLER':>14} {'* SAHA':>12}")
    print("-" * 52)
    for b in BLOECKE:
        key = RES.get(b)
        if key is None or key not in res:
            print(f"{b.upper():10} {'— keine Reihe im Stand —':>40}")
            continue
        ist = res[key]["bip_bio_usd"]
        print(f"{b.upper():10} {ist:>12.4f} "
              f"{ist * (1 + g[b]['niveau_abschlag_pct'] / 100.0):>14.4f} "
              f"{ist * (1 + s[b]['niveau_abschlag_pct'] / 100.0):>12.4f}")
    print()
    print("Schalter nach dem Lauf zurueckgestellt auf:", RW["aktive_regel"])
    if "--json" in sys.argv:
        print(json.dumps({"GRUENDLER": g, "SAHA": s, "bip_ist": res},
                         ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
