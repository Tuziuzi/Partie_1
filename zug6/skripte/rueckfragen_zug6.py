#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rückfragen Zug 6 an die Spieler und Tischfragen an den Gastgeber.

Grundlage: Prüfer BP-01 (CLAUDE.md §6), die Blattleser und die Gegenprüfung vom 25.11.2026
(Journal Z6-045 bis Z6-049). Jede Zahl stammt aus einem Skriptlauf, der im Journal steht.

Vertraulichkeit (CLAUDE.md §5): Die Rückfragen an einen Spieler nennen nur seine eigene Lage. Was ein
anderer Spieler befohlen hat, steht ausschließlich in den Tischfragen an den Gastgeber.

    python3 zug6/skripte/rueckfragen_zug6.py
"""
import html
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from briefing_zug6 import STIL, FONTS          # noqa: E402  gleiche Gestaltung wie Briefing und Nachtrag

W = os.path.abspath(os.path.join(HIER, "..", ".."))
AUS = os.path.join(W, "zug6", "rueckfragen")


def e(s):
    return html.escape(s, quote=True)


def seite(titel, leiste, unter, abschnitte, fuss):
    teile = []
    for kopf, punkte in abschnitte:
        li = "".join(f"<li>{p}</li>" for p in punkte)
        teile.append(f"<section><h2>{e(kopf)}</h2><ol class='liste'>{li}</ol></section>")
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titel)}</title>
{FONTS}{STIL}</head><body>
<main class="rahmen">
<header>
  <div class="leiste">{leiste}</div>
  <h1 style="margin-top:.8rem">{e(titel)}</h1>
  <p class="unter">{unter}</p>
</header>
{''.join(teile)}
<footer class="fuss">{fuss}</footer>
</main></body></html>
"""


ANDI = [
    ("Bitte beantworten — sonst wirken diese Befehle nicht", [
        "<b>Befehl 5 (Militär):</b> Das Ziel fehlt. Welche Handlung meinen Sie konkret: eine Kriegsstufe mit Rolle gegen wen, "
        "Maßnahmen am eigenen Bodensegment oder etwas anderes? Taiwan führt der Spielstand nicht als eigene Seite, es gehört "
        "zum Block »Rest«. Und gilt »geheim« <i>oder</i> »dual use«? Das Bunkern von Rohstoffen hat in dieser Partie keinen "
        "Regelweg, weil das Ressourcenmodul nicht läuft.",
        "<b>Befehl 6 (Nachrichtendienste, Ziel China):</b> Mit welchem Hebel und auf welcher Stufe soll gegen die Opposition "
        "vorgegangen werden: Repression über 0,8, Überwachung im Inland, politischer Ausschluss oder Zensur? »Ausrotten« "
        "legt ein Ergebnis fest; das entscheidet die Regel, nicht der Befehl.",
        "<b>Cyberoperation Umfang 5:</b> Welches Ziel genau? Möglich sind eine benannte Anlage des Blocks Rest "
        "(tanegashima, uchinoura, naro, mahia, palmachim, semnan, sohae) oder dessen Rechenzentren. Der zweite Weg findet "
        "bei der derzeitigen Cyberlage nicht statt. Ohne Ziel-Anlage wird nicht gewürfelt.",
        "<b>Rüstung ANGESPANNT:</b> Welcher Wert zwischen 3,5 und 4,5 % des BIP? Die höhere Stufe wirkt ab Zug 7.",
        "<b>State of the Art, 10 Punkte:</b> Gegen welche Fraktion und welche Teilstreitkraft sollen sie wirken, und in "
        "welchem Konflikt? Ohne militärische Begründung wirken sie nicht.",
        "<b>Forschung, nachgeholte L1-Ration 2030:</b> Meinen Sie Plasma-Recycling von Abfall in sortenreine Rohstoffe "
        "(Stufe L1, frei würfelbar) oder atomgenaue Neusynthese (gesperrt bis 2075)? Und welche Wirkung soll die Technik "
        "im Spiel haben? Zum Teilen mit einer anderen Fraktion: Eine L1-Technik geht in Delta V nicht auf andere über, und "
        "die Ration ist nicht übertragbar.",
        "<b>Sanktion »UN umfassend« gegen die EU:</b> Meinen Sie wirklich die UN-Sanktion oder eine Einzelsanktion? Über "
        "die UN-Form muss der Tisch noch entscheiden.",
    ]),
    ("Zur Kenntnis, keine Antwort nötig", [
        "Ihr Bodenkonto ist nach der Korruptionsbuchung neu: 2691,1 t statt 2659,0 t, Hochtechnologie-Tranche 403,7 t "
        "statt 398,9 t. Ihre Prozentwerte gelten unverändert (Nachtrag, Fassung 2).",
        "Ihre Hochtechnologie-Aufträge passen in die Tranche. Die Sprengköpfe kosten auf Ihrer Produktionsstufe 5 t je Stück.",
        "Die ASAT-Schüsse laufen auf einer neuen Linie; geliefert wird frühestens in zwei Jahren.",
        "Blatt 4: Zugeteilt sind 10 von 20 Rechenpunkten. Nicht zugeteilte Punkte verfallen nicht, wirken aber auch nicht. "
        "Das bestellte Kraftwerk ist erst nach zwei Jahren nutzbar; Bau, Kraftwerk und Lizenz kosten Geld auf Blatt 1, "
        "dort steht noch kein Posten.",
        "Ihr Geheimschreiben: Absprachen mit einer anderen Fraktion haben im Spiel nur über ein von beiden unterzeichnetes "
        "Memorandum eine Form. Was ein anderer Spieler versprochen haben soll, übernimmt die Spielleitung nicht als Tatsache.",
        "Ihre Siegprämie aus Zug 5 ist eingelöst (L1 Küstenschutz). Die erste Fassung Ihres Nachtrags sagte etwas anderes; "
        "das war ein Fehler der Spielleitung.",
    ]),
]

JAKOB_INDIEN = [
    ("Bitte beantworten — sonst wirken diese Befehle nicht", [
        "<b>Wechsel zur Autokratie:</b> In Zug 6 nicht möglich. Es gibt einen mehrzügigen Weg, die legale Aushöhlung "
        "(Strategie Wahl, Notstand oder beides). Möchten Sie ihn beginnen? Er setzt eine Tischentscheidung zur vollen "
        "ERDE-01-Aufstellung Indiens voraus, Ihr Blatt hat dafür noch kein Feld, und er wirkt frühestens ab Zug 7; bis zu "
        "einem hybriden Regime vergehen mehrere Züge.",
        "<b>Kriegsstufe W2, Rolle Angreifer:</b> Die Bedingung »wenn der Wechsel klappt« ist ohne Verfallszug "
        "zurückgewiesen und könnte in Zug 6 ohnehin nicht eintreten. Soll W2 unbedingt gelten, und gegen welchen Gegner, "
        "oder entfällt der Befehl? Ein Zoom-in braucht außerdem Art, Ort, Kräfte und Auflagen.",
        "<b>Sabotage Umfang 5 mit falscher Flagge:</b> Welche Anlage im Block Rest (tanegashima, uchinoura, naro, mahia, "
        "palmachim, semnan, sohae) oder die Rechenzentren des Blocks? Taiwan führt der Spielstand nicht als eigene Seite. "
        "Ohne Ziel-Anlage wird nicht gewürfelt.",
        "<b>»Bomben an kritischer Infrastruktur der EU deponieren«:</b> Dafür gibt es keinen Regelweg im Operationskatalog. "
        "Meinen Sie eine Sabotage an einer benannten EU-Anlage oder eine Vorpositionierung in einem Sektor? Achtung: Mit "
        "0 % Geheimdiensten auf Blatt 3 haben Sie in Zug 6 nur 2 Operationsplätze.",
        "<b>Forschung, nachgeholte L1-Ration 2030 »Starship«:</b> Möchten Sie die Fähigkeit »Starship-Trägerklasse« "
        "erforschen (Würfel 1W6, Erfolg ab 4) oder ein Starship-Fahrzeug bauen (Werftauftrag ohne Wurf und ohne Ration)? Aus "
        "der Beschaffung in Zug 5 ist kein Besitz gebucht.",
        "<b>State of the Art, 11 Punkte (110 t):</b> Gegen welche Fraktion und welche Teilstreitkraft? In einem Zoom-in "
        "dürfen sie nicht zusätzlich angerechnet werden.",
        "<b>Raumfahrtquote 0,5 %:</b> Sie springt zwei Stufen und ist zurückgewiesen. Möchten Sie einen Wert in der nächsten "
        "Stufe setzen (0,10 bis unter 0,30 %)?",
        "<b>Trainingslauf angesagt:</b> Ohne Rechenpunkte auf dem Trainingskonto entfällt er. Möchten Sie Punkte auf das "
        "Trainingskonto legen?",
    ]),
    ("Zur Kenntnis, keine Antwort nötig", [
        "Die Nukleardoktrin »Ersteinsatz begrenzt« ist mit Ihrem Arsenal deklarierbar. Wie sie sich zur offenen Frage aus "
        "Zug 4 verhält, entscheidet der Tisch.",
        "Der Cyberangriff auf die EU (Blatt 4) findet nicht statt: Bei gleicher Cyberstufe gibt es keinen Angriff.",
        "Der Orbitalanteil von 5 % ohne Beleg zählt als 0.",
        "Ihr Bodenkonto bleibt bei 764,0 t, die Tranche bei 114,6 t; Ihre 110 t State of the Art passen.",
    ]),
]

TISCH = [
    ("Vor der Auflösung zu entscheiden", [
        "<b>ERDE-01-Vollaufstellung (Z6-035).</b> Seit Zug 1 nicht gemacht. Davon hängen ab: Indiens Weg zur Autokratie, "
        "das geschönte Lagebild Chinas und die Eingaben der Kaskade. Jetzt nachholen oder weiter ohne?",
        "<b>Bindet das Kriegsverbot des Templates »euLike« Indien?</b> Indien trägt es nur als Rückfall beim Setup, nicht "
        "nach Kanon; die Zeile hat kein »solange Demokratie«. Für Erdkriege eine Regellücke.",
        "<b>Taiwan als eigene Seite?</b> Indien und China zielen beide auf Taiwan. Der Stand führt es nur im Block Rest; "
        "nach LW-01 muss es herausgezogen werden und eigene Werte bekommen, sonst gibt es weder Ziel-Anlage noch Gefecht.",
        "<b>Gemeinsamer Angriff zweier Fraktionen:</b> Kein Regelort. Jede Fraktion braucht eine eigene Kriegsorder und "
        "eigene Gefechtszeile; zwei Angreifer zu einem Kräfteverhältnis zu rechnen, ist nicht gebaut.",
        "<b>Zwei UN-Sanktionen gegen die EU</b> (Indien und China, beide »umfassend«): Nach dem Wortlaut zulässig, weil der "
        "Stand keinen UN-Block führt. Offen: Zählen beide oder wirkt es einmal? Hat die EU über Frankreich ein Veto? Was "
        "kostet es den Verhänger (OF-HK-105)?",
        "<b>Indiens Doktrin aus Zug 4 (Z5-014):</b> Nach der Präzedenz aus Zug 2 wäre der Aufstieg auf Stufe 4 nichtig. Gilt "
        "er? Davon hängt ab, ob »Ersteinsatz begrenzt« ein Schritt abwärts oder eine Bestätigung ist.",
        "<b>Teilen einer L1-Technik:</b> Zug 5 hat eine Lizenz China → Indien über FO-01 gebucht (E-Z5-02), Delta V kennt "
        "dafür keinen Weg (OF-DV-36). Gilt die Präzedenz weiter?",
    ]),
    ("Von der Spielleitung bei der Auflösung zu bereinigen (zur Bestätigung)", [
        "Bestand ungleich Buchung: Sprengköpfe China 700 gegen 726, Indien 190 gegen 199; Indiens Repression 0,4 gegen 0,6 "
        "(Z6-036); Indiens Geheimdienstplätze stehen noch auf dem Zug-5-Wert (85 %, 8 Plätze), für Zug 6 gelten 2.",
        "Die nachgeholte L1-Ration läuft als dokumentierte Übersteuerung (Rationsjahr 2030), weil der Resolver 2031 nicht "
        "als Rationsjahr kennt.",
        "Chinas Rüstungsstufe ANGESPANNT wird mit Bestellzug 6 gebucht, nicht mit dem vorbefüllten Bestellzug 5, sonst "
        "wirkte sie einen Zug zu früh.",
        "Das Druckkonto der Grauzone (Indien gegen EU) zerfällt in Zug 6 auch ohne neue Operation.",
    ]),
    ("Zur Kenntnis", [
        "Die EU ist nach SV-01 (A3, V2) vertreten; das Blatt hält alle Treuhand-Schranken. Eine Zeile (Frankreich-Gespräche) "
        "hat der Guard wegen eines Wortfehlgriffs gestoppt; sie bleibt im Status quo.",
        "Zwei eigene Fehler der Spielleitung sind korrigiert: Chinas Siegprämie war eingelöst (Z6-037 widerrufen), und die "
        "Korruptionsbuchung wirkt sehr wohl auf die Bodenkonten (Z6-033 widerrufen; Konten neu gebucht).",
    ]),
]


def main():
    os.makedirs(AUS, exist_ok=True)
    fuss = ("SCHWARZE SEE · Zug 6 · Grundlage: Befehlsprüfer, Blattleser und Gegenprüfung vom 25.11.2026, Journal "
            "Z6-044 bis Z6-049. Antworten bitte als Wunsch formulieren (»Ich möchte …«, »China soll …«).")
    dateien = {
        "Rueckfragen_Zug6_ANDI_CHINA.html": seite(
            "Rückfragen China", "<span class='vs'>Vertraulich</span><span>Nur Andi · China</span><span>Zug 6 · Jahr 2031</span>",
            "Ihr Blatt ist eingegangen und geprüft. Diese Punkte brauchen Ihre Antwort, bevor der Zug aufgelöst wird.",
            ANDI, fuss),
        "Rueckfragen_Zug6_JAKOB_INDIEN.html": seite(
            "Rückfragen Indien", "<span class='vs'>Vertraulich</span><span>Nur Jakob · Indien</span><span>Zug 6 · Jahr 2031</span>",
            "Ihr Blatt ist eingegangen und geprüft. Diese Punkte brauchen Ihre Antwort als Indien-Spieler.",
            JAKOB_INDIEN, fuss),
        "Tischfragen_Zug6_Gastgeber.html": seite(
            "Tischfragen Zug 6", "<span class='vs'>Nur Gastgeber</span><span>Jakob als Spielleitung</span><span>Zug 6 · Jahr 2031</span>",
            "Hier laufen die Blätter mehrerer Fraktionen zusammen. Nicht an Spieler weitergeben.",
            TISCH, fuss),
    }
    for name, inhalt in dateien.items():
        open(os.path.join(AUS, name), "w", encoding="utf-8").write(inhalt)
        print("geschrieben:", os.path.join("zug6", "rueckfragen", name))


if __name__ == "__main__":
    main()
