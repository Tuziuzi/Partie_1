#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B-2 Kaskadenwurf fuer Zug 5 (2030) — Nachwurf nach Tischentscheidung Z6-011/B-30.

Tischentscheidung 28.10.2026: nachwuerfeln, Wirkung ab Zug 6 vorwaerts; Zug 5
bleibt gebucht.

SEED. regime.md »Kaskade (B-2)« woertlich: »wuerfelt W10000 <= p*10000 (Stufe
`aufloesung`, Seed aus der Registry, Nonce `b2|<staat>|<akteur>`)«. Stufe
`aufloesung` der Zug-5-Registry ist 20300103 — derselbe Seed, auf dem auch die
uebrigen Zug-5-Wuerfe liegen (audit.wuerfe W-005-0001 und W-005-0002). Die
Zuege 2-4 protokollierten <Jahr>0107 (Stufe `kipppunkte`); diese Abweichung von
der Regelstelle wird als Befund gefuehrt, nicht fortgeschrieben.

EINGABEN. b und z sind die ZUG-5-Werte aus dem Stand
(module.erde01.daten.staaten.<block>.kaskade_b2_vorschau: b und z_alt), nicht
die Zug-6-Werte z_neu — der A-6.7-z-Zuschlag wirkt erst ab Zug 6.

Regelinstanz ist erde01_engine.kaskade. Dieses Skript setzt keine Formel.

    python3 zug6/skripte/kaskade_zug5_nachwurf.py
    python3 zug6/skripte/kaskade_zug5_nachwurf.py --json
"""
import json, os, sys

SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/"
      "erde01-gm")
sys.path.insert(0, os.path.join(SK, "scripts"))
import erde01_engine as E          # noqa: E402

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ST = os.path.join(W, "stand", "erde01_state_schwarzesee.json")

BLOECKE = ["usa", "eu", "indien", "china", "russland", "rest"]
ZUG = 5
AKTEUR = ""          # Vorgabe des Motors; kein frei gewaehlter Nonce-Anteil


def main():
    stand = json.load(open(ST))
    reg = stand["kopf"]["seed_registry"]
    seed = reg["stufen_seeds"]["aufloesung"]
    staaten = stand["module"]["erde01"]["daten"]["staaten"]

    print("B-2 KASKADENWURF ZUG 5 (2030) — NACHWURF (Z6-011 / B-30)")
    print("Regelort: regime.md »Kaskade (B-2)« · Motor: erde01_engine.kaskade")
    print(f"Seed {seed} (kopf.seed_registry.stufen_seeds.aufloesung, Zug-5-Registry)")
    print(f"Formel: p = clamp((b - 0,15) * 0,15 * z, 0, 0,95) · Wurf W10000 <= p*10000")
    print()
    print(f"{'Block':10} {'b':>5} {'z_alt':>7} {'p/Zug':>9} {'Schwelle':>9} "
          f"{'Wurf':>6} {'Ergebnis':>10}")
    print("-" * 64)

    roh, ausgeloest = {}, []
    for b in BLOECKE:
        v = staaten[b]["kaskade_b2_vorschau"]
        bw, z = v["b"], v["z_alt"]
        r = E._still(E.kaskade, bw, z, staat=b, wurf_an=True, seed=seed,
                     zug=ZUG, akteur=AKTEUR)
        roh[b] = r
        p = r["p_je_zug"]
        schwelle = p * 10000
        wurf = r["wurf"]["ergebnis"]
        aus = r["ausgeloest"]
        if aus:
            ausgeloest.append(b)
        print(f"{b.upper():10} {bw:>5} {z:>7} {p:>8.5f} {schwelle:>9.1f} "
              f"{wurf:>6} {'KASKADE' if aus else 'ruhig':>10}")

    print()
    if ausgeloest:
        print("AUSGELOEST:", ", ".join(x.upper() for x in ausgeloest))
        print("Folge (regime.md B-2): innenlage.zustimmung_geaeussert := legitimitaet/100.")
        print("Tischentscheidung: Wirkung ab Zug 6, Zug 5 bleibt gebucht.")
    else:
        print("Kein Block ausgeloest — die Luecke in der Kaskadenreihe ist geschlossen,")
        print("ohne dass sich an der Lage etwas aendert.")
    print()
    print("ROHAUSGABE JE BLOCK (woertlich fuer das Journal):")
    for b in BLOECKE:
        r = roh[b]
        print(f"  {b}: wurf={json.dumps(r['wurf'], ensure_ascii=False)} "
              f"p_je_zug={r['p_je_zug']} ausgeloest={r['ausgeloest']} "
              f"seed_quelle={r.get('seed_quelle')}")

    if "--json" in sys.argv:
        print(json.dumps(roh, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
