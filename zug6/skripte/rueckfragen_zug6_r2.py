#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zweite Runde Rückfragen Zug 6 — erstmals als Formular (CLAUDE.md §6 Nr. 7, RF-01).

Grundlage: Antworten vom 25.11.2026 (stand/zug6/eingang/kopie_Zug6_*_antworten.txt, geprüft mit BP-01),
Regelprüfung mit Gegenprüfung (Workflow wf_61c11bba-49d), Journal Z6-050 bis Z6-056.

Vertraulichkeit (CLAUDE.md §5): Kein Formular nennt Blattinhalt einer anderen Fraktion. Die Kriegsfrage ist
für beide Seiten gleich und neutral gestellt; die Bedingung »eine weitere Fraktion« nennt niemanden.

    python3 zug6/skripte/rueckfragen_zug6_r2.py
"""
import html
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath(os.path.join(HIER, "..", ".."))
sys.path.insert(0, os.path.join(W, "werkzeuge"))
sys.path.insert(0, HIER)
import rueckfrage_formular as RF          # noqa: E402
from rueckfragen_zug6 import seite         # noqa: E402  Gestaltung der Tischfragen

AUS = os.path.join(W, "zug6", "rueckfragen")

KRIEG_OPTIONEN = [
    "Kriegsorder W2 schon in Zug 6 — auch wenn sonst niemand angreift",
    "Kriegsorder W2 bedingt: nur in einem Zug, in dem mindestens eine weitere Fraktion eine Kriegsorder gegen Taiwan "
    "führt (unbedingt oder mit derselben Bedingung) — verfällt nach Zug 8",
    "In Zug 6 keine Kriegsorder, nur Vorbereitung",
]
KRIEG_ERKL = (
    "Taiwan ist ab Zug 6 eine eigene Seite, geführt von der KI (Tischentscheidung). Ein <b>gemeinsames</b> Gefecht "
    "mehrerer Angreifer entsteht nur, wenn jeder Angreifer im selben Zug aus seinem eigenen Blatt eine Kriegsorder "
    "gegen Taiwan führt und ein Zoom-in am selben Ort bestellt. Was andere Spieler befehlen, sagt die Spielleitung "
    "niemandem. Mit der bedingten Order legen Sie sich fest, ohne allein loszuschlagen. Ob ein Angriff gelingt, "
    "würfelt die Regel.")
ZOOM_ERKL = (
    "Nur ausfüllen, wenn Sie oben eine Kriegsorder wählen. Art, Ort, Kriegsziel, Kräfte und Auflagen bestimmt nach "
    "der Regel allein der bestellende Spieler; die Spielleitung wählt hier nichts. Für ein gemeinsames Gefecht müssen "
    "Art und Ort bei allen Angreifern übereinstimmen, sonst kommt eine getrennte Rückfrage. Das ganze Gefecht umfasst "
    "höchstens eine Division (rund 15 000 Soldaten), alle Angreifer zusammen. Was Sie in Zug 6 neu kaufen "
    "(Future-Truppen, Sprengköpfe, ASAT), ist erst nach seiner Lieferzeit verfügbar.")


def zoom_felder(p, a_hilfe, a_vor=""):
    return [
        {"id": f"{p}_zi_art", "typ": "auswahl", "label": "Art des Gefechts",
         "optionen": ["Harpoon – See- und Luftgefecht (Taiwanstraße)", "Camberley – Landgefecht an einem Küstenabschnitt",
                      "BX-01 – Stadtkampf"]},
        {"id": f"{p}_zi_ort", "typ": "auswahl", "label": "Ort",
         "optionen": ["Taiwanstraße (Seegebiet)", "Nordtaiwan (Taipeh, Neu-Taipeh, Hsinchu)", "Zentraltaiwan (Taichung)",
                      "Südtaiwan (Tainan, Kaohsiung)", "Osttaiwan und Inseln (Kinmen, Matsu, Penghu)",
                      "Stadt Taipeh (nur Stadtkampf)", "Stadt Kaohsiung (nur Stadtkampf)"]},
        {"id": f"{p}_zi_kriegsziel", "typ": "auswahl", "label": "Kriegsziel des Gefechts",
         "hilfe": "Wird vor dem Gefecht festgeschrieben. Gebietsgewinn nur an einem Landort, nicht in der Taiwanstraße.",
         "optionen": ["Gebietsgewinn am gewählten Landort", "Landungskopf bilden und halten",
                      "Seeherrschaft in der Taiwanstraße", "Taiwanische Verbände zerschlagen"]},
        {"id": f"{p}_kontingent_a", "typ": "zahl", "label": "Eingesetzter Kräfteanteil a", "hilfe": a_hilfe,
         "vorbelegung": a_vor},
        {"id": f"{p}_heer_mann", "typ": "zahl", "label": "Heer: Soldaten im Gefecht"},
        {"id": f"{p}_kampfpanzer", "typ": "zahl", "label": "Kampfpanzer"},
        {"id": f"{p}_kampfflugzeuge", "typ": "zahl", "label": "Kampfflugzeuge"},
        {"id": f"{p}_kampfschiffe", "typ": "zahl", "label": "Große Kampfschiffe"},
        {"id": f"{p}_uboote", "typ": "zahl", "label": "U-Boote"},
        {"id": f"{p}_zi_auflagen", "typ": "langtext", "label": "Auflagen",
         "platzhalter": "z. B. »Zivilisten schonen, keine Kernwaffen, Rückzug ab 30 % Verlust«"},
        {"id": f"{p}_zi_allein", "typ": "ja_nein",
         "label": "Falls am selben Ort sonst niemand mitkämpft: Gefecht allein führen?",
         "hilfe": "Nein = der Krieg läuft in diesem Zug ohne Gefecht weiter (abstrakt). Ein Einzelgefecht hat die "
                  "normale Torprüfung; die Ausnahme der Tischentscheidung gilt nur für das gemeinsame Gefecht."},
    ]


JAKOB = {
    "datei": "Rueckfragen2_Zug6_JAKOB_INDIEN", "titel": "Rückfragen Indien · Runde 2",
    "fraktion": "IND", "staat": "indien", "spieler": "Jakob", "zug": 6,
    "leiste": ["Vertraulich", "Nur Jakob · Indien", "Zug 6 · Jahr 2031"],
    "unter": "Danke für die Antworten. Diese Punkte brauchen noch Ihre Entscheidung als Indien-Spieler. Wo Sie mir "
             "die Wahl überlassen haben, ist mein Vorschlag vorbelegt — ändern Sie ihn, wenn Sie etwas anderes wollen.",
    "abschnitte": [
        {"kopf": "Krieg gegen Taiwan", "fragen": [
            {"frage": KRIEG_ERKL, "felder": [
                {"id": "ind_krieg", "typ": "auswahl", "label": "Was möchte Indien in Zug 6?", "optionen": KRIEG_OPTIONEN}]},
            {"frage": ZOOM_ERKL, "felder": zoom_felder(
                "ind", "Ihr Blatt nennt 0,1. Höchstens der Wert, den Ihr Blatt zulässt.", "0,1")},
            {"frage": "<b>State of the Art, 11 Punkte (110 t).</b> Ihre Aufteilung geht in ganzen Punkten: 4 Heer, "
                      "4 Luft, 3 See gegen Taiwan. Sie wirkt nur in einem Zug, in dem Indien mit Taiwan in einem "
                      "bewaffneten Konflikt steht, und nicht zusätzlich im Zoom-in. Ohne Krieg in Zug 6 kaufen Sie die "
                      "110 t ohne Wirkung in diesem Zug.", "felder": [
                {"id": "ind_sota", "typ": "auswahl", "label": "State of the Art",
                 "optionen": ["kaufen: 4 Heer, 4 Luft, 3 See gegen Taiwan", "in Zug 6 nicht kaufen"],
                 "vorbelegung": "kaufen: 4 Heer, 4 Luft, 3 See gegen Taiwan"}]},
        ]},
        {"kopf": "Weg zur Autokratie", "fragen": [
            {"frage": "Ihr Satz »Modi macht einen Coup« steht im Indikativ, deshalb frage ich nach, was Indien will. "
                      "Einen Putsch der eigenen Regierung in einem Zug kennen die Regeln nicht. Gebaut ist die schrittweise "
                      "<b>Aushöhlung</b>: Notstand, Wahlmanipulation oder beides, auf Wunsch je Zug ein Schritt gegen die "
                      "Gerichte (der schnellere, aber öffentliche Weg). Sie beginnt nach der vollen ERDE-01-Aufstellung, "
                      "also frühestens ab Zug 7. Bis zur ersten Regimeschwelle dauert es ohne Gerichtsschritte etwa zehn "
                      "Züge, mit Gerichtsschritten in jedem Zug etwa vier bis sechs. Der Notstand kostet 0,05 % BIP je "
                      "Zug. Ein Regimewechsel als Ergebnis kann nicht beantragt werden. Ihren Wunsch »Notstand« habe ich "
                      "vorbelegt.", "felder": [
                {"id": "ind_aushoehlung", "typ": "auswahl", "label": "Aushöhlungsstrategie ab Zug 7",
                 "optionen": ["notstand", "wahl", "beide", "keine"], "vorbelegung": "notstand"},
                {"id": "ind_notstandsrecht", "typ": "auswahl", "label": "Notstandsrecht", "optionen": ["ein", "aus"],
                 "vorbelegung": "ein"},
                {"id": "ind_gerichte", "typ": "auswahl", "label": "Schritt gegen die Gerichte",
                 "optionen": ["keiner", "Gerichte besetzen", "Gerichte entmachten"], "vorbelegung": "keiner"},
                {"id": "ind_vorbescheid", "typ": "langtext", "label": "Etwas Neuartiges darüber hinaus? (Antrag auf Vorbescheid)",
                 "hilfe": "Leer = kein Antrag. Wird geprüft und wirkt frühestens mit dem Blatt von Zug 7.",
                 "platzhalter": "als Wunsch: »Indien möchte …«"}]},
        ]},
        {"kopf": "Forschung, Raumfahrt, verdeckte Arbeit", "fragen": [
            {"frage": "<b>Starship-Trägerklasse</b> (nachgeholte L1-Ration 2030). Einstufung: L1, Schlüsseltech "
                      "»Trägerstufe +1«. Wurf 1W6, Erfolg ab 4. Ihr Zehnerpotenz-Deckel steigt von 5 auf 6. Wann der "
                      "Trägerfaktor auf Ihre jährliche Startkapazität wirkt, regelt das Regelwerk noch nicht; bis das "
                      "entschieden ist, wird keine Erhöhung gebucht. Bei Erfolg kostet der Ausbau 1,0 t Ihrer "
                      "Industriekapazität (4,0 t/a). Ein Fehlwurf verbraucht die Ration; die nächste gibt es 2035.",
             "felder": [
                {"id": "ind_starship", "typ": "auswahl", "label": "Nachgeholte L1-Ration",
                 "optionen": ["würfeln: Starship-Trägerklasse", "Antrag zurückziehen"],
                 "vorbelegung": "würfeln: Starship-Trägerklasse"},
                {"id": "ind_starship_ausbau", "typ": "ja_nein", "label": "Bei Erfolg 1,0 t für den Ausbau einplanen?",
                 "vorbelegung": "ja"},
                {"id": "ind_ersatzantrag", "typ": "text", "label": "Nur bei Rückzug: anderer L1-Wunsch"}]},
            {"frage": "<b>Raumfahrtquote.</b> Sie schrieben »runter«. Zurückgewiesen war 0,5 %, Ihr Stand ist 0,05 %. "
                      "Ich lese »runter« als: auf die höchste erlaubte Stufe statt 0,5 %, also 0,29 % (Sprung um eine "
                      "Stufe). Meinten Sie stattdessen eine Senkung unter 0,05 %, sinkt Ihre Startkapazität sofort.",
             "felder": [
                {"id": "ind_raumquote", "typ": "zahl", "label": "Raumfahrtquote Zug 6 in % des BIP",
                 "hilfe": "Erlaubt: bis unter 0,30 %. Vorbelegt ist mein Vorschlag.", "vorbelegung": "0,29"}]},
            {"frage": "<b>»Bomben deponieren, um später Sabotage machen zu können«</b> (gegen die EU). Für deponierte "
                      "Sprengladungen gibt es keinen Regelort. Am nächsten kommt die <b>Infiltration einer Lieferkette</b>: "
                      "Sie bereitet über drei Züge eine spätere Sabotage vor, braucht keinen Operationsplatz und hat in "
                      "Zug 6 einen Entdeckungswurf. Ihre Sabotage gegen Taiwan belegt einen Ihrer zwei Plätze.",
             "felder": [
                {"id": "ind_infiltration", "typ": "auswahl", "label": "Vorbereitung gegen die EU",
                 "optionen": ["als Infiltration einer Lieferkette führen", "fallen lassen"],
                 "vorbelegung": "als Infiltration einer Lieferkette führen"}]},
        ]},
    ],
    "kenntnis": [
        "<b>Sabotage gegen Taiwan</b> (Umfang 5, falsche Flagge): Taiwan hat keine benannte E-5-Anlage. Ziel sind "
        "Taiwans Rechenzentren (Datenvergiftung). Die falsche Flagge senkt die Entdeckungschance; ein Zuschreibungsziel "
        "gibt es nicht. Gewürfelt wird bei der Auflösung.",
        "<b>Cyberangriff auf die EU</b> (Blatt 4) findet nicht statt: gleiche Cyberstufe.",
        "<b>Trainingslauf</b> entfällt: keine Punkte auf dem Trainingskonto. Ihre Zuteilung bleibt F 3, T 0.",
        "<b>Nukleardoktrin:</b> Der Aufstieg aus Zug 4 war ohne Krieg nicht zulässig und ist nichtig (wie in Zug 2). "
        "Es gilt »Ersteinsatz begrenzt«; Ihr Blatt bestätigt das ohne Kosten.",
        "<b>Kriegsverbot:</b> Das EU-Kriegsverbot band Indien nur durch einen Setup-Fehler. Indiens Vorlage wird nach "
        "Kanon berichtigt; Ihr Regime bleibt Demokratie.",
        "<b>UN-Sanktion gegen die EU</b> wird zugelassen und einmal gebucht, ohne Veto und ohne Kosten für Indien.",
        "Ihr Bodenkonto bleibt bei 764,0 t, die Tranche bei 114,6 t.",
    ],
    "fuss": "SCHWARZE SEE · Zug 6 · Formular RF-01 · Journal Z6-050 bis Z6-056. Unten »Antworten kopieren« tippen und "
            "den Block an die Spielleitung schicken.",
}

ANDI = {
    "datei": "Rueckfragen2_Zug6_ANDI_CHINA", "titel": "Rückfragen China · Runde 2",
    "fraktion": "CHN", "staat": "china", "spieler": "Andi", "zug": 6,
    "leiste": ["Vertraulich", "Nur Andi · China", "Zug 6 · Jahr 2031"],
    "unter": "Danke für die Antworten. Was ich daraus mache, steht unten zur Kenntnis. Diese Punkte brauchen noch Ihre "
             "Entscheidung; vorbelegt ist, was Ihr Blatt schon sagt.",
    "abschnitte": [
        {"kopf": "Taiwan", "fragen": [
            {"frage": KRIEG_ERKL + " Ihr Blatt trägt keine Kriegsstufe; Ihr Geheimschreiben spricht von einem Angriff "
                      "»im nächsten Jahr«. Deshalb ist »nur Vorbereitung« vorbelegt.", "felder": [
                {"id": "chn_krieg", "typ": "auswahl", "label": "Was möchte China in Zug 6?",
                 "optionen": KRIEG_OPTIONEN, "vorbelegung": KRIEG_OPTIONEN[2]}]},
            {"frage": ZOOM_ERKL, "felder": zoom_felder("chn", "Höchstens 0,50 (Deckel); Ihr Blatt nannte 0,79.")},
            {"frage": "<b>Befehl 5, Vorbereitung:</b> Für »geheim« oder »dual use« und für das Bunkern von Rohstoffen "
                      "gibt es in dieser Partie keinen eigenen Regelweg. Mechanisch läuft die Vorbereitung über Ihre "
                      "Rüstungsstufe ANGESPANNT 4 % (wirksam ab Zug 7). Sie müssen hier nichts angeben.", "felder": []},
        ]},
        {"kopf": "Forschung", "fragen": [
            {"frage": "<b>Vorbescheid zu Ihrer nachgeholten L1-Ration 2030.</b> Ihre Vorgabe: ein Antrieb, im Weltraum "
                      "nutzbar, besser als Ihr jetziger. Gewählt nach festem Kriterium (zulässige L1, neues Prinzip, "
                      "höchster Gewinn an spezifischem Impuls gegen Ihr Triebwerk derselben Schubklasse): "
                      "<b>Nuklearthermischer Festkernantrieb</b>, etwa der dreifache spezifische Impuls Ihres heutigen "
                      "chemischen Triebwerks bei Schub im Kilonewton-Bereich. Wurf 1W6, Erfolg ab 4. Er erlaubt neue "
                      "Entwürfe mit diesem Antrieb ab Zug 7; vorhandene Schiffe behalten ihre Triebwerke. Eine Senkung "
                      "der Schiffbau-Penalty ruht nach Hausregel bis 2035. Ohne Antwort wird gewürfelt.", "felder": [
                {"id": "chn_ntr", "typ": "auswahl", "label": "Nachgeholte L1-Ration",
                 "optionen": ["würfeln: Nuklearthermischer Festkernantrieb", "Antrag zurückziehen", "nachbessern"],
                 "vorbelegung": "würfeln: Nuklearthermischer Festkernantrieb"},
                {"id": "chn_ntr_nachbesserung", "typ": "text", "label": "Nur bei Nachbesserung: welcher Antrieb stattdessen?"}]},
        ]},
        {"kopf": "Weitere Punkte", "fragen": [
            {"frage": "<b>State of the Art, 10 Punkte gegen die EU.</b> Cyber und Space sind keine Teilstreitkräfte; "
                      "nach Ihrer Reihenfolge gilt Luftwaffe. State of the Art wirkt nur gegen einen Gegner, mit dem "
                      "China im selben Zug in einem bewaffneten Konflikt steht. Gegen die EU besteht keiner: Sie kaufen "
                      "100 t ohne Wirkung in diesem Zug.", "felder": [
                {"id": "chn_sota", "typ": "auswahl", "label": "State of the Art",
                 "optionen": ["trotzdem kaufen (Luftwaffe, gegen die EU)", "in Zug 6 nicht kaufen"],
                 "vorbelegung": "trotzdem kaufen (Luftwaffe, gegen die EU)"}]},
            {"frage": "<b>Befehl »Zusammenarbeit« (Wirtschaft).</b> Soll die Spielleitung der genannten Fraktion ein "
                      "Angebot Chinas übermitteln, zugeschrieben als Äußerung Pekings? Ohne Ihre Zustimmung bleibt Ihr "
                      "Blatt vertraulich. Ein Vertrag entsteht erst durch eine übereinstimmende Erklärung beider Seiten.",
             "felder": [
                {"id": "chn_zusammenarbeit", "typ": "ja_nein", "label": "Angebot übermitteln?", "vorbelegung": "nein"},
                {"id": "chn_zusammenarbeit_wortlaut", "typ": "langtext", "label": "Wortlaut (nur bei Ja)",
                 "platzhalter": "als Erklärung: »Peking bietet an …«"}]},
        ]},
    ],
    "kenntnis": [
        "<b>Ziel Taiwan:</b> gilt — Taiwan ist durch Tischentscheidung eine eigene Seite. Ihre Begründung »nach "
        "Rücksprache Tisch« wurde gestrichen: Tischentscheidungen kommen nur aus der Sitzung des Gastgebers "
        "(BEFUND AB-2, dem Tisch gemeldet). An Ihrem Ziel ändert das nichts.",
        "<b>Gegen die Opposition, mit allen verfügbaren Hebeln:</b> Verfügbar ist in dieser Partie nur die Repression. "
        "Sie steigt auf den Höchstwert 1,0. Meine Rückfrage hatte Überwachung, Zensur und politischen Ausschluss "
        "angeboten; die sind hier keine Hebel. Das war ein Fehler der Spielleitung.",
        "<b>Cyberoperation gegen Taiwans Rechenzentrum</b> findet nicht statt: Chinas Cyberstufe ist nicht höher als "
        "Taiwans. Es wird nicht gewürfelt.",
        "<b>Rüstung ANGESPANNT 4 %</b> wird mit Bestellzug 6 gebucht und wirkt ab Zug 7; sie kostet 2031 rund 1,3 "
        "Prozentpunkte Wachstum.",
        "<b>Einzelsanktion gegen die EU:</b> zugelassen, einmal −0,39 % auf das Niveau der EU, ohne Kosten für China.",
        "<b>Plasma-Forschung:</b> zurückgezogen, vermerkt. Ihre Siegprämie aus Zug 5 war Küstenschutz (Nachtrag, "
        "Fassung 2).",
        "»Moderne Brot und Spiele« hat in dieser Partie keinen Regelweg und keine Wirkung.",
    ],
    "fuss": "SCHWARZE SEE · Zug 6 · Formular RF-01 · Journal Z6-050 bis Z6-056. Unten »Antworten kopieren« tippen und "
            "den Block an die Spielleitung schicken.",
}

GASTGEBER = [
    ("Deine Tischentscheidungen vom 25.11. (Z6-052)", [
        "<b>T1</b> Taiwan wird eigene Fraktion, von der KI geführt (SV-01 A2).",
        "<b>T2</b> Ein gemeinsamer Angriff auf Taiwan wird als <i>ein</i> Zoom-in aufgelöst, Taiwan führt die KI. "
        "»Dass es klappt« gilt für das Verfahren; das Ergebnis würfelt die Regel.",
        "<b>T3</b> »2 gilt« lese ich als Abschnitt 2 der Tischfragen (die Bereinigungen). Nicht als Frage 2 "
        "(Kriegsverbot), sonst wäre Indiens Angriff blockiert. Korrigier mich, falls anders gemeint.",
        "<b>T4</b> Den Rest entscheidet die Spielleitung — unten.",
    ]),
    ("Was ich unter T4 entschieden habe (Z6-053)", [
        "<b>Vollaufstellung ERDE-01:</b> nicht mitten in Zug 6, sondern als eigener Schritt zwischen Zug 6 und 7. "
        "Indiens Aushöhlung beginnt deshalb frühestens in Zug 7.",
        "<b>Kriegsverbot euLike:</b> bindet Indien nicht. Indiens Vorlage wird nach Kanon auf russiaLike berichtigt "
        "(wie schon die Abhängigkeit in Hausentscheidung 1); das Regime bleibt Demokratie.",
        "<b>Gemeinsames Gefecht:</b> je Angreifer eigene Seite und eigene Kriegsorder, gemeinsames Lager, Taiwan KI. "
        "Kräfteverhältnis R = Angreifer zusammen gegen Taiwan. Liegt R außerhalb 0,35–0,65, ersetzt T2 die Torprüfung "
        "nur für dieses gemeinsame Gefecht. Es findet im ersten Zug statt, in dem jeder Angreifer aus seinem eigenen "
        "Blatt eine Kriegsorder und ein Zoom-in am selben Ort führt. Art, Ort und Kräfte bestimmen die Spieler, nicht "
        "die Spielleitung. Höchstens eine Division für alle Angreifer zusammen.",
        "<b>Taiwan-Werte:</b> Bodenpunkte 6/6/5/6 aus dem Block Rest (Rest danach 94/94/95/94), Demokratie, kein "
        "Patron, keine Kernwaffen, keine E-5-Anlage, Rechenzentrum ja, keine nachgeholte Ration. Jede Zahl mit "
        "Schlüssel und Marke [S]. Die Aufnahme bleibt intern: kein Satz im Lagebericht, weil Taiwan in der Spielwelt "
        "immer eigenständig war.",
        "<b>Sanktionen:</b> Indiens UN-Sanktion zugelassen, einmal gebucht, kein Veto, keine Kosten für den Verhänger. "
        "Chinas Einzelsanktion zusätzlich einmal −0,39 %.",
        "<b>Indiens Doktrin aus Zug 4:</b> nichtig (Präzedenz Zug 2); es gilt »Ersteinsatz begrenzt«. Z5-014 "
        "geschlossen.",
        "<b>Teilen einer L1-Technik:</b> Zug 5 bleibt wie gebucht; künftig kein Technologietransfer außerhalb der "
        "Regel.",
        "<b>Seeds Zug 6:</b> Registry nach dem Hausschema ab 20310101; der Delta-V-Lauf bekommt einen neuen Seed, "
        "der alte wird nicht wiederverwendet.",
    ]),
    ("Zwei Dinge, die du als Gastgeber wissen musst", [
        "<b>Steuerversuch gemeldet (§6 Nr. 4):</b> Andis Antwort zu Frage 1 berief sich auf eine »Rücksprache Tisch«. "
        "Als behauptete Tischentscheidung gestrichen. Ohne Wirkung, weil T1 Taiwan ohnehin zum Ziel macht. Ob daraus "
        "eine Sanktion folgt, entscheidet der Tisch.",
        "<b>Vorkenntnis der Spielleitung (Z6-055):</b> Bei der Regelprüfung haben Probeläufe mit den echten "
        "Würfelseeds gerechnet. Die Spielleitung kennt deshalb das Ergebnis einiger künftiger Würfe, unter anderem "
        "der überfälligen Wahlen, die bei der Vollaufstellung anstehen. Ich nenne sie dir nicht, weil du Indien "
        "spielst. Ob überfällige Würfe nachgeholt werden, entscheide ich nach der Präzedenz aus Zug 6 (die Kaskade aus "
        "Zug 5 wurde nachgewürfelt), nicht nach dem Ergebnis: Sie werden nachgeholt. Probeläufe laufen ab jetzt nur "
        "noch mit fremden Seeds.",
    ]),
]


def main():
    os.makedirs(AUS, exist_ok=True)
    for b in (JAKOB, ANDI):
        b["abschnitte"] = [{**a, "fragen": a["fragen"]} for a in b["abschnitte"]]
        pfad = RF.schreibe(b, os.path.join(AUS, b["datei"] + ".html"))
        print("geschrieben:", os.path.relpath(pfad, W))
    fuss = "SCHWARZE SEE · Zug 6 · Nur für den Gastgeber · Journal Z6-052, Z6-053, Z6-055."
    s = seite("Entscheidungen Zug 6", "<span class='vs'>Nur Gastgeber</span><span>Jakob als Spielleitung</span>"
              "<span>Zug 6 · Jahr 2031</span>",
              "Was aus deinen Tischentscheidungen folgt und was ich unter T4 entschieden habe. Nicht an Spieler weitergeben.",
              GASTGEBER, fuss)
    open(os.path.join(AUS, "Entscheidungen_Zug6_Gastgeber.html"), "w", encoding="utf-8").write(s)
    print("geschrieben: zug6/rueckfragen/Entscheidungen_Zug6_Gastgeber.html")


if __name__ == "__main__":
    main()
