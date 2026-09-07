#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Datenblatt der drei CHN-Raumfahrzeuge — MODUS B, volle Penaltykette."""
import json, datetime

E = json.load(open("Ships/chn_raumfahrzeuge_2030.json"))
L = json.load(open("Ships/entwuerfe/loesung_chn_modusB.json"))
HK = {"pay_dry": ("Nutzlast / trocken", 6.8, 58.2), "paybus_dry": ("(Nutzlast+Bus) / trocken", 17.7, 78.2),
      "struct_dry": ("Struktur / trocken", 10.7, 20.6), "dry_wet": ("trocken / nass", 40.2, 93.3),
      "pp_dry": ("Kraftwerk+Batterie / trocken", 5.0, 15.0)}
def z(x, n=1): return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

B = ['<meta charset="utf-8"><title>CHN Raumfahrzeuge 2030</title><style>'
 ':root{--grund:#f4eede;--feld:#fffdf6;--linie:#d6cdb6;--schrift:#1d2b36;--leise:#5c6b76;'
 '--blau:#2e6c96;--rot:#a8412a;--gruen:#4a7a42;--ocker:#8a6d1f}'
 '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--grund:#0f151a;--feld:#161f27;'
 '--linie:#26343e;--schrift:#e7eef4;--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;--ocker:#dcb45e}}'
 ':root[data-theme="dark"]{--grund:#0f151a;--feld:#161f27;--linie:#26343e;--schrift:#e7eef4;'
 '--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;--ocker:#dcb45e}'
 'body{background:var(--grund);color:var(--schrift);font:15px/1.5 -apple-system,BlinkMacSystemFont,'
 '"Segoe UI",Roboto,sans-serif;margin:0;padding:14px}'
 'h1{font-size:19px;margin:0 0 2px}h2{font-size:16px;margin:0 0 10px;color:var(--blau)}'
 'h3{font-size:13px;margin:14px 0 6px;color:var(--leise);text-transform:uppercase;letter-spacing:.06em}'
 '.kopf{color:var(--leise);font-size:12.5px;margin-bottom:16px}'
 '.karte{background:var(--feld);border:1px solid var(--linie);border-radius:10px;padding:12px 14px;margin-bottom:14px}'
 '.warn{border-left:3px solid var(--ocker)}'
 'table{border-collapse:collapse;width:100%;font-size:13.5px}'
 'td,th{border-bottom:1px solid var(--linie);padding:5px 6px;text-align:left;vertical-align:top}'
 'th{color:var(--leise);font-weight:600}td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}'
 '.wrap{overflow-x:auto}code{font-size:12.5px}'
 '.tag{display:inline-block;font-size:11.5px;padding:1px 7px;border-radius:9px;border:1px solid var(--linie);'
 'color:var(--leise);margin:0 4px 4px 0}.tagN{border-color:var(--ocker);color:var(--ocker)}'
 '.ok{color:var(--gruen)}.hm{color:var(--ocker)}.bad{color:var(--rot)}.fett{font-weight:700}'
 'p{margin:8px 0 0;font-size:13px}.q{color:var(--leise);font-size:12px}</style>']

B.append('<h1>Chinesische Raumfahrzeuge — Neuberechnung in Modus B</h1>')
B.append('<div class="kopf">Kampagne SCHWARZE SEE · Stand nach Zug&nbsp;5 (2030) · Unified Shipyard v5.22, '
 'ship_export&nbsp;2.2<br><b>Korrigiert:</b> die erste Fassung lief in Modus&nbsp;A und nahm damit die '
 'Nachbau-Ausnahme in Anspruch. <code>construction.md</code> gewährt sie nur für '
 '<code>designMode:&nbsp;"reconstruction"</code>, also für ein reales System mit veröffentlichter '
 'Startmasse. Diese drei sind Kampagnenentwürfe ohne reales Vorbild — die Ausnahme steht ihnen nicht zu. '
 f'Alle drei Kanäle laufen jetzt vollständig. Erzeugt {datetime.date.today().isoformat()}.</div>')

B.append('<div class="karte"><h2>Die Penaltykette</h2><div class="wrap"><table>'
 '<tr><th>Kanal</th><th>Regel</th><th>Wirkung hier</th></tr>'
 '<tr><td><b>K1</b> Strukturabgabe</td><td>+(Vorteile − Nachteile) Prozentpunkte auf Struktur und Tank, '
 'Boden&nbsp;0 bei Vorteile&nbsp;≤&nbsp;Nachteile</td><td>läuft in beiden Modi</td></tr>'
 '<tr><td><b>K2</b> Nutzlastmultiplikator</td><td><code>np = 3 + adv − disadv</code>; <code>cm</code>: '
 'np≥2→np, np=1→2, <b>np≤0→1 (geklemmt, kein ×3)</b>; <code>final = Basis × cm × disc × (1+env)</code>, '
 'dann <b>×3</b> für Hochenergie</td><td><b>der übersehene Kanal</b></td></tr>'
 '<tr><td><b>K3</b> Hardwaremassen</td><td>reale Katalogmassen</td><td>läuft in beiden Modi</td></tr>'
 '</table></div>'
 '<p><b>Penalty-Reduktion durch Forschung ist 2030 nicht verfügbar.</b> <code>construction.md</code> nennt '
 'L1/L2/L3 = −1/−2/−3 Penalties, aber <code>research.md</code> schaltet L1 frühestens <b>2035</b> frei, und '
 '<code>factions.*.research.completedL1/L2/L3</code> sind bei allen Fraktionen leer. Auch der Küstenschutz '
 'aus Chinas Siegprämie zählt nicht: er wurde als Hausentscheidung gebucht und steht nicht im L1-Katalog '
 '(Journal Z5‑039). Es bleiben ausschliesslich <b>benannte Nachteile, je −1</b>.</p></div>')

for s in E["ships"]:
    c = s["customData"]; did = c["kampagnenDesign"]; d = L[did]
    mb = c["massBreakdown_kg"]; k = c["k2Kette"]; bg = c["begruendungVorNachteile"]
    B.append('<div class="karte">')
    B.append(f'<h2>{s["name"]} <span class="q">— {c["kampagnenName"]} · {did}</span></h2>')
    B.append(''.join(f'<span class="tag">{esc(t)}</span>' for t in
             [s["class"], c["structureClass"], f'Struktur {c["structureTax"]["struct_pct"]:.0f} % / '
              f'Tank {c["structureTax"]["tank_pct"]:.0f} %'] + c["advantages"])
             + ''.join(f'<span class="tag tagN">{esc(t)}</span>' for t in c["disadvantages"]))

    B.append('<h3>Penaltykette</h3><div class="wrap"><table>'
      f'<tr><th>Basisnutzlast</th><td class="n">{z(k["basis_kg"])} kg</td>'
      f'<th>Herkunft</th><td>{esc(c["kampagnenName"])} — {esc(c.get("nutzlastHerkunft","siehe Notiz"))}</td></tr>'
      f'<tr><th>np = 3 + {len(c["advantages"])} − {len(c["disadvantages"])}</th><td class="n fett">{k["np"]}</td>'
      f'<th>cm</th><td class="n">{z(k["cm"],0)}</td></tr>'
      f'<tr><th>Hochenergie</th><td class="n">×{z(k["hochenergie_faktor"],0)}</td>'
      f'<th>Nutzlast endgültig</th><td class="n fett">{z(k["nutzlast_final_kg"])} kg</td></tr>'
      f'<tr><th>zum Vergleich: ohne geheilte Penalty (np = 3)</th><td class="n">'
      f'{z(k["vergleich_ohne_geheilte_penalty_kg"])} kg</td>'
      f'<th>Faktor gegenüber jetzt</th><td class="n">×{z(k["vergleich_ohne_geheilte_penalty_kg"]/k["nutzlast_final_kg"],1)}</td></tr>'
      '</table></div>')

    B.append('<h3>Vorteile und Nachteile — benannt, begründet, mit Spielwirkung</h3><div class="wrap"><table>'
      '<tr><th>Art</th><th>Bezeichnung</th><th>Begründung</th></tr>')
    for a in c["advantages"]:
        B.append(f'<tr><td class="ok">Vorteil</td><td class="fett">{esc(a)}</td><td>{esc(bg[a])}</td></tr>')
    for a in c["disadvantages"]:
        B.append(f'<tr><td class="hm">Nachteil</td><td class="fett">{esc(a)}</td><td>{esc(bg[a])}</td></tr>')
    if not c["advantages"]:
        B.append('<tr><td class="hm">—</td><td class="fett">keine Vorteile</td><td>Das Schiff läuft auf der '
                 'Basis der Tax-Tabelle: −200&nbsp;°C, freie Rundumsicht. Keine Strahlungs-Härtung, kein '
                 'thermischer Betrieb darüber hinaus, keine Sensor-Suite. Das ist der Preis dafür, dass die '
                 'gebuchte Startmasse hält.</td></tr>')
    B.append('</table></div>')

    B.append('<h3>Kenngrössen</h3><div class="wrap"><table>')
    B.append(f'<tr><th>Startmasse (nass)</th><td class="n fett">{z(mb["nass"])} kg</td>'
             f'<th>gebuchter Anker</th><td class="n">{z(c["gebuchteStartmasse_kg"])} kg '
             f'<span class="ok">± 0,0000 %</span></td></tr>')
    B.append(f'<tr><th>Trockenmasse</th><td class="n">{z(mb["trocken"])} kg</td>'
             f'<th>Treibstoff</th><td class="n">{z(mb["treibstoff"])} kg ({s["engines"][0]["propType"]})</td></tr>')
    B.append(f'<tr><th>Triebwerke</th><td colspan="3">'
             + ' · '.join(f'{e["count"]} × {esc(e["name"])} ({e["simultaneous"]} gleichzeitig)'
                          for e in s["engines"]) + '</td></tr>')
    B.append(f'<tr><th>Isp</th><td class="n">{s["isp"]} s</td>'
             f'<th>Schub gleichzeitig</th><td class="n">{z(c["thrust_simultaneous_N"],3)} N</td></tr>')
    B.append(f'<tr><th>Δv gesamt</th><td class="n fett">{z(s["currentDeltaV"])} m/s</td>'
             f'<th>Manöverzeit</th><td class="n">{z(c["maneuverTime_s"]/3600,2)} h '
             f'({z(c["maneuverTime_s"]/86400,1)} d)</td></tr>')
    B.append(f'<tr><th>davon Manöverbudget</th><td class="n">{z(c["dv_manoever_kms"]*1000)} m/s</td>'
             f'<th>davon Bahnhaltung</th><td class="n">{z(max(c["dv_stationshaltung_kms"],0)*1000)} m/s</td></tr>')
    B.append(f'<tr><th>Kraftwerk</th><td class="n">{z(c["powerPlant"]["output_kw"],2)} kW solar, '
             f'α 15 kg/kW</td><th>Batterie</th><td class="n">{z(c["powerPlant"]["battery_kg"])} kg / '
             f'{z(c["powerPlant"]["battery_hours"],1)} h</td></tr>')
    B.append('</table></div>')

    B.append('<div class="wrap"><table><tr><th>Massenposten</th>'
             + ''.join(f'<th class="n">{h}</th>' for h in
                       ["Nutzlast","Bus","Triebw.","Kraftw.","PMAD","Batt.","Radiator","Tank","Struktur"])
             + '</tr><tr><td>kg</td>'
             + ''.join(f'<td class="n">{z(mb[x])}</td>' for x in
                       ["nutzlast","bus","triebwerke","kraftwerk","pmad","batterie","radiator","tank","struktur"])
             + '</tr></table></div>')

    B.append('<div class="wrap"><table><tr><th>Hüllkurve (20 reale Systeme)</th><th class="n">Wert</th>'
             '<th class="n">Spanne</th><th>Befund</th></tr>')
    for kk,(lbl,lo,hi) in HK.items():
        v=c["huellkurve"][kk]; drin = lo<=v<=hi
        B.append(f'<tr><td>{lbl}</td><td class="n">{z(v)} %</td><td class="n">{z(lo)}–{z(hi)} %</td>'
                 f'<td class="{"ok" if drin else "hm"}">'
                 f'{"in der Hüllkurve" if drin else "ausserhalb — siehe Befund"}</td></tr>')
    B.append('</table></div>')
    B.append(f'<p class="q">{esc(s["notes"])}</p></div>')

B.append('<div class="karte warn"><h2>Befunde</h2><div class="wrap"><table>'
 '<tr><th>Nr.</th><th>Befund</th></tr>'

 '<tr><td>B-1</td><td><b>Der Fehler der ersten Fassung.</b> Ich habe die Entwürfe in Modus&nbsp;A gebaut '
 'und damit K2 übersprungen. Modus&nbsp;A gilt nur für ein reales Schiff mit veröffentlichter Startmasse; '
 '<code>construction.md</code> knüpft die Ausnahme von Weight&nbsp;Penalty&nbsp;3 ausdrücklich an '
 '<code>designMode:&nbsp;"reconstruction"</code> und schliesst mit «Ohne diese Deklaration gilt der '
 'Normalfall». Diese drei haben kein reales Vorbild. Alles neu gerechnet.</td></tr>'

 '<tr><td>B-2</td><td><b>Himmelsauge und Feldzeichen halten ihre 2&nbsp;t nur bei np&nbsp;=&nbsp;0.</b> '
 'Das heisst: <b>keine Vorteile, drei Nachteile.</b> Bei voller Penalty (np&nbsp;=&nbsp;3, nichts geheilt) '
 'wäre die Nutzlast 9&nbsp;000&nbsp;kg statt 1&nbsp;000&nbsp;kg — neunfach, das Schiff läge weit jenseits '
 'von 2&nbsp;t. Die gebuchte Masse ist also nur zu halten, wenn beide Satelliten ungehärtet, '
 'doktrinär gebunden und einmalverwendbar sind. Das ist kein Rechentrick, sondern eine Aussage über die '
 'Schiffe: China hat billige Wegwerfsatelliten im Orbit, keine gehärteten.</td></tr>'

 '<tr><td>B-3</td><td><b>Der Scorer ist mit Monergol nicht baubar.</b> Mit Hydrazin (Isp&nbsp;230, '
 'Shijian-25-Anker) kommt er auf 2&nbsp;157,7&nbsp;kg — <b>+157,7&nbsp;kg (+7,9&nbsp;%)</b> über den '
 'gebuchten 2&nbsp;t, und das schon bei Busmasse&nbsp;null. Die Physik erzwingt den lagerfähigen '
 '<b>Bipropellant MMH/NTO bei Isp&nbsp;315</b> (490&nbsp;N Haupttriebwerk, Shijian-21/TJS-Anker, dazu '
 '4&nbsp;×&nbsp;22&nbsp;N Lageregelung). Damit: 1&nbsp;446,9&nbsp;kg trocken + 553,1&nbsp;kg Treibstoff '
 '= genau 2&nbsp;000&nbsp;kg, 53,6&nbsp;kg Bus bleiben. Manöverzeit 0,83&nbsp;h statt 3,73&nbsp;h.</td></tr>'

 '<tr><td>B-4</td><td><b>Die Himmelsbrücke verträgt die volle Härtung.</b> Als einziger der drei bleibt sie '
 'auch mit drei Vorteilen unter dem Anker: np&nbsp;=&nbsp;6, cm&nbsp;6, Hochenergie&nbsp;×3, also '
 '<b>Faktor&nbsp;18</b> auf die Basisnutzlast — 150&nbsp;kg werden zu 2&nbsp;700&nbsp;kg, und die '
 '5&nbsp;t halten mit 594,6&nbsp;kg Bus. Sie ist damit das einzige strahlungs­gehärtete, thermisch und '
 'magnetisch ausgelegte chinesische Bahnobjekt.</td></tr>'

 '<tr><td>B-5</td><td><b>Δv war nicht getrackt — jetzt gebucht.</b> Alle fünf Scorer standen nach Zug&nbsp;5 '
 'weiterhin auf <code>dv_kms&nbsp;1.0</code>, obwohl <code>scoring.md</code> 1&nbsp;km/s je Versuch '
 'berechnet und alle fünf gescort haben. Abgeschrieben auf <b>0,0&nbsp;km/s</b>, Status '
 '<code>verbraucht</code>. <b>Folge für Zug&nbsp;6:</b> die fünf Scorer können nicht mehr scoren. Da sie '
 'jetzt zusätzlich den Nachteil «Single-Use» tragen, sind sie auch nicht betankbar — China muss für '
 'Zug&nbsp;6 neu starten, wenn es die Zonen halten will.</td></tr>'

 '<tr><td>B-6</td><td><b>Zwei Hüllkurvenausreisser bleiben, benannt statt wegretuschiert.</b> '
 '<i>trocken/nass</i> liegt bei Himmelsauge (97,8&nbsp;%) und Himmelsbrücke (95,3&nbsp;%) über der Spanne '
 '40,2–93,3&nbsp;%: kein Referenzsystem trägt so wenig Δv, das sparsamste ist SPADEX mit 150&nbsp;m/s bei '
 '93,3&nbsp;%. Beim Feldzeichen liegt <i>Nutzlast/trocken</i> bei 69,1&nbsp;% statt 6,8–58,2&nbsp;%, weil '
 'der 1‑t‑Rahmen im Katalog des Spiels ein <i>Nutzlastposten</i> ist (<code>comps shipframe</code>) und '
 'nicht Struktur; als (Rahmen+Bus)/trocken gemessen sind es 72,8&nbsp;% und damit innerhalb.</td></tr>'

 '<tr><td>B-7</td><td><b>REGELLÜCKE (unverändert):</b> Für passive Aufklärung gibt es kein Vorteils-Preset; '
 'alle vier Sensor-Suites sind aktiv. Beim Himmelsauge ist das jetzt konsequent aufgelöst — es trägt gar '
 'keinen Vorteil, dafür den Nachteil «Hoher EM-Abdruck», der zu einem aktiven Grossapertur-Sensor auch '
 'sachlich passt.</td></tr>'

 '<tr><td>B-8</td><td><b>Modellierungsvorbehalt, offengelegt.</b> «Struktur 1&nbsp;t» und «Sensor 1&nbsp;t» '
 'lese ich als die Katalogposten <code>comps shipframe</code> (1&nbsp;000&nbsp;kg) und '
 '<code>comps sensor_geo «Sensor: to GEO»</code> (1&nbsp;000&nbsp;kg) — Wortlaut und Masse stimmen exakt. '
 'Beide gehen damit in die K2-Basis ein, und die Strukturabgabe K1 kommt obendrauf. Das ist die '
 'konservative Lesart; wer den Rahmen stattdessen als Struktur führt, bekommt leichtere Schiffe. '
 'Entscheidung des Tisches.</td></tr>'
 '</table></div></div>')

B.append('<p class="q">Rechenweg: <code>Ships/konstruktion_chn_modusB.py</code> (Penaltykette und Löser) · '
 '<code>Ships/export_chn.py</code> (ship_export) · <code>Ships/stats_html.py</code> (dieses Blatt). '
 'Massenmodell aus OW-01 <code>scripts/nachbau.py</code>, gegen 32 reale Orbitalsysteme geprüft. '
 'Vertraulich wie jedes Befehlsblatt.</p>')

open("Ships/CHN_Raumfahrzeuge_Stats.html","w").write("\n".join(B))
print("-> Ships/CHN_Raumfahrzeuge_Stats.html")
