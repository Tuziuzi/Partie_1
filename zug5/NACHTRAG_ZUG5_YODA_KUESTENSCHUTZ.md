# Nachtrag Zug 5 — Romans Redaktion und Andis Siegprämie

**06.09.2026 · beide Punkte gebucht**

---

## A. EU / Roman — »Yoda-Inspektoren«, Blatt 4 redigiert

### Was den Befehl wirklich blockiert hat

Ich hatte gemeldet, Yoda sei 2030 nicht forschbar, weil `research.md` die erste
Stufe L1 auf **2035** legt. **Diese Sperre gilt für Yoda gar nicht.**

Ein Inspektorsatellit ist kein Eintrag der L-Leiter, sondern ein **Gerät**.
`bodenschirm-gm/referenz/03_bodenstoerer.md` §9 ordnet die Zuständigkeiten
ausdrücklich zu:

| Wer | Was |
|---|---|
| **NW-01** | die Annäherung, das Lauschen, die Entdeckung des Inspektors, der Treibstoff, das Risiko |
| **OB-01 §3** | der Eskalationsbeitrag des koorbitalen Vorgangs |
| **BS-01** | nur die Umrechnung des erworbenen Wissens in Dezibel am Bodenstörer |

Die L1-Kategorienliste in `research.md` führt Schneller Schiffe bauen ·
Trägersystem-Boost · Met Budget · Anti-Forschung I · Kategorie-Boosts ·
Cyberangriffe — Inspektorsatelliten stehen dort nicht, weil sie dort nicht
hingehören. Sie werden **entworfen, gebaut und geflogen**, nicht freigeschaltet.

**Der echte Blocker war Blatt 4:** kein Projektname, kein Einsatz, keine
Kontenzuteilung. Ohne Einsatz E ist die FO-01-Rate
`p = 1 − exp(−ln2 · (E/E₀_eff)^β · m)` schlicht nicht rechenbar. Das ist das
Bedienproblem, und genau das ist jetzt redigiert.

### Was ich eingetragen habe

```
bf_f_projekt1 = "Yoda-Inspektoren (Inspektorsatellit)"
bf_f_stufe1   = "L1"
bf_f_einsatz1 = "1,0 JB"
```

`fo01_rechner.py rate --einsatz 1.0 --stufe L1`:

```
{"mechanik": "R-1", "stufe": "L1", "e0": 0.25, "einsatz_gesamt": 1.0,
 "e0_effektiv": 0.25, "m": 1.0, "p_erfolg": 0.75,
 "erwartete_zuege": 1.33, "p_in_4_zuegen": 0.99609}
```

**Die Entwicklung läuft ab Zug 5 mit 75 % Erfolgschance je Zug.** Roman kann den
Einsatz jederzeit anders setzen — die Kurve:

| Einsatz | p je Zug | erwartete Züge | p in 4 Zügen |
|---|---|---|---|
| 0,25 JB (= E₀) | 0,500 | 2,00 | 0,938 |
| 0,50 JB | 0,625 | 1,60 | 0,980 |
| 0,75 JB | 0,699 | 1,43 | 0,992 |
| **1,00 JB** | **0,750** | **1,33** | **0,996** |
| 1,50 JB | 0,817 | 1,22 | 0,999 |
| 2,00 JB | 0,859 | 1,16 | 1,000 |

### Was am Zug-5-Ergebnis nicht anders wird

Nichts. Der Tisch hat recht: **geflogen wären sie ohnehin nicht.** `launch_c2.md`
prüft die Startkapazität »im Jahr der Fertigstellung (Phase 7 / BZ-01-Abschluss)«.
Zwischen Forschungserfolg, Entwurf, Bau und Start liegen mehrere Züge. Der
Rundenscore von Zug 5 bleibt CHN 5 : USA 1.

### Was Roman noch liefern muss

1. **Die Zuteilung der 8 Rechenpunkte.** Sie laufen weiter leer. Für die
   Führungsplätze, an denen die Inspektoren später hängen, genügen **0,16 RP**
   auf Konto O (0,02 je gebundenem Slot) — ohne sie steht der Deckungsgrad auf
   null und kostet nach `launch_c2.md` §3.2 **−1 Initiative und −1 auf Duelle
   je zwei fehlende Slots**. Konto F verkürzt zusätzlich die Forschungszeit.
2. **Den Entwurf.** Sobald die Forschung sitzt, braucht es einen Shipyard-Entwurf
   (Masse, Δv, Sensor) und einen BZ-01-Bauauftrag. Erst dann greift die
   Startkapazität von 45 t/a.
3. Die Raumfahrtquote: C-9 ist aktiv, R1 → R2 kostet **0,042 Pp Wachstum**
   einmalig und hebt die Kapazität auf höchstens 56,25 t/a (K-17).

---

## B. China / Andi — Siegprämie: L1 »Küstenschutz«

**Gebucht** als Auszahlung aus »Krieg gewonnen«: sofort in Phase 6, timelinefrei,
zusätzlich zur Jahresration, nicht ansparbar. Damit ist die offene Frage aus dem
Rückgabebrief (§Punkt 5, vom Vertreter durch Schranke abgelehnt) vom Spieler
selbst entschieden.

### Was die Technologie tut

`ereignisse.md` §Schadensfunktion (G-2), wörtlich:

> Aktive Regel: Default `Schaden = 1,2 % · ΔT²` des BIP. […]
> Regional: arm ×1,7 · reich ×0,4. **Anpassung halbiert den Grenzschaden** [QG-13].

Bestätigt in `erde01_regeln.json`: `klima.schaden.anpassung_halbiert_grenzschaden = true`.

Bei der aktuellen Erwärmung von **T = 1,4131 °C** (aus dem Spielstand):

| Block | Faktor | Schaden % BIP | Grenzschaden | mit Anpassung |
|---|---:|---:|---:|---:|
| USA | 0,7672 | 1,838 | 2,602 /°C | 1,301 /°C |
| **China** | 0,7737 | **1,854** | 2,624 /°C | **1,312 /°C** |
| EU | 0,8419 | 2,017 | 2,855 /°C | 1,428 /°C |
| **Indien** | 1,6092 | **3,856** | 5,458 /°C | **2,729 /°C** |
| Russland | 1,5584 | 3,734 | 5,285 /°C | 2,643 /°C |
| Rest | 1,1235 | 2,692 | 3,810 /°C | 1,905 /°C |

In Geld, bei einer Erwärmung von 1,4131 auf 2,0 °C:

| | ohne Anpassung | mit Anpassung | Ersparnis |
|---|---|---|---|
| China | 1,854 % → 3,714 % (+320,0 Mrd/a) | 1,854 % → 2,784 % (+160,0 Mrd/a) | **160,0 Mrd USD/a** |
| Indien | 3,856 % → 7,724 % (+191,6 Mrd/a) | 3,856 % → 5,790 % (+95,8 Mrd/a) | **95,8 Mrd USD/a** |

**Indien ist der am härtesten getroffene Block der Partie** (Faktor 1,6092, der
höchste von sechs). Für Neu-Delhi ist das Geschenk relativ zur Wirtschaftsleistung
fast doppelt so viel wert wie für Peking.

### Die Weitergabe an Indien

FO-01 S-6 **HANDEL/LIZENZ**, `fo01_rechner.py handel --stufe L1`:

```
{"mechanik": "S-6", "kosten_jb": 0.15, "decke_e0": 0.7, "absorption": 1.0,
 "ertrag_jb": 0.175, "politischer_preis": "Buendnisbindung, Auflagen, Sichtbarkeit",
 "entdeckung": false}
```

- Legal, kein Erfolgswurf, keine Entdeckung, keine Attribution.
- Indien zahlt **0,15 Jahresbudget** und erhält **0,175 JB** Ertrag, gedeckelt bei
  **0,70 E₀** — kodifiziertes Wissen vollständig, stillschweigendes Können gar nicht.
- »Nicht mit anderen Fraktionen« ist über die Lizenzauflagen durchsetzbar.

> **Aber der Vorgang selbst ist nicht geheim.** Der politische Preis nennt
> ausdrücklich **Sichtbarkeit**. USA, EU, Russland und Rest sehen, dass Peking und
> Neu-Delhi ein Technologieabkommen geschlossen haben — sie sehen nur nicht den Inhalt.
> Wer den Vorgang verdecken will, braucht einen anderen Weg als eine Lizenz.

> **Und eine Pikanterie, die dem Tisch gehört:** Im selben Zug ist Indiens Versuch,
> einen Kopf aus Chinas Trägerraketenprogramm abzuwerben, **gescheitert und
> aufgeflogen** (K-10). Peking weiß, dass Neu-Delhi es zum zweiten Jahr in Folge
> versucht hat — und verschenkt gleichzeitig seine Klimatechnologie dorthin.

---

## Zwei Vorbehalte, gemeldet statt gefüllt

### RG-Z5-12 · »Küstenschutz« steht nicht im L1-Katalog

`research.md` führt unter »Nicht-kooperative Forschung« (= L1): Schneller Schiffe
bauen · Trägersystem-Boost · Met Budget · Anti-Forschung I · Kategorie-Boosts ·
Cyberangriffe. Klimaanpassung ist kein Eintrag dieser Liste — die L-Leiter ist eine
Raumfahrt-Leiter. Gebucht als **Hausentscheidung des Tisches**, nicht als Regelfolge.

Der Gegengrund, der dafür spricht: Es gibt **keinen anderen definierten Erwerbsweg**
für Anpassung (siehe B-35). Wer sie will, hat regeltechnisch nur diesen.

### B-35 · Die Anpassungsregel hat keinen Erwerbspfad und keinen Code

`klima.schaden.anpassung_halbiert_grenzschaden = true` steht in den Daten,
»Anpassung halbiert den Grenzschaden« steht im Referenztext — aber:

- **Keine Erwerbsregel.** Nirgends steht, was Anpassung kostet, wie lange sie
  dauert, welche Voraussetzung sie hat oder ob sie je Block oder je Region gilt.
- **Kein Codepfad.** `erde01_engine.py klima(T, arm, reich, regional, dT)` kennt
  keinen Anpassungsparameter. Die Halbierung ist in `zug5/skripte/kuestenschutz.py`
  von Hand nach dem Regeltext gerechnet.
- **Unklar, worauf sie wirkt.** »Grenzschaden« ist die Ableitung `2,4 % · ΔT`.
  Ob die Halbierung ab dem Erwerbszeitpunkt gilt (so gerechnet), rückwirkend auf
  das Niveau oder nur auf küstennahe Anteile, sagt keine Regel.

**Befund an die Skillpflege**, und eine Rückfrage an den Tisch, sobald sich die
Erwärmung nennenswert bewegt.
