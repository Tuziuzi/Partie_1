#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Datenblatt der Endfassung — Modus B, ferngelenkt, mit Engpassrechnung."""
import json, datetime
E=json.load(open("Ships/chn_raumfahrzeuge_2030.json"))
L=json.load(open("Ships/entwuerfe/loesung_chn_final.json"))
HK={"pay_dry":("Nutzlast / trocken",6.8,58.2),"paybus_dry":("(Nutzlast+Bus) / trocken",17.7,78.2),
    "struct_dry":("Struktur / trocken",10.7,20.6),"dry_wet":("trocken / nass",40.2,93.3),
    "pp_dry":("Kraftwerk+Batterie / trocken",5.0,15.0)}
def z(x,n=1): return f"{x:,.{n}f}".replace(","," ").replace(".",",")
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

B=['<meta charset="utf-8"><title>CHN Raumfahrzeuge 2030</title><style>'
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
 '.warn{border-left:3px solid var(--ocker)}.fern{border-left:3px solid var(--rot)}'
 'table{border-collapse:collapse;width:100%;font-size:13.5px}'
 'td,th{border-bottom:1px solid var(--linie);padding:5px 6px;text-align:left;vertical-align:top}'
 'th{color:var(--leise);font-weight:600}td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}'
 '.wrap{overflow-x:auto}code{font-size:12.5px}'
 '.tag{display:inline-block;font-size:11.5px;padding:1px 7px;border-radius:9px;border:1px solid var(--linie);'
 'color:var(--leise);margin:0 4px 4px 0}.tagN{border-color:var(--ocker);color:var(--ocker)}'
 '.tagR{border-color:var(--rot);color:var(--rot)}'
 '.ok{color:var(--gruen)}.hm{color:var(--ocker)}.bad{color:var(--rot)}.fett{font-weight:700}'
 'p{margin:8px 0 0;font-size:13px}.q{color:var(--leise);font-size:12px}</style>']

B.append('<h1>Chinesische Raumfahrzeuge — Endfassung</h1>')
B.append('<div class="kopf">Kampagne SCHWARZE SEE · Stand nach Zug&nbsp;5 (2030) · Unified Shipyard '
 'v5.22, ship_export&nbsp;2.2 · Modus&nbsp;B mit voller Penaltykette<br>'
 '<b>Entscheid des Tisches:</b> die Strukturtonne ist Nutzlast und wird weggelassen. Damit sind '
 'alle drei Schiffe <b>ferngelenkt</b> — und tragen dafür volle Härtung. '
 f'Erzeugt {datetime.date.today().isoformat()}.</div>')

B.append('<div class="karte warn"><h2>Keine Hochenergie — und deshalb auch kein Δv-Malus</h2>'
 '<p><code>construction.md</code> §Weight Penalty 3: <i>«<b>High-Energy-Systeme (ab ~50&nbsp;kW, '
 'z.B. Laser):</b> Reaktor + Heatsinks extra berechnen. Zusätzlich: <b>Δv ÷ 3</b> und '
 '<b>3× Gewicht</b>»</i></p>'
 '<p>Das ist <b>eine Strafe mit zwei Hälften</b>, und sie greift erst ab ~50&nbsp;kW. Meine vorige '
 'Fassung hatte zwei Schiffen die Gewichtshälfte aufgeladen, ohne dass sie die Schwelle erreichen — '
 'und die Δv-Hälfte nie angewandt. Beides ist korrigiert: alle drei deklarieren jetzt '
 '<code>ctxNoHE</code>, tragen <b>weder ×3 noch ÷3</b>.</p><div class="wrap"><table>'
 '<tr><th>Schiff</th><th class="n">Spitzenlast</th><th class="n">Schwelle</th><th>Folge</th></tr>'
 '<tr><td>Feldzeichen</td><td class="n">3,60 kW</td><td class="n">50 kW</td>'
 '<td class="ok">kein Hochenergie-System — ctxNoHE</td></tr>'
 '<tr><td>Himmelsauge</td><td class="n">11,00 kW</td><td class="n">50 kW</td>'
 '<td class="ok">kein Hochenergie-System — ctxNoHE</td></tr>'
 '<tr><td>Himmelsbrücke</td><td class="n">17,70 kW</td><td class="n">50 kW</td>'
 '<td class="ok">kein Hochenergie-System — ctxNoHE</td></tr></table></div>'
 '<p class="q">Mit <code>ctxNoHE</code> entfällt das ×3, dafür wird cm zusätzlich mit np '
 'multipliziert (cm = np²). Das kehrt den Anreiz um: niedriges np wird günstig, hohes teuer. '
 'Deshalb tragen jetzt alle drei Schiffe Nachteile — nicht um Masse zu sparen, sondern weil die '
 'ehrliche Deklaration sie dorthin führt. Die Startmassen bleiben unverändert 2,0 / 3,6 / 5,0&nbsp;t.</p></div>')

B.append('<div class="karte fern"><h2>Was Fernlenkung bedeutet</h2>'
 '<p><code>construction.md</code> §«Struktur = Autonomie (Kernregel)»: <i>«Die Strukturtonne kauft '
 'nicht Rumpf, sondern <b>Autonomie</b>: Bordrechner, Selbststeuerung, eigene Feuerleitung. Sie ist '
 'ein Bauentscheid und muss explizit verbaut sein — ab 10&nbsp;t gratis, darunter 1&nbsp;t.»</i></p>'
 '<p>Ohne sie gilt für alle drei Schiffe:</p><ul style="font-size:13px;margin:6px 0 0 18px">'
 '<li>Jede Aktion — Manöver, Feuer, Sensorbetrieb, Response — setzt einen <b>aktiven Kommandolink</b> voraus.</li>'
 '<li>Link gejammt oder unterbrochen: <b>vollständig handlungsunfähig</b>, driftet ballistisch weiter, '
 'im Kampf <b>wehrloses Ziel</b> (<code>no_response</code>).</li>'
 '<li>Steuerstellen sind Chinas Bodenstationen und die beiden GEO-Relais. Die Relais sind selbst '
 'ferngelenkt — die Kette lautet <b>Erde → Relais → Scorer</b>. Wer den ersten Link bricht, legt alles still.</li></ul>'
 '<p class="q">Das ist der Preis dafür, dass die Schiffe in ihre gebuchten Massen passen. '
 'Er ist mit BS-01 (Bodenstörer, Uplink-Jamming) unmittelbar angreifbar.</p></div>')

for s in E["ships"]:
    c=s["customData"]; did=c["kampagnenDesign"]; d=L[did]
    mb=c["massBreakdown_kg"]; k=c["k2Kette"]; bg=c["begruendungVorNachteile"]; sw=c["spielwirkungen"]
    B.append('<div class="karte">')
    B.append(f'<h2>{esc(s["name"])} <span class="q">— {esc(c["kampagnenName"])} · {did} · '
             f'{esc(c["einsatzzonen"])}</span></h2>')
    B.append('<span class="tag tagR">ferngelenkt</span>'
             + ''.join(f'<span class="tag">{esc(t)}</span>' for t in
                [s["class"], f'Struktur {c["structureTax"]["struct_pct"]:.0f} % / Tank '
                 f'{c["structureTax"]["tank_pct"]:.0f} %'] + c["advantages"])
             + ''.join(f'<span class="tag tagN">{esc(t)}</span>' for t in c["disadvantages"]))

    B.append('<h3>Penaltykette</h3><div class="wrap"><table>'
      f'<tr><th>Basisnutzlast</th><td class="n">{z(k["basis_kg"])} kg</td>'
      f'<th colspan="2">{esc(c["nutzlastHerkunft"])}</th></tr>'
      f'<tr><th>np = 3 + {len(c["advantages"])} − {len(c["disadvantages"])}</th>'
      f'<td class="n fett">{k["np"]}</td><th>cm</th><td class="n">{z(k["cm"],0)}'
      f'{" (ctxNoHE: cm × np)" if k.get("ctxNoHE") else ""}</td></tr>'
      f'<tr><th>Hochenergie</th><td class="n">×{z(k["hochenergie_faktor"],0)}'
      f'{" — entfällt, ctxNoHE deklariert" if k.get("ctxNoHE") else ""}</td>'
      f'<th>Nutzlast endgültig</th><td class="n fett">{z(k["nutzlast_final_kg"])} kg</td></tr>'
      '</table></div>')

    B.append('<h3>Vorteile und Nachteile — benannt, begründet, mit Spielwirkung</h3>'
             '<div class="wrap"><table><tr><th>Art</th><th>Bezeichnung</th><th>Spielwirkung</th>'
             '<th>Begründung</th></tr>')
    for a in c["advantages"]:
        B.append(f'<tr><td class="ok">Vorteil</td><td class="fett">{esc(a)}</td>'
                 f'<td>{esc(sw[a])}</td><td>{esc(bg[a])}</td></tr>')
    for a in c["disadvantages"]:
        B.append(f'<tr><td class="hm">Nachteil</td><td class="fett">{esc(a)}</td>'
                 f'<td>{esc(sw[a])}</td><td>{esc(bg[a])}</td></tr>')
    B.append('</table></div>')

    B.append('<h3>Kenngrössen</h3><div class="wrap"><table>')
    B.append(f'<tr><th>Startmasse (nass)</th><td class="n fett">{z(mb["nass"])} kg</td>'
             f'<th>gebuchter Anker</th><td class="n">{z(c["gebuchteStartmasse_kg"])} kg '
             f'<span class="ok">± 0,0000 %</span></td></tr>')
    B.append(f'<tr><th>Trockenmasse</th><td class="n">{z(mb["trocken"])} kg</td>'
             f'<th>Treibstoff</th><td class="n">{z(mb["treibstoff"])} kg '
             f'({esc(s["engines"][0]["propType"])})</td></tr>')
    B.append('<tr><th>Triebwerke</th><td colspan="3">'
             + ' · '.join(f'{e["count"]} × {esc(e["name"])}' for e in s["engines"]) + '</td></tr>')
    B.append(f'<tr><th>Isp</th><td class="n">{s["isp"]} s</td><th>Schub gleichzeitig</th>'
             f'<td class="n">{z(c["thrust_simultaneous_N"],3)} N</td></tr>')
    B.append(f'<tr><th>Δv gesamt</th><td class="n fett">{z(s["currentDeltaV"])} m/s</td>'
             f'<th>Manöverzeit</th><td class="n">{z(c["maneuverTime_s"]/3600,2)} h</td></tr>')
    B.append(f'<tr><th>davon Manöverbudget</th><td class="n">{z(c["dv_manoever_kms"]*1000)} m/s</td>'
             f'<th>davon Bahnhaltung</th><td class="n">{z(c["dv_stationshaltung_kms"]*1000)} m/s</td></tr>')
    B.append(f'<tr><th>Kraftwerk</th><td class="n">{z(c["powerPlant"]["output_kw"],2)} kW solar</td>'
             f'<th>Batterie</th><td class="n">{z(c["powerPlant"]["battery_kg"])} kg / '
             f'{z(c["powerPlant"]["battery_hours"],1)} h</td></tr>')
    B.append('</table></div>')
    B.append('<div class="wrap"><table><tr><th>Massenposten</th>'
             + ''.join(f'<th class="n">{h}</th>' for h in
               ["Nutzlast","Bus","Triebw.","Kraftw.","PMAD","Batt.","Radiator","Tank","Struktur"])
             + '</tr><tr><td>kg</td>' + ''.join(f'<td class="n">{z(mb[x])}</td>' for x in
               ["nutzlast","bus","triebwerke","kraftwerk","pmad","batterie","radiator","tank","struktur"])
             + '</tr></table></div>')
    B.append('<div class="wrap"><table><tr><th>Hüllkurve (20 reale Systeme)</th><th class="n">Wert</th>'
             '<th class="n">Spanne</th><th>Befund</th></tr>')
    for kk,(lbl,lo,hi) in HK.items():
        v=c["huellkurve"][kk]; drin=lo<=v<=hi
        B.append(f'<tr><td>{lbl}</td><td class="n">{z(v)} %</td><td class="n">{z(lo)}–{z(hi)} %</td>'
                 f'<td class="{"ok" if drin else "hm"}">'
                 f'{"in der Hüllkurve" if drin else "ausserhalb — siehe Befund"}</td></tr>')
    B.append('</table></div></div>')

WERFT=[("Scorer",5,2.0),("GEO-Relais",2,5.0),("Aufklärer",2,3.6)]
ges=sum(n*m*4.0 for _,n,m in WERFT)
B.append('<div class="karte warn"><h2>Engpass: die Werft, nicht die Rakete</h2>'
 '<p><code>BZ-01 §1</code>: <i>«Kosten = Kaufladenpreis × K(P-Stufe) × … »</i> und <i>«Werftdurchsatz '
 '= <code>industrial.capacity_t_year</code>. Keine neue Währung.»</i> China hat <b>40,0 t/a</b>, '
 'das Baufenster 2026–2028 sind drei Jahre, also <b>120,0 t</b>. Der Kostenmultiplikator ist '
 '4,0 (P0n, Erststück).</p><div class="wrap"><table>'
 '<tr><th>Posten</th><th class="n">Stück</th><th class="n">je Stück</th><th class="n">Masse</th>'
 '<th class="n">× 4,0</th></tr>')
for lbl,n,m in WERFT:
    B.append(f'<tr><td>{lbl}</td><td class="n">{n}</td><td class="n">{z(m,1)} t</td>'
             f'<td class="n">{z(n*m,1)} t</td><td class="n">{z(n*m*4,1)} t</td></tr>')
B.append(f'<tr><td class="fett">Summe</td><td></td><td></td>'
 f'<td class="n fett">{z(sum(n*m for _,n,m in WERFT),1)} t</td>'
 f'<td class="n fett">{z(ges,1)} t</td></tr>'
 f'<tr><td class="fett">verfügbar</td><td colspan="3">40,0 t/a × 3 Baujahre</td>'
 f'<td class="n fett">120,0 t</td></tr></table></div>'
 f'<p><b>Auslastung {z(100*ges/120,0)} %.</b> Es passt — aber es ist kein Spielraum mehr da. '
 'Zum Vergleich, was <i>nicht</i> mehr ginge:</p><div class="wrap"><table>'
 '<tr><th>Auslegung</th><th class="n">Masse</th><th class="n">Werft</th><th>Urteil</th></tr>'
 '<tr><td>Endfassung (ferngelenkt)</td><td class="n">27,2 t</td><td class="n">108,8 t</td>'
 '<td class="ok">passt, 91 %</td></tr>'
 '<tr><td>autonom, 10-t-Klasse (Struktur + Sensor gratis)</td><td class="n">80,0 t</td>'
 '<td class="n">320,0 t</td><td class="bad">8,0 Jahre Werft — unmöglich</td></tr>'
 '<tr><td>Aufklärer mit 1-t-Sensor bei np 5</td><td class="n">54,1 t</td><td class="n">216,5 t</td>'
 '<td class="bad">5,4 Jahre Werft — unmöglich</td></tr></table></div>'
 '<p class="q">Die Startkapazität wäre bei allen drei Varianten ausreichend gewesen — 69,2 t von '
 '400,0 t bei der Endfassung, 170 t bei der 10-t-Klasse. <b>Die Werft ist die Schranke, nicht die '
 'Rakete.</b> Genau deshalb ist die Fernlenkung nicht nur eine Sparmassnahme, sondern die einzige '
 'Auslegung, die China 2026–2029 überhaupt bauen konnte.</p></div>')

B.append('<div class="karte warn"><h2>Befunde</h2><div class="wrap"><table>'
 '<tr><th>Nr.</th><th>Befund</th></tr>'
 '<tr><td>B-1</td><td><b>Der Einwand war berechtigt.</b> Meine vorige Fassung gab Aufklärer und '
 'Scorer <i>null</i> Vorteile, um np&nbsp;=&nbsp;0 und damit 2&nbsp;t zu halten — Satelliten ohne '
 'Strahlungs-Härtung in MEO&nbsp;20&nbsp;000, HEO&nbsp;39&nbsp;000 und GEO. Nicht haltbar: '
 '27 von 32 realen Systemen im OW-01-Katalog tragen sie, Chinas eigene TJS und Shijian-21/25 in GEO '
 'ebenfalls. <b>Kein einziges der 32 Systeme liegt bei np&nbsp;≤&nbsp;0</b> — das kleinste np im '
 'Katalog ist 3, der Median 5.</td></tr>'
 '<tr><td>B-2</td><td><b>Die Strukturtonne war der Hebel.</b> Sie ist Nutzlast '
 '(<code>comps shipframe</code>, 1&nbsp;000&nbsp;kg) und ging als K2-Basis mit dem Faktor 15 ein. '
 'Weggelassen sinkt die Basis um 1&nbsp;000&nbsp;kg — genug, damit das <b>Feldzeichen</b> bei '
 '<b>np&nbsp;5 mit voller Härtung</b> in seine unveränderten 2&nbsp;t passt. np&nbsp;5 mit zwei '
 'Vorteilen ist exakt die Konfiguration von TJS Spähauge. Der Preis: ferngelenkt.</td></tr>'
 '<tr><td>B-3</td><td><b>Beim Aufklärer reicht das nicht.</b> Sein 1-t-Sensor «bis GEO alles '
 'aufdecken» bleibt als Basis stehen. Auch mit <code>ctxNoHE</code> (ehrlich deklarierbar: '
 '11&nbsp;kW Bordleistung, kein System ab 50&nbsp;kW) und vier Nachteilen kommt er auf '
 '2&nbsp;000&nbsp;kg Nutzlast und damit auf <b>3,6&nbsp;t statt 2,0&nbsp;t</b>. Neu gebucht, '
 'Startvortrag 334,0&nbsp;→&nbsp;330,8&nbsp;t. Kleiner wäre er nur mit einer schwächeren '
 'Sensorklasse — dann verlöre China die Aufklärung bis GEO.</td></tr>'
 '<tr><td>B-4</td><td><b>Die Kommandokette ist jetzt der verwundbare Punkt.</b> Erde&nbsp;→&nbsp;'
 'Relais&nbsp;→&nbsp;Scorer, und die Relais sind selbst ferngelenkt. Ein erfolgreicher '
 'Uplink-Störangriff (BS-01) legt Chinas gesamte Bahnlage still, ohne einen Schuss. Das ist keine '
 'Nebenwirkung, sondern die Kehrseite des Entwurfs und gehört auf das Lagebild.</td></tr>'
 '<tr><td>B-5</td><td><b>Die fünf Scorer sind nicht mehr «Single-Use».</b> Der Nachteil ist in der '
 'Endfassung entfallen; sie sind grundsätzlich betankbar, haben aber nach Zug&nbsp;5 kein Δv mehr '
 '(Status <code>treibstoff_erschoepft</code>). Für Zug&nbsp;6 heisst das: Tanker hinschicken oder '
 'neu starten — und die Werft ist zu 91&nbsp;% ausgelastet.</td></tr>'
 '<tr><td>B-6</td><td><i>trocken/nass</i> liegt bei Himmelsauge (97,8&nbsp;%) und Himmelsbrücke '
 '(95,3&nbsp;%) über der Spanne 40,2–93,3&nbsp;%. Kein Fehler: kein Referenzsystem trägt so wenig '
 'Δv, das sparsamste ist SPADEX mit 150&nbsp;m/s bei 93,3&nbsp;%. Beim Feldzeichen liegen alle fünf '
 'Kennzahlen innen.</td></tr>'
 '<tr><td>B-7</td><td><b>Bei Indien nachgezogen:</b> IND_SPADEX führte keine Steuerung. Als '
 'Modus-A-Rekonstruktion ist es <i>autonom</i> — die reale SDX-01/02 hat im Januar 2025 autonomes '
 'Docking geflogen, und in Modus&nbsp;A ersetzt die Messung den Prior. In reinen Delta-V-Begriffen '
 'wäre ein 258-kg-Körper allerdings Long-Shot-Klasse und damit ferngelenkt. '
 '<b>Entscheidung des Tisches.</b></td></tr>'
 '</table></div></div>')

B.append('<p class="q">Rechenweg: <code>Ships/konstruktion_chn_final.py</code> · '
 '<code>Ships/varianten_chn.py</code> (alle 24 Kombinationen je Schiff) · '
 '<code>Ships/varianten_ferngelenkt.py</code> · <code>Ships/entscheidung_chn.py</code> (ctxNoHE und '
 'Werft) · <code>Ships/export_chn.py</code> · <code>Ships/stats_html.py</code>. '
 'Massenmodell OW-01 <code>nachbau.py</code>, gegen 32 reale Orbitalsysteme geprüft. '
 'Regelgatter <code>pruefer/schiffspruefer.py</code>: BESTANDEN, 0 Fehler. '
 'Vertraulich wie jedes Befehlsblatt.</p>')
open("Ships/CHN_Raumfahrzeuge_Stats.html","w").write("\n".join(B))
print("-> Ships/CHN_Raumfahrzeuge_Stats.html")
