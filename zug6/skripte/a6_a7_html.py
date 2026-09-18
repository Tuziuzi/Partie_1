#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GM-Datenblatt zur Erstbuchung von A-6 KORRUPTION und A-7 TERROR."""
import json, os, sys, datetime

W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SK = ("/root/.claude/skills/synced/"
      "2c0e114f-f980-4879-be59-84347099c9f5_db129feb-ec7e-452e-ac0f-412f398c1773/erde01-gm")
sys.path.insert(0, os.path.join(SK, "scripts"))
import erde01_engine as E                                        # noqa: E402
TT = E.REGELN["innenpolitik"]["terror"]

S = json.load(open(os.path.join(W, "stand", "erde01_state_schwarzesee.json"), encoding="utf-8"))
ST = S["module"]["erde01"]["daten"]["staaten"]
BL = ["usa", "eu", "indien", "china", "russland", "rest"]


def z(x, n=2):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def pz(x, n=2):
    return z(x * 100, n) + "&nbsp;%"


B = ['<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
     '<title>A-6 Korruption / A-7 Terror</title><style>'
     ':root{--grund:#f4eede;--feld:#fffdf6;--linie:#d6cdb6;--schrift:#1d2b36;--leise:#5c6b76;'
     '--blau:#2e6c96;--rot:#a8412a;--gruen:#4a7a42;--ocker:#8a6d1f}'
     '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--grund:#0f151a;--feld:#161f27;'
     '--linie:#26343e;--schrift:#e7eef4;--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;--ocker:#dcb45e}}'
     ':root[data-theme="dark"]{--grund:#0f151a;--feld:#161f27;--linie:#26343e;--schrift:#e7eef4;'
     '--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;--ocker:#dcb45e}'
     'body{background:var(--grund);color:var(--schrift);font:15px/1.55 -apple-system,BlinkMacSystemFont,'
     '"Segoe UI",Roboto,sans-serif;margin:0;padding:14px}'
     'h1{font-size:19px;margin:0 0 2px}h2{font-size:16px;margin:0 0 10px;color:var(--blau)}'
     'h3{font-size:12.5px;margin:14px 0 6px;color:var(--leise);text-transform:uppercase;letter-spacing:.06em}'
     '.kopf{color:var(--leise);font-size:12.5px;margin-bottom:16px}'
     '.karte{background:var(--feld);border:1px solid var(--linie);border-radius:10px;padding:12px 14px;margin-bottom:14px}'
     '.warn{border-left:3px solid var(--ocker)}.gap{border-left:3px solid var(--rot)}'
     '.gut{border-left:3px solid var(--gruen)}'
     'table{border-collapse:collapse;width:100%;font-size:13.5px}'
     'td,th{border-bottom:1px solid var(--linie);padding:5px 6px;text-align:left;vertical-align:top}'
     'th{color:var(--leise);font-weight:600}td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}'
     '.wrap{overflow-x:auto}code{font-size:12.5px}'
     '.ok{color:var(--gruen)}.hm{color:var(--ocker)}.bad{color:var(--rot)}.fett{font-weight:700}'
     'p{margin:8px 0 0;font-size:13px}.q{color:var(--leise);font-size:12px}'
     'ul{margin:8px 0 0;padding-left:20px;font-size:13px}li{margin:3px 0}</style>']

B.append('<h1>A-6&nbsp;Korruption und A-7&nbsp;Terror — Erstbuchung</h1>')
B.append('<div class="kopf">Kampagne SCHWARZE SEE · ERDE-01 · Stand nach Zug&nbsp;5 '
         '(2030-12-31), wirksam ab Zug&nbsp;6 · Regelort '
         '<code>erde01-gm:references/korruption_terror.md</code> · gerechnet mit '
         '<code>erde01_engine.py</code> und <code>hybrid01.py</code><br>'
         '<b>GM-Blatt.</b> Es trägt die Werte <i>aller</i> Fraktionen und geht so in keinen '
         'SITREP. Jede Fraktion erfährt ihre eigene Lage; fremde Werte sind nach '
         'CLAUDE.md&nbsp;§5 vertraulich.<br>'
         f'Erzeugt {datetime.date.today().isoformat()}.</div>')

# ---------------------------------------------------------------- Übersicht
B.append('<div class="karte"><h2>Die Lage aller sechs Blöcke</h2><div class="wrap"><table>'
         '<tr><th>Block</th><th>Regimetyp</th><th class="n">K</th><th class="n">T</th>'
         '<th class="n">Gefechts&shy;wert</th><th class="n">Beschaffungs&shy;schwund</th>'
         '<th class="n">f<sub>Korr</sub> auf A-2</th><th class="n">z-Zuschlag B-2</th></tr>')
for b in BL:
    e = ST[b]; k = e["korruption"]; t = e["terrorlage"]
    kl = "bad" if k["f_korruption_coup"] > 1 else "ok"
    B.append(f'<tr><td class="fett">{e["name"]}</td><td>{k["regimetyp"]}</td>'
             f'<td class="n">{z(k["K"])}</td><td class="n fett">{z(t["T"], 4)}</td>'
             f'<td class="n">{z(k["gefechtswert_faktor"], 3)}</td>'
             f'<td class="n">{pz(k["beschaffungsschwund_anteil"], 1)}</td>'
             f'<td class="n {kl}">×{z(k["f_korruption_coup"], 3)}</td>'
             f'<td class="n">+{z(k["kaskade_z_zuschlag"], 3)}</td></tr>')
B.append('</table></div><p><b>K</b> ist der Korruptionsbestand 0…1 auf der V-Dem-Skala, '
         '<b>T</b> die Wahrscheinlichkeit, dass ein Zug einen zugprägenden Vorfall trägt — '
         '<i>keine</i> Anschlagszahl. Der Regimetyp ist keine Setzung: '
         '<code>staaten_2026.json</code> nennt ihn, und die Feinheit reich/arm leitet '
         '<code>hybrid01.regime_fuer</code> aus BIP-Anteil je Bevölkerungsanteil ab '
         '(Schwelle&nbsp;1,0). K ohne Eigenwert im Stand ist nach A-6.1 der Startwert des '
         'Regimetyps.</p></div>')

# ------------------------------------------------------------------- A-6
B.append('<div class="karte"><h2>A-6 — was der Korruptionsbestand kostet</h2><div class="wrap"><table>'
         '<tr><th>Block</th><th class="n">K</th><th class="n">Verlust&shy;aufschlag</th>'
         '<th class="n">wahre Zustimmung</th><th class="n">Niveau&shy;abschlag</th>'
         '<th class="n">Über&shy;gangs&shy;wachstum</th></tr>')
for b in BL:
    e = ST[b]; k = e["korruption"]
    n = k["niveau_abschlag_pct"]
    nk = "ok" if n > 0 else ("bad" if n < -5 else "hm")
    B.append(f'<tr><td class="fett">{e["name"]}</td><td class="n">{z(k["K"])}</td>'
             f'<td class="n">×{z(k["verlustaufschlag"], 3)}</td>'
             f'<td class="n">{z(k["wahre_zustimmung_pp"])}&nbsp;Pp</td>'
             f'<td class="n {nk}">{"+" if n > 0 else ""}{z(n, 3)}&nbsp;%</td>'
             f'<td class="n ok">0,00&nbsp;Pp</td></tr>')
B.append('</table></div>'
         '<p><b>Gefechtswert</b> <code>1 − 0,45·K·(1 + 0,5·Ferne)</code>, oben mit '
         'Ferne&nbsp;0 (Kampf daheim). Der Ferne-Term ist der einzige als Wechselwirkung '
         '<i>gemessene</i> Teil des Regelortes [QK-07 Binetti 2024]: bei einer Expedition '
         '(Ferne&nbsp;1) fällt Russland von 0,676 auf <b>0,514</b>, Indien von 0,797 auf '
         '<b>0,696</b>. <b>Beschaffungsschwund</b> <code>0,35·K</code> wirkt auf C-3 <i>und '
         'auf jeden ZH-01-Kauf</i> — der Spieler bekommt weniger, als sein Blatt ausweist.</p>'
         '<p><b>Übergangswachstum ist im Erstlauf für alle null</b>, weil ΔK&nbsp;=&nbsp;0. '
         'A-6.2 trennt streng: der <i>Bestand</i> ergibt einen einmaligen Niveauabschlag, '
         'nur die <i>Änderung</i> ergibt eine Wachstumsrate (−0,0615&nbsp;Pp je 0,01&nbsp;ΔK '
         'über zehn Jahre). Wer den Bestand als Jahresrate bucht, macht aus −17&nbsp;% Niveau '
         'ein Dauerwachstum — genau der Fehler, an dem der Regelort beinahe gescheitert wäre.</p></div>')

# ------------------------------------------------------------------- A-2
B.append('<div class="karte warn"><h2>Folge 1 — der Coup-Track dreht sich</h2>'
         '<p>A-6.8 Kernasymmetrie [QK-13, QK-14]: <code>1 + 0,60·K</code> in der Demokratie, '
         '<code>1 − 0,35·K</code> in Autokratie und Hybrid. <b>Korruption kittet die '
         'Autokratie und sprengt die Demokratie.</b></p><div class="wrap"><table>'
         '<tr><th>Block</th><th class="n">bisher gebucht</th><th class="n">mit A-6</th>'
         '<th class="n">Änderung</th><th class="n">ohne Rezessionsflag</th></tr>')
for b in BL:
    c = ST[b]["coup_track_vorschau"]
    a, n = c["rezession"]["p_ohne_A6"], c["rezession"]["p_mit_A6"]
    o = c["ohne_rezession"]["p_mit_A6"]
    kl = "bad" if n > a else "ok"
    B.append(f'<tr><td class="fett">{ST[b]["name"]}</td><td class="n">{pz(a, 3)}</td>'
             f'<td class="n fett">{pz(n, 3)}</td>'
             f'<td class="n {kl}">{"+" if n > a else ""}{z((n/a-1)*100, 1)}&nbsp;%</td>'
             f'<td class="n q">{pz(o, 3)}</td></tr>')
B.append('</table></div><p>Die Spalte «bisher gebucht» reproduziert die im Stand stehenden '
         'Zug-4-Werte auf drei Nachkommastellen — das ist die Gegenprobe, dass hier nichts '
         'Neues erfunden wurde. <b>Patronage steht bei allen auf 0.</b> Acht Posten gäben '
         '<code>0,96⁸ = 0,72</code> auf den Track und kosteten je Posten +0,01&nbsp;K und '
         '0,05&nbsp;%&nbsp;BIP. <b>Gewürfelt ist nichts</b>: der scharfe A-2-Wurf gehört in '
         'die Zug-6-Auflösung mit dem Zug-6-Seed, und der Rezessionsflag für 2030 ist noch '
         'nicht gestellt — darum stehen beide Spalten.</p></div>')

# ------------------------------------------------------------------- B-2
B.append('<div class="karte warn"><h2>Folge 2 — das Kaskadenrisiko steigt für jeden</h2>'
         '<p>A-6.7 gibt <code>+0,25·K</code> auf das <code>z</code> der B-2-Kaskade, '
         'ausdrücklich additiv zum GZ-01-Druckkonto.</p><div class="wrap"><table>'
         '<tr><th>Block</th><th class="n">b</th><th class="n">z alt</th><th class="n">z neu</th>'
         '<th class="n">p alt</th><th class="n">p neu</th></tr>')
for b in BL:
    q = ST[b]["kaskade_b2_vorschau"]
    B.append(f'<tr><td class="fett">{ST[b]["name"]}</td><td class="n">{z(q["b"])}</td>'
             f'<td class="n">{z(q["z_alt"], 3)}</td><td class="n">{z(q["z_neu"], 3)}</td>'
             f'<td class="n">{pz(q["alt"]["p_je_zug"])}</td>'
             f'<td class="n fett">{pz(q["neu"]["p_je_zug"])}</td></tr>')
B.append('</table></div><p><code>p = clamp((b − 0,15)·0,15·z, 0, 0,95)</code>. Das '
         '<code>b</code> der Domäne Innenpolitik ist aus den gebuchten Kaskadenwerten der '
         'Züge 1 bis 4 rückgerechnet und dort an allen sieben Buchungen mit der Repression '
         'identisch. Das <code>z</code> der EU steht bereits auf 1,103 aus dem '
         'GZ-01-Druckkonto Stufe&nbsp;G2 (Zug&nbsp;5). Die USA bleiben bei 0,00&nbsp;%, weil '
         'b&nbsp;=&nbsp;0,05 unter der Schwelle L0&nbsp;=&nbsp;0,15 liegt. '
         '<b>China hat erneut den höchsten Wert am Tisch</b> — nach der Präferenzkaskade von '
         'Zug&nbsp;4 der zweite Anlauf auf dieselbe Leiste.</p></div>')

# ------------------------------------------------------------------- A-7
B.append('<div class="karte"><h2>A-7 — die Terrorlage, aufgeschlüsselt</h2><div class="wrap"><table>'
         '<tr><th>Block</th><th class="n">f<sub>Regime</sub></th><th class="n">Repression</th>'
         '<th class="n">Δ Repression</th><th class="n">bip_index</th><th class="n">T</th></tr>')
for b in BL:
    e = ST[b]; t = e["terrorlage"]
    d = t["d_repression"]
    B.append(f'<tr><td class="fett">{e["name"]}</td><td class="n">{z(t["f_regime"])}</td>'
             f'<td class="n">{z(e["repression"]["wert"])}</td>'
             f'<td class="n {"bad" if d > 0 else "ok"}">{"+" if d >= 0 else ""}{z(d, 4)}</td>'
             f'<td class="n">{z(e["bip_index"]["gebucht"], 3)}</td>'
             f'<td class="n fett">{z(t["T"], 4)}</td></tr>')
B.append('</table></div>'
         '<p><code>T = 0,20 · f<sub>Regime</sub> · (1 + 0,9·Ausschluss) · (0,9 + 0,2·bip_index) '
         '+ Δ<sub>Repression</sub> + Δ<sub>Gegenterror</sub></code>, Deckel 0,95.</p>'
         '<p class="bad"><b>Indien trägt die höchste Terrorlage am Tisch — und zahlt sie '
         'selbst.</b> Von 0,4403 kommen 0,2303 aus Regimetyp und Wohlstand, aber '
         '<b>+0,2100 aus der eigenen Repression von 0,60</b>. Das ist die Repressionsfalle '
         'A-7.2 [QT-05 Piazza 2017]: Repression, die gewaltlose Kanäle schliesst, <i>hebt</i> '
         'den Inlandsterror; ein Abschreckungszweig existiert allein in Autokratien [QT-06]. '
         'Dieselbe Reglerstellung kauft schon das B-2-Kaskadenrisiko — sie zahlt hier ein '
         'zweites Mal. <b>Der Spieler wird nach Regel nicht vorgewarnt.</b></p>'
         '<p>Umgekehrt zieht dieselbe additive Regel China auf <b>0,0000</b>: '
         '0,20&nbsp;×&nbsp;0,55&nbsp;×&nbsp;0,9869&nbsp;=&nbsp;0,1086 minus '
         '0,20&nbsp;×&nbsp;0,80&nbsp;=&nbsp;0,16 ergibt −0,0514, geklemmt auf null. '
         'Siehe RG-A7-BODEN weiter unten.</p></div>')

# --------------------------------------------------------------- A-7.5
B.append('<div class="karte gut"><h2>A-7.5 — auf Blockgrösse ist der Wachstumskanal null</h2>'
         '<div class="wrap"><table><tr><th>Block</th><th class="n">Bev. (Mio.)</th>'
         '<th class="n">Vorfälle je Mio. bei <i>einem</i> Vorfall</th>'
         '<th class="n">Abstand zur Schwelle 0,05</th><th>Kanal</th></tr>')
for b in BL:
    e = ST[b]; t = e["terrorlage"]
    jm = t["vorfaelle_je_mio_bei_1_vorfall"]
    B.append(f'<tr><td class="fett">{e["name"]}</td>'
             f'<td class="n">{z(e["bevoelkerung_mio"], 0)}</td>'
             f'<td class="n">{z(jm, 5)}</td><td class="n">Faktor {z(0.05/jm, 1)}</td>'
             f'<td class="ok fett">{t["wachstumskanal"]}</td></tr>')
B.append('</table></div><p>Wörtlich aus dem Regelort: <i>«Auf Blockgrösse ist der '
         'Wachstumskanal null [QT-11 Gaibulloev &amp; Sandler 2019]. Ein Vorfall in einem '
         '340-Mio.-Block sind 0,003 je Mio. und liegt weit unter der Schwelle. Wer trotzdem '
         'eine Zahl bucht, erfindet sie.»</i> Der knappste Abstand ist Russland mit Faktor 7, '
         'der weiteste REST mit Faktor 220. <b>Terror kostet in dieser Partie kein '
         'Wachstum.</b></p>'
         '<p>Es bleiben genau drei Kanäle: das <b>Gegenterrorbudget</b> mit −0,10&nbsp;Pp je '
         'Stufe (steht überall auf 0, kostet also nichts), die <b>Rally</b> bei V3 und V4 mit '
         '+10&nbsp;Pp über A-2b (Halbwertszeit 0,5&nbsp;Züge), und <b>−1 Legitimität</b> bei '
         'V3+ in einer Demokratie <i>ausschliesslich dann, wenn eine Warnung vorlag und '
         'ungenutzt blieb</i> [QT-32b Tavares 2004].</p></div>')

# --------------------------------------------------------- Akteure & Klassen
B.append('<div class="karte"><h2>Was ein Vorfallwurf hergibt</h2>'
         '<p>Zwei Würfe: <b>W1000 gegen T</b> (trägt der Zug einen Vorfall?), dann <b>W100</b> '
         'für den Akteur und <b>W100</b> für die Klasse, verschoben um '
         '<code>round(12·(Letalität − 1))</code>.</p><div class="wrap"><table>'
         '<tr><th></th><th>Typ</th><th class="n">Gewicht</th><th class="n">Letalität</th>'
         '<th>Ziel</th><th class="n">Enthauptung</th></tr>')
for k in ["T1", "T2", "T3", "T4", "T5", "T6", "T7"]:
    a = TT["akteure"][k]
    mk = ' <span class="hm">(max V1)</span>' if a.get("max_klasse") else ""
    B.append(f'<tr><td class="fett">{k}</td><td>{a["name"]}{mk}</td>'
             f'<td class="n">{z(a["gewicht"])}</td><td class="n">{z(a["letalitaet"])}</td>'
             f'<td>{a["ziel"]}</td><td class="n">{z(a["enthauptung_faktor"])}</td></tr>')
B.append('</table></div><div class="wrap"><table>'
         '<tr><th>Klasse</th><th class="n">Tafel</th><th>Bedeutung</th></tr>')
for kl in ["V1", "V2", "V3", "V4"]:
    lo, hi = TT["vorfall"]["tafel_W100"][kl]
    sp = f"{lo}" if lo == hi else f"{lo}–{hi}"
    B.append(f'<tr><td class="fett">{kl}</td><td class="n">{sp}</td>'
             f'<td>{TT["vorfall"]["klassen"][kl]}</td></tr>')
B.append('</table></div><p><b>V4 verlangt Fähigkeit <i>und</i> einen Bestätigungswurf '
         'W100&nbsp;≤&nbsp;10.</b> Ohne ihn trug die Letalitätsverschiebung allein schon '
         '8&nbsp;% aller Vorfälle nach V4 — ein 9/11 alle zwölf Jahre je Staat. '
         '<b>T5 kann der Wurf nicht über den Nadelstich hinaustragen</b>: Umweltbewegte '
         'gebrauchen so gut wie nie tödliche Gewalt — «Ökotage» statt «Ökoterror» '
         '[QT-30 Fleming 2024]. Der Ökofaschismus gehört zu T3, nicht zu T5 '
         '[QT-28 Macklin 2022].</p></div>')

# --------------------------------------------------------------- RULES-GAPs
gaps = [
    ("RG-A6-VORZEICHEN", "Das Vorzeichen in Autokratien — GRUENDLER oder SAHA",
     "QK-01 Gründler/Potrafke 2019 und QK-06 Saha/Sen 2020 widersprechen sich im "
     "<b>Vorzeichen</b> für Autokratien. <b>GRUENDLER</b> (aktiv) ×1,3 — der Effekt ist "
     "dort stärker. <b>SAHA</b> (bereit) ×(−0,5) — Korruption <i>hebt</i> dort das "
     "Wachstum (Ostasien-Paradox, 100+ Staaten 1984–2016). Betroffen: China, Russland, "
     "REST. Solange ΔK = 0, macht die Wahl keinen Unterschied; sie schlägt durch, sobald "
     "ein Autokrat Korruption bekämpft oder Patronage kauft — unter SAHA würde eine "
     "Antikorruptionskampagne in China das Wachstum <i>senken</i>. "
     "Der Regelort legt das ausdrücklich dem Tisch vor, wie PENNY und BETTER ANGELS."),
    ("RG-A6-NIVEAU", "Niveauabschlag gerechnet, nicht auf die BIP-Reihe gebucht",
     "Der Bestand ergibt: USA und EU <b>+15,30&nbsp;%</b> · Indien 0,00&nbsp;% · China "
     "<b>−3,683&nbsp;%</b> · Russland <b>−19,89&nbsp;%</b> · REST −7,367&nbsp;%. "
     "<b>Nicht gebucht</b>, aus zwei Gründen. <i>Erstens:</i> die BIP-Reihe startet 2026 "
     "aus realen Daten und trägt das Korruptionsniveau der Blöcke bereits — ein zweites "
     "Mal buchen wäre genau die Doppelbuchung, vor der CLAUDE.md&nbsp;§2 warnt. "
     "<i>Zweitens:</i> das vom Regelort genannte Zielfeld <code>index_real</code> ist in "
     "diesem Code eine EH-01-Energiekostengrösse (<code>index_real = kosten / kosten0</code>), "
     "keine BIP-Reihe; der Stand führt es nicht. Die Zahlen stehen vollständig im Stand. "
     "Wer sie bucht, muss sie <b>in beide Richtungen</b> buchen — bei USA und EU wäre es "
     "ein Zuschlag."),
    ("RG-A7-BIP", "bip_index ist auf 0…1 nicht definiert",
     "A-7.1 rechnet <code>(0,9 + 0,2·bip_index)</code>, sagt aber nicht, wie der Wohlstand "
     "eines Blocks auf 0…1 abgebildet wird. Der Stand führt den Wohlstandsindex von 0,396 "
     "(Indien) bis 3,732 (USA). Gebucht ist <b>L1 normiert</b> (w / max&nbsp;w, also "
     "1,0 = reichster Block). Alternative <b>L2 geklemmt</b> (min(1, w), Weltdurchschnitt "
     "und darüber = 1,0). Der Unterschied ist klein, weil der Faktor nur zwischen 0,90 und "
     "1,10 läuft: EU 0,2676 gegen 0,2900 · Indien 0,4403 gegen 0,4548 · Russland 0,1000 "
     "gegen 0,1090 · REST 0,1952 gegen 0,2232 · USA und China unverändert. Beide Zahlen "
     "stehen im Stand."),
    ("RG-A7-BODEN", "China fällt bei T auf den Boden — die Formel kann negativ werden",
     "China kommt auf <b>T = 0,0000</b>, und das ist eine Klemmung, kein Rechenergebnis: "
     "roh −0,0514. Der Regelort rechnet sein eigenes Beispiel bei Repression 0,6 noch auf "
     "T 0,023 vor; bei 0,8 trägt der additive Repressionsterm die Grösse unter null. "
     "Innerhalb der Regel richtig gerechnet — der Einparteienstaat mit maximaler Repression "
     "ist nach QT-02 und QT-06 tatsächlich der terrorunanfälligste Fall — aber es heisst, "
     "dass <b>China bis auf Weiteres gar keinen Vorfallwurf hat</b>. Verwandt mit O-31: "
     "die Basisraten für T sind gegen kein Länderpanel kalibriert."),
]
B.append('<div class="karte gap"><h2>Vier Regellücken, dem Tisch vorgelegt</h2>')
for ref, titel, txt in gaps:
    B.append(f'<h3>{ref} — {titel}</h3><p>{txt}</p>')
B.append('</div>')

# ------------------------------------------------------------------ Befunde
B.append('<div class="karte warn"><h2>Drei Befunde nebenbei</h2>'
         '<h3>B-30 — Zug 5 hat keine B-2-Kaskadenwürfe gebucht</h3>'
         '<p>Die Züge 1 bis 4 führen ihre Kaskadenwürfe namentlich mit Seed (Zug&nbsp;4: '
         '258 gegen 975, der Treffer in China). Für Zug&nbsp;5 steht weder in '
         '<code>domaenen_zug5</code> noch in <code>AUFLOESUNG_ZUG5.md</code> noch im '
         'Zugjournal ein Wurf. Entweder gefallen und nicht protokolliert, oder ausgefallen. '
         '<b>Nicht von mir nachgeholt</b> — ein Wurf in einem scharf gebuchten Zug ist keine '
         'Korrektur, die ein Bediener allein vornimmt.</p>'
         '<h3>B-31 — fünf Regler stehen auf null, weil Blatt 4 sie erst ab Zug 6 führt</h3>'
         '<p>Ausschluss, Gegenterror, Einschluss, Patronage und Antikorruption sind '
         '<i>Spielerbefehle</i>, keine Zustandsgrössen. <code>blattlesen.py</code> weist '
         'Unlesbares nach V24 ausdrücklich zurück, statt zu raten — also wird auch hier nicht '
         'geraten. Folge: <code>f_Ausschluss</code> steht überall auf 1,0 und trägt zur '
         'Terrorlage nichts bei, obwohl politischer Ausschluss mit ×(1&nbsp;+&nbsp;0,9·a) der '
         'zweitstärkste und einzige mit Güte&nbsp;A belegte Treiber wäre [QT-03]. '
         '<b>Einschluss wirkt mit zwei Zügen Verzug</b> und ist nach A-7.6 der einzige '
         'dauerhafte Hebel — wer in Zug&nbsp;6 nichts setzt, hat vor Zug&nbsp;9 nichts davon.</p>'
         '<h3>B-32 — REST führt bis heute keinen A-2-Coup-Track</h3>'
         '<p>Die Züge 2 bis 5 buchen den Coup-Track für RUS, IND, CHN, EU und seit Zug&nbsp;4 '
         'die USA — REST kommt in keiner Zeile vor (verwandt mit B-27, wo '
         '<code>bodenlage.py</code> REST ebenfalls überspringt). Dabei hat REST als hybrid mit '
         'p_basis&nbsp;0,045 den <b>höchsten Grundwert der Tafel</b>: 5,342&nbsp;% je Zug mit '
         'Rezessionsflag, 3,634&nbsp;% ohne — in beiden Fällen mehr als Russland.</p></div>')

# ------------------------------------------------------------------- Prüfung
B.append('<div class="karte gut"><h2>Geprüft</h2><ul>'
         '<li><b>WN-01-Validator</b> — BESTANDEN, 0 Fehler, 0 Warnungen</li>'
         '<li><b>SP-01 Schiffsprüfer</b> (Gatter nach CLAUDE.md&nbsp;§0) — BESTANDEN, '
         '0 Fehler; ein Hinweis, Chinas Werft zu 91&nbsp;% ausgelastet</li>'
         '<li><b>erde01_engine selftest</b> — 30 ok, 0 FAIL</li>'
         '<li><b>Gegenprobe A-2</b> — die Werte vor A-6 reproduzieren die gebuchten '
         'Zug-4-Zahlen auf drei Nachkommastellen</li>'
         '<li><b>Gegenprobe Repression Russland</b> — 0,50 aus dem gebuchten B-2-Wert '
         '5,25&nbsp;% rückgerechnet, an sieben Buchungen bestätigt</li></ul>'
         '<p class="q">Jede Zahl auf diesem Blatt stammt aus <code>erde01_engine.py</code> '
         'oder <code>hybrid01.py</code>, aufgerufen von '
         '<code>zug6/skripte/a6_a7_buchung.py</code>. Keine stammt aus dem Kopf. '
         'Journal: <code>zug6/journal/journal_zug6.jsonl</code>, Einträge Z6-001 bis Z6-013.</p></div>')

pfad = os.path.join(W, "zug6", "A6_Korruption_A7_Terror_Zug6.html")
open(pfad, "w", encoding="utf-8").write("".join(B))
print(pfad)
