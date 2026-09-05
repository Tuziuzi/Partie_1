# ÜBERGABE — SCHWARZE SEE in einer neuen Sitzung fortsetzen

**Stand: Zug 4 (2029) gebucht · Zug 5 (2030) offen, Blätter ausgegeben** · 05.09.2026, Rev. E

---

## 0. Der kürzeste Weg

1. `SCHWARZE_SEE_spielstand_zug5.zip` in die neue Sitzung hochladen und auspacken.
2. **Pfade neu pinnen** (§1) — der einzige Pflichthandgriff.
3. Ausgefüllte Blätter hochladen, »Zug 5 auflösen« sagen.

Vorher offen: **fünf Entscheidungen aus KB-02** (§6). Die erste davon ändert die
gedruckten Bodenkonten auf zwei der neun Blätter — wenn du sie rückwirkend
entscheidest, müssen EU und Indien neu gedruckt werden, bevor gespielt wird.

---

## 1. Pfade neu pinnen (Pflicht)

`config.json` trägt absolute Pfade und sha256-Pins der alten Sitzung. Der
Skill-Ordner heißt in jeder Sitzung anders. Einmal ausführen, im Ordner mit
`gamestate.json`:

```bash
python3 - <<'PY'
import json, hashlib, pathlib, glob
S = pathlib.Path(sorted(glob.glob("/root/.claude/skills/synced/*/"))[0])
WS = pathlib.Path(".").resolve()
c = json.loads((WS/"config.json").read_text(encoding="utf-8"))
c["workspace"] = str(WS)
for k, d in (("deltav","deltav-game-master"), ("erde01","erde01-gm"),
             ("lagewerk","lagewerk"), ("ob01","orbitalbruecke-gm"),
             ("shipyard","shipyard-designer"), ("werkbuch","werkbuch-bauzeiten"),
             ("zeughaus","zeughaus-gm"), ("denkwerk","denkwerk-compute"),
             ("eichwerk","eichwerk-ksn"), ("bodenbruecke","bodenbruecke-gm"),
             ("neuzeug","neuzeug-gm"), ("forschungswerk","forschungswerk-fue"),
             ("fremdwerk","fremdwerk-etz"), ("implosion","implosion-wirtschaftswaffe"),
             ("geistwerk","geistwerk-verstand")):
    c["skill_verzeichnisse"][k] = str(S/d)
# ACHTUNG: vier Pfade weichen vom Schema ab — erde01_patch liegt im LAGEWERK,
# fo01 unter »skripte« (nicht scripts), ew01 heisst ew01_rechner, ge01 im GEISTWERK.
REL = {"deltav_engine":"deltav-game-master/scripts/deltav_engine.py",
       "orbital":"deltav-game-master/scripts/orbital_mechanics.py",
       "resolve_round":"deltav-game-master/scripts/resolve_round.py",
       "erde01_engine":"erde01-gm/scripts/erde01_engine.py",
       "eh01":"erde01-gm/scripts/eh01.py",
       "wn01_validator":"erde01-gm/scripts/wn01_validator.py",
       "erde01_patch":"lagewerk/scripts/erde01_patch.py",
       "ob01":"orbitalbruecke-gm/scripts/ob01.py",
       "lw01":"lagewerk/scripts/lw01.py",
       "bz01":"werkbuch-bauzeiten/scripts/bz01_calc.py",
       "zh01":"zeughaus-gm/scripts/zh01.py",
       "zh01_blatt":"zeughaus-gm/scripts/zh01_blatt.py",
       "zh01_blattlesen":"zeughaus-gm/scripts/zh01_blattlesen.py",
       "dw01":"denkwerk-compute/scripts/dw01.py",
       "nz01":"neuzeug-gm/scripts/nz01.py",
       "fo01":"forschungswerk-fue/skripte/fo01_rechner.py",
       "ew01":"eichwerk-ksn/scripts/ew01_rechner.py",
       "ge01":"geistwerk-verstand/scripts/ge01.py"}
fehlt = []
for n, rel in REL.items():
    p = S/rel
    if not p.exists(): fehlt.append(f"{n} -> {p}"); continue
    c["engines"][n] = {"pfad": str(p),
                       "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
(WS/"config.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
print("gepinnt:", len(c["engines"]), "Engines ·", S)
if fehlt:
    print("NICHT GEFUNDEN — Pfad im Skillordner suchen und hier eintragen:")
    for x in fehlt: print("  ", x)
PY
```

Muss **»gepinnt: 18 Engines«** ohne eine einzige FEHLT-Zeile ausgeben. Erscheint
eine, hat der Skillordner die Datei verschoben — dann
`find $S -name "<dateiname>"` und den Pfad in `REL` korrigieren.

Danach Gegenprobe: `python3 $S/zeughaus-gm/scripts/zh01.py pruefe` muss
**18 von 18 BESTANDEN** liefern.

---

## 2. Wer ist wer

| Rolle | Person | Fraktion | Autonomie |
|---|---|---|---|
| Host / GM-Operator | **Jakob** | spielt zugleich **Indien** | Mensch |
| Spieler | **Andi** | **China** | Mensch |
| Spieler | **Roman** | **EU** | Mensch, in Zug 2 und 4 vertreten (SV-01 V2) |
| NPC | — | USA · Russland · Rest | zuletzt **A3** (HE-22: Profilvektor aus der Befehlshistorie) |

Der GM (die Sitzung) ist **Spielleiter**, nicht Mitspieler. Jakob ist zugleich
Auftraggeber und Spieler — bei Indien-Entscheidungen also sauber trennen:
Regelfragen beantwortet der GM, Indien-Befehle kommen von Jakob als Spieler.

---

## 3. Arbeitsweise — bindend

Diese Punkte sind über vier Züge gewachsen und stehen nicht zur Disposition:

1. **Jede Zahl kommt aus einem Skript.** Kein Schätzen, kein Kopfrechnen. Würfe
   über Python mit gesetztem Seed, Wurf und Schwelle ins Journal.
2. **Regellücken werden gemeldet, nicht gefüllt.** Wörtlich: »Umgehung ist kein
   Fix, und Regellücken werden gemeldet, nicht gefüllt.« Wenn eine Regel
   schweigt, kommt ein `regelluecke`-Eintrag ins Journal und die Frage an den
   Tisch — keine stille GM-Setzung.
3. **Befunde an den Skills** (`befund`, B-nn) werden ebenso journalisiert, auch
   wenn sie den GM selbst betreffen. B-23 und B-26 hat Jakob angestoßen.
4. **SITREPs sind asymmetrisch.** Jede Fraktion bekommt nur, was sie wissen
   kann. Verdecktes (S-01-Prämisse, F-01-Kaskade, EW-01-Hauptbuch, fremde
   Würfe) gehört **nie** in einen SITREP.
5. **Ausgabe wörtlich.** Skriptausgaben werden zitiert, nicht paraphrasiert.
6. **Dateinamen mit Spielernamen** (`ANDI_CHINA_*`, `ROMAN_EU_*`,
   `JAKOB_INDIEN_*`) — nach der Blattverwechslung in Zug 4 vereinbart.
7. Vor jeder Buchung ein **Snapshot** nach `snapshots/`.

---

## 4. Wo die Partie steht

**Jahr 2030 · Runde 4 abgeschlossen · Zug 5 offen · Phase `setup`.**

### Scoring

| | Zonen | Serie |
|---|---|---|
| **China** | LEO · MEO · HEO · SSO · GEO | **2** — noch **eine** Runde bis »Krieg gewonnen« |
| USA | earthSurface | 0 |
| EU · Indien · Russland · Rest | — | 0 |

»Krieg gewonnen« zahlt einen freien Forschungsdurchbruch, timelinefrei. **Das
ist die dringendste Lage der Partie.**

### Wirtschaft (Ende 2029)

China 15,0587 · EU 19,1162 · Indien 4,0870 Bio USD.
Alle drei schrumpfen seit 2026 in jedem Jahr — das ist **RG-Z5-01**, siehe §6.

### Bodenkonten Zug 5 (gebucht, HE-15 BIP-gekoppelt)

| | Ausgaben | Konto | Tranche | Vortrag 2030 |
|---|---|---|---|---|
| China | 266,5 Mrd | 2 232,5 t | 334,9 t | 334,0 t |
| EU | 334,4 Mrd | 1 602,6 t | 240,4 t | 45,0 t |
| Indien | 81,9 Mrd | 601,0 t | 90,2 t | 40,0 t |
| USA (NPC) | 997,0 Mrd | 7 463,6 t | 1 119,5 t | 2 000,0 t |
| Russland (NPC) | 149,0 Mrd | 1 079,8 t | 162,0 t | 100,0 t |

Chinas Vortrag ist erstmals gekürzt: 66 t sind 2029 geflogen (Z-1.5).

### Stand je Fraktion

| | Doktrin | Arsenal | Qualität | RP / Prüfer |
|---|---|---|---|---|
| China | `ambiguitaet` | 726 (+50 in Indien) | Heer · SAM · Marine **future**, Luft legacy | 20 / **P0** |
| EU | keine erklärt | 290 | alle **legacy** | 8 / P0 |
| Indien | `de_eskalationsschlag` (oberste Stufe) | 199 | Heer **future** | 3 / P0 |
| USA | — | 3 700 | SAM modern | 55 / **P0** |
| Russland | `de_eskalationsschlag` | 4 309 | Heer future | 1 / P0 |

### Was in Zug 5 mitläuft

- **Chinas C-7-Zündung ist weiter aktiv** — fünfter Kaskadenwurf fällig.
  Vier Würfe sind bisher vorbeigegangen.
- **Chinas Präferenzkaskade (B-2) ist in Zug 4 eingetreten.** Die Bias-Funktion
  ist gebrochen: Andi liest ab sofort dieselben Zahlen wie der GM.
- **Kapitalmarktausschluss China** läuft bis Zug 11 (bzw. Zug 4+4, wenn
  Entscheidung E-2 aus §6 fällt).
- **Zwei ungespielte Attributionen der EU gegen Indien**: B2 aus Zug 1,
  A1 aus Zug 4 (Rammversuch, Eskalationsrecht).
- **Reale Satelliten sind Bahnobjekte** (HE-21) und angreifbar.
- Chinas zwei Aufklärer decken **jedes Bahnobjekt bis GEO** auf.

---

## 5. Blätter Zug 5 — ausgegeben

In `blaetter/zug5/`, je Spieler drei PDFs (ausfüllbare Formulare):

- `Befehlsblatt_<NAME>_Zug5.pdf` — Blatt 1/2, ERDE-01-Befehle
- `Blatt3_BODEN_<NAME>_Zug5.pdf` — ZH-01, Bodenkonto gedruckt (VORGABE)
- `Blatt4_RECHENWERK_<NAME>_Zug5.pdf` — DW-01, Bestand und Prüfer gedruckt

Gelesen werden sie mit:
```bash
python3 $S/zeughaus-gm/scripts/zh01_blattlesen.py blaetter/zug5/Blatt3_*.pdf
python3 $S/erde01-gm/scripts/blattlesen.py <Befehlsblatt.pdf>
```

**Neu erzeugen** (falls eine Entscheidung aus §6 die VORGABE ändert):
```bash
S=<Skillordner>
python3 $S/zeughaus-gm/scripts/zh01_blatt.py --fraktion EU --zug 5 \
  --gamestate gamestate.json --lagewerk $S/lagewerk/daten/konventionell_2026.json \
  --c2 NORMATIV --w-index 1.0 --erde01 $S/erde01-gm \
  --konto-t <KONTO> --tranche-t <TRANCHE> --aus blaetter/zug5
python3 work/blatt4_rechenwerk.py --fraktion EU --zug 5 \
  --erde01 $S/erde01-gm --gamestate gamestate.json --aus blaetter/zug5
python3 $S/erde01-gm/scripts/befehlsblatt.py --zug=5 --staaten=china,eu,indien
```
`--doktrin` nur setzen, wo eine Stufe erklärt ist: China `ambiguitaet`,
Indien `de_eskalationsschlag`, EU **keine**. Danach die Dateien aus
`$S/erde01-gm/spielmaterial/` auf Spielernamen umbenennen.

---

## 6. Fünf offene Entscheidungen (KB-02)

Der Forschungsbericht `forschung/wachstumsbuch/KB-02_WACHSTUMSBUCH.md` liegt
im Paket (Hauptbericht + sechs Anhänge, ~200 Quellen). **Nichts davon ist
gebucht.** Zu entscheiden:

**E-1 · Basiswachstumspfad ab Zug 5 oder rückwirkend.**
ERDE-01 bemisst jeden Schock in Prozentpunkten der *Wachstumsrate*, definiert
aber keine Basisrate — in dieser Kampagne wurde die Lücke mit null gefüllt.
Tafelwerte 2025–30: China 4,3 · EU 1,2 · Indien 6,5 %/a.

| | Ist 2029 | rückwirkend | Bodenkonto Zug 5 Ist | rückwirkend |
|---|---|---|---|---|
| China | 15,0587 | 17,2064 | 2 232,5 t | 2 503,1 t |
| EU | 19,1162 | 19,8235 | 1 602,6 t | **1 660,5 t** |
| Indien | 4,0870 | 4,9523 | 601,0 t | **719,3 t** |

**Rückwirkend heißt: Blatt 3 für EU und Indien neu drucken, bevor gespielt wird.**
Chinas Blatt ebenfalls. Die Budgetvergleiche der Züge 2–4 bleiben stehen.

**E-2 · Schockform umstellen** (Niveau statt Dauerrate, mit Erholungsregel).
Betrifft den EU-Handelsabbruch, Chinas Kapitalmarktausschluss (3+4 statt 10
Züge) und die I2-Bankenkrise. Empfehlung: ab Zug 5, nicht rückwirkend.

**E-3 · EH-01-Deckel und Beschleunigungsleiter.** Gehört an den
Skill-Maintainer, nicht in die Kampagne — in vier Zügen hat kein Block seinen
Zubaudeckel erreicht.

**E-4 · SAEED 1,10 ersetzen** (Rüstung → Wachstum). Keine Rückwirkung, C-3 hat
nie gefeuert.

**E-5 · DW-01-Zivilkonto** (KI-Wachstumsbeitrag) auf die sättigende Formel mit
J-Kurve. Empfehlung: ab Zug 5.

Dazu **§8 des Berichts: Nahtstelle zur Singularität.** Drei Regime R0/R1/R2,
vier aufgelöste Kollisionen mit S-01, Energiedecke. Die Kampagne steht in R0;
die P10 des S-01-Schwellenjahrs ist 2031, der Jahreswurf läuft ab 2035 mit
Gate ×0,35 davor.

---

## 7. Offene Regellücken und Befunde

| ID | Was |
|---|---|
| **RG-Z4-01** | Wie tief schneidet eine B-2-Präferenzkaskade? Die −2,0 Pp sind eine GM-Bemessung ohne Regeltafel, ausdrücklich revidierbar. |
| **RG-Z5-01** | ERDE-01 hat keinen Basiswachstumspfad (→ E-1). |
| **B-26 / HE-23** | Prüferunterhalt (DW-01 §9.1) war nie gebucht. Verfall ist ab Zug 5 gebucht, **nicht rückwirkend**: USA P2→P0, China P3→P0. Ab Zug 5 gehört der Unterhalt als Wirtschaftsposten auf Blatt 4 (P1 1 · P2 5 · P3 20 Mrd $/a). |
| **B-24** | DW-01 Rundenablauf Schritt 2 (Energie-/Wasserlast an EH-01 melden) wurde nie ausgeführt. Gegenprobe P-Z5-01: der Bestand von 100 RP weltweit ist **richtig** — Compute-Zubau ist ein Kaufakt, niemand hat je gebaut. |
| **B-25** | ZONENFAKTOR kennt kein HEO; Sammelzonen-Strings werden still übersprungen. Bauplan-Einträge einzeln je Zone führen. |
| **B-19 / B-20 / B-21** | Hausformulare in `work/` umgehen bekannte Skriptfehler (SITREP-Filter, Postfach-Zugfilter, Float-Vergleich). Nicht entfernen. |

Vollständige Liste: `journal.jsonl` (104 Einträge), Typen `regelluecke`,
`befund`, `hausentscheidung` (HE-9…HE-23), `korrektur` (K-2…K-5).

---

## 8. Was im Paket liegt

```
gamestate.json                  Delta-V-Spielstand (Zonen, Scoring, Zeughaus, Compute)
erde01_state_schwarzesee.json   ERDE-01 (Wahrheit, Glauben, Postfach, Audit)
config.json                     Pfade + sha256-Pins  ← §1 neu setzen
journal.jsonl                   104 Einträge, die vollständige Regelgeschichte
blaetter/zug5/                  neun ausgegebene Blätter Zug 5
sitreps/                        SITREPs Zug 2–4, je Spieler
work/                           Hausformulare und -skripte (B-19/B-20/B-23-Fixes)
work/sv01/                      NPC-Befehlssätze, SITREP-Filter, Profilhistorien
snapshots/ · saves/             Rücksprungpunkte je Zug
forschung/wachstumsbuch/        KB-02 + sechs Anhänge + Prüfrechnung
UEBERGABE_ZUG5.md               dieses Dokument
BEFUNDLISTE_Skillpflege.md      offene Punkte an den Skills (für Codex)
```

Die Blätter der Züge 1–4 sind **nicht** im Paket (verbraucht). Wer sie braucht:
`blaetter/zug2` … `zug4` in der alten Sitzung.

---

## 9. Ablauf einer Auflösung (bewährt)

1. Snapshot nach `snapshots/gamestate_vor_zugN.json` und
   `erde01_vor_zugN.json`.
2. Blätter lesen (`zh01_blattlesen.py`, `blattlesen.py`), Findings V11–V20
   prüfen — **stille Kürzungen sind verboten**, Abweichungen kommen als Befund
   zurück.
3. NPC-Züge nach SV-01 erzeugen (Stufe mit Jakob klären: A2/A3/A4).
4. ERDE-01-Postfach aufbauen — **mit Zugfilter** (B-20: alte Befehle nach
   `archiv` verschieben, sonst greifen Vorjahresbefehle erneut).
5. `eh01.py spiel zug` · `resolve_round.py run` · Fachmodule.
6. Scoring: Earth Surface **Best-of-3** (Militärpunkte / Eskalationsdominanz /
   Infowar via cyberLevel) — **getrennt** vom Bodenkampf-Budget-Scoring
   (Geheimdienste / Force Projection / Modernisierung), das eigene
   Extra-Erd-Scorings vergibt. Diese Trennung wurde zweimal falsch gemacht
   (K-4). Alle sechs Fraktionen nehmen an den Tonnenvergleichen teil (HE-19).
7. `wn01_validator.py` (muss BESTANDEN), B-18-Wächter, `zh01.py pruefe`.
8. `resolve_round.py finalize`, Journal schreiben, Save nach `saves/`.
9. Drei asymmetrische SITREPs schreiben, dann Blätter für den Folgezug.

---

## 10. Vokabular

**Vortrag** = nicht geflogene Startkapazität des Vorjahrs, fließt ins Bodenkonto
(Z-1.3). **Tranche** = Hochtechnologie-Deckel, 15 % des Bodenkontos, verfällt
ungenutzt. **VORGABE** = gedruckter Standwert auf dem Blatt, vom Spieler nicht
zu ändern. **Prüfer P0–P3** = Instanz, die synthetische Trainingsdaten
beurteilen kann. **g_T** = Compute-Gate der KI-Führung. **Ω (Omega)** =
Skalenstufe der Ω-Leiter (WN-02). **JB** = Jahresbudget der Forschung.
