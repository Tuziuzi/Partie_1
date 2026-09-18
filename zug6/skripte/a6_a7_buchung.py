#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-6 KORRUPTION und A-7 TERROR — Erstbuchung fuer alle sechs Bloecke.

Regelinstanz ist ausschliesslich erde01-gm/scripts/erde01_engine.py und
hybrid01.py. Dieses Skript setzt KEINE eigene Formel; es besorgt die
Eingaben, ruft den Motor und legt das Ergebnis ab (CLAUDE.md §3).

Stand: nach Zug 5 (2030-12-31) — Eroeffnungslage fuer Zug 6.

    python3 zug6/skripte/a6_a7_buchung.py            Tafel
    python3 zug6/skripte/a6_a7_buchung.py --json     Buchungssatz
    python3 zug6/skripte/a6_a7_buchung.py --schreiben  in den Stand buchen
"""
import json, os, sys

SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/"
      "erde01-gm")
sys.path.insert(0, os.path.join(SK, "scripts"))
import erde01_engine as E          # noqa: E402
import hybrid01 as H               # noqa: E402

still = E._still
REGELN = E.REGELN["innenpolitik"]
KK, TT, CC = REGELN["korruption"], REGELN["terror"], REGELN["coup"]

STAND = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "stand", "erde01_state_schwarzesee.json")

BLOECKE = ["usa", "eu", "indien", "china", "russland", "rest"]
NAME = {"usa": "USA", "eu": "EU", "indien": "INDIEN", "china": "CHINA",
        "russland": "RUSSLAND", "rest": "REST"}

# --- Repression: Bestand am Ende von Zug 5 ----------------------------------
# Jede Zeile traegt ihren Beleg aus dem Stand. Geschaetzt ist nichts.
REPRESSION = {
    "usa":      (0.05, "regler_2027; domaenen_zug3 und zug4 bestaetigen 0,05"),
    "eu":       (0.20, "regler_2026 (0,08 -> 0,20); zug3 und zug4 bestaetigen 0,20"),
    "indien":   (0.60, "domaenen_zug4: 'Indien hebt die Repression von 0,4 auf 0,6'"),
    "china":    (0.80, "regler_2026 (0,72 -> 0,80); zug3 und zug4 bestaetigen 0,80"),
    "russland": (0.50, "ABGELEITET aus dem gebuchten B-2-Wert 5,25 % (domaenen_zug4) "
                       "ueber p = (rep - 0,15) * 0,15; an sieben Buchungen bestaetigt"),
    "rest":     (0.38, "staaten_2026.json; NPC-Aggregat, in fuenf Zuegen nie bewegt"),
}

# Blatt 4 fuehrt Ausschluss, Gegenterror, Einschluss, Patronage und
# Antikorruption erst ab Zug 6. Ohne Blatteintrag wird NICHT geraten
# (V24-Logik in blattlesen.py) — es gilt der Motorvorgabewert.
AUSSCHLUSS, GEGENTERROR, EINSCHLUSS, PATRONAGE, BEKAEMPFUNG = 0.0, 0, 0, 0, 0

# B-2: das b der Domaene innenpolitik. Aus den gebuchten Kaskadenwerten der
# Zuege 1-4 rueckgerechnet; es ist an allen sieben Buchungen identisch mit der
# Repression. p_alt = (rep - 0,15) * 0,15 * z, z = 1,0 ausser EU.
Z_ALT = {"usa": 1.0, "eu": 1.103, "indien": 1.0, "china": 1.0,
         "russland": 1.0, "rest": 1.0}
Z_ALT_BELEG = {"eu": "domaenen_zug5: GZ-01-Druckkonto Stufe G2 -> z-Zuschlag +0,103"}


def bip_indizes():
    """bip_index 0..1 aus dem Wohlstandsindex (BIP-Anteil / Bev-Anteil).

    A-7.1 nennt bip_index, definiert die Abbildung auf 0..1 aber nicht
    -> RULES-GAP RG-A7-BIP. Beide Lesarten werden gerechnet:
      L1 NORMIERT (gebucht): w / max(w) — 1,0 = reichster Block.
      L2 GEKLEMMT:           min(1, w)  — Weltdurchschnitt und darueber = 1,0.
    Der Regler traegt hoechstens +-10 % auf T (Faktor 0,9 + 0,2*bip_index).
    """
    w = {b: H.wohlstandsindex(b) for b in BLOECKE}
    wmax = max(w.values())
    return (w, {b: round(w[b] / wmax, 4) for b in BLOECKE},
            {b: round(min(1.0, w[b]), 4) for b in BLOECKE})


def buchungssatz():
    wohl, l1, l2 = bip_indizes()
    schwelle = TT["wirkung"]["wachstum"]["schwelle_vorfaelle_je_mio"]
    out = {}
    for b in BLOECKE:
        regime = H.regime_fuer(b)
        bev = H.BEVOELKERUNG_MIO[b]
        rep, rep_beleg = REPRESSION[b]
        K = KK["startwerte_je_regime"][regime]

        kor = still(E.korruption, K, regime, ferne=0.0, dK=0.0, jahre_je_zug=1)
        ter = still(E.terrorlage, regime, ausschluss=AUSSCHLUSS, repression=rep,
                    bip_index=l1[b], gegenterror=GEGENTERROR, K=K)
        ter2 = still(E.terrorlage, regime, ausschluss=AUSSCHLUSS, repression=rep,
                     bip_index=l2[b], gegenterror=GEGENTERROR, K=K)

        # A-2 Vorschau: derselbe Bestand, einmal ohne und einmal mit A-6.
        # Der SCHARFE Wurf gehoert in die Zug-6-Aufloesung mit dem Zug-6-Seed;
        # hier wird nur die Wahrscheinlichkeit gestellt.
        # ACHTUNG: _K() liefert auch bei korruption=None den Regimetyp-Startwert.
        # Der Motor kann den Zustand VOR A-6 also nicht mehr rechnen. Die
        # Vergleichszahl wird darum aus den Faktoren herausdividiert, die der
        # Motor selbst zurueckgibt — nicht nachgebaut.
        coup_vor = {}
        for flag in (True, False):
            mit = still(E.coup, regime, rezession=flag, korruption=K,
                        patronage=PATRONAGE, zug=0, akteur=f"vorschau_{b}")
            p_ohne = mit["p_je_zug"] / (mit["f_korruption"] * mit["f_patronage"])
            coup_vor["rezession" if flag else "ohne_rezession"] = {
                "p_ohne_A6": round(p_ohne, 5), "p_mit_A6": mit["p_je_zug"],
                "p_basis": CC["p_basis"][regime],
                "f_rezession": (CC["f_rezession"] if flag else 1.0),
                "f_korruption": mit["f_korruption"],
                "f_patronage": mit["f_patronage"],
                "hinweis": "Wurf verworfen. Der scharfe A-2-Wurf gehoert in die "
                           "Zug-6-Aufloesung mit dem Zug-6-Seed."}

        # B-2 Vorschau: nur der z-Zuschlag aus A-6.7 kommt hinzu.
        z_alt, z_neu = Z_ALT[b], Z_ALT[b] + kor["kaskade_z_zuschlag"]
        b2 = {"b": rep, "b_herkunft": "Domaene innenpolitik; aus den gebuchten "
                                      "Kaskadenwerten Zug 1-4 rueckgerechnet",
              "z_alt": round(z_alt, 4), "z_neu": round(z_neu, 4),
              "alt": still(E.kaskade, rep, z_alt),
              "neu": still(E.kaskade, rep, z_neu)}
        if b in Z_ALT_BELEG:
            b2["z_alt_beleg"] = Z_ALT_BELEG[b]

        je_mio = 1.0 / bev
        out[b] = {
            "name": NAME[b],
            "regimetyp": regime,
            "regimetyp_herkunft": ("staaten_2026.json; die Feinheit reich/arm "
                                   "abgeleitet in hybrid01.regime_fuer "
                                   "(BIP-Anteil je Bev-Anteil, Schwelle 1,0)"),
            "bevoelkerung_mio": bev,
            "wohlstandsindex": round(wohl[b], 4),
            "bip_index": {"gebucht": l1[b], "lesart": "L1 normiert auf den "
                          "reichsten Block", "alternative_L2_geklemmt": l2[b],
                          "T_bei_L2": ter2["T"], "rules_gap": "RG-A7-BIP"},
            "repression": {"wert": rep, "beleg": rep_beleg},
            "ausschluss": {"wert": AUSSCHLUSS,
                           "beleg": "Blatt 4 fuehrt das Feld erst ab Zug 6; ohne "
                                    "Eintrag gilt der Motorvorgabewert 0,0. Nicht "
                                    "geraten (V24-Logik blattlesen.py)."},
            "korruption": dict(kor,
                               K_herkunft="A-6.1 Startwert des Regimetyps — der "
                                          "Stand fuehrt keinen Eigenwert",
                               niveau_gebucht=False,
                               niveau_begruendung=(
                                   "RG-A6-NIVEAU: nicht auf die BIP-Reihe gebucht. "
                                   "(1) Die Reihe startet 2026 aus realen Daten und "
                                   "traegt das Korruptionsniveau bereits — ein "
                                   "zweites Mal buchen waere Doppelbuchung "
                                   "(CLAUDE.md §2). (2) Das vom Regelort genannte "
                                   "Zielfeld index_real ist in diesem Code eine "
                                   "EH-01-Energiekostengroesse, keine BIP-Reihe; "
                                   "der Stand fuehrt es nicht."),
                               patronage_posten=PATRONAGE,
                               bekaempfung_stufe=BEKAEMPFUNG),
            "terrorlage": dict(ter,
                               einschluss_stufe=EINSCHLUSS,
                               wachstumskanal=("NULL" if je_mio < schwelle else "AKTIV"),
                               vorfaelle_je_mio_bei_1_vorfall=round(je_mio, 6),
                               schwelle_vorfaelle_je_mio=schwelle,
                               wirkung_wachstum_pp=0.0,
                               wirkung_gegenterrorbudget_pp=round(
                                   -0.10 * GEGENTERROR, 2),
                               a7_5="Auf Blockgroesse ist der Wachstumskanal null "
                                    "[QT-11]. Wer trotzdem eine Zahl bucht, "
                                    "erfindet sie."),
            "coup_track_vorschau": coup_vor,
            "kaskade_b2_vorschau": b2,
        }
    return out


def tafel(d):
    z = []
    z.append(f"{'Block':9} {'Regime':17} {'K':>5} {'T':>7} {'Gefw':>6} "
             f"{'Schwund':>8} {'f_coup':>7} {'z+':>6} {'Wachstum':>9}")
    z.append("-" * 82)
    for b in BLOECKE:
        e = d[b]
        k, t = e["korruption"], e["terrorlage"]
        z.append(f"{e['name']:9} {e['regimetyp']:17} {k['K']:5.2f} {t['T']:7.4f} "
                 f"{k['gefechtswert_faktor']:6.3f} "
                 f"{k['beschaffungsschwund_anteil']*100:7.1f}% "
                 f"{k['f_korruption_coup']:7.3f} "
                 f"{k['kaskade_z_zuschlag']:+6.3f} {t['wachstumskanal']:>9}")
    return "\n".join(z)


def schreiben(d):
    with open(STAND, encoding="utf-8") as f:
        s = json.load(f)
    daten = s["module"]["erde01"]["daten"]
    staaten = daten.setdefault("staaten", {})
    for b in BLOECKE:
        staaten.setdefault(b, {}).update(d[b])
    daten["a6_a7_erstbuchung"] = {
        "zug": 5, "stand": "2030-12-31", "wirksam_ab": "Zug 6",
        "regelort": "erde01-gm:references/korruption_terror.md (A-6, A-7)",
        "regelinstanz": "scripts/erde01_engine.py korruption | terrorlage | coup | kaskade",
        "gebucht": [
            "K je Block aus dem Regimetyp-Startwert (A-6.1)",
            "T je Block aus A-7.1 mit dem Repressionsbestand",
            "die abgeleiteten A-6-Faktoren (Coup, Gefechtswert, Verlust, "
            "Beschaffungsschwund, Legitimitaet, z-Zuschlag)",
        ],
        "nicht_gebucht": [
            "Uebergangswachstum: dK = 0 im Erstlauf, also 0,0 Pp (A-6.2)",
            "Niveauabschlag auf die BIP-Reihe -> RG-A6-NIVEAU",
            "Terror-Wachstumskanal: auf Blockgroesse null (A-7.5)",
            "Vorfallwuerfe W1000 gegen T: gehoeren in die Zug-6-Aufloesung, "
            "nicht rueckwirkend in fuenf gebuchte Zuege",
            "A-2- und B-2-Wuerfe: nur Vorschau, der scharfe Wurf laeuft in Zug 6",
        ],
        "rules_gaps": ["RG-A6-VORZEICHEN (GRUENDLER aktiv / SAHA bereit)",
                       "RG-A6-NIVEAU", "RG-A7-BIP", "RG-A7-BODEN"],
    }
    with open(STAND, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)
    return STAND


if __name__ == "__main__":
    d = buchungssatz()
    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=1))
    elif "--schreiben" in sys.argv:
        print(tafel(d)); print()
        print("gebucht nach", schreiben(d))
    else:
        print(tafel(d))
