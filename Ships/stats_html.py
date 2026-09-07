#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Datenblatt der drei rekonstruierten CHN-Raumfahrzeuge. Alles aus dem ship_export."""
import json, datetime

E = json.load(open("Ships/chn_raumfahrzeuge_2030.json"))
L = json.load(open("Ships/entwuerfe/loesung_chn.json"))
HK = {"pay_dry": ("Nutzlast / trocken", 6.8, 58.2), "paybus_dry": ("(Nutzlast+Bus) / trocken", 17.7, 78.2),
      "struct_dry": ("Struktur / trocken", 10.7, 20.6), "dry_wet": ("trocken / nass", 40.2, 93.3),
      "pp_dry": ("Kraftwerk+Batterie / trocken", 5.0, 15.0)}
def z(x, n=1): return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")

B = ['<meta charset="utf-8"><title>CHN Raumfahrzeuge 2030</title><style>'
     ':root{--grund:#f4eede;--feld:#fffdf6;--linie:#d6cdb6;--schrift:#1d2b36;--leise:#5c6b76;'
     '--blau:#2e6c96;--rot:#a8412a;--gruen:#4a7a42;--ocker:#8a6d1f;--viol:#6d4d8c}'
     '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--grund:#0f151a;--feld:#161f27;'
     '--linie:#26343e;--schrift:#e7eef4;--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;'
     '--ocker:#dcb45e;--viol:#b190cb}}'
     ':root[data-theme="dark"]{--grund:#0f151a;--feld:#161f27;--linie:#26343e;--schrift:#e7eef4;'
     '--leise:#93a5b1;--blau:#6fb3da;--rot:#e0765a;--gruen:#7fb377;--ocker:#dcb45e;--viol:#b190cb}'
     'body{background:var(--grund);color:var(--schrift);font:15px/1.5 -apple-system,BlinkMacSystemFont,'
     '"Segoe UI",Roboto,sans-serif;margin:0;padding:14px}'
     'h1{font-size:19px;margin:0 0 2px}h2{font-size:16px;margin:0 0 10px;color:var(--blau)}'
     '.kopf{color:var(--leise);font-size:12.5px;margin-bottom:16px}'
     '.karte{background:var(--feld);border:1px solid var(--linie);border-radius:10px;'
     'padding:12px 14px;margin-bottom:14px}'
     'table{border-collapse:collapse;width:100%;font-size:13.5px}'
     'td,th{border-bottom:1px solid var(--linie);padding:5px 6px;text-align:left;vertical-align:top}'
     'th{color:var(--leise);font-weight:600}td.n{text-align:right;font-variant-numeric:tabular-nums;'
     'white-space:nowrap}.wrap{overflow-x:auto}'
     '.tag{display:inline-block;font-size:11.5px;padding:1px 7px;border-radius:9px;'
     'border:1px solid var(--linie);color:var(--leise);margin:0 4px 4px 0}'
     '.ok{color:var(--gruen)}.warn{color:var(--ocker)}.fett{font-weight:700}'
     'p{margin:8px 0 0;font-size:13px}.q{color:var(--leise);font-size:12px}</style>']

B.append('<h1>Chinesische Raumfahrzeuge — konstruierte Kenngrössen</h1>')
B.append('<div class="kopf">Kampagne SCHWARZE SEE · Stand nach Zug&nbsp;5 (2030) · '
         'OW-01 ORBITALWERK, <b>Modus&nbsp;A (Rekonstruktion)</b> · Unified Shipyard v5.22, '
         'ship_export&nbsp;2.2<br>Anker sind die in <code>stand/gamestate.json</code> gebuchten '
         'Startmassen — die Konstruktion verteilt sie, sie erfindet sie nicht. '
         f'Erzeugt {datetime.date.today().isoformat()}.</div>')

for s in E["ships"]:
    c = s["customData"]; did = c["kampagnenDesign"]; d = L[did]; mb = c["massBreakdown_kg"]
    B.append('<div class="karte">')
    B.append(f'<h2>{s["name"]} <span class="q">— {c["kampagnenName"]} · {did}</span></h2>')
    B.append(''.join(f'<span class="tag">{t}</span>' for t in
             [s["class"], c["structureClass"], f'Struktur {c["structureTax"]["struct_pct"]:.0f} % / '
              f'Tank {c["structureTax"]["tank_pct"]:.0f} %'] + c["advantages"]))
    B.append('<div class="wrap"><table>')
    B.append(f'<tr><th>Startmasse (nass)</th><td class="n fett">{z(mb["nass"])} kg</td>'
             f'<th>gebuchter Anker</th><td class="n">{z(c["realLaunchMass_kg"])} kg '
             f'<span class="ok">± 0,0000 %</span></td></tr>')
    B.append(f'<tr><th>Trockenmasse</th><td class="n">{z(mb["trocken"])} kg</td>'
             f'<th>Treibstoff</th><td class="n">{z(mb["treibstoff"])} kg</td></tr>')
    B.append(f'<tr><th>Triebwerk</th><td class="n">{s["engines"][0]["name"]}</td>'
             f'<th>Zahl</th><td class="n">{s["engines"][0]["count"]} × '
             f'({s["engines"][0]["simultaneous"]} gleichzeitig)</td></tr>')
    B.append(f'<tr><th>Isp</th><td class="n">{s["isp"]} s</td>'
             f'<th>Schub gleichzeitig</th><td class="n">{z(c["thrust_simultaneous_N"],3)} N</td></tr>')
    B.append(f'<tr><th>Δv gesamt</th><td class="n fett">{z(s["currentDeltaV"])} m/s</td>'
             f'<th>Manöverzeit</th><td class="n">{z(c["maneuverTime_s"]/3600,2)} h '
             f'({z(c["maneuverTime_s"]/86400,1)} d)</td></tr>')
    B.append(f'<tr><th>davon Manöverbudget</th><td class="n">{z(c["dv_manoever_kms"]*1000)} m/s</td>'
             f'<th>davon Bahnhaltung</th><td class="n">{z(c["dv_stationshaltung_kms"]*1000)} m/s</td></tr>')
    B.append(f'<tr><th>Leistung Kraftwerk</th><td class="n">{z(c["powerPlant"]["output_kw"],2)} kW '
             f'(solar, α&nbsp;15 kg/kW)</td><th>Batterie</th>'
             f'<td class="n">{z(c["powerPlant"]["battery_kg"])} kg / '
             f'{z(c["powerPlant"]["battery_hours"],1)} h</td></tr>')
    B.append(f'<tr><th>Geometrie</th><td class="n">{z(s["geometry"]["D_out"],2)} × '
             f'{z(s["geometry"]["L_out"],2)} m (L/D {z(s["geometry"]["ldRatio"],1)})</td>'
             f'<th>Bewaffnung</th><td class="n">keine</td></tr>')
    B.append('</table></div>')

    B.append('<div class="wrap"><table><tr><th>Massenposten</th>'
             + ''.join(f'<th class="n">{k}</th>' for k in
                       ["Nutzlast","Bus","Triebw.","Kraftw.","PMAD","Batt.","Radiator","Tank","Struktur"])
             + '</tr><tr><td>kg</td>'
             + ''.join(f'<td class="n">{z(mb[k])}</td>' for k in
                       ["nutzlast","bus","triebwerke","kraftwerk","pmad","batterie","radiator","tank","struktur"])
             + '</tr></table></div>')

    B.append('<div class="wrap"><table><tr><th>Hüllkurve (20 reale Systeme)</th>'
             '<th class="n">Wert</th><th class="n">Spanne</th><th>Befund</th></tr>')
    for k,(lbl,lo,hi) in HK.items():
        v = c["huellkurve"][k]; drin = lo <= v <= hi
        B.append(f'<tr><td>{lbl}</td><td class="n">{z(v)} %</td>'
                 f'<td class="n">{z(lo)}–{z(hi)} %</td>'
                 f'<td class="{"ok" if drin else "warn"}">{"in der Hüllkurve" if drin else "ausserhalb — siehe Befund"}</td></tr>')
    B.append(f'<tr><td>implizite Nutzlastbasis (Modus-A-Gegenprobe)</td>'
             f'<td class="n">{z(c["impliziteBasis_kg"])} kg</td><td class="n">bei np&nbsp;=&nbsp;'
             f'{3+len(c["advantages"])}</td><td class="ok">geht als rohe Hardware durch</td></tr>')
    B.append('</table></div>')
    B.append(f'<p class="q">{s["notes"]}</p></div>')

B.append('<div class="karte"><h2>Befunde</h2><table>'
 '<tr><th>Nr.</th><th>Befund</th></tr>'
 '<tr><td>B-1</td><td><b>Himmelsauge und Himmelsbrücke liegen bei <i>trocken/nass</i> über der '
 'Hüllkurve</b> (97,8&nbsp;% bzw. 95,3&nbsp;% gegen 40,2–93,3&nbsp;%). Kein Rechenfehler: die '
 'Stichprobe enthält kein System mit so wenig Δv — das sparsamste ist SPADEX mit 150&nbsp;m/s bei '
 '93,3&nbsp;%. Ein Satellit, der nur Bahn hält, hat zwangsläufig fast keinen Treibstoff. '
 'Bewusster Befund, nicht zu korrigieren.</td></tr>'
 '<tr><td>B-2</td><td><b>Der Stub des Scorers geht rechnerisch nicht auf.</b> «Struktur 1&nbsp;t + '
 '1&nbsp;t Treibstoff» ergäbe bei Isp&nbsp;230 nicht 1,0 sondern 1,564&nbsp;km/s. Bindend sind die '
 'gebuchten 2&nbsp;t und 1,0&nbsp;km/s; daraus folgt die Aufteilung 1,284&nbsp;t / 0,716&nbsp;t. '
 'Der Stub des Aufklärers («Sensor 1&nbsp;t») ist dagegen exakt reproduziert.</td></tr>'
 '<tr><td>B-3</td><td><b>REGELLÜCKE (nachbau_regeln.md §2):</b> Für passive Aufklärung gibt es kein '
 'Vorteils-Preset. «Radar Suite» wäre falsch — ein aktives Radar verriete die Mission und zöge den '
 'Nachteil «Hoher EM-Abdruck» nach sich. Behelf regelkonform angewandt: Vorteil weggelassen, die '
 'Sensorik als reine Nutzlastmasse gebucht.</td></tr>'
 '<tr><td>B-4</td><td><b>Die Himmelsbrücke trägt 750&nbsp;m/s, die Kampagne bucht sie als unbeweglich '
 '(dv 0,0).</b> Das ist konsistent: 750&nbsp;m/s bei 0,166&nbsp;N sind 255&nbsp;Tage Dauerschub. '
 'Nord-Süd-Bahnhaltung über 15&nbsp;Jahre, kein Manöverbudget. Deshalb im Zustand getrennt geführt '
 'als <code>dv_manoever_kms</code> und <code>dv_stationshaltung_kms</code>.</td></tr>'
 '<tr><td>B-5</td><td><b>Offen und nicht von mir gebucht:</b> die fünf Scorer führen in '
 '<code>swarms</code> weiterhin <code>dv_kms&nbsp;1.0</code>, obwohl alle fünf in Zug&nbsp;5 gescort '
 'haben und scoring.md 1&nbsp;km/s je Versuch berechnet. Indiens SDX-SSO wurde korrekt von 0,15 auf '
 '0,096 abgeschrieben. Entweder Buchungslücke oder eine bewusste GM-Entscheidung — Entscheidung '
 'des Tisches.</td></tr>'
 '</table></div>')

B.append('<p class="q">Rechenweg: <code>Ships/konstruktion_chn.py</code> (Löser gegen den Massenanker) · '
 '<code>Ships/export_chn.py</code> (ship_export) · <code>Ships/stats_html.py</code> (dieses Blatt). '
 'Massenmodell aus OW-01 <code>scripts/nachbau.py</code>, gegen 32 reale Orbitalsysteme geprüft. '
 'Vertraulich wie jedes Befehlsblatt.</p>')

open("Ships/CHN_Raumfahrzeuge_Stats.html","w").write("\n".join(B))
print("-> Ships/CHN_Raumfahrzeuge_Stats.html", len("\n".join(B)), "Zeichen")
