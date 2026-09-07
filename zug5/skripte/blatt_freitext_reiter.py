#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSBAUSTEIN — fuenfter Reiter »FREITEXT« fuer das HTML-Befehlsblatt.

Der Erzeuger baut vier Reiter (1 Politik · 2 Energie · 3 Boden · 4 Rechnen).
Der Tisch will einen fuenften: EIN Freitextfeld fuer den GANZEN Zug — das,
was die Spieler bisher als Word-Dokument nebenher geschickt haben (Romans
»Entscheidungen von Europa fuer Zug 5«, Jakobs »Zug 5 Indien«).

WARUM DAS OHNE JAVASCRIPT GEHT: Die Exportfunktion werte() sammelt woertlich
    $$("[id^=f_]").forEach(function (el) { var name = el.id.slice(2); ... })
also JEDES Element, dessen id mit f_ beginnt. Ein neues <textarea id="f_freitext">
landet damit von selbst unter blatt.felder.freitext im Kopierblock, und
zh01_blattlesen.py liest es ueber lies_kopie() -> blatt["felder"] mit ein.
Kein Eingriff in die Skriptdatei, keine zweite Codestelle.

ABGRENZUNG (Z-8.2, drei Dokumente, drei Leserkreise):
  BLATT           Zahlen, an den GM — bei Demokratien im Folgezug oeffentlich
  GEHEIMSCHREIBEN Freitext, NUR der GM, nie veroeffentlicht
  MEMORANDUM      gemeinsam ausgearbeitet, alle kennen es
Dieser Reiter gehoert zum BLATT. Er ist der OFFENE Freitext. Was verdeckt
bleiben soll, gehoert weiterhin ins Geheimschreiben auf Blatt 3 — der Reiter
sagt das dem Spieler auch.

Aufruf: python3 blatt_freitext_reiter.py <datei.html> [...]
"""
import sys, re

def nav_neu(n):
    return ('<a href="#blatt%d"><span>%d &nbsp;<b>Freitext</b></span></a>\n</div></nav>' % (n, n))

ABSCHNITT = '''
<section class="blatt" id="blatt{n}"><div class="h"><div class="blattkopf">\
<div class="nr">BLATT {n} VON {n}</div><h2>FREITEXT</h2>\
<div class="quelle">Hausblatt · ein Feld fuer den ganzen Zug</div></div>\
<div class="band gruen"><b>Hier steht, was in kein Feld passt.</b>Absichten, \
Begruendungen, Absprachen, Bedingungen, Reden, Drohungen, alles, was die Zahlen \
auf den Blaettern 1 bis 4 nicht ausdruecken. Der Text reist mit dem Knopf \
&raquo;Zug kopieren&laquo; als <code>felder.freitext</code> mit und wird vom \
Leser unveraendert uebernommen &mdash; der GM kuerzt ihn nicht.</div>\
<div class="band blau"><b>Vertraulich wie das ganze Blatt.</b>Dieser Text geht an den GM und an niemanden sonst. Kein Mitspieler liest ihn &mdash; SITREPs sind asymmetrisch, und was eine Fraktion nicht wissen kann, steht nicht darin.</div><div class="band rot"><b>Eines darf hier nicht stehen: Zahlen, die anderswo hingeh&ouml;ren.</b>Bei einer Demokratie werden im Folgezug die <i>Werte</i> des Blatts bekannt &mdash; die Summen, nicht die Absicht. Wer eine Ausgabe in den Freitext schreibt, statt sie in ihr Feld zu setzen, entzieht sie der Ver&ouml;ffentlichungspflicht. Genau das verhindert Z-8.2 mit dem Satz: <i>&raquo;die Summe wird bekannt, die Absicht nicht&laquo;</i>. Absichten, Begr&uuml;ndungen, Reden, Drohungen, Bedingungen &mdash; alles richtig hier. Zahlen geh&ouml;ren in ihre Felder.</div><div class="band gruen"><b>Wof&uuml;r dann noch das Geheimschreiben?</b>F&uuml;r den Fall, dass der Text auch <i>strukturell</i> getrennt reisen soll: es f&auml;hrt in einem eigenen Block mit eigenem Schema, nie im selben JSON wie die Blattwerte. Ein Unterschied im Transportweg, nicht in der Vertraulichkeit.</div><label class="f"><span class="lab">Freitext fuer den ganzen Zug &mdash; so lang Sie wollen</span>\
<textarea id="f_freitext" rows="26" placeholder="Was Sie in diesem Zug vorhaben und warum. \
Worauf Sie reagieren. Was Sie den anderen sagen und was Sie ihnen nicht sagen. \
Bedingungen (&raquo;falls X, dann Y&laquo;) bitte mit dem Zug nennen, in dem sie verfallen."></textarea></label>\
<div class="fuss">Leer lassen ist erlaubt &mdash; dann taucht das Feld im Kopierblock gar nicht auf.</div>\
</div></section>
'''

def patch(pfad):
    s = open(pfad, encoding="utf-8").read()
    # Wie viele Blaetter hat dieses Exemplar? Ohne DW-01 sind es nur drei.
    vorhanden = sorted(int(m) for m in re.findall(r'<section class="blatt" id="blatt(\d+)"', s))
    if not vorhanden:
        print(f"  {pfad}: keine Blattabschnitte gefunden — NICHT angefasst."); return False
    n = vorhanden[-1] + 1
    if f'id="blatt{n}"' in s or 'FREITEXT</h2>' in s:
        print(f"  {pfad}: Reiter ist schon da — nichts getan."); return False
    if "</div></nav>" not in s:
        print(f"  {pfad}: Rahmen unbekannt (kein </div></nav>) — NICHT angefasst."); return False
    s = s.replace("</div></nav>", nav_neu(n), 1)
    # Der Abschnitt kommt hinter das letzte </section> der Blattkette.
    i = s.rfind("</section>")
    s = s[:i + len("</section>")] + ABSCHNITT.replace("{n}", str(n)) + s[i + len("</section>"):]
    # Blattzaehler mitziehen: "BLATT n VON 4" -> "VON 5"
    s = re.sub(r"(BLATT \d+ VON )\d+", lambda m: m.group(1) + str(n), s)
    open(pfad, "w", encoding="utf-8").write(s)
    print(f"  {pfad}: Reiter {n} »Freitext« eingefuegt (textarea id=f_freitext).")
    return True

if __name__ == "__main__":
    n = sum(patch(p) for p in sys.argv[1:])
    print(f"{n} Datei(en) ergaenzt.")
