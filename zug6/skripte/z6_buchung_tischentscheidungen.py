#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buchung der vier Tischentscheidungen vom 28.10.2026 (Zug 6, Jahr 2031).

  Z6-006  RG-A6-VORZEICHEN  SAHA aktiv statt GRUENDLER (x-0,5 fuer Autokratien)
  Z6-005  RG-A6-NIVEAU      Niveauabschlag auf die BIP-Reihe, in beide Richtungen
  Z6-011  B-30              B-2-Kaskadenwurf Zug 5 nachgewuerfelt, Wirkung ab Zug 6
  Z6-018  RG-FO-2030        L1-Ration 2030 wird in Zug 6 nachgeholt  (nur Hausregel;
                            die Wuerfe fallen in der Zug-6-Aufloesung)

Regelinstanz ist erde01_engine.py. Dieses Skript setzt KEINE Formel (CLAUDE.md §3);
es ruft den Motor und legt ab.

    python3 zug6/skripte/z6_buchung_tischentscheidungen.py              Trockenlauf
    python3 zug6/skripte/z6_buchung_tischentscheidungen.py --schreiben  scharf
"""
import json, os, shutil, sys, datetime

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import erde01_hausregeln as HR                                    # noqa: E402
HR.anwenden()                                  # SAHA VOR dem ersten Motoraufruf
import erde01_engine as E                                         # noqa: E402
import hybrid01 as H                                              # noqa: E402

W = os.path.join(HIER, "..", "..")
ERDE = os.path.join(W, "stand", "erde01_state_schwarzesee.json")
GS = os.path.join(W, "stand", "gamestate.json")

BLOECKE = ["usa", "eu", "indien", "china", "russland", "rest"]
RES = {"china": "china", "eu": "eu", "indien": "indien"}   # nur diese drei fuehren eine Reihe
KK = E.REGELN["innenpolitik"]["korruption"]
ZUG = 6
HEUTE = "2026-10-28"

NIVEAU_BEGR = (
    "RG-A6-NIVEAU: AUF DIE BIP-REIHE GEBUCHT (Tischentscheidung 28.10.2026, "
    "Variante 'beides so buchen wie entschieden'). Einmalbuchung nach A-6.2 "
    "(Niveau, keine Jahresrate), symmetrisch in beide Richtungen. Zwei "
    "Asymmetrien wurden dem Tisch vor der Buchung vorgelegt und in Kauf "
    "genommen: (1) unter SAHA ist der Abschlag fuer Autokratien eine PRAEMIE, "
    "Indien ist mit K = K_ref 0,45 der einzige Block ohne Wirkung; (2) eine "
    "BIP-Reihe fuehrt der Stand nur fuer china, eu und indien — USA, Russland "
    "und REST bleiben unberuehrt (KB-02 W-1a Fn. 1; vgl. RG-Z5-03).")

RULES_GAP_NEU = (
    "QK-01 und QK-06 widersprechen sich im VORZEICHEN fuer Autokratien. "
    "ENTSCHIEDEN am Tisch 28.10.2026 (Z6-006 / RG-A6-VORZEICHEN): aktiv ist "
    "SAHA (x-0,5, QK-06 Saha/Sen 2020, Ostasien-Paradox); GRUENDLER (x1,3) "
    "bleibt als Alternativregel bereit. Der Schalter liegt im Skill-Asset und "
    "wird kampagnenseitig von zug6/skripte/erde01_hausregeln.py gesetzt — der "
    "Motor bietet dafuer weder Zustandsfeld noch CLI-Flag (Befund Z6-023).")

# Zug-5-Nachwurf: Rohausgabe aus kaskade_zug5_nachwurf.py, woertlich.
KASKADE_Z5 = [
    ("usa",      943, 0.0),
    ("eu",      3812, 0.00827),
    ("indien",  5183, 0.0675),
    ("china",   8380, 0.0975),
    ("russland", 6334, 0.0525),
    ("rest",    7480, 0.0345),
]


def a6_neu():
    """A-6 je Block unter SAHA — ein Motorlauf je Block, nichts nachgebaut."""
    out = {}
    for b in BLOECKE:
        regime = H.regime_fuer(b)
        K = KK["startwerte_je_regime"][regime]
        out[b] = E._still(E.korruption, K, regime, ferne=0.0, dK=0.0,
                          jahre_je_zug=1)
    return out


def main():
    schreiben = "--schreiben" in sys.argv
    erde = json.load(open(ERDE))
    gs = json.load(open(GS))
    staaten = erde["module"]["erde01"]["daten"]["staaten"]
    res = erde["truth"]["ressourcen"]
    neu = a6_neu()

    print("=" * 78)
    print("BUCHUNG DER TISCHENTSCHEIDUNGEN — Zug 6 (2031)")
    print("Modus:", "SCHARF (--schreiben)" if schreiben else "TROCKENLAUF")
    print("=" * 78)

    # ── 1. A-6 unter SAHA ────────────────────────────────────────────────────
    print()
    print("1. Z6-006 SAHA — niveau_abschlag_pct je Block")
    print(f"   {'Block':10} {'Regel alt':11} {'alt':>9} -> {'Regel neu':9} {'neu':>9}")
    for b in BLOECKE:
        alt = staaten[b]["korruption"]
        print(f"   {b.upper():10} {alt.get('aktive_regel',''):11} "
              f"{alt['niveau_abschlag_pct']:>8.3f}% -> {neu[b]['aktive_regel']:9} "
              f"{neu[b]['niveau_abschlag_pct']:>8.3f}%")

    # ── 2. Niveauabschlag auf die BIP-Reihe ──────────────────────────────────
    print()
    print("2. Z6-005 Niveauabschlag auf truth.ressourcen.<block>.bip_bio_usd")
    buchungen, bip_neu = [], {}
    for b in BLOECKE:
        key = RES.get(b)
        pct = neu[b]["niveau_abschlag_pct"]
        if key is None or key not in res:
            print(f"   {b.upper():10} keine Reihe im Stand — nicht gebucht "
                  f"(waere {pct:+.3f} %)")
            continue
        ist = res[key]["bip_bio_usd"]
        delta = round(ist * pct / 100.0, 4) + 0.0   # -0.0 -> 0.0
        ziel = round(ist + delta, 4)
        bip_neu[key] = ziel
        print(f"   {b.upper():10} {ist:>9.4f} {delta:>+9.4f} -> {ziel:>9.4f} "
              f"({pct:+.3f} %)")
        buchungen.append({
            "id": f"Z6-A6NIVEAU-{key}", "zug": ZUG, "fraktion": key,
            "konto": "bip_bio_usd", "delta": delta,
            "grund": (f"A-6.2 Niveauabschlag als Einmalbuchung: {pct:+.3f} % "
                      f"({ist} -> {ziel} Bio USD). K = {neu[b]['K']} gegen "
                      f"K_ref {neu[b]['niveau_bezug']}, f_regime aus SAHA "
                      f"(Z6-006). Niveau, keine Jahresrate."),
            "beleg": ("erde01_engine.korruption · korruption_terror.md A-6.2/A-6.3 · "
                      "Tischentscheidung 28.10.2026 (Z6-005, Z6-006) · "
                      "zug6/skripte/z6_buchung_tischentscheidungen.py")})

    # ── 3. Kaskadenwurf Zug 5 ────────────────────────────────────────────────
    print()
    print("3. Z6-011 B-2-Kaskadenwurf Zug 5 (Seed 20300103, Stufe aufloesung)")
    vorhanden = len(erde["audit"]["wuerfe"])
    wuerfe = []
    for i, (b, erg, p) in enumerate(KASKADE_Z5, 1):
        nr = vorhanden + i
        wuerfe.append({
            "id": f"W-005-{nr:04d}", "id_motor": f"W-005-{i:04d}",
            "zug": 5, "stufe": "aufloesung", "seed": 20300103,
            "wurf": "W10000", "ergebnis": erg,
            "zweck": f"Kaskade B-2 {b} — Nachwurf Zug 5 (Z6-011/B-30)",
            "regelref": "B-2", "schwelle": round(p * 10000, 1),
            "kaskade": erg <= p * 10000,
            "nonce": f"b2|{b}|",
            "nachgewuerfelt": ("Tischentscheidung 28.10.2026: Zug 5 bleibt "
                               "gebucht, Wirkung ab Zug 6. Eingaben b und z_alt "
                               "aus kaskade_b2_vorschau des Stands."),
            "id_hinweis": ("id_motor ist die Nummer aus der Rohausgabe; die id "
                           "ist auf den Bestand von audit.wuerfe fortgezaehlt, "
                           "weil W-005-0001..0006 schon belegt waren.")})
        print(f"   {b.upper():10} Wurf {erg:>5} gegen Schwelle "
              f"{p*10000:>7.1f} -> {'KASKADE' if erg <= p*10000 else 'ruhig'}")
    print("   Ergebnis: kein Block ausgeloest.")

    # ── 4. Hausregeln + Aenderungslog ───────────────────────────────────────
    hausregeln = [
        {"regel": "A-6.3 Vorzeichen in Autokratien", "rev": "SAHA",
         "geltung": "ab Zug 6 (2031)",
         "entscheidung": "Z6-006 / RG-A6-VORZEICHEN — Tisch, 28.10.2026",
         "wirkung": "f_regime Autokratie -0,5 statt 1,3 (CHN, RUS, REST)",
         "schalter": ("innenpolitik.korruption.regimewirkung_wachstum.aktive_regel "
                      "im Skill-Asset; kampagnenseitig gesetzt von "
                      "zug6/skripte/erde01_hausregeln.py"),
         "beleg": "erde01-gm:references/korruption_terror.md A-6.3 · QK-06 Saha/Sen 2020"},
        {"regel": "A-6.2 Niveauabschlag", "rev": "gebucht",
         "geltung": "Einmalbuchung in Zug 6 (2031)",
         "entscheidung": "Z6-005 / RG-A6-NIVEAU — Tisch, 28.10.2026",
         "wirkung": ("auf truth.ressourcen.<block>.bip_bio_usd, symmetrisch; "
                     "nur china, eu, indien fuehren eine Reihe"),
         "beleg": "erde01-gm:references/korruption_terror.md A-6.2 · KB-02 §0.4 (Niveau, nicht Rate)"},
        {"regel": "Forschung Rev. D — L1-Ration 2030", "rev": "nachgeholt",
         "geltung": "Zug 6 (2031), einmalig",
         "entscheidung": "Z6-018 / RG-FO-2030 — Tisch, 28.10.2026",
         "wirkung": ("je Fraktion ein L1-Wurf in Zug 6, obwohl 2031 regulaer "
                     "keine Ration traegt; Chinas Streak-Tech bleibt zusaetzlich"),
         "beleg": "deltav-game-master:references/research.md Rev. D §1.1/§1.2/§7"},
    ]
    log = [
        {"zug": ZUG, "hausentscheidung": True,
         "eintrag": ("Z6-006 RG-A6-VORZEICHEN entschieden: SAHA aktiv (x-0,5 fuer "
                     "Autokratien) statt GRUENDLER (x1,3). A-6 fuer alle sechs "
                     "Bloecke neu gerechnet; nur niveau_abschlag_pct aendert sich, "
                     "weil dK = 0 ist.")},
        {"zug": ZUG, "hausentscheidung": True,
         "eintrag": ("Z6-005 RG-A6-NIVEAU entschieden: Niveauabschlag als "
                     "Einmalbuchung auf die BIP-Reihe, in beide Richtungen. "
                     "eu +15,300 %, china +1,417 %, indien +0,000 %. USA, "
                     "Russland und REST fuehren keine Reihe und bleiben "
                     "unberuehrt — Asymmetrie vorgelegt und in Kauf genommen.")},
        {"zug": ZUG, "hausentscheidung": True,
         "eintrag": ("Z6-011 B-30 entschieden: B-2-Kaskadenwurf fuer Zug 5 "
                     "nachgewuerfelt, Seed 20300103 (Stufe aufloesung der "
                     "Zug-5-Registry, derselbe Seed wie W-005-0001/0002). "
                     "Alle sechs Bloecke ruhig; Zug 5 bleibt unveraendert.")},
        {"zug": ZUG, "hausentscheidung": True,
         "eintrag": ("Z6-018 RG-FO-2030 entschieden: die einmalige L1-Ration des "
                     "Jahres 2030 wird in Zug 6 fuer alle sechs Fraktionen "
                     "nachgeholt. Die Wuerfe fallen in der Zug-6-Aufloesung.")},
    ]

    print()
    print("4. Hausregeln:", len(hausregeln), "· Aenderungslog:", len(log),
          "· truth.buchungen:", len(buchungen), "· audit.wuerfe:", len(wuerfe))

    if not schreiben:
        print()
        print("TROCKENLAUF — nichts geschrieben. Mit --schreiben buchen.")
        return 0

    # ── schreiben ────────────────────────────────────────────────────────────
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap = os.path.join(W, "stand", "snapshots")
    os.makedirs(snap, exist_ok=True)
    for p, name in ((ERDE, "erde01_vor_z6_tischentscheidungen"),
                    (GS, "gamestate_vor_z6_tischentscheidungen")):
        shutil.copy2(p, os.path.join(snap, f"{name}_{stamp}.json"))

    for b in BLOECKE:
        alt = staaten[b]["korruption"]
        frisch = dict(neu[b])
        frisch["rules_gap"] = RULES_GAP_NEU if frisch.get("rules_gap") else None
        for feld in ("K_herkunft", "patronage_posten", "bekaempfung_stufe"):
            if feld in alt:
                frisch[feld] = alt[feld]
        frisch["niveau_gebucht"] = bool(RES.get(b) in res)
        frisch["niveau_begruendung"] = NIVEAU_BEGR
        frisch["niveau_zielfeld"] = (
            f"truth.ressourcen.{RES[b]}.bip_bio_usd" if RES.get(b) in res
            else "— der Stand fuehrt fuer diesen Block keine BIP-Reihe")
        staaten[b]["korruption"] = frisch

    for key, wert in bip_neu.items():
        res[key]["bip_bio_usd"] = wert
    erde["truth"]["buchungen"].extend(buchungen)
    erde["audit"]["wuerfe"].extend(wuerfe)
    erde["kopf"]["aenderungslog"].extend(log)
    # kopf.zug und kopf.uhr.datum_ingame bleiben auf 5 / 2030-12-31: sie
    # beschreiben den ABGESCHLOSSENEN Zug. Zug 6 ist nicht aufgeloest; die
    # Fortschreibung gehoert in die Aufloesung, nicht in diese Buchung.

    gs["state"].setdefault("houseRules", []).extend(hausregeln)
    gs["meta"]["lastModified"] = datetime.datetime.now().isoformat(timespec="seconds")

    for p, obj in ((ERDE, erde), (GS, gs)):
        tmp = p + ".neu"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, p)

    print()
    print("GEBUCHT. Sicherung in stand/snapshots/*_%s.json" % stamp)
    print("kopf.zug bleibt 5 (abgeschlossener Zug) — Zug 6 ist nicht aufgeloest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
