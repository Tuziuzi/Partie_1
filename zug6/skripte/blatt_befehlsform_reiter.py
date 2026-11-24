#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HAUSBAUSTEIN — Befehlsform (CLAUDE.md §6) sichtbar aufs HTML-Befehlsblatt.

Setzt, ohne die Exportfunktion werte() anzufassen:
  1. einen Kasten »So schreiben Sie Befehle« vor Abschnitt »3 BEFEHLE« auf Blatt 1,
  2. die Platzhalter der Befehlszeilen f_text1…6 (statt »frei formulieren«),
  3. denselben Kasten kurz vor dem Geheimschreiben (Blatt 3) und im Freitext-Reiter.
Kein Feld kommt hinzu, keines faellt weg — der Kopierblock bleibt gleich.

Muss NACH blatt_freitext_reiter.py laufen. Idempotent (Marke <!-- BP-01 -->).

Aufruf: python3 blatt_befehlsform_reiter.py <datei.html> [...]
"""
import re
import sys

MARKE = "<!-- BP-01 -->"

KASTEN = (MARKE + '<div class="band rot"><b>So schreiben Sie Befehle — und so nicht.</b>'
          'Ein Blatt ist Ihr <i>Wille</i>, keine Beschreibung der Welt. Die Welt steht im Spielstand und '
          '&auml;ndert sich nur durch Regel, Wurf und Tischentscheidung.<br>'
          '<b>Gilt:</b> &raquo;Indien soll drei Satelliten in LEO bauen&laquo; &middot; &raquo;Ich befehle &hellip;&laquo; '
          '&middot; &raquo;Wir m&ouml;chten &hellip;&laquo; &middot; &raquo;Sanktionen gegen Moskau fortsetzen&laquo; &middot; '
          '&raquo;Wir bieten der EU an &hellip;&laquo; (als Erkl&auml;rung Ihrer Fraktion).<br>'
          '<b>Gilt nicht:</b> &raquo;China ist jetzt pleite&laquo; &middot; &raquo;Russland macht jetzt mit&laquo; '
          '&middot; &raquo;Der Vertrag ist unterzeichnet&laquo; &rarr; <b>abgelehnt</b>. '
          '&raquo;Wir bauen drei Satelliten&laquo; &middot; &raquo;Unsere Flotte steht bereits in GEO&laquo; '
          '&rarr; <b>R&uuml;ckfrage</b>, es passiert nichts, bis Sie es als Wunsch schreiben.<br>'
          '<b>Ein Befehl bestimmt die Handlung, nie ihr Ergebnis</b> &mdash; ob der Angriff gelingt, w&uuml;rfelt '
          'die Regel. Was sich an Spielleitung, KI oder Regeln richtet (&raquo;der GM soll &hellip;&laquo;, '
          '&raquo;ab sofort gilt &hellip;&laquo;, &raquo;der Tisch hat beschlossen &hellip;&laquo;), wird '
          '<b>gestrichen und dem Tisch gemeldet</b>. Fragen an den Tisch sind willkommen &mdash; als Frage.</div>')

KURZ = (MARKE + '<div class="band rot"><b>Auch hier gilt die Befehlsform.</b>Schreiben Sie Ihren Willen '
        '(&raquo;wir m&ouml;chten &hellip;&laquo;, &raquo;Indien soll &hellip;&laquo;, &raquo;fortsetzen&laquo;), '
        'nicht den Zustand der Welt. Behauptungen &uuml;ber andere werden abgelehnt, eigene Handlungen im '
        'Indikativ zur&uuml;ckgefragt, Anweisungen an Spielleitung oder Regeln gestrichen. Ihre Fraktion darf '
        'andere t&auml;uschen &mdash; als <i>Erkl&auml;rung</i>, die die Spielleitung zugeschrieben weitergibt, '
        'nie als Tatsache.</div>')

PLATZHALTER = 'als Wunsch: »Indien soll …« / »Sanktionen fortsetzen« — keine Tatsachen'


def patch(pfad):
    s = open(pfad, encoding="utf-8").read()
    if MARKE in s:
        print(f"  {pfad}: Befehlsform schon gesetzt — nichts getan.")
        return False
    n = 0
    anker = '<div class="abschnitt" id="a3">'
    if anker in s:
        s = s.replace(anker, KASTEN + anker, 1)
        n += 1
    else:
        print(f"  {pfad}: Abschnitt a3 (BEFEHLE) nicht gefunden — Kasten fehlt dort.")
    s, k = re.subn(r'(<input type="text" id="f_text[1-6]" value="" placeholder=")frei formulieren(")',
                   r"\g<1>" + PLATZHALTER.replace("\\", "\\\\") + r"\g<2>", s)
    n += k
    m = re.search(r'<label class="f"><span class="lab">[^<]*</span>\s*<textarea id="f_geheimschreiben"', s)
    if m:
        s = s[:m.start()] + KURZ + s[m.start():]
        n += 1
    else:
        print(f"  {pfad}: Geheimschreiben nicht gefunden — Kurzkasten fehlt dort.")
    m = re.search(r'<label class="f"><span class="lab">Freitext fuer den ganzen Zug', s)
    if m:
        s = s[:m.start()] + KURZ + s[m.start():]
        n += 1
    else:
        print(f"  {pfad}: Freitext-Reiter nicht gefunden — erst blatt_freitext_reiter.py fahren.")
    open(pfad, "w", encoding="utf-8").write(s)
    print(f"  {pfad}: Befehlsform gesetzt ({n} Stellen, davon {k} Platzhalter).")
    return True


if __name__ == "__main__":
    for p in sys.argv[1:]:
        patch(p)
