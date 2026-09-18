#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSBAUSTEIN — Reiter »INNENLAGE« (A-6 Korruption, A-7 Terror).

Der Erzeuger zh01_blatt.py baut vier Reiter (1 Politik · 2 Energie · 3 Boden ·
4 Rechnen). A-6 und A-7 sind seit dem 08.09.2026 Regelorte von ERDE-01 und seit
Zug 6 gebucht — aber die fuenf Regler, die sie steuern, sind SPIELERBEFEHLE und
stehen auf keinem Blatt dieser Kampagne (Befund B-31). Ohne sie ist das Modul
gebucht und unspielbar.

WIE DIE FELDER ZURUECKKOMMEN: werte() sammelt jedes Element mit id="f_…" in
blatt.felder. Die Namen sind genau die, die erde01-gm/scripts/blattlesen.py
erwartet: antikorr · patronage · gegenterror · einschluss · ausschluss ·
enth_typ · enth_alter · enth_art. Kein Eingriff in eine Skilldatei.

WAS HIER BEWUSST NICHT STEHT (blattlesen.py, woertlich): »Was hier NICHT
geprueft wird: der Purge bei Bekaempfungsstufe 3 in einer Autokratie (A-6.6)
und die Repressionsfalle (A-7.2). Beide sind Fallen, und eine Vorpruefung, die
jede Falle ausschildert, ist ein Loesungsbogen.« Das Blatt nennt Kosten und
Nennwirkung — nicht die Falle.

VERTRAULICHKEIT: jedes Blatt traegt ausschliesslich die Werte SEINER Fraktion.

Aufruf: python3 blatt_innenlage_reiter.py <datei.html> [...]
"""
import json, os, re, sys

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/erde01-gm")
sys.path.insert(0, os.path.join(SK, "scripts"))
import erde01_engine as E                                          # noqa: E402
KK = E.REGELN["innenpolitik"]["korruption"]
TT = E.REGELN["innenpolitik"]["terror"]

ST = json.load(open(os.path.join(W, "stand", "erde01_state_schwarzesee.json"),
                    encoding="utf-8"))["module"]["erde01"]["daten"]["staaten"]
BLOCK = {"IND": "indien", "CHN": "china", "EU": "eu",
         "USA": "usa", "RUS": "russland", "REST": "rest"}


def z(x, n=2):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def regler(fid, lab, wert, maxi, schritt, fuss, farbe="ocker", einh=""):
    marken = "".join(f"<span>{z(m, 0)}</span>" for m in (0, maxi // 2, maxi)) \
        if isinstance(maxi, int) else ""
    return (f'<div class="regler {farbe}" data-regler="{fid}"><div class="zeileR">'
            f'<span class="lab">{lab}</span><span class="wert">'
            f'<input type="number" id="f_{fid}" inputmode="decimal" step="{schritt}" '
            f'min="0" max="{maxi}" value="{wert}" data-unberuehrt="1" aria-label="{lab}">'
            f'<span class="einh">{einh}</span></span></div>'
            f'<input type="range" class="schieber" min="0" max="{maxi}" step="{schritt}" '
            f'value="{wert}" tabindex="-1" aria-hidden="true"><div class="marken">{marken}</div>'
            f'<div class="ausserhalb"></div><div class="fuss">{fuss}</div></div>')


def abschnitt(n, ges, fid):
    e = ST[BLOCK[fid]]
    k, t = e["korruption"], e["terrorlage"]
    b2 = e["kaskade_b2_vorschau"]
    cv = e["coup_track_vorschau"]["rezession"]
    dem = k["regimetyp"].startswith("demokratie")

    # ---- Klasse S: gedruckt, kein Eingabefeld (Z-8.3) -------------------
    stand = (
        '<div class="abschn"><h3>Ihr Stand — gedruckt, nicht einzutragen</h3>'
        '<table class="innentab"><tr><th>Groesse</th><th>Wert</th><th>woher</th></tr>'
        f'<tr><td>Regimetyp</td><td><b>{k["regimetyp"]}</b></td>'
        '<td>staaten_2026.json; reich/arm abgeleitet aus BIP je Kopf</td></tr>'
        f'<tr><td>K — Korruption</td><td><b>{z(k["K"])}</b></td>'
        '<td>A-6.1, Startwert des Regimetyps</td></tr>'
        f'<tr><td>T — Terrorlage</td><td><b>{z(t["T"], 4)}</b></td>'
        '<td>A-7.1, mit Ihrer Repression und Ihrem K</td></tr>'
        f'<tr><td>Gefechtswert daheim</td><td>{z(k["gefechtswert_faktor"], 3)}</td>'
        '<td>A-6.5, <code>1 − 0,45·K·(1 + 0,5·Ferne)</code></td></tr>'
        f'<tr><td>Gefechtswert Expedition</td><td>{z(1 - 0.45*k["K"]*1.5, 3)}</td>'
        '<td>A-6.5 mit Ferne 1 — je weiter, desto teurer</td></tr>'
        f'<tr><td>Verlustaufschlag</td><td>×{z(k["verlustaufschlag"], 3)}</td>'
        '<td>A-6.5</td></tr>'
        f'<tr><td>Beschaffungsschwund</td><td><b>{z(k["beschaffungsschwund_anteil"]*100, 1)} %</b></td>'
        '<td>A-6.5 — wirkt auf JEDEN ZH-01-Kauf</td></tr>'
        f'<tr><td>Coup-Track A-2</td><td>{z(cv["p_mit_A6"]*100, 3)} % je Zug</td>'
        f'<td>mit f<sub>Korr</sub> ×{z(k["f_korruption_coup"], 3)}</td></tr>'
        f'<tr><td>Kaskade B-2</td><td>{z(b2["neu"]["p_je_zug"]*100, 2)} % je Zug</td>'
        f'<td>z-Zuschlag +{z(k["kaskade_z_zuschlag"], 3)} aus A-6.7</td></tr>'
        '</table><div class="fuss">Diese Zahlen sind Feldklasse S: sie stehen fest, '
        'Sie tragen sie nicht ein. Was Sie eintragen, steht darunter.</div></div>')

    # ---- A-6 Regler -----------------------------------------------------
    bk = KK["bekaempfung"]["stufen"] if isinstance(KK["bekaempfung"].get("stufen"), list) \
        else None
    tafel = ""
    if bk:
        tafel = ('<table class="innentab"><tr><th>Stufe</th><th>ΔK je Zug</th><th>Kosten</th></tr>'
                 + "".join(f'<tr><td>{s["stufe"]}</td><td>{z(s["dK_je_zug"], 3)}</td>'
                           f'<td>{z(s["kosten_pct_bip"], 2)} % BIP</td></tr>' for s in bk)
                 + "</table>")

    a6 = ('<div class="abschn"><h3>A-6 — Korruption</h3>'
          '<div class="band ocker"><b>Zwei Hebel, entgegengesetzte Richtung.</b>'
          'Bekaempfung senkt K und kostet BIP. Patronage kauft Ruhe auf dem Coup-Track '
          'und HEBT K. Beides im selben Zug ist erlaubt und hebt sich teilweise auf.</div>'
          + tafel
          + regler("antikorr", "Korruptionsbekaempfung (Stufe 0–3)", 0, 3, 1,
                   "A-6.6. Wirkt langsam: der volle Lebensstandardgewinn ist erst nach "
                   "zehn Jahren gemessen [QK-02]. In diesem Zug sehen Sie die Kosten.")
          + regler("patronage", "Patronageposten (0–8)", 0, 8, 1,
                   "A-6.4. <code>0,96^n</code> auf den Coup-Track, hoechstens acht Posten. "
                   "Je Posten +0,01 K und 0,05 % BIP. Ein Posten senkt das Coup-Risiko "
                   "staerker als +1 Pp Wachstum [QK-15 Arriola 2009].")
          + '</div>')

    # ---- A-7 Regler -----------------------------------------------------
    gt = TT["gegenmassnahmen"]["gegenterror"]["stufen"]
    ei = TT["gegenmassnahmen"]["einschluss"]["stufen"]
    daempfer = 1 - 0.5 * k["K"]
    gtab = ('<table class="innentab"><tr><th>Stufe</th><th>ΔT nominal</th>'
            f'<th>bei Ihnen (×{z(daempfer, 2)})</th><th>Kosten</th></tr>'
            + "".join(f'<tr><td>{s["stufe"]}</td><td>{z(s["dT"], 3)}</td>'
                      f'<td><b>{z(s["dT"]*daempfer, 4)}</b></td>'
                      f'<td>{z(s["kosten_pct_bip"], 2)} % BIP</td></tr>' for s in gt)
            + "</table>")
    etab = ('<table class="innentab"><tr><th>Stufe</th><th>Δ Ausschluss</th><th>Kosten</th></tr>'
            + "".join(f'<tr><td>{s["stufe"]}</td><td>{z(s["d_ausschluss"], 3)}</td>'
                      f'<td>{z(s["kosten_pct_bip"], 2)} % BIP</td></tr>' for s in ei)
            + "</table>")

    a7 = ('<div class="abschn"><h3>A-7 — Terror</h3>'
          '<div class="band blau"><b>T ist keine Anschlagszahl.</b>T ist die '
          'Wahrscheinlichkeit, dass dieser Zug einen <i>zugpraegenden</i> Vorfall traegt. '
          'Alles darunter ist Grundrauschen und wird nicht gebucht. Der Normalfall eines '
          'Vorfalls ist der Nadelstich ohne Tote — das ist Befund, nicht Milde '
          '[ueber 8000 Anschlaege USA/GB 1970–2017, QT-33].</div>'
          '<div class="band gruen"><b>Auf Blockgroesse kostet Terror kein Wachstum.</b>'
          'A-7.5 setzt die Schwelle bei 0,05 Vorfaellen je Million Einwohner; Ihr Block '
          f'liegt bei {z(t["vorfaelle_je_mio_bei_1_vorfall"], 5)} je Vorfall. Der '
          'Wachstumskanal ist NULL. Was bleibt: Ihr Gegenterrorbudget mit −0,10 Pp je '
          'Stufe, die Rally bei einem Massenanschlag, und — nur in einer Demokratie und '
          'nur wenn eine Warnung vorlag und ungenutzt blieb — ein Punkt Legitimitaet.</div>'
          '<h4>Gegenterror</h4>' + gtab
          + regler("gegenterror", "Gegenterror (Stufe 0–3)", 0, 3, 1,
                   f"A-7.6. Wirkt nur, soweit der Apparat nicht gekauft ist: "
                   f"×(1 − 0,5·K) = ×{z(daempfer, 2)} bei Ihrem K von {z(k['K'])}. "
                   "Dazu −0,10 Pp Wachstum je Stufe.", farbe="rot")
          + '<h4>Einschluss</h4>' + etab
          + regler("einschluss", "Einschluss (Stufe 0–3)", 0, 3, 1,
                   "A-7.6. Wirkt mit ZWEI Zuegen Verzug und ist der einzige dauerhafte "
                   "Hebel [QT-03, QT-12]. In der Zugbilanz kostet er zunaechst nur.",
                   farbe="gruen")
          + regler("ausschluss", "Politischer Ausschluss (0,00–1,00)", z(e["ausschluss"]["wert"]).replace(",", "."),
                   1, 0.05,
                   "A-7.1, Faktor <code>(1 + 0,9·Ausschluss)</code> — der staerkste "
                   "belegte Treiber der Terrorlage [QT-03 Ghatak/Gold 2019, Guete A]. "
                   "Steht auf 0,00, weil ihn bisher kein Blatt gefuehrt hat. "
                   "Tragen Sie ein, was Ihrer Innenpolitik entspricht.", farbe="viol")
          + '</div>')

    # ---- Enthauptung ----------------------------------------------------
    opt = "".join(f'<option value="{k2}">{k2} — {a["name"]}</option>'
                  for k2, a in sorted(TT["akteure"].items())
                  if isinstance(a, dict) and "name" in a)
    enth = ('<div class="abschn"><h3>Enthauptung — nur wenn Sie eine Gruppe im Visier haben</h3>'
            '<div class="band ocker"><b>Fangen und Toeten sind nicht dasselbe.</b>'
            'Gezieltes <i>Fangen</i> schreckt auch nicht anvisierte Gruppen ab; gezieltes '
            '<i>Toeten</i> tut das nicht — und wenn die Gruppe nicht zerfaellt, wird die '
            'verbleibende Gewalt unterschiedsloser [QT-17 Tominaga 2018, QT-15/QT-16]. '
            'Alte, grosse, religioese und separatistische Gruppen widerstehen '
            '[QT-14 Jordan].</div>'
            f'<label class="f"><span class="lab">Akteur</span><select id="f_enth_typ" '
            f'data-unberuehrt="1"><option value="keine" selected>keine</option>{opt}</select></label>'
            '<label class="f"><span class="lab">Art</span><select id="f_enth_art" '
            'data-unberuehrt="1"><option value="-" selected>-</option>'
            '<option value="fangen">fangen</option><option value="toeten">toeten</option>'
            '</select></label>'
            '<label class="f"><span class="lab">Alter der Gruppe in Zuegen</span>'
            '<input type="number" id="f_enth_alter" inputmode="numeric" step="1" min="0" '
            'value="" data-unberuehrt="1" aria-label="Alter der Gruppe"></label>'
            '<div class="fuss">A-7.7: <code>p = 0,33 · e^(−Alter/12) · Enthauptungsfaktor</code>. '
            'Leer lassen heisst: keine Enthauptung in diesem Zug.</div></div>')

    stil = ('<style>.innentab{border-collapse:collapse;width:100%;margin-top:8px;'
            'font-size:13px}.innentab td,.innentab th{border-bottom:1px solid var(--linie);'
            'padding:5px 6px;text-align:left}.innentab th{color:var(--leise);font-weight:600;'
            'font-size:12px}.innentab td:not(:first-child){text-align:right;'
            'font-variant-numeric:tabular-nums;white-space:nowrap}'
            '.innentab td:last-child{text-align:left;color:var(--leise);font-size:12px;'
            'white-space:normal}</style>')
    return (f'<section class="blatt" id="blatt{n}">{stil}<div class="h"><div class="blattkopf">'
            f'<div class="nr">BLATT {n} VON {ges}</div><h2>INNENLAGE</h2>'
            f'<div class="quelle">ERDE-01 A-6 Korruption · A-7 Terror · Hausblatt</div></div>'
            '<div class="band rot"><b>Neu in dieser Partie.</b>A-6 und A-7 sind seit Zug 6 '
            'gebucht. Fuenf Regler steuern sie, und sie standen bisher auf keinem Blatt. '
            'Alle stehen auf 0 — das ist kein Befund ueber Ihr Land, sondern das Fehlen '
            'eines Befehls. Ab hier befehlen Sie.</div>'
            + stand + a6 + a7 + enth + '</div></section>')


def patch(pfad):
    s = open(pfad, encoding="utf-8").read()
    if 'INNENLAGE</h2>' in s:
        print(f"  {os.path.basename(pfad)}: Reiter ist schon da — nichts getan."); return False
    m = re.search(r'"fraktion"\s*:\s*"([A-Z]+)"', s)
    if not m or m.group(1) not in BLOCK:
        print(f"  {os.path.basename(pfad)}: Fraktion nicht erkannt — NICHT angefasst."); return False
    fid = m.group(1)
    vorhanden = sorted(int(x) for x in re.findall(r'<section class="blatt" id="blatt(\d+)"', s))
    if not vorhanden or "</div></nav>" not in s:
        print(f"  {os.path.basename(pfad)}: Rahmen unbekannt — NICHT angefasst."); return False
    n = vorhanden[-1] + 1
    s = s.replace("</div></nav>",
                  f'<a href="#blatt{n}"><span>{n} &nbsp;<b>Innenlage</b></span></a>\n</div></nav>', 1)
    i = s.rfind("</section>")
    s = s[:i + 10] + abschnitt(n, n, fid) + s[i + 10:]
    s = re.sub(r"(BLATT \d+ VON )\d+", lambda x: x.group(1) + str(n), s)
    open(pfad, "w", encoding="utf-8").write(s)
    print(f"  {os.path.basename(pfad)}: Reiter {n} »Innenlage« ({fid}) eingefuegt.")
    return True


if __name__ == "__main__":
    print(f"{sum(patch(p) for p in sys.argv[1:])} Datei(en) ergaenzt.")
