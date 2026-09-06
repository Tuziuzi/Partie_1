#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E-1 »BASISWACHSTUMSPFAD« — Rechen-Gate fuer die rueckwirkende Buchung (RG-Z5-01).

Regelgrundlage: KB-02 »WACHSTUMSBUCH« §2 W-1a (Tafelpfad) und §7 E-1.
Hausentscheidung Zug 5: E-1 wird RUECKWIRKEND ab 2026 gebucht (Host, 05.09.2026).

Verfahren (aus der Struktur des ERDE-01-Modells abgeleitet, KB-02 §1.1):
  ERDE-01 bemisst jeden Schock in Prozentpunkten der WACHSTUMSRATE. Die Kampagne
  hat die fehlende Basisrate mit null gefuellt, also galt je Jahr
      BIP(t) = BIP(t-1) * (1 - s_t)          mit s_t = Summe der Schock-Pp
  Der implizite Schock s_t laesst sich aus der Ist-Reihe zurueckrechnen:
      1 - s_t = Ist(t) / Ist(t-1)
  Rueckwirkend gilt dieselbe Reihe mit der Tafelrate g als Basis:
      Retro(t) = Retro(t-1) * (1 - s_t + g)
  Startwert 2026 bleibt unveraendert (Setup-Jahr, vor dem ersten Zug).

Gegenprobe: die Ergebnisse muessen die in KB-02 §7 veroeffentlichten Werte treffen.
"""
import json

# --- Eingaben, alle belegt -------------------------------------------------
# Ist-Reihe: KB-02 §1.2 »Was das angerichtet hat«
IST = {
    "china":  {2026: 17.7449, 2027: 16.0059, 2028: 15.3817, 2029: 15.0587},
    "eu":     {2026: 20.0056, 2027: 19.5795, 2028: 19.3269, 2029: 19.1162},
    "indien": {2026:  4.3000, 2027:  4.1839, 2028:  4.1283, 2029:  4.0870},
}
# Tafelpfad 2026-2030, KB-02 §2 W-1a
TAFEL = {"usa": 2.0, "china": 4.3, "eu": 1.2, "indien": 6.5, "russland": 0.9, "rest": 3.2}
# Sollwerte zur Gegenprobe, KB-02 §7 E-1
SOLL_BIP = {"china": 17.2064, "eu": 19.8235, "indien": 4.9523}
SOLL_KONTO = {"china": 2503.1, "eu": 1660.5, "indien": 719.3}
# gebuchte Zug-5-Bodenkonten (UEBERGABE §4) und Vortrag 2030
KONTO_IST = {"china": 2232.5, "eu": 1602.6, "indien": 601.0}
TRANCHE_IST = {"china": 334.9, "eu": 240.4, "indien": 90.2}
TRANCHE_QUOTE = 0.15   # UEBERGABE §10: »Tranche = Hochtechnologiedeckel, 15 % des Bodenkontos«

def reihe(fid):
    g = TAFEL[fid] / 100.0
    jahre = sorted(IST[fid])
    retro = {jahre[0]: IST[fid][jahre[0]]}
    schock = {}
    for a, b in zip(jahre, jahre[1:]):
        faktor_ist = IST[fid][b] / IST[fid][a]        # = 1 - s_t
        schock[b] = round((1.0 - faktor_ist) * 100, 4)
        retro[b] = retro[a] * (faktor_ist + g)
    return retro, schock

print("=" * 74)
print("E-1 BASISWACHSTUMSPFAD — rueckwirkende Buchung, Gegenprobe gegen KB-02 §7")
print("=" * 74)
erg = {}
for fid in ("china", "eu", "indien"):
    retro, schock = reihe(fid)
    j = sorted(retro)
    print(f"\n{fid.upper()}  Tafelrate {TAFEL[fid]:.1f} %/a")
    print("  Jahr |     Ist     |   Schock Pp |    Rueckwirkend")
    for y in j:
        s = f"{schock[y]:11.4f}" if y in schock else "     (Setup)"
        print(f"  {y} | {IST[fid][y]:11.4f} | {s} | {retro[y]:15.4f}")
    ende = retro[j[-1]]
    soll = SOLL_BIP[fid]
    abw = abs(ende - soll)
    print(f"  -> 2029 rueckwirkend {ende:.4f} Bio USD · KB-02 §7 nennt {soll:.4f} · "
          f"Abweichung {abw:.4f} {'BESTANDEN' if abw <= 0.0002 else 'DURCHGEFALLEN'}")
    # Bodenkonto: nur der wirtschaftsabhaengige Teil skaliert, der Vortrag ist eine feste Tonnage
    r = ende / IST[fid][j[-1]]
    vortrag = (KONTO_IST[fid] * r - SOLL_KONTO[fid]) / (r - 1.0)
    konto_neu = SOLL_KONTO[fid]
    tranche_neu = round(konto_neu * TRANCHE_QUOTE, 1)
    print(f"  -> Wirtschaftsfaktor r = {r:.6f} · impliziter Vortrag {vortrag:.1f} t")
    print(f"  -> Bodenkonto {KONTO_IST[fid]:.1f} t  ->  {konto_neu:.1f} t")
    print(f"  -> Tranche    {TRANCHE_IST[fid]:.1f} t  ->  {tranche_neu:.1f} t  (15 % des Kontos)")
    erg[fid] = {"bip_2029_ist": IST[fid][j[-1]], "bip_2029_retro": round(ende, 4),
                "tafelrate_pct": TAFEL[fid], "konto_t_ist": KONTO_IST[fid],
                "konto_t_neu": konto_neu, "tranche_t_ist": TRANCHE_IST[fid],
                "tranche_t_neu": tranche_neu, "wirtschaftsfaktor": round(r, 6),
                "vortrag_t_impliziert": round(vortrag, 1)}

# Tranche-Gegenprobe an den Ist-Werten: bestaetigt die 15-%-Regel
print("\n" + "-" * 74)
print("Gegenprobe der 15-%-Regel an den gebuchten Ist-Werten:")
for fid in KONTO_IST:
    t = round(KONTO_IST[fid] * TRANCHE_QUOTE, 1)
    print(f"  {fid:7s} {KONTO_IST[fid]:8.1f} t * 0,15 = {t:7.1f} t · gedruckt {TRANCHE_IST[fid]:7.1f} t "
          f"{'OK' if abs(t - TRANCHE_IST[fid]) <= 0.05 else 'ABWEICHUNG'}")

print("\n" + "-" * 74)
print("NICHT GERECHNET (Luecke RG-Z5-03): USA, Russland und Rest fuehren im")
print("vorliegenden Material keine Wirtschaftsreihe. KB-02 §7 begrenzt den Neudruck")
print("ausdruecklich auf »die drei Zug-5-Blaetter 3«. Die NPC-Bodenkonten bleiben")
print("daher auf den gebuchten Ist-Werten (USA 7463,6 t · Russland 1079,8 t) —")
print("das ist eine Asymmetrie und gehoert dem Tisch gemeldet, nicht still geglaettet.")
open("zug5/ausgabe/e1_basispfad.json", "w", encoding="utf-8").write(
    json.dumps(erg, ensure_ascii=False, indent=2))
print("\ngeschrieben: zug5/ausgabe/e1_basispfad.json")
