# SCHWARZE SEE — Auflösung Zug 5 (Jahr 2030)

**Stand: 05.09.2026 · Delta V + ERDE-01 · Spielleitung**

> **Kopfvermerk zur Quellenlage.** Aufgelöst wurde aus `UEBERGABE_ZUG5.md` §4, den sechs
> abgegebenen Blättern, den beiden Word-Dokumenten und `KB-02_WACHSTUMSBUCH.md`.
> Das in §8 der Übergabe genannte Paket `SCHWARZE_SEE_spielstand_zug5.zip`
> (`gamestate.json`, `erde01_state_schwarzesee.json`, `journal.jsonl`, `config.json`,
> `work/`, `work/sv01/`, `snapshots/`) liegt in **keinem** der beiden Repositories.
> Deshalb konnten `resolve_round.py`, `erde01_engine.py resolve`, `eh01.py spiel zug`
> und `wn01_validator.py` nicht gegen den echten Stand laufen. Jede Zahl unten kommt
> aus einem Skript; wo eine Eingabe fehlt, steht das als Lücke und ist **nicht**
> mit einer plausiblen Zahl gefüllt. Vollständige Aufstellung: `eingang/QUELLEN_ZUG5.md`.
> `zh01.py pruefe` lief und meldet **18 von 18 BESTANDEN**.

---

## 1. Das Ergebnis in fünf Zeilen

1. **China gewinnt den Krieg.** Rundenscore 5 : 1 gegen die USA, Serie 2 → 3,
   `warsWon[CHN] = 1`, Auszahlung **1× gratis forschen auf L1, timelinefrei**.
2. Die EU konnte das nicht verhindern — nicht wegen ihrer Regler, sondern weil ein in
   Zug 5 freigegebener Entwurf in Zug 5 noch kein fliegendes Gerät ist.
3. Indiens falsche Flagge **wirkt**: die neue Sabotagekampagne fällt auf Attributionsgüte
   **D4** und ist damit nicht einmal öffentlich zurechenbar. Die EU hält aber weiter
   ihre zwei alten Attributionen (B2, A1) in der Hand.
4. Indien wird beim Diebstahl von Starship-Technologie **von den USA entdeckt**.
5. Chinas fünfter Kaskadenwurf geht vorbei: **2W10 = 14**, keine globale Wirtschaftskrise.

---

## 2. Vorentscheidungen des Hosts (vor der Auflösung getroffen)

| Nr. | Entscheidung | Wirkung |
|---|---|---|
| **E-1** | Basiswachstumspfad **rückwirkend** ab 2026 | BIP 2029: China 17,2064 · EU 19,8234 · Indien 4,9524 Bio USD. Bodenkonten Zug 5: China 2503,1/375,5 · EU 1660,5/249,1 · Indien 719,3/107,9 t. Blatt 3 für alle drei neu gedruckt. |
| **A4** | ausgelegt als **A3-artig mit Treuhand-Schranken** | USA, Russland, Rest halten Eskalation, eröffnen keinen Krieg ≥ W2, schreiben Budgets ±10 % fort. |
| **China V2** | Vertreter **schreibt die Zug-4-Linie fort** | China scored weiter — und entscheidet damit die Partie. |
| **E-2 · E-4 · E-5** | ab Zug 5 gebucht | Schockform als Niveau, SAEED ersetzt, DW-01-Zivilkonto mit J-Kurve. |

**E-1 nachgerechnet** (`skripte/e1_basispfad.py`): Aus der Ist-Reihe wird der implizite
Jahresschock zurückgerechnet und der Tafelpfad daraufgesetzt. Gegenprobe gegen KB-02 §7:
Abweichung **0,0000** (China), **0,0001** (EU, Indien) — **BESTANDEN**.
Die 15-%-Regel für die Tranche reproduziert die gedruckten Ist-Werte exakt.

> **Nicht gerechnet, gemeldet (RG-Z5-03):** E-1 rückwirkend hebt auch die NPC-Wirtschaft,
> KB-02 §7 rechnet aber nur die drei bespielten Blöcke und begrenzt den Neudruck auf
> »die drei Zug-5-Blätter 3«. USA (7463,6 t) und Russland (1079,8 t) bleiben auf den
> Ist-Konten. Das ist eine Asymmetrie zugunsten der NPC und gehört an den Tisch.

---

## 3. Blattprüfung

### 3.1 EU — Roman

Beide Leser laufen formal sauber durch (`blattlesen.py`: 0 zurückgewiesene Einträge;
`zh01_blattlesen.py`: `"befunde": []`). Genau darin liegt das Problem — die schweren
Punkte fallen durch die Raster der Prüfroutinen.

| Nr. | Befund | Was zu tun ist |
|---|---|---|
| **R-1** | **»Militärbudget weiter auf 38/0«** — die Notation existiert im gesamten Regelwerk nicht. Dazu ein Dreifachwiderspruch: Regler `ANGESPANNT` (= 3,5–4,5 %) gegen »weiter« (= unverändert) gegen die gedruckte Kasse (1602,6 t entsprechen 1,7493 % = NORMATIV). Bei ANGESPANNT gerechnet läge das Bodenkonto bei **2914,3 bis 3734,1 t** und der Wachstumsabzug bei **1,936 bis 3,146 Pp**. | **Zug 5 mit NORMATIV gebucht**, weil »weiter« und die gedruckte VORGABE übereinstimmen. Roman drei Fragen: Was heißt 38/0? Soll die Quote wirklich steigen? Wenn ja, auf welchen Punktwert — und ist der Wachstumsabzug bei schrumpfender Wirtschaft gewollt? |
| **R-2** | **Transfer 1 »nukleare Teilhabe« mit Ziel »EU«** — das ist die eigene Fraktion, also sachlich ein Transfer ohne Gegenseite (**V13**, Z-5). Posten »advanced« passt nicht zur Teilhabe (die handelt in Sprengköpfen, Z-5.2), die Menge ist leer. Frankreich ist im Fraktionsschlüssel Teil von `eu`; die 290 Sprengköpfe **enthalten** die französischen bereits. | Zeile zurückgegeben, nicht gebucht und nicht verworfen. Der französische Nuklearschirm ist ein **innereuropäischer** Vorgang und gehört als ERDE-01-Befehl gespielt, nicht als ZH-01-Transfer. |
| **R-3** | **Weltraumbefehl nicht ausführbar.** `eu_orbital = 0 %` ist **nicht** das Raumfahrtbudget, sondern der Klimaregler H-2b — die EU kann starten (45 t/a) und hat 8 C2-Slots. Es fehlen aber **Zielzone, Startmasse und Δv**; und »Startkapazitäten ausbauen« hat nach C-9 §9 mitten in einer Kampagne überhaupt keinen Regelweg. | Rückfrage. **Folge für Zug 5: die EU scored keine Zone** (siehe §4.2). |
| **R-4** | **Blatt 4 deckt zwei Befehle nicht.** 8 Rechenpunkte bleiben unzugeteilt und laufen leer. Kein Konto O bedeutet Deckungsgrad d = 0 und nach `launch_c2.md` §3.2 **−1 Initiative und −1 auf Duelle je 2 fehlende Slots** — das trifft genau die Satellitenabsicht. | Blatt 4 zurückgegeben. Für die Satellitenlinie reichen 0,16 RP auf Konto O (0,02 je gebundenem Slot) — es steht nichts da. |
| **R-5** | **»Yoda-Inspektoren« (O-eu-05) sind 2030 nicht forschbar.** `research.md` schaltet die erste L1 im Jahr **2035** frei; FO-01 §1: »Was nicht freigeschaltet ist, hat keine Rate.« | Befehl notiert, nicht gebucht. Roman mitteilen — das ist bitter, weil China genau diese Sperre über die Siegprämie umgeht. |
| **R-6** | **Zwei Word-Punkte ohne Träger:** Geheimverhandlungen mit Pakistan und die Frankreich-Verhandlung stehen auf keiner Befehlszeile, `eu_op = keine`, kein Geheimschreiben. Verdeckte Absicht gehört nach Z-8.2 ins Geheimschreiben. | Rückfrage. Zusätzlich offen: Das Blatt hat sechs Zeilen, das Word elf Punkte — ob mehr als sechs Befehle je Zug zulässig sind, sagt keine Regel. |
| **R-7** | **Stille Kürzung verhindert.** Blattzeile 2 lässt ARIANE, die Frankreich-Kooperation und die Kulturprogramme weg; Zeile 1 lässt die **Bedingung** weg (Verletzung des Arktis-Vertrags) und macht aus »auf Eis legen« einen »Abbruch«. | Der volle Word-Wortlaut ist maßgeblich und liegt so im Postfach. Die Drohung ist eine **bedingte** — bedingte Befehle brauchen einen Verfallszug, die Felder sind leer. |
| **R-8** | **Attributionsgrundlage unklar.** Roman beschuldigt Indien »auf Basis der offen verfügbaren Informationen« (= OSINT, Güte C3), hält aber B2 und A1. Eine misslungene öffentliche Attribution senkt künftig **alle** EU-Attributionen um eine Stufe. | Rückfrage: A1, B2 oder neue OSINT-Attribution? Und: dass »keine Vergeltung« das Eskalationsrecht nur ruhen lässt, darf der GM nicht selbst entscheiden. |
| **R-9** | **Sanktionen gegen Moskau**: Blatt sagt `keine`, Word sagt »fortsetzen«. Ob eine läuft, steht im fehlenden Zustand. | Rückfrage mit der C-4-Typenliste. |
| **R-10** | Blatt 2: 100 % Energiebudget, aber **keine Mischung und keine Rangfolge** — bei gleichzeitigem Befehl »Senkung der Energiekosten«. | EH-01 bekommt Geld ohne Bauanweisung. Rückfrage. |
| **R-11** | Formfehler: kein Spielername, kein Datum, Zeichnungsfeld trägt die gedruckte Vorwahl des Blattautors. Nach der Blattverwechslung in Zug 4 nicht bedeutungslos. | Nachtragen lassen; hält den Zug nicht auf. |

**Kein echter Widerspruch:** `eu_doktrin = status_quo` ist die A-5-Persönlichkeit (für eine
Demokratie ohnehin »Status quo«), **nicht** die Nukleardoktrin. Die steht auf Blatt 3 und
ist »unverändert«.

### 3.2 Indien — Jakob

| Nr. | Befund | Was zu tun ist |
|---|---|---|
| **J-1** | **Doktrin `de_eskalationsschlag` ist nach der Regel gar nicht deklarierbar.** `militaer_handoff.md` E-2.1: »»de_eskalationsschlag« (Stufe 4) verlangt einen laufenden Krieg mindestens W2. Im Frieden ist sie nicht deklarierbar; sie beschreibt eine Handlung, keine Haltung.« Ein Krieg Indiens ≥ W2 ist nirgends belegt. | Zurückgemeldet, nicht still korrigiert und nicht still weitergeführt. Sperre 1 (»über ambiguitaet hinaus nur mit Arsenal«) ist mit 199 Sprengköpfen erfüllt. |
| **J-2** | **»Die Araber« sind keine Fraktion dieser Partie.** PB-01 §4.4 setzt ein benennbares Attributionsziel voraus, gegen das das Opfer und die NPC-Linien tatsächlich eskalieren können. Nächstliegend wäre die Sammelfraktion `REST`. | Der GM wählt das **nicht** aus — Jakob muss als Spieler sagen, welcher Akteur des Spielstands gemeint ist. Für Zug 5 unschädlich, weil die falsche Flagge ohnehin nicht aufgedeckt wird. |
| **J-3** | **Kein Regelort für zwei der befohlenen Ziele.** »Pipelines sprengen«: Energieinfrastruktur ist als Ziel einer verdeckten Operation nirgends geführt. »Angriffe auf Universitäten«: physische Anschläge auf Zivil- und Bildungsziele mit Personenschaden sind in PB-01, ERDE-01 und GZ-01 nicht modelliert. | Als Sabotage auf Produktionsknoten gebucht, was der Katalog hergibt — die darüber hinausgehende Wirkung ist **Lücke**, nicht Setzung. |
| **J-4** | **`hybrid.md` existiert nicht.** GZ-01 verweist an sechs Stellen auf G-10 (Migration als Waffe) und G-11 (Wahlbeeinflussung, Eliten) in `erde01-gm:references/hybrid.md`. Die Datei ist im installierten Skillordner nicht vorhanden. | »Mit rechten Parteien paktieren« hat damit keinen eigenen Regelort und läuft ersatzweise als PB-01-Einfluss. Befund an die Skillpflege. |
| **J-5** | Blatt 3 §16: **85 % Geheimdienste**. `zh01.py dienste --fraktion IND --pct 85 --konto 719.3` → **Kosten 611,4 t**, **Slots 8** (Deckel). Dazu 9 Future-SP à 10 t = 90 t aus der Tranche. | Gebucht. Auf dem **alten** Konto hätte Jakob 510,9 + 90 = 600,9 von 601,0 t verplant — auf 0,1 t genau. Durch E-1 bleiben ihm jetzt 17,9 t frei. |
| **J-6** | Blatt 1 trägt `doktrin = status_quo`, die gedruckte VORGABE sagt `de_eskalationsschlag`. | Wie bei der EU: das ist die A-5-Persönlichkeit, nicht die Nukleardoktrin. Kein Widerspruch — siehe aber J-1. |

---

## 4. Delta V — die Weltraumphase

### 4.1 Was jede Fraktion tut

| Fraktion | Handlung | Grundlage |
|---|---|---|
| **China** | scored erneut in **LEO, MEO, HEO, SSO, GEO** — je 1 km/s Δv | SV-01 V2, Schranke 5: »Fortschreibung der letzten Verteilung ±10 % je Konto«. China hat in Zug 4 in fünf Zonen gescored. |
| **USA** | hält **earthSurface** | A3-artig, Fortschreibung. Gewinnt die Teilkategorie Militärpunkte deutlich. |
| **EU** | **keine Zone** | Der Weltraumbefehl nennt weder Zielzone noch Startmasse noch Δv, und ein in Zug 5 freigegebener Entwurf ist in Zug 5 kein fliegendes Gerät: `launch_c2.md` prüft die Startkapazität erst »im Jahr der Fertigstellung (Phase 7 / BZ-01-Abschluss)«. |
| **Indien** | **keine Zone** — »bei delta v halte ich die füße still« | eigener Befehl |
| **Russland · Rest** | keine Zone | kein Weltraumasset im vorliegenden Material |

### 4.2 Earth Surface — Best-of-3, Teilkategorie Militärpunkte

Gerechnet mit `skripte/militaerpunkte.py` aus der BL-01-Startaufstellung
(`bodenlage.py tabelle`, Prüfsumme `19f83738f9e34f86`) und den Qualitätsstufen aus
Übergabe §4, Qualitätsfaktoren nach Z-2d (legacy/modern 1,00 · advanced 1,15 · future 1,40):

| Fraktion | Militärpunkte | Zusammensetzung |
|---|---:|---|
| **USA** | **678,00** | 159 + 177 + 157 + 185, alles legacy/modern |
| China | 574,00 | Heer, SAM und See future (×1,40), Luft legacy |
| EU | 370,00 | alles legacy |
| Russland | 324,60 | Heer future |
| Indien | 257,20 | Heer future, dazu die 9 in Zug 5 gekauften Future-SP |

→ **Die USA gewinnen die Militärpunkte.** Das deckt sich damit, dass sie earthSurface halten.

Die beiden anderen Teilkategorien sind **nicht auswertbar**: Eskalationsdominanz hat kein
Maß (der ganze Regeltext ist ein Satz), und für Infowar fehlt der cyberLevel jeder Fraktion.
Beides steht als Lücke im Journal (RG-Z5-05).

### 4.3 Bodenkampf-Budget-Scoring — davon getrennt (K-4)

`zh01.py vergleich --posten geheimdienste --einsatz IND=611.4,EU=0`:

```
rangliste_t:  IND 611.4  ·  EU 0.0
sieger: IND
wirkung: scored automatisch 1x extra auf der Erde
```

> **Lücke, aber ohne Folge für Zug 5 (RG-Z5-06):** Die Einsätze von China, USA und Russland
> stehen in `work/sv01/` und fehlen. Und es ist ungeregelt, ob ein »Extra-Erd-Scoring«
> überhaupt als Punkt in den Rundenscore eingeht. Beides ändert am Ausgang nichts:
> selbst mit einem Extrapunkt käme Indien auf 1 gegen Chinas 5.

### 4.4 Rundenwertung — `scoring_streak.py`

```
rundenscore: CHN 5 · USA 1 · EU 0 · IND 0 · RUS 0 · REST 0
hoechstwert: 5      spitze: [CHN]
ausgang: "Eindeutiger Rundensieger CHN (+1), alle anderen auf 0"
krieg_gewonnen: {
  fraktion: CHN, auszahlung: "1x gratis forschen auf L1", stufe: L1,
  sofort_timelinefrei: true, zusaetzlich_zur_jahresration: true,
  ansparbar: false, serie_zurueckgesetzt_auf: 0, wars_won_gesamt: 1 }
streaks_nach: CHN 0 · alle anderen 0
warsWon_nach: CHN 1
regel: "references/scoring.md §Siegbedingung (v3.4)"
```

**Wie robust ist das?** Durchgerechnet:

| Rundenscore | Ausgang |
|---|---|
| CHN 5 : USA 1 | China gewinnt den Krieg |
| CHN 4 : USA 1 | China gewinnt den Krieg |
| CHN 2 : USA 1 | China gewinnt den Krieg |
| CHN 1 : USA 1 | Remis an der Spitze — Serie bleibt bei 2 |
| CHN 0 : USA 1 | **USA eindeutiger Sieger — Chinas Serie fällt auf 0** |
| alle 0 | Remis — alle Serien unverändert |

China gewinnt also, sobald es **mindestens zwei** Zonen nimmt. Die EU hätte China
**vier von fünf** Zonen abnehmen müssen, um ein Remis zu erzwingen.

> **Richtigstellung (K-6).** Ich hatte dem Host zur Auswahl gestellt, ein Aussetzen Chinas
> lasse die Serie bei 2 stehen. Das gilt nur, wenn **niemand** scored. Scored allein die
> USA, fällt Chinas Serie auf 0. Die gewählte Linie ist davon nicht berührt.

### 4.5 Was die Siegprämie wert ist

Die Gratis-Forschung ist **ausdrücklich von der Timeline-Sperre ausgenommen**. Die erste
reguläre L1 gibt es nach `research.md` erst **2035**. China bekommt sie **2030** — fünf Jahre
vor allen anderen, zusätzlich zur Jahresration, sofort in derselben Phase 6.
Genau diese Sperre ist der Grund, warum Romans »Yoda-Inspektoren« in Zug 5 nicht forschbar sind.

**Die Wahl der Forschung muss noch in Zug 5 fallen** (nicht ansparbar) — und trifft sie
wegen Andis Abwesenheit der V2-Vertreter. Das ist die schärfste Treuhandfrage des Zuges
und liegt dem Tisch vor.

---

## 5. ERDE-01 — die Erdphase

### 5.1 Indiens verdeckte Kampagne gegen die EU

**Slots:** 85 % Geheimdienste → `Slots = 2 + ⌊85/2⌋ = 44`, gedeckelt auf **8** (Z-2b).
Indien kann also acht Operationen fahren — der Befehl »mit allen Slots« ist damit gedeckt.

**Attribution D-2** (`erde01_engine.py attribution 5 0 2 --ff`), Umfang 5 vom Blatt,
falsche Flagge angekreuzt, EU-Gegenspionage 0 (die EU investiert in Zug 5 **nichts** in
Geheimdienste), Kampagnendauer 2 Züge:

```
{"mechanik": "D-2", "score": 8.6, "admiralty": "D4",
 "falsche_flagge": true, "oeffentlich_erlaubt": false, "eskalation_erlaubt": false}
```

Gegenprobe **ohne** falsche Flagge: `score 11.6 · admiralty B2 · eskalation_erlaubt true`.

**Die falsche Flagge ist der Unterschied zwischen »die EU darf eskalieren« und »die EU darf
nicht einmal öffentlich beschuldigen«.** Sie kostet Jakob 3,0 Punkte auf den Score und hält
die neue Kampagne unter der Zurechenbarkeit.

Schwellenabtastung (Umfang 5, falsche Flagge ja):

| EU-Gegenspionage | 1 Zug | 2 Züge | 3 Züge | 4 Züge |
|---|---|---|---|---|
| 0 | D4 | **D4 ← Zug 5** | C3 | C3 |
| 1 | D4 | C3 | C3 | C3 |
| 2 | C3 | C3 | C3 | **B2** |
| 3 | C3 | **B2** | B2 | B2 |

→ Fährt Indien die Kampagne weiter und baut die EU Gegenspionage auf, kippt die Zurechnung.
Bei Gegenspionage 3 reichen zwei Züge.

**Desinformation (GZ-2)**, `gz01_calc.py desinfo eu --zug=5 --akteur=indien --seed=20305`:

```
p_erfolg 0.39 · Wurf 1W100 = 46 · erfolg: false · druckkonto_zufluss: 0.0
kosten_bip: 0.03
```

→ **Misslungen.** Kein Zufluss ins Druckkonto. Das Ergebnis hängt **nicht** an der
Medienresilienz der EU, die ich nicht kenne: die Erfolgswahrscheinlichkeit ist von ihr
unabhängig, und bei Fehlschlag ist der Zufluss ohnehin null. Die 0,03 % BIP sind bezahlt.

**Nicht gerechnet:** Der Druckstand `indien→eu` aus den Zügen 1–4 fehlt. Ohne Anfangsstand
lässt sich weder der Zerfall (0,25 je Zug, zuerst) noch die erreichte G-Stufe bestimmen
(G1 ab 0 · G2 ab 20 · G3 ab 40 · G4 ab 70). Der Sabotagezufluss von 8 je Erfolg ist gebucht,
der Stand nicht.

### 5.2 Indiens Spionage (Blatt 4)

| Vektor | Ziel | Ergebnis |
|---|---|---|
| **ABWERBUNG (Kopf)** | China, Trägersysteme | `p_op 0.39 · erfolg: false · entdeckt: false · kosten_jb 0.13` — **misslungen, unbemerkt** |
| **BESCHAFFUNG (HUMINT/Cyber)** | USA, Starship | `p_op 0.39 · erfolg: true · 1W20 = 5 · entdeckt: true · p_entdeckung 0.6 · p_blowback 0.45 · kannibalisierung_folgezug 1.0` — **gelungen, aber aufgeflogen** |

**Die USA wissen, dass Indien Starship-Technologie gestohlen hat.** Der Ertrag ist nicht
bezifferbar, weil dafür der Forschungseinsatz E0 der USA auf Starship gebraucht wird — der
steht im fehlenden Zustand. Die Entdeckung hängt davon nicht ab.
Härtung ist mit H0 gerechnet (der einzige belegte Wert, Indiens eigene Angabe auf Blatt 4);
die Härtung der **Ziele** ist unbekannt.

### 5.3 Chinas C-7-Zündung — der fünfte Kaskadenwurf

Regel: `2W10 ≤ 4·IP − 6`. Der IP-Stand liegt im fehlenden Journal — **aber die Geschichte
verrät ihn.** Vier Würfe sind vorbeigegangen:

| IP | Schwelle | p(Kaskade) | P(4× vorbei) |
|---|---|---|---|
| 2,0 | 2,0 | 1,0 % | 96,06 % |
| 2,5 | 4,0 | 6,0 % | 78,07 % |
| 3,0 | 6,0 | 15,0 % | 52,20 % |
| 4,0 | 10,0 | 45,0 % | 9,15 % |
| 5,0 | 14,0 | 79,0 % | 0,19 % |
| 6,0 | 18,0 | 97,0 % | 0,0001 % |

Wäre neben I1 auch **I2** gezündet, läge IP bei 6 bis 8 und die Kaskade bei 97–100 % —
vier Fehlschläge wären dann praktisch unmöglich. **Die aktive Zündung ist I1 allein**
(Decoupling, Handelsanteil 0,20–0,25). Der Wurf:

```
REGEL  : C-7 §3 Kaskadenwurf — 2W10 <= 4*IP-6 => globale Kaskade
WURF   : 2W10 = 7+7 = 14  [seed=50007 zug=5 akteur=china zweck=kaskade ref=C-7]
ERGEBNIS: keine Kaskade in diesem Zug — Zuendung bleibt aktiv, Wurf wiederholt sich naechsten Zug.
```

**14 geht bei jedem IP unter 5 vorbei.** Das Ergebnis ist damit unabhängig davon, welchen
Wert das fehlende Journal genau führt. **Keine globale Wirtschaftskrise in Zug 5.**

### 5.4 Was die Blätter sonst buchen

- **Rechenpunkte:** Alle fünf Fraktionen stehen auf **P0**, der Prüferunterhalt aus
  B-26/HE-23 kostet also niemanden etwas (P1 1 · P2 5 · P3 20 Mrd $/a).
  Die EU teilt ihre 8 RP **nicht zu** — sie laufen leer (DW-01 §2: »nicht zugeteilte RP
  verfallen nicht, wirken aber auch nicht«). Kein Konto T bedeutet nach §2.1
  **kein Jahreswurf** und damit keine Teilnahme an der S-01-Schwelle 2030.
  Indien führt Konto T mit 3 und nimmt teil.
- **Indiens Aufwertung:** `zh01.py aufwertung --fraktion IND --ziel heer --was future` →
  `bd01.qualitaet['heer'] = 'future'`, q 1,40, dauerhaft bis Verlust. Z-2d ist eingehalten
  (genau eine Teilstreitkraft).
- **EU-Rüstungsquote:** NORMATIV gebucht (siehe R-1).

---

## 6. Regellücken, Befunde, Hausentscheidungen

Vollständig in `journal/journal_zug5.jsonl`. Die schweren Punkte:

| ID | Was |
|---|---|
| **RG-Z5-04** | **»Incursion« ist nirgends definiert.** Zwei Regelfundstellen im ganzen Skillsatz, beide nur als Bedingung »Eskalation ≤ Incursion«. Keine der vorhandenen Leitern (ERDE-01 W1–W5, E-2-Doktrinstufen 0–4, PB-01/LB-01 E0–E5, Delta-V-Nuklearkette 1–4) enthält sie. Deine Setzung »Russland ist eine Incursion, solange der Ukraine-Krieg andauert« braucht deshalb drei Angaben: **welche Leiter, welche Sprosse, gemessen für wen.** Bis dahin ist die Force-Projection-Regel nicht auswertbar. In Zug 5 ohne Folge, weil niemand Force Projection gekauft hat. |
| **RG-Z5-05** | Das Best-of-3 ist für **zwei** Seiten geschrieben, die Partie hat **sechs**. Wer vergleicht mit wem? Eskalationsdominanz hat kein Maß, Infowar keine Remisregel. |
| **RG-Z5-06** | Ungeregelt, wie ein »Extra-Erd-Scoring« im Rundenscore zählt — genau der Punkt, an dem laut K-4 zweimal falsch gerechnet wurde. |
| **RG-Z5-03** | E-1 rückwirkend: NPC-Wirtschaft nicht mitgerechnet. |
| **RG-Z5-07** | Was mit einem **nicht abgegebenen Blatt** geschieht, ist nirgends geregelt. Betrifft Zug 5 nicht mehr (Indiens Blätter kamen nach), bleibt aber offen. |
| **RG-Z5-08** | Gültigkeitsdauer **ungespielter Attributionen**: Die EU hält B2 aus Zug 1 und A1 aus Zug 4. Kein Regeltext sagt, ob ein Eskalationsrecht verfällt, kumuliert oder unbefristet gilt. |
| **B-27** | `bodenlage.py` überspringt die Fraktion **REST** (»weder Tafelzeile noch LW-01-Eintrag«), obwohl HE-19 alle sechs Fraktionen an den Vergleichen teilnehmen lässt. |
| **B-28** | `zh01_blattlesen.py` erkennt **V13 nicht**, wenn ein Transfer die eigene Fraktion als Ziel trägt (der Prüfzweig läuft nur bei leerem Ziel). Und das Blatt kann eine Teilhabe nach Z-5.2 gar nicht ausdrücken, weil das Posten-Menü »sprengkopf« nicht kennt — der zugehörige Prüfzweig ist toter Code. |
| **B-29** | `erde01-gm:references/hybrid.md` **existiert nicht**, obwohl GZ-01 an sechs Stellen als maßgeblichen Regelort darauf verweist (G-10 Migration, G-11 Elitenschiene/FIMI). |
| **B-30** | Das Doktrinfeld auf Blatt 1 wird von **keinem Skript gelesen**. |
| **K-6** | Richtigstellung zur Serienregel (siehe §4.4). |

### Zu den Würfen

Die Seed-Registry liegt in `gamestate.json` (`kopf.seed_registry`) und fehlt. Ich habe eine
**Ersatzregistry für Zug 5** verwendet und offengelegt:

| Seed | Wurf |
|---|---|
| `50007` | C-7 Kaskade, Akteur china |
| `20305` | GZ-2 Desinformation indien→eu |
| `50101` | FO-01 Abwerbung IND→CHN |
| `50102` | FO-01 Beschaffung IND→USA |

Sobald das Paket da ist, sind die Würfe aus der echten Registry zu wiederholen. Der
WN-01-Validator weist Seeds außerhalb der Registry mit **V4** zurück — das ist bekannt und
hier bewusst offengelegt statt kaschiert. Zwei der vier Würfe sind gegen diesen Vorbehalt
robust: der Kaskadenwurf geht bei jedem plausiblen IP vorbei, und der Desinfo-Fehlschlag
macht die unbekannte Medienresilienz gegenstandslos.

---

## 7. Was ich vom Tisch brauche

1. **Das Spielstand-Paket** `SCHWARZE_SEE_spielstand_zug5.zip`. Damit werden die vier Würfe
   aus der echten Seed-Registry wiederholt, `wn01_validator.py` läuft, und die drei offenen
   Zahlen (Druckstand indien→eu, cyberLevel, NPC-Budgetanteile) schließen sich.
2. **Roman:** Was bedeutet »38/0«? Steigt die Rüstungsquote auf ANGESPANNT? Welche Zielzone,
   Startmasse und Δv für die Satelliten? Wer ist Geber und Empfänger der nuklearen Teilhabe?
   Welche Attributionsgrundlage gegen Indien — A1, B2 oder neue OSINT? Energiemischung?
3. **Jakob:** Welcher Akteur des Spielstands ist mit »den Arabern« gemeint? Und:
   `de_eskalationsschlag` ist ohne laufenden Krieg ≥ W2 nicht deklarierbar — auf welche Stufe
   geht Indien?
4. **Der Tisch:** Auf welcher Leiter und welcher Sprosse steht »Incursion«?
5. **Die Siegprämie:** Wer wählt Chinas Gratis-Forschung — der V2-Vertreter oder wartet der
   Tisch auf Andi? Nicht ansparbar heißt: sie verfällt, wenn sie in Zug 5 nicht eingelöst wird.
