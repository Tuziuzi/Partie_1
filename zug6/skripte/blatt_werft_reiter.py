#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSBAUSTEIN — Reiter »PRIVATWERK & WERFT« (PW-01, BZ-01 Rev. B, Forschung Rev. D).

Drei Regeln haben sich am 19.09.2026 geaendert und bilden sich auf keinem
bisherigen Blatt ab:

  PW-01 »PRIVATWERK« v1.0   — neues Modul. Privater Startsektor als eigenes
                              Konto, Regulierungsleiter RG0-RG3, staatliche
                              Bestellung, Vorrangleiter in Phase 2.
  BZ-01 »WERKBUCH« Rev. B   — Werftdurchsatz mit Massebasis, dazu ein zweiter
                              Term: gebaute Fertigungslinien, gedeckelt auf
                              0,50 x Startkapazitaet.
  Forschung Rev. D          — Weltuhr statt Timeline. 2031 traegt KEINE Ration.

Feldnamen: pw_rg, pw_best_gut, pw_best_masse, bz_linie_nennrate,
bz_linie_design, bz_linie_tempo. Sie reisen ueber werte() als blatt.felder.*
mit, wie jedes andere f_-Feld.

Aufruf: python3 blatt_werft_reiter.py <datei.html> [...]
"""
import json, os, re, sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GS = json.load(open(os.path.join(W, "stand", "gamestate.json"), encoding="utf-8"))

RG = [("PW-01:RG0", "laissez-faire",
       "nur militaerischer Vorrang; staatlich-zivil verdraengt nicht; "
       "Bestellung zum Marktpreis", "x1,00"),
      ("PW-01:RG1", "Lizenz",
       "volle Vorrangleiter, die Lizenz kann verweigert werden; Bestellung von "
       "Guetern, die die Linie schon baut", "x1,00"),
      ("PW-01:RG2", "Lenkung",
       "zusaetzlich: Bestellung darf ein EIGENES Design vorschreiben "
       "(Serienzaehler x0,5); Preisregime hoechstens MK-01:PR2; automatisch "
       "bei Kriegswirtschaft", "x0,50"),
      ("PW-01:RG3", "Requisition",
       "je Zug wandern 25 % der privaten Kapazitaet in das eigene Werftkonto; "
       "Preis administriert; Hysterese wie C-9 §3.1", "0")]


def z(x, n=1):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def abschnitt(n, fid):
    f = GS["factions"][fid]
    p = f.get("private") or {}
    r = f["economy"]["resources"]
    launch = r["launch"]["capacity_t_year"]
    vortrag = r["launch"].get("restraum_vortrag_t", 0.0)
    werft = r["industrial"]["capacity_t_year"]
    staatl = p.get("_staatlich_verfuegbar_t_a", launch)
    deckel = 0.5 * launch
    demokratie = fid in ("USA", "EU", "IND")

    lin = "".join(
        f'<tr><td>{l["art"]}</td><td>{l["band"]}</td><td>{l["dienst"]}</td>'
        f'<td>{z(l["anteil_nachfrage"]*100, 0)} %</td>'
        f'<td>{("%s t" % z(l["stueck_masse_t"], 2)) if l.get("stueck_masse_t") else "—"}</td>'
        f'<td>{l.get("p_stufe") or "—"}</td></tr>' for l in p.get("linien", []))

    rgtab = "".join(
        f'<tr><td><b>{k}</b></td><td>{kurz}</td><td>{txt}</td><td>{w}</td></tr>'
        for k, kurz, txt, w in RG)
    rgopt = "".join(
        f'<option value="{k}"{" selected" if k == p.get("rg") else ""}>{k} — {kurz}</option>'
        for k, kurz, _, _ in RG)

    gueter = [("-", "— nichts bestellen —")] + [
        (l["art"], l["art"].replace("_", " ")) for l in p.get("linien", [])]
    gopt = "".join(f'<option value="{k}">{t}</option>' for k, t in gueter)

    rg3 = ('<div class="band rot"><b>RG3 ist in einer Demokratie nur mit '
           'Kriegswirtschaft zulaessig.</b>Und er kostet: Zufluss an die '
           'A-3 Audience Costs. Requisition ist kein Regler, den man '
           'ausprobiert.</div>' if demokratie else
           '<div class="band rot"><b>RG3 kostet auch den Autokraten.</b>'
           'Je Zug auf RG3 steigt Ihre Korruption um <b>&Delta;K +0,05</b> '
           '(A-6). Sie haben seit gestern einen K-Wert; er ist auf dem Reiter '
           '&raquo;Innenlage&laquo; gedruckt.</div>')

    return f'''<section class="blatt" id="blatt{n}"><style>
.wtab{{border-collapse:collapse;width:100%;margin-top:8px;font-size:13px}}
.wtab td,.wtab th{{border-bottom:1px solid var(--linie);padding:5px 6px;text-align:left}}
.wtab th{{color:var(--leise);font-weight:600;font-size:12px}}
.wtab td:nth-child(n+2){{color:var(--leise);font-size:12px}}
.wzahl{{display:flex;justify-content:space-between;gap:10px;padding:5px 0;
  border-bottom:1px solid var(--linie);font-size:13.5px}}
.wzahl b{{font-variant-numeric:tabular-nums;white-space:nowrap}}</style>
<div class="h"><div class="blattkopf"><div class="nr">BLATT {n} VON {n}</div>
<h2>PRIVATWERK &amp; WERFT</h2>
<div class="quelle">PW-01 v1.0 &middot; BZ-01 Rev. B &middot; Forschung Rev. D &middot; Hausblatt</div></div>

<div class="band rot"><b>Drei Regeln sind seit gestern neu.</b>Der private
Raumfahrtsektor ist ein eigenes Konto geworden, der Werftdurchsatz hat einen
zweiten Term bekommen, und die Forschung laeuft nicht mehr nach Zeitleiste,
sondern nach Weltuhr. Alles drei steht ab hier.</div>

<div class="abschn"><h3>PW-01 &mdash; Ihr Privatsektor</h3>
<div class="band ocker"><b>Der Privatsektor ist ein ANTEIL Ihrer
Startkapazit&auml;t, kein Zuschlag darauf.</b>Die Zahl, mit der Sie seit
Spielbeginn rechnen, enthielt ihn bereits &mdash; er wird jetzt nur sichtbar.
Wer beide Konten addiert, bekommt keinen schlechten Wurf, sondern eine
Unm&ouml;glichkeitsmeldung (Riegel PW-01:S1).</div>
<div class="wzahl"><span>Startkapazit&auml;t national</span><b>{z(launch)} t/a</b></div>
<div class="wzahl"><span>davon privat ({z(p.get("anteil_2026", 0)*100, 0)} %)</span><b>{z(p.get("capacity_t_year", 0))} t/a</b></div>
<div class="wzahl"><span>staatlich verf&uuml;gbar</span><b>{z(staatl)} t/a</b></div>
<div class="wzahl"><span>Restraum-Vortrag aus dem Vorjahr</span><b>{z(vortrag)} t</b></div>
<div class="wzahl"><span>privates Lager</span><b>{z(p.get("stockpile_t", 0))} t</b></div>
<div class="wzahl"><span>Regulierungsstufe</span><b>{p.get("rg", "—")}</b></div>
<div class="fuss">Vorrang in Phase 2, feste Reihenfolge:
<b>milit&auml;risch &rarr; staatlich-zivil &rarr; Ihre Bestellung &rarr; privat
aus eigenem Antrieb</b>. Was verdr&auml;ngt wird, ist nicht verloren, sondern
gestreckt &mdash; und steht im SITREP als &raquo;verdr&auml;ngt&laquo;.</div>

<h4>Was Ihr Privatsektor selbst baut</h4>
<table class="wtab"><tr><th>Linie</th><th>Band</th><th>Dienst</th>
<th>Anteil</th><th>St&uuml;ck</th><th>Serie</th></tr>{lin}</table>

<h4>Regulierung</h4>
<table class="wtab"><tr><th>Stufe</th><th>kurz</th><th>Zugriff</th><th>Wachstum</th></tr>{rgtab}</table>
{rg3}
<label class="f"><span class="lab">Regulierungsstufe f&uuml;r diesen Zug</span>
<select id="f_pw_rg" data-unberuehrt="1">{rgopt}</select></label>
<div class="fuss">H&ouml;her hei&szlig;t mehr Zugriff und weniger Wachstum.
Kriegswirtschaft setzt RG2 von selbst.</div>

<h4>Bestellung beim Privatsektor</h4>
<div class="band gruen"><b>Der Vorteil ist die warme Linie.</b>Sie kaufen sich
in eine laufende Serie ein und rechnen mit dem <i>privaten</i> Serienz&auml;hler
statt mit Ihrem eigenen Werftdurchsatz. Gezahlt wird in %&nbsp;BIP.
Eine Bestellung gr&ouml;&szlig;er als {z(p.get("capacity_t_year", 0))} t/a wird
<b>abgewiesen</b>, nicht stillschweigend gestreckt.</div>
<label class="f"><span class="lab">Gut</span>
<select id="f_pw_best_gut" data-unberuehrt="1">{gopt}</select></label>
<label class="f"><span class="lab">Masse in Tonnen</span>
<input type="number" id="f_pw_best_masse" inputmode="decimal" step="0.1" min="0"
 value="" data-unberuehrt="1" aria-label="Bestellmasse"></label>
<div class="fuss">Ein bestelltes Kraftwerk erzeugt einen EH-01-Zubau auf dem
Tr&auml;ger <code>sbsp</code>.</div></div>

<div class="abschn"><h3>BZ-01 Rev. B &mdash; Ihre Werft</h3>
<div class="band blau"><b>Der Werftdurchsatz hat einen zweiten Term bekommen.</b>
Bisher war er allein an Ihre Startkapazit&auml;t gekoppelt. Neu: <b>gebaute
Fertigungslinien</b> z&auml;hlen dazu &mdash; bis zu einem Deckel von
0,50&nbsp;&times;&nbsp;Startkapazit&auml;t.</div>
<div class="wzahl"><span>Werftdurchsatz heute</span><b>{z(werft)} t/a</b></div>
<div class="wzahl"><span>davon aus Linien</span><b>0,0 t/a</b></div>
<div class="wzahl"><span>Deckel D (0,50 &times; Start)</span><b>{z(deckel)} t/a</b></div>
<div class="fuss">Kapitalkosten einer Linie = Nennrate &times; Kaufladenpreis je
Tonne &times; 1 Jahr. Hochlauf <b>10 &middot; 40 &middot; 80 &middot; 100 %</b>
&uuml;ber vier Z&uuml;ge; im beschleunigten Bau das Doppelte an Kapital und
40&nbsp;/&nbsp;100&nbsp;% in zwei Z&uuml;gen. Eine Linie setzt ein
unbesch&auml;digtes Bodensegment (E-5) voraus.</div>
<label class="f"><span class="lab">Neue Linie: Nennrate in t/a (leer = keine)</span>
<input type="number" id="f_bz_linie_nennrate" inputmode="decimal" step="1" min="0"
 value="" data-unberuehrt="1" aria-label="Nennrate"></label>
<label class="f"><span class="lab">Wof&uuml;r? (Entwurf oder Klasse)</span>
<input type="text" id="f_bz_linie_design" value="" data-unberuehrt="1"
 placeholder="z. B. Feldzeichen-Klasse" aria-label="Design der Linie"></label>
<label class="f"><span class="lab">Tempo</span>
<select id="f_bz_linie_tempo" data-unberuehrt="1">
<option value="normal" selected>normal (10/40/80/100 % in vier Z&uuml;gen)</option>
<option value="beschleunigt">beschleunigt (Kapital &times;2, 40/100 % in zwei Z&uuml;gen)</option>
</select></label></div>

<div class="abschn"><h3>Forschung Rev. D &mdash; die Weltuhr</h3>
<div class="band viol"><b>Es gibt kein Forschungsbudget mehr.</b>Geld kauft
Schiffe, Startmasse und Kriegswirtschaft &mdash; keine Technologien. Jede
Fraktion hat <b>pro Jahr genau eine Ration</b>: einen Wurf auf einer Stufe
eigener Wahl. Nicht ansparbar, nicht &uuml;bertragbar.</div>
<table class="wtab"><tr><th>Jahr</th><th>Ration</th><th>Stufen</th></tr>
<tr><td>bis 2029</td><td>&mdash;</td><td>keine</td></tr>
<tr><td><b>2030</b></td><td><b>einmalig eine</b></td><td>L1</td></tr>
<tr><td><b>2031&ndash;2034</b></td><td><b>&mdash;</b></td><td><b>keine</b></td></tr>
<tr><td>ab 2035</td><td>j&auml;hrlich eine</td><td>L1</td></tr>
<tr><td>ab 2046</td><td>j&auml;hrlich eine</td><td>L1 &middot; L2</td></tr>
<tr><td>ab 2058</td><td>j&auml;hrlich eine</td><td>L1 &middot; L2 &middot; L3 &middot; Anything Goes</td></tr></table>
<div class="band ocker"><b>2031 tr&auml;gt keine Ration.</b>Dieser Zug hat kein
Forschungsfeld, und das ist kein Versehen: die L&uuml;cke 2031&ndash;2034 ist
Teil der Regel. Was Sie in diesem Zug tun k&ouml;nnen, ist einen
<b>Vorbescheid</b> beantragen &mdash; im Freitext beschreiben, was Sie ab 2035
erforschen wollen; der GM stuft es vorab ein. Das kostet nichts und bindet
nichts.</div>
<div class="fuss"><b>Technologie oder Werftauftrag?</b> &Auml;ndert es die
Baukastenliste, ist es eine Technologie. Ist es ein Teil daraus &mdash; ein
neuer Schiffstyp, ein besser gepanzertes Schiff &mdash;, ist es ein
Werftauftrag: ohne Wurf, ohne Ration, gleich zu bestellen.</div></div>
</div></section>'''


def patch(pfad):
    s = open(pfad, encoding="utf-8").read()
    if "PRIVATWERK &amp; WERFT</h2>" in s or "PRIVATWERK & WERFT</h2>" in s:
        print(f"  {os.path.basename(pfad)}: Reiter ist schon da."); return False
    m = re.search(r'"fraktion"\s*:\s*"([A-Z]+)"', s)
    if not m or m.group(1) not in GS["factions"]:
        print(f"  {os.path.basename(pfad)}: Fraktion nicht erkannt."); return False
    vor = sorted(int(x) for x in re.findall(r'<section class="blatt" id="blatt(\d+)"', s))
    if not vor or "</div></nav>" not in s:
        print(f"  {os.path.basename(pfad)}: Rahmen unbekannt."); return False
    n = vor[-1] + 1
    s = s.replace("</div></nav>",
                  f'<a href="#blatt{n}"><span>{n} &nbsp;<b>Werft</b></span></a>\n</div></nav>', 1)
    i = s.rfind("</section>")
    s = s[:i + 10] + abschnitt(n, m.group(1)) + s[i + 10:]
    s = re.sub(r"(BLATT \d+ VON )\d+", lambda x: x.group(1) + str(n), s)
    open(pfad, "w", encoding="utf-8").write(s)
    print(f"  {os.path.basename(pfad)}: Reiter {n} »Werft« ({m.group(1)}) eingefuegt.")
    return True


if __name__ == "__main__":
    print(f"{sum(patch(p) for p in sys.argv[1:])} Datei(en) ergaenzt.")
