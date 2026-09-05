# Korrekturen nach Einspielen von `SCHWARZE_SEE_spielstand_zug5.zip`

**Pfade nach §1 neu gepinnt: »gepinnt: 18 Engines«, keine FEHLT-Zeile.**
**`zh01.py pruefe`: 18 von 18 BESTANDEN. `wn01_validator.py`: BESTANDEN (0 Fehler, 0 Warnungen, 3 Hinweise).**

Alle Würfe sind aus der Seed-Registry des Zustands neu gefallen. Was sich dadurch
geändert hat — und was nicht.

---

## Was sich bestätigt hat

| Größe | Vorab | Spielstand |
|---|---|---|
| Ω-Stufe | 0 (abgeleitet) | **0** ✓ |
| Serie China | 2 | **2** ✓ |
| Zonen-Controller | CHN ×5, USA earthSurface | ✓ identisch |
| `groundForces` aller fünf Fraktionen | aus BL-01 rekonstruiert | **exakt identisch** ✓ |
| Qualität je Teilstreitkraft | aus Übergabe §4 | **exakt identisch** ✓ |
| Militärpunkte-Sieger | USA 678 vor China 574 | ✓ unverändert |
| Rundenausgang | China gewinnt den Krieg | ✓ unverändert |
| Kaskade Zug 5 | keine | ✓ unverändert |
| Attributionsgüte Indien→EU | D4 | **D4** (bzw. C3), Eskalationsrecht in **keiner** Lesart ✓ |

---

## Was ich korrigieren muss

### K-7 · Der C-7-Rückschluss war falsch, das Ergebnis nicht

Ich hatte aus vier vorbeigegangenen Würfen geschlossen, es könne nur **I1** gezündet
sein, weil I1+I2 eine Kaskadenwahrscheinlichkeit von 97 % ergäbe. Der Zustand sagt:
**I1 *und* I2 sind gezündet, IP = 2,9** (I1 1,4 + I2 1,5), Schwelle 5,6, p ≈ 10 %.

Mein Denkfehler lag im Handelsanteil: ich hatte 0,20–0,25 angesetzt, der Zustand führt
**0,142**. Damit fällt I1 auf 1,42 und I2 auf 1,5 statt auf 4–6.

Der Wurf mit dem Registry-Seed:
```
EINGABEN: IP=2.9 -> Schwelle 4*IP-6 = 5.6
WURF   : 2W10 = 3+8 = 11  [seed=516033064 zug=5 akteur=china zweck=kaskade ref=C-7]
ERGEBNIS: keine Kaskade in diesem Zug — Zuendung bleibt aktiv.
```
**Keine Kaskade.** Fünfter Wurf ohne Treffer.

### K-8 · Indiens Sabotage GELINGT — den Wurf hatte ich gar nicht gemacht

Das ist die schwerste Lücke meiner ersten Auflösung: Ich habe Attribution, Desinformation
und Spionage gewürfelt, aber **die Sabotageoperation selbst nicht**.

```
{"id": "W-005-0001", "zug": 5, "stufe": "aufloesung", "seed": 20300103,
 "wurf": "W1000", "ergebnis": 232, "zweck": "D-1 Sabotage IND->EU Umfang 5 ff"}
  Schwelle p=0,39 -> Treffer bei <= 390.  Wurf 232 -> ERFOLG
{"id": "W-005-0002", ... "zweck": "PB-01 Aufdeckung Sabotage IND->EU", "ergebnis": 891}
```

**Nach drei Fehlschlägen in Folge (Züge 2, 3, 4) trifft Indien in Zug 5 — und bleibt
unentdeckt.** Die Pipelines fliegen wirklich.

### K-9 · Die Desinformation gelingt ebenfalls

Mit dem Registry-Seed statt meinem Ersatz-Seed: **1W100 = 26 gegen Schwelle 39 → Erfolg**,
Druckkonto-Zufluss **15,3**. Ich hatte einen Fehlschlag gemeldet.

> Die Medienresilienz der EU ist im Zustand **nicht geführt** (es gibt keinen
> `gz01`-Block). Das Skript rechnet mit 0,0. Bei 0,35 wären es 9,9, bei 0,70 nur 4,6.
> Der **Erfolg** hängt nicht daran, die **Höhe des Zuflusses** schon. Bleibt Lücke.

### K-10 · Beide Spionageziele stehen auf Härtung H2, nicht H0

`forschung.fraktionen.USA.haertung = "H2"`, `.CHN.haertung = "H2"`. Ich hatte mit H0
gerechnet, weil auf Indiens Blatt 4 H0 steht — das ist aber Indiens **eigene** Härtung,
nicht die der Ziele. Statt p = 0,39 gilt p = **0,25**.

| Operation | vorab gemeldet | korrekt |
|---|---|---|
| Abwerbung IND→CHN | misslungen, **unentdeckt** | misslungen, **ENTDECKT** — Peking merkt es |
| Beschaffung IND→USA | gelungen, entdeckt | gelungen, entdeckt (unverändert), p_entdeckung 0,76 |

Indien wird also in Zug 5 **von beiden** bestohlenen Mächten bemerkt — von China und von
den USA. In Zug 4 war es nur China.

### K-11 · Die USA gewinnen den Geheimdienstvergleich, nicht Indien

Ich hatte gemeldet, die NPC-Einsätze fehlten. Sie stehen im Zustand unter
`zeughaus.fraktionen.*.dienste.kosten_t` — ich hatte den falschen Schlüssel gelesen.

```
sieger: USA
rangliste_t:  USA 746.4 · IND 611.4 · CHN 280.7 · RUS 151.2 · EU 0.0
wirkung: scored automatisch 1x extra auf der Erde
```

Das »1× extra Erd-Scoring« geht an **Washington**. Am Ausgang ändert es nichts: selbst mit
einem Extrapunkt stünden die USA bei 2 gegen Chinas 5.

### K-12 · Die Attributionsparameter waren falsch geraten — das Ergebnis stimmt trotzdem

Die Kampagne rechnet `gegenspionage` = **Netzstufe des Opfers** (aus den Slots:
≤3→N1 · 4–6→N2 · 7–8→N3) und `zuege` = **1 je Operation**, nicht die Kampagnendauer.
Gegenprobe: Zug 4 wird mit `attribution 5 2 1 --ff` auf **9,8 / C3** exakt reproduziert.

Zug 5, zwei Lesarten:

| Lesart | Score | Güte | öffentlich | Eskalation |
|---|---|---|---|---|
| EU bucht 0 % → 2 Slots → **N1** | 8,8 | **D4** | nein | **nein** |
| EU führt Zug-4-Stand fort (97,2 t, 5 Slots, **N2**) | 9,8 | **C3** | ja | **nein** |

> **Neue Rückfrage an Roman (RG-Z5-10):** Ein leeres Anteilsfeld — heißt das 0 % oder
> »unverändert«? Sein Wort-Dokument sagt »Militärbudget **weiter**«. Davon hängt ab, ob
> Brüssel Neu-Delhi öffentlich benennen darf. **Eskalationsrecht gibt es in keiner der
> beiden Lesarten** — die falsche Flagge hält.

### K-13 · REST steht im Zustand, BL-01 hat es nur übersprungen

`groundForces.REST = {heer 100, luft 100, sam 100, see 100}` mit BL-01-Beleg. Damit gilt:

| | Militärpunkte |
|---|---:|
| USA | **678,00** |
| China | 574,00 |
| **REST** | **400,00** |
| EU | 370,00 |
| Russland | 324,60 |
| Indien | 244,60 |

REST liegt vor der EU. Befund B-27 bleibt bestehen, betrifft aber nur das *Werkzeug*
`bodenlage.py`, nicht den Spielstand.

### K-14 · Indiens 9 Future-SP heben die Stärkepunkte nicht

`zeughaus.fraktionen.IND.aufwertung_zug4` weist bereits 9 Future-SP für 90 t aus —
`groundForces.IND.heer` steht trotzdem unverändert auf 64, bei `qualitaet.heer = future`.
Der Kauf **erhält die Kategorie**, er addiert keine Punkte. Indien bleibt bei **244,60**,
nicht 257,20 wie von mir gemeldet.

### K-15 · Das Druckkonto Indien→EU steht jetzt

Es gab bisher **keinen** `gz01`-Block, Anfangsstand also 0.

```
zufluesse: sabotage 8,0 + einfluss 6,0 + desinformation 15,3 = 29,3
stand_nach: 29.3 · graue_zone_stufe: "G2" · stufe_name: "Kampagne"
schwellen: {spuerbar: true, reagieren_ohne_attribution: false, krise: false}
wirkung_innenunterstuetzung: -1.213 · z_zuschlag_b2: 0.103 -> z_nach: 1.103
befund: "diffuser Druck ohne Urheber"
```

Die EU spürt den Druck, darf aber noch **nicht** innenpolitisch darauf reagieren
(Schwelle 40). Chinas Präferenzkaskaden-Faktor der EU steigt um 0,103.

---

## Zwei neue Befunde an die Skills

| ID | Was |
|---|---|
| **B-32** | `erde01_engine.py wurf` nimmt in der Kommandozeile **weder `--seed` noch `--akteur`** entgegen — anders als `coup`, `kampf`, `schicksal`, `kipp`, die `(zug, akt, sd)` durchreichen. Zwei verschiedene Operationen desselben Zuges würfeln damit identisch; genau der Fehler, vor dem das Modul unter P4-05 selbst warnt. Die Funktion `wurf(..., seed=, zug=, nonce=)` kann es, die CLI reicht es nicht durch. Ich habe die Funktion deshalb direkt aufgerufen. |
| **B-33** | Die Würfe der Züge 2–4 (`work/sv01/ops_zug*.json`, Seeds `5160 3x 0xx`) sind aus dem Material **nicht reproduzierbar**: weder `random.Random(seed)` noch der dokumentierte Generator `_gen(seed, stufe, zug, nonce)` trifft die protokollierten Ergebnisse. Die Replay-Pflicht (WN-01 Pflicht 5) ist für diese Würfe damit nicht erfüllt. Das erzeugende Skript liegt nicht im Paket. |

---

## Nachtrag aus dem Regelwerk-Durchlauf (13 Module)

### K-16 · Militärpunkte zählen rohe Stärkepunkte, nicht qualitätsgewichtete

`scoring.md` Zeile 27, wörtlich: »**Militärpunkte**: Wer mehr konventionelle
**Stärkepunkte** hat«. Kein Qualitätsfaktor. Ich hatte die BD-01-§8-Faktoren
(future 1,40) angesetzt — die gehören in den Gefechtswert für ERDE-01s
Kräfteverhältnis R, nicht in diese Zeile. Zwei Leser sind unabhängig darauf gestoßen.

| | roh (gültig) | gewichtet (mein Fehler) |
|---|---:|---:|
| USA | **678** | 678,00 |
| China | **440** | 574,00 |
| REST | **400** | 400,00 |
| EU | **370** | 370,00 |
| Russland | **293** | 324,60 |
| Indien | **219** | 244,60 |

**Sieger in beiden Lesarten: USA.** Der Ausgang steht, die Zahlen für China, Russland
und Indien waren zu hoch.

### K-17 · C-9 IST aktiv — Romans Ausbaubefehl ist buchbar

Ich hatte gemeldet, »Startkapazitäten ausbauen« habe nach C-9 §9 mitten in einer
laufenden Kampagne keinen Regelweg. Der Spielstand widerlegt das:

```
state.houseRules[0] = {"regel": "C-9 Raumfahrtquote", "rev": "B",
  "geltung": "ab Setup — §9.3 (Zug 1 ungespielt; vier der fünf §9-Einwände entfallen)",
  "q_raum_2026": {"USA": 0.0025, "CHN": 0.001, "EU": 0.0005, ...},
  "kap_2026_t_a": {"USA": 2000.0, "CHN": 400.0, "EU": 45.0, ...},
  "rampendeckel": "aufwärts ×1,25 je Zug (§3.1), abwärts sofort, Hysterese <50 % Peak"}
```

C-9 wurde beim Setup aktiviert. Die EU steht auf **R1 = 0,05 %**. Der Sprungdeckel
lässt eine Stufe je Zug, also auf **R2 = 0,10 %**. Preis nach `ob01.py quote`:

```
{"mechanik": "C-9.2", "delta_pp": 0.05, "wachstumsabzug_pp": 0.042,
 "semantik": "Uebergangsmechanik: Anheben kostet, Halten neutral, Absenken schreibt gut"}
```

**0,042 Prozentpunkte Wachstum, einmalig.** Der Rampendeckel hebt die Startkapazität
höchstens auf 45 × 1,25 = **56,25 t/a**.

> **Am Zug-5-Ausgang ändert das nichts:** Die Kapazität wirkt auf *Starts*, und die
> Startprüfung läuft nach `launch_c2.md` »im Jahr der Fertigstellung (Phase 7 /
> BZ-01-Abschluss)«. Ein in Zug 5 freigegebener Entwurf fliegt in Zug 5 nicht.
> Die EU scored weiterhin keine Zone. **Aber der Befehl ist buchbar** und hätte
> gebucht werden müssen — er ist Romans einzige Weichenstellung gegen China im Orbit.
> Blatt 1 hat dafür kein Feld (C-9 offener Punkt O-15: der sechste Regler fehlt).

### K-18 · Die EU bucht in Zug 5 null Tonnen

ZH-01-Befund zu Romans Blatt 3: außer der zurückgewiesenen Transferzeile steht dort
**kein einziger Einsatz und keine einzige Stückzahl**. Nach Z-1.4 (»Was im Zug nicht
gebucht ist, verfällt«) verfällt damit das **gesamte Bodenkonto von 1 660,5 t** samt
der Tranche von 249,1 t. Das ist keine Strafe, sondern die Haushaltslogik — aber es
gehört Roman vor der Buchung gesagt.

### Offen geblieben: wie viele Operationen sind »alle Slots«?

Der PB-01-Leser liest Jakobs »mit allen Slots« als **acht** Operationen (Slots = 8 laut
`zeughaus.fraktionen.IND.dienste.slots`). Die Kampagnenpraxis der Züge 2–4 ist eine
andere: `work/sv01/ops_zug*.json` führt je Zug **zwei** indische Operationen, nicht acht.
Ich habe nach der Praxis aufgelöst (eine Sabotage Umfang 5 plus zwei Spionagevektoren).
Bei acht Operationen vervielfachte sich der Druckzufluss und Indien stünde statt bei
G2 möglicherweise bei G3. **Rückfrage an Jakob, keine GM-Setzung.**
