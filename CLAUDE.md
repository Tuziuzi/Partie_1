# SCHWARZE SEE — bindende Arbeitsregeln

Kampagne Delta V + ERDE-01, jährliche Züge. Jakob ist Gastgeber/GM-Bediener und
spielt Indien. Diese Datei hält fest, was in dieser Partie schon einmal
schiefgegangen ist. Sie ist kein Stilhinweis.

## 0. Vor jeder Buchung: das Gatter laufen lassen

```bash
python3 pruefer/schiffspruefer.py
```

**Kein Zug wird scharf gebucht, solange das Gatter FEHLER meldet.** Es läuft
zusätzlich automatisch beim Sitzungsstart (`.claude/settings.json`). Warnungen
sind zu lesen und zu benennen, nicht stillschweigend zu übergehen.

Die anderen Prüfer bleiben unberührt und laufen weiter mit:
`zh01.py pruefe` (ZH-01) und der WN-01-Validator für `erde01_state_schwarzesee.json`.

## 1. Schiffe: Auslegungsmodus ist eine Behauptung, die belegt werden muss

`construction.md` §Weight Penalty 3, wörtlich:

> Bei einem Schiff mit `customData.designMode: "reconstruction"` (veröffentlichte
> Startmasse eines realen Systems) wird Weight Penalty 3 **nicht** aufgeschlagen.
> **Ohne diese Deklaration gilt der Normalfall.**

Daraus folgt hart:

- **Modus A (Rekonstruktion) nur mit realem Vorbild.** Der Entwurf muss
  `realSystem` UND `realLaunchMass_kg` führen. Eine GM-Buchung, eine Zahl aus
  einem Befehlsblatt oder ein Stub sind **keine** veröffentlichte Startmasse.
  IND_SPADEX darf Modus A (ISRO SDX-01/02, real). Die drei chinesischen
  Entwürfe dürfen es nicht — sie haben kein Vorbild.
- **Modus B (Neukonstruktion) ist der Normalfall.** Dann laufen alle drei Kanäle:
  K1 Strukturabgabe, **K2 Nutzlastmultiplikator**, K3 Hardwaremassen. K2 ist der
  Kanal, der übersehen wird.
  `np = 3 + adv − disadv` · cm: np≥2→np, np=1→2, **np≤0→1 (geklemmt, kein ×3)** ·
  `final = Basis × cm × disc × (1+env)`, dann **×3** ausser `ctxNoHE`.
- **Penalty-Reduktion durch Forschung nur, wenn wirklich beherrscht.**
  L1/L2/L3 = −1/−2/−3, aber L1 wird frühestens **2035** freigeschaltet, L2 ab 2046,
  L3 über S-01 Stufe C oder ab 2058. Vor 2035 gibt es sie also für niemanden.
  `factions.*.research.completedL1/L2/L3` ist die einzige gültige Quelle —
  Hausentscheidungen wie der Küstenschutz zählen nicht.
- **Vorteile und Nachteile werden benannt, nie gezählt.** Nur die 26 bzw. 7
  Presets. Jede Zuschreibung braucht `begruendung` UND `spielwirkung`. Ein
  Vorteil ohne Wirkung ist Zierrat, ein Nachteil ohne Wirkung ist geschenkt.
- **Massenschluss und Ziolkowski müssen halten**, und die gebuchte Startmasse
  darf nie kleiner sein als die konstruierte Nassmasse.

## 2. Verbrauch wird gebucht, nicht erzählt

- **Scoring kostet 1 km/s je Versuch** (`scoring.md` §Grundregeln). Wer eine Zone
  hält, hat dafür bezahlt — die Abschreibung gehört in denselben Zug wie die
  Wertung, nicht in den nächsten.
- **Bauaufträge kosten Werftdurchsatz.** `Kosten = Kaufladenpreis × K(P-Stufe) ×
  K(beta) × K(Rate) × K(Orga)`, bezahlt aus `industrial.capacity_t_year`
  (BZ-01 §1, »Keine neue Währung«). Jeder `bz01.bauplan`-Eintrag führt
  `werft_gebucht_t`. **Offen seit Zug 1 für alle Fraktionen** (Journal Z5-070) —
  ab Zug 6 verbindlich.
- **Bestand = Buchungssumme.** C2-Slots, Konten, Zähler: wenn die Wirkung
  gebucht ist, muss die Herkunft mitgebucht sein. `slots_total` ohne
  `geo_relays` war genau dieser Fehler.

## 3. Rechnen

Jede Zahl kommt aus einem Skript, nie aus dem Kopf und nie aus dem Gedächtnis.
Regelinstanzen: `bz01_calc.py` (Bauzeiten), `nachbau.py` (Massenmodell),
`zh01.py` (Bodenkonto), `scoring_streak.py` (Serie). Regelstellen werden vor der
Anwendung nachgelesen und wörtlich zitiert, nicht erinnert.

## 4. Was wo liegt

- `stand/` ist **gitignoriert** — der Arbeitsstand lebt nur im Container.
  Alles Bewahrenswerte gehört in `SCHWARZE_SEE_spielstand_zug<N>.zip` und ins Repo.
- `Ships/` Konstruktionen und `ship_export`-Dateien.
- `pruefer/` das Gatter aus Abschnitt 0.
- `zug<N>/journal/` das Zugjournal; Befunde werden dort abgelegt, nicht nur im Chat.

## 5. Vertraulichkeit

Befehlsblätter sind vertraulich gegenüber Mitspielern — **einschliesslich des
Freitextes**. SITREPs sind asymmetrisch und tragen nie, was eine Fraktion nicht
wissen kann. Die Veröffentlichungspflicht der Demokratien betrifft die **Werte**,
nie die Absicht: die Summe wird bekannt, der Zweck nicht.
