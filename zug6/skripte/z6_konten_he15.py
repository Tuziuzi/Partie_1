#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zug-6-Bodenkonten nach der Niveaubuchung Z6-025 neu buchen (HE-15 BIP-Kopplung).

Z5-046 rechnete die Zug-6-Konten als zh01.py konto --ausgaben <BIP 2030 x Quote> --restraum-vortrag <v>.
Z6-025 hat das BIP 2030 von china und eu danach einmalig verschoben. Dieses Skript rechnet denselben
Weg mit dem gebuchten BIP neu (Probe: mit dem alten BIP muessen exakt die Z5-046-Werte herauskommen,
sonst bricht es ab) und bucht zug6_t / zug6_tranche_t / zug6_ausgaben_mrd neu; die alten Werte bleiben
als *_vor_z6025 stehen. Regelinstanz ist zh01.py (CLAUDE.md §3).

    python3 zug6/skripte/z6_konten_he15.py              Trockenlauf
    python3 zug6/skripte/z6_konten_he15.py --schreiben  scharf
"""
import datetime, glob, json, os, shutil, subprocess, sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GS, ERDE = os.path.join(W, "stand", "gamestate.json"), os.path.join(W, "stand", "erde01_state_schwarzesee.json")
ZH = sorted(glob.glob("/root/.claude/skills/synced/*/zeughaus-gm/scripts/zh01.py"))[0]
QUOTE = {"CHN": 1.7697, "EU": 1.7493, "IND": 2.0039}       # Z5-046, Prozent des BIP, unveraendert gegen Zug 5
STAAT = {"CHN": "china", "EU": "eu", "IND": "indien"}


def konto(f, ausg, vortrag):
    r = subprocess.run([sys.executable, ZH, "konto", "--fraktion", f, "--ausgaben", str(ausg),
                        "--restraum-vortrag", str(vortrag), "--json"], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    h = d["hochtechnologie"]
    return d["bodenkonto_t"], (h.get("tranche_t") if isinstance(h, dict) else h)


def main():
    schreiben = "--schreiben" in sys.argv
    g, e = json.load(open(GS)), json.load(open(ERDE))
    buch = {b["fraktion"]: b["delta"] for b in e["truth"]["buchungen"] if b["id"].startswith("Z6-A6NIVEAU-")}
    neu = {}
    for f in ("CHN", "EU", "IND"):
        s = STAAT[f]; nach = e["truth"]["ressourcen"][s]["bip_bio_usd"]; vor = round(nach - buch[s], 4)
        b = g["zeughaus"]["fraktionen"][f]["bodenkonto"]; v = b["zug6_vortrag_t"]
        a_vor = round(vor * 1000 * QUOTE[f] / 100, 1); a_nach = round(nach * 1000 * QUOTE[f] / 100, 1)
        k0, t0 = konto(f, a_vor, v)
        if (k0, t0) != (b["zug6_t"], b["zug6_tranche_t"]) and "zug6_t_vor_z6025" not in b:
            raise SystemExit(f"PROBE GESCHEITERT {f}: alter Weg ergibt {k0}/{t0}, gebucht {b['zug6_t']}/{b['zug6_tranche_t']}")
        k1, t1 = konto(f, a_nach, v)
        neu[f] = (a_nach, k1, t1)
        print(f"{f}: BIP {vor} -> {nach} · Ausgaben {a_vor} -> {a_nach} Mrd · Konto {k0} -> {k1} t · Tranche {t0} -> {t1} t")
    if not schreiben:
        print("TROCKENLAUF — nichts geschrieben."); return 0
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(GS, os.path.join(W, "stand", "snapshots", f"gamestate_vor_z6_konten_{stamp}.json"))
    for f, (a, k, t) in neu.items():
        b = g["zeughaus"]["fraktionen"][f]["bodenkonto"]
        if "zug6_t_vor_z6025" not in b:
            b["zug6_t_vor_z6025"], b["zug6_tranche_t_vor_z6025"], b["zug6_ausgaben_mrd_vor_z6025"] = \
                b["zug6_t"], b["zug6_tranche_t"], b["zug6_ausgaben_mrd"]
        b["zug6_t"], b["zug6_tranche_t"], b["zug6_ausgaben_mrd"] = k, t, a
        b["zug6_beleg_z6025"] = ("Neu gebucht 25.11.2026 nach der Niveaubuchung Z6-025 (BIP 2030 verschoben): "
                                 "zh01.py konto --ausgaben <BIP x Quote> --restraum-vortrag <v>, Quote nach Z5-046; "
                                 "zug6/skripte/z6_konten_he15.py; Journal Z6-045")
    json.dump(g, open(GS + ".neu", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(GS + ".neu", GS)
    print("GEBUCHT, Sicherung snapshots/gamestate_vor_z6_konten_%s.json" % stamp); return 0


if __name__ == "__main__":
    sys.exit(main())
