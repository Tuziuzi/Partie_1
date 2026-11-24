#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spielerbriefing Zug 6 (2031): ein gemeinsames Briefing und je Spieler ein
vertraulicher Nachtrag.

Jede Zahl kommt aus dem Stand (CLAUDE.md §3): gamestate.json und
erde01_state_schwarzesee.json. Das gemeinsame Briefing traegt KEINEN Wert, den
eine Fraktion ueber eine andere nicht wissen kann (CLAUDE.md §5) — es nennt
Regeln, Tischentscheidungen und den Ablauf. Eigene Lagen stehen nur im Nachtrag.

    python3 zug6/skripte/briefing_zug6.py

Schreibt nach zug6/briefing/:
  Briefing_Zug6.html                    Seite ohne Dokumentrahmen (Artifact-Quelle)
  Nachtrag_Zug6_<SPIELER>.html          eigenstaendige Dateien, vertraulich
"""
import html
import json
import os

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GS = os.path.join(W, "stand", "gamestate.json")
ERDE = os.path.join(W, "stand", "erde01_state_schwarzesee.json")
AUS = os.path.join(W, "zug6", "briefing")

SPIELER = [("CHN", "china", "ANDI_CHINA", "Andi", "China"),
           ("EU", "eu", "ROMAN_EU", "Roman", "EU"),
           ("IND", "indien", "JAKOB_INDIEN", "Jakob", "Indien")]
SCORING_KOSTEN = 1.0     # scoring.md »Grundregeln«: 1 km/s je Versuch


def z(x, n=1):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def e(s):
    return html.escape(str(s), quote=True)


STIL = """
<style>
/* Layout: eine Lesespalte, Klassifizierungsleiste oben, Nummern nur wo die Reihenfolge echt ist */
:root {
  --papier: #F2F4F3; --karte: #FFFFFF; --tinte: #17202A; --grau: #56616B; --linie: #D3D9DC;
  --akzent: #22456A; --gilt: #1D6646; --gilt-bg: #E2F0E8; --nicht: #A3302B; --nicht-bg: #F6E3E1;
  --frage: #835600; --frage-bg: #F5ECD8;
  --display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --text: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --papier: #11161B; --karte: #182027; --tinte: #E5E9EC; --grau: #98A4AE; --linie: #29323A;
  --akzent: #8DB3DC; --gilt: #72CFA0; --gilt-bg: #15302A; --nicht: #F0897F; --nicht-bg: #3A1D1B;
  --frage: #E7B65C; --frage-bg: #33280F; color-scheme: dark; } }
:root[data-theme="dark"] {
  --papier: #11161B; --karte: #182027; --tinte: #E5E9EC; --grau: #98A4AE; --linie: #29323A;
  --akzent: #8DB3DC; --gilt: #72CFA0; --gilt-bg: #15302A; --nicht: #F0897F; --nicht-bg: #3A1D1B;
  --frage: #E7B65C; --frage-bg: #33280F; color-scheme: dark; }
body { background: var(--papier); color: var(--tinte); font-family: var(--text); font-size: 16px; line-height: 1.55; margin: 0; }
.rahmen { max-width: 44rem; margin: 0 auto; padding-block: 1.25rem 3rem;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 1.75rem; }
.leiste { font-family: var(--mono); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--grau); border-top: 3px solid var(--akzent); padding-top: .5rem; display: flex; flex-wrap: wrap; gap: .25rem 1rem; }
.leiste .vs { color: var(--nicht); font-weight: 600; }
h1 { font-family: var(--display); font-weight: 600; font-size: clamp(2rem, 7vw, 2.8rem); line-height: 1.05;
  margin: 0; letter-spacing: .01em; text-wrap: balance; }
.unter { color: var(--grau); margin: .35rem 0 0; }
h2 { font-family: var(--display); font-weight: 600; font-size: 1.45rem; line-height: 1.15; margin: 0 0 .6rem;
  letter-spacing: .02em; text-wrap: balance; }
h3 { font-size: 1rem; margin: 0 0 .35rem; }
p { margin: 0 0 .7rem; max-width: 65ch; }
p:last-child { margin-bottom: 0; }
section { display: flex; flex-direction: column; gap: .2rem; }
.kern { background: var(--karte); border: 1px solid var(--linie); border-radius: 6px; padding: 1.1rem 1.1rem 1.2rem; }
.paar { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin: .5rem 0 .9rem; }
@media (max-width: 560px) { .paar { grid-template-columns: 1fr; } }
.spalte { border-radius: 5px; padding: .8rem .9rem; min-width: 0; }
.spalte.gilt { background: var(--gilt-bg); }
.spalte.nicht { background: var(--nicht-bg); }
.spalte .kopf { font-family: var(--mono); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; font-weight: 600; margin-bottom: .4rem; }
.gilt .kopf { color: var(--gilt); } .nicht .kopf { color: var(--nicht); }
.spalte ul { margin: 0; padding-left: 1.1rem; display: flex; flex-direction: column; gap: .3rem; }
.folgen { width: 100%; border-collapse: collapse; font-size: .93rem; }
.folgen td { padding: .45rem .5rem; border-top: 1px solid var(--linie); vertical-align: top; }
.folgen td:first-child { white-space: nowrap; font-weight: 600; width: 1%; }
.marke { display: inline-block; font-family: var(--mono); font-size: .72rem; padding: .05rem .4rem; border-radius: 3px; letter-spacing: .04em; }
.m-gilt { background: var(--gilt-bg); color: var(--gilt); } .m-nicht { background: var(--nicht-bg); color: var(--nicht); }
.m-frage { background: var(--frage-bg); color: var(--frage); }
.liste { margin: 0; padding-left: 1.2rem; display: flex; flex-direction: column; gap: .55rem; }
.ref { font-family: var(--mono); font-size: .78rem; color: var(--grau); white-space: nowrap; }
.tabelle { overflow-x: auto; border: 1px solid var(--linie); border-radius: 6px; background: var(--karte); }
.tabelle table { border-collapse: collapse; width: 100%; font-size: .92rem; font-variant-numeric: tabular-nums; }
.tabelle th, .tabelle td { padding: .5rem .5rem; text-align: left; border-bottom: 1px solid var(--linie); white-space: nowrap; }
.tabelle th { font-family: var(--mono); font-size: .7rem; letter-spacing: .07em; text-transform: uppercase; color: var(--grau); font-weight: 500; }
.tabelle td.z { text-align: right; } .tabelle tr:last-child td { border-bottom: 0; }
.hinweis { border-left: 3px solid var(--frage); background: var(--frage-bg); padding: .7rem .85rem; border-radius: 0 5px 5px 0; }
.warnung { border-left: 3px solid var(--nicht); background: var(--nicht-bg); padding: .7rem .85rem; border-radius: 0 5px 5px 0; }
.fuss { font-size: .82rem; color: var(--grau); border-top: 1px solid var(--linie); padding-top: .8rem; }
code { font-family: var(--mono); font-size: .85em; }
a { color: var(--akzent); }
</style>
"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600'
         '&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&display=swap">')


# ------------------------------------------------------------------ Fakten
def fakten():
    g = json.load(open(GS, encoding="utf-8"))
    er = json.load(open(ERDE, encoding="utf-8"))
    buch = {b["fraktion"]: b for b in er["truth"]["buchungen"] if str(b.get("id", "")).startswith("Z6-A6NIVEAU-")}
    out = {"jahr": g["state"]["currentYear"], "runde": int(g["state"]["turnNumber"]) + 1,
           "warsWon": g["scoring"]["warsWon"], "f": {}}
    for kurz, staat, _sp, _n, _l in SPIELER:
        fr = g["factions"][kurz]
        assets = []
        for sid, s in (fr.get("swarms") or {}).items():
            assets.append({"name": sid, "art": "Eigenbau", "count": s.get("count"), "zone": s.get("zone"),
                           "dv": float(s.get("dv_kms") or 0.0), "status": s.get("status") or ""})
        for sid, s in (fr.get("realsatelliten") or {}).items():
            assets.append({"name": sid, "art": "Bestand", "count": s.get("count"), "zone": s.get("zone"),
                           "dv": float(s.get("delta_v_kms") or 0.0), "status": s.get("rolle") or ""})
        ind = fr["economy"]["resources"].get("industrial", {})
        b = buch.get(staat)
        bip = None
        if b:
            nach = er["truth"]["ressourcen"][staat]["bip_bio_usd"]
            bip = {"vor": round(nach - b["delta"], 4), "nach": nach, "delta": b["delta"],
                   "pct": er["module"]["erde01"]["daten"]["staaten"][staat]["korruption"]["niveau_abschlag_pct"]}
        bk = g["zeughaus"]["fraktionen"][kurz]["bodenkonto"]
        konto = {"alt": bk.get("zug6_t_vor_z6025", bk["zug6_t"]), "neu": bk["zug6_t"],
                 "tr_alt": bk.get("zug6_tranche_t_vor_z6025", bk["zug6_tranche_t"]), "tr_neu": bk["zug6_tranche_t"]}
        out["f"][kurz] = {
            "konto": konto,
            "assets": assets, "dv_max": max((a["dv"] for a in assets), default=0.0),
            "werft_t_a": ind.get("capacity_t_year"), "werft_frei_t": ind.get("available_t"),
            "lager_t": ind.get("stockpile_t"), "bip": bip,
            "completedL1": fr.get("research", {}).get("completedL1", []),
            "regel": er["module"]["erde01"]["daten"]["staaten"][staat]["korruption"]["aktive_regel"],
        }
    return out


# ------------------------------------------------------------------ Gemeinsames Briefing
def gemeinsam(F):
    return f"""<title>Briefing Zug 6</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}{STIL}
<main class="rahmen">
<header>
  <div class="leiste"><span>SCHWARZE SEE</span><span>Zug {F['runde']} · Jahr {F['jahr']}</span><span>Leserkreis: alle Spieler</span></div>
  <h1 style="margin-top:.8rem">Briefing Zug {F['runde']}</h1>
  <p class="unter">Für Andi (China), Roman (EU) und Jakob (Indien). Ihre neuen Befehlsblätter und ein vertraulicher Nachtrag zu Ihrer eigenen Lage kommen einzeln.</p>
</header>

<section>
  <h2>Wo wir stehen</h2>
  <p>Zug 5 (2030) ist gebucht. Zug {F['runde']} spielt das Jahr {F['jahr']}. Die Spielleitung arbeitet ab jetzt mit dem Regelstand vom 24.11.2026; Ihre Befehlsblätter sind damit neu erzeugt. Eine Neuerung betrifft jeden Satz, den Sie schreiben. Sie steht deshalb zuerst.</p>
</section>

<section class="kern">
  <h2>Neu: Befehle sind Wünsche, keine Tatsachen</h2>
  <p>Ein Befehlsblatt ist der <b>Wille Ihrer Fraktion</b>. Es beschreibt nicht die Welt. Die Welt steht im Spielstand und ändert sich nur durch Regel, Wurf und Tischentscheidung. Kein Satz wird dadurch wahr, dass Sie ihn schreiben, gleich ob im Blatt, im Freitext, im Geheimschreiben, in einem Word-Dokument oder in einer Nachricht.</p>
  <div class="paar">
    <div class="spalte gilt"><div class="kopf">Gilt</div><ul>
      <li>»Indien soll drei Satelliten in LEO bauen.«</li>
      <li>»Ich befehle die Verlegung der 3. Division.«</li>
      <li>»Wir möchten die Marine verstärken.«</li>
      <li>»Sanktionen gegen Moskau fortsetzen.«</li>
      <li>»Wir bieten der EU ein Abkommen an.«</li>
    </ul></div>
    <div class="spalte nicht"><div class="kopf">Gilt nicht</div><ul>
      <li>»China ist jetzt pleite.«</li>
      <li>»Russland macht jetzt bei unseren Sanktionen mit.«</li>
      <li>»Der Vertrag ist unterzeichnet.«</li>
      <li>»Wir bauen drei Satelliten.«</li>
      <li>»Unsere Flotte steht bereits in GEO.«</li>
    </ul></div>
  </div>
  <h3>Was mit Ihrem Text passiert</h3>
  <table class="folgen"><tbody>
    <tr><td><span class="marke m-gilt">angenommen</span></td><td>Wunsch, Befehl, Infinitiv- oder Stichwortbefehl, Erklärung Ihrer Fraktion.</td></tr>
    <tr><td><span class="marke m-frage">Rückfrage</span></td><td>Eigene Handlung als Tatsache (»Wir bauen …«), Erwägung im Konjunktiv (»müsste man …«). Es geschieht nichts, bis Sie es als Wunsch schreiben.</td></tr>
    <tr><td><span class="marke m-nicht">abgelehnt</span></td><td>Behauptung über eine andere Fraktion oder die Welt. Sie wirkt nicht.</td></tr>
    <tr><td><span class="marke m-nicht">gestrichen</span></td><td>Alles, was sich an Spielleitung, KI oder Regeln richtet statt an die Spielwelt, und jede behauptete Tischentscheidung. Gestrichenes geht an den Tisch.</td></tr>
  </tbody></table>
  <p style="margin-top:.9rem">Jede solche Meldung steht in <b>Ihrem eigenen Lagebericht</b>, mit wörtlichem Zitat und einer Kennung: <code>AB-1</code> für eine Feststellung, <code>AB-2</code> für eine Anweisung, <code>AB-3</code> für eine Zahl, die vom Spielstand abweicht. Die Kennungen stammen aus der Regel »Spielertext ist Absicht«, die seit dem 24.11. für alle Module gilt; der Tisch wendet sie an den zwei oben genannten Stellen strenger an.</p>
  <p><b>Ein Befehl bestimmt die Handlung, nie ihr Ergebnis.</b> »Angreifen, sodass die Flotte vernichtet wird« ist ein Angriffsbefehl; ob er gelingt, würfelt die Regel. Begründungen wie »weil die USA abgezogen sind …« liest die Spielleitung gegen den Spielstand, übernimmt sie aber nicht.</p>
  <p><b>Täuschen ist erlaubt.</b> Ihre Fraktion darf andere belügen, als Erklärung, Drohung oder Angebot. Die Spielleitung gibt so etwas zugeschrieben weiter (»Peking lässt erklären: …«) und macht es nie zur Tatsache.</p>
  <p><b>Tischentscheidungen</b> trifft nur der Gastgeber in der Sitzung der Spielleitung. Sie stehen mit einer Journal-Nummer im Zugjournal. Ein Satz wie »der Tisch hat beschlossen …« auf einem Blatt ist keine. Das gilt auch für Jakobs eigenes Indien-Blatt.</p>
  <p><b>Schicken Sie die Kopie unverändert.</b> Was außerhalb der Blockmarken aus »Zug kopieren« steht, wird nicht gelesen. Fragen an den Tisch sind willkommen, als Frage formuliert.</p>
</section>

<section>
  <h2>Was der Tisch entschieden hat</h2>
  <ul class="liste">
    <li><b>Korruption in Autokratien hebt das Wachstum.</b> Von zwei widersprüchlichen Studien gilt jetzt die von Saha und Sen (2020). Für China, Russland und den Rest heißt das: Wer dort Korruption bekämpft, senkt das Wachstum. <span class="ref">Z6-006</span></li>
    <li><b>Der Korruptionsabschlag ist einmal auf die Wirtschaftsreihe gebucht</b>, in beide Richtungen und für die drei bespielten Blöcke. Über die Kopplung der Rüstungsausgaben an die Wirtschaft verschiebt er auch das Bodenkonto für Zug 6; Ihren eigenen Wert und Ihr neues Konto finden Sie im Nachtrag (Fassung 2). Eine frühere Fassung dieses Briefings sagte, die Buchung wirke nicht; das war falsch. <span class="ref">Z6-005 · Z6-045</span></li>
    <li><b>Der fehlende Kaskadenwurf aus Zug 5 ist nachgeholt.</b> Kein Block ist ausgelöst worden. <span class="ref">Z6-011</span></li>
    <li><b>Die Forschungsration des Jahres 2030 wird in Zug 6 nachgeholt.</b> Jede Fraktion hat einen Wurf auf Stufe L1 (1W6, Erfolg ab 4). Wünschen Sie ihn auf dem Blatt; die Spielleitung stellt vor dem Wurf einen Vorbescheid aus. Techniken der Klasse K0 und K1 sind frei, K2 nur mit offenem Tor. <span class="ref">Z6-018</span></li>
  </ul>
</section>

<section>
  <h2>Was sich an den Regeln geändert hat</h2>
  <ul class="liste">
    <li><b>Forschung, Weltuhr Rev. E.</b> 2031 bis 2034 gibt es regulär keine Ration. Ab 2035 jährlich eine, wählbar L1 oder L2; L2 erst nach der neuen Reifeprüfung. L3 und »Anything Goes« öffnen sich nur nach einer abgeschlossenen und durchgedrungenen Singularität. Die frühere Zeile »ab 2058« ist gestrichen.</li>
    <li><b>Blatt 2 Energie</b> hat ein neues Feld: welche Verbrauchergruppe bei Stromknappheit zuletzt abgeregelt wird.</li>
    <li><b>Wärmebuch.</b> Raumschiffe führen Wärme jetzt als Zustand; neue Entwürfe tragen ihre Kühlkreise im Export.</li>
    <li><b>Neue Module</b> für Bündnisse, Kriegsende, Weltordnung, Staatsbau und Unruhe sind angedockt. In SCHWARZE SEE wirken sie erst, wenn der Tisch sie einschaltet.</li>
  </ul>
</section>

<section>
  <h2>Zur Erinnerung: Wertung im All</h2>
  <p>Jeder Wertungsversuch kostet {z(SCORING_KOSTEN)} km/s Delta-v. In jeder Zone außer der Erdoberfläche braucht er ein eigenes Raumfahrzeug, das diesen Betrag zu Zugbeginn noch im Tank hat. Wer kein solches Fahrzeug hat, bekommt für die Zone in diesem Zug keinen Punkt. Wie es um Ihre eigenen Fahrzeuge steht, steht im Nachtrag.</p>
</section>

<section>
  <h2>Ablauf Zug {F['runde']}</h2>
  <ol class="liste">
    <li>Befehlsblatt im Browser öffnen und ausfüllen. Befehle als Wunsch schreiben; die Kästen auf Blatt 1, beim Geheimschreiben und im Freitext zeigen wie.</li>
    <li>Knopf »Zug kopieren« drücken und den Text <b>unverändert</b> an Jakob schicken.</li>
    <li>Die Spielleitung prüft jede Kopie nach der Befehlsform und meldet Rückfragen zurück.</li>
    <li>Auflösung des Zugs. Danach bekommt jede Fraktion ihren eigenen Lagebericht.</li>
  </ol>
  <p style="margin-top:.6rem">Abgabe nach Ansage des Gastgebers.</p>
</section>

<footer class="fuss">SCHWARZE SEE · Delta V und ERDE-01 · Regelstand 24.11.2026 (Abend) · Zugjournal Zug 6, Einträge Z6-005 bis Z6-049. Befehlsblätter sind vertraulich gegenüber Mitspielern, einschließlich des Freitexts.</footer>
</main>
"""


# ------------------------------------------------------------------ Nachtrag je Spieler
def nachtrag(F, kurz, staat, spieler, name, land):
    f = F["f"][kurz]
    zeilen = []
    for a in sorted(f["assets"], key=lambda a: (-a["dv"], a["name"])):
        ok = a["dv"] >= SCORING_KOSTEN - 1e-9
        zeilen.append(
            f"<tr><td>{e(a['name'])}</td><td class='z'>{z(a['dv'], 3)}</td>"
            f"<td><span class='marke {'m-gilt' if ok else 'm-nicht'}'>{'ja' if ok else 'nein'}</span></td>"
            f"<td>{e(a['zone'])}</td><td class='z'>{e(a['count'])}</td></tr>")
    wertbar = f["dv_max"] >= SCORING_KOSTEN - 1e-9
    urteil = (f"<p>Mindestens ein Fahrzeug hat {z(SCORING_KOSTEN)} km/s im Tank und kann in Zug {F['runde']} eine Zone werten.</p>"
              if wertbar else
              f"<div class='warnung'><b>Kein eigenes Fahrzeug hat {z(SCORING_KOSTEN)} km/s im Tank.</b> Ihr höchstes Restbudget sind "
              f"{z(f['dv_max'], 3)} km/s. Ohne Betankung oder Neubau mit genug Delta-v kann {e(land)} in Zug {F['runde']} keine Zone im All werten. "
              f"Die Erdoberfläche braucht kein Fahrzeug.</div>")
    teile = []
    if kurz == "CHN":
        teile.append(
            "<section><h2>Ihre Wertungsflotte</h2>"
            "<p>Ihre fünf Scorer haben den Wertungsversuch aus Zug 5 bezahlt und stehen auf Restbudget null; der Status lautet "
            "»Treibstoff erschöpft«. Sie sind grundsätzlich betankbar, brauchen dafür aber einen Tanker. Ein Nachbau Ihrer Baumuster "
            "ist durch den Serienzähler günstiger als der Erstbau. Bauzeit und Werftkosten rechnet die Spielleitung auf Anfrage.</p></section>")
        teile.append(
            "<section><h2>Korruption und Wachstum</h2>"
            "<p>Unter der neuen Regel hebt Korruption in Autokratien das Wachstum. Für Sie heißt das konkret: Eine Antikorruptionskampagne "
            "auf Blatt 5 senkt Chinas Wachstum, statt es zu heben. Patronage, die Korruption mehrt, hebt es. Beides wirkt erst, wenn sich "
            "der Korruptionsstand ändert; solange Sie nichts tun, bleibt alles, wie es ist.</p></section>")
        teile.append(
            "<section><h2>Ihre Siegprämie aus Zug 5</h2>"
            "<div class='hinweis'><p><b>Korrektur zur ersten Fassung.</b> Ihre Siegprämie ist eingelöst: in Zug 5 als "
            "L1 »Küstenschutz« (Klimaanpassung, halbiert Chinas Grenzschaden aus der Erwärmung; Hausentscheidung des "
            "Tisches, Journal Z5-037). Die erste Fassung dieses Nachtrags sagte fälschlich, sie sei offen. Unabhängig davon "
            "haben Sie in Zug 6 die nachgeholte L1-Ration aus 2030.</p></div></section>")
    bip = f["bip"]
    if bip:
        if abs(bip["delta"]) < 1e-9:
            bt = (f"<p>Ihr Korruptionsstand liegt genau auf dem Bezugswert. Der einmalige Abschlag ist darum null; "
                  f"die Wirtschaftsreihe bleibt bei {z(bip['nach'], 4)} Billionen US-Dollar.</p>")
        else:
            bt = (f"<p>Der einmalige Korruptionsabschlag ist gebucht: {z(bip['pct'], 3)} % auf die Wirtschaftsreihe, von "
                  f"{z(bip['vor'], 4)} auf {z(bip['nach'], 4)} Billionen US-Dollar.</p>")
        k = f["konto"]
        if abs(k["neu"] - k["alt"]) < 1e-9:
            kt = (f"<p>Ihr Bodenkonto für Zug {F['runde']} bleibt bei {z(k['neu'])} t, die Hochtechnologie-Tranche bei "
                  f"{z(k['tr_neu'])} t.</p>")
        else:
            kt = (f"<p><b>Folge für Ihr Blatt 3:</b> Die Rüstungsausgaben hängen an der Wirtschaft. Ihr Bodenkonto für "
                  f"Zug {F['runde']} steigt damit von {z(k['alt'])} auf <b>{z(k['neu'])} t</b>, die Hochtechnologie-Tranche "
                  f"von {z(k['tr_alt'])} auf <b>{z(k['tr_neu'])} t</b>. Ihr Blatt zeigt noch die alten Werte. Ihre Anteile "
                  f"in Prozent gelten unverändert und werden mit dem neuen Konto gerechnet.</p>")
        teile.append("<section><h2>Wirtschaft</h2>" + bt + kt +
                     "<p class='ref'>Korrektur: Die erste Fassung dieses Nachtrags sagte, die Buchung wirke nicht auf das "
                     "Bodenkonto. Das war falsch (Journal Z6-045).</p></section>")
    teile.append(
        f"<section><h2>Werft und Forschung</h2>"
        f"<p>Ihre Werft leistet {z(f['werft_t_a'])} t im Jahr; für {F['jahr']} ist davon nichts gebunden. Im Lager liegen "
        f"{z(f['lager_t'])} t. Jeder Bauauftrag kostet Werftdurchsatz und wird ab diesem Zug gebucht.</p>"
        f"<p>Sie haben in Zug {F['runde']} einen Forschungswurf auf L1 (nachgeholte Ration 2030). Nennen Sie auf dem Blatt, welche "
        f"Fähigkeit Sie erforschen möchten; die Spielleitung stuft sie im Vorbescheid ein, bevor gewürfelt wird.</p></section>")

    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nachtrag Zug {F['runde']} {e(land)}</title>
{FONTS}{STIL}</head><body>
<main class="rahmen">
<header>
  <div class="leiste"><span class="vs">Vertraulich</span><span>Nur {e(name)} · {e(land)}</span><span>Zug {F['runde']} · Jahr {F['jahr']}</span><span>Fassung 2 · 25.11.2026</span></div>
  <h1 style="margin-top:.8rem">Nachtrag {e(land)}</h1>
  <p class="unter">Ihre eigene Lage zu Beginn von Zug {F['runde']}. Ergänzt das gemeinsame Briefing. Nicht an Mitspieler weitergeben.</p>
</header>
<section><h2>Ihre Fahrzeuge im All</h2>
<div class="tabelle"><table><thead><tr><th>Verband</th><th>Δv km/s</th><th>Wertbar</th><th>Zone</th><th>Anz.</th></tr></thead>
<tbody>{''.join(zeilen)}</tbody></table></div>
{urteil}</section>
{''.join(teile)}
<footer class="fuss">Alle Werte aus dem Spielstand vor Zug {F['runde']} (gamestate.json, erde01_state_schwarzesee.json), erzeugt von zug6/skripte/briefing_zug6.py. Befehle bitte als Wunsch formulieren, siehe gemeinsames Briefing.</footer>
</main></body></html>
"""


def main():
    F = fakten()
    os.makedirs(AUS, exist_ok=True)
    p = os.path.join(AUS, "Briefing_Zug6.html")
    open(p, "w", encoding="utf-8").write(gemeinsam(F))
    print("geschrieben:", os.path.relpath(p, W))
    for kurz, staat, spieler, name, land in SPIELER:
        p = os.path.join(AUS, f"Nachtrag_Zug6_{spieler}.html")
        open(p, "w", encoding="utf-8").write(nachtrag(F, kurz, staat, spieler, name, land))
        f = F["f"][kurz]
        print(f"geschrieben: {os.path.relpath(p, W)}  · dv_max {f['dv_max']} · Werft {f['werft_t_a']} t/a · BIP {f['bip']}")


if __name__ == "__main__":
    main()
