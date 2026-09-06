# Zug 5 — Quellenlage (was belegt ist und was fehlt)

## A. Im Repository vorhanden
| Datei | Inhalt |
|---|---|
| `UEBERGABE_ZUG5.md` | Stand nach Zug 4, Rev. E — §4 Scoring/Wirtschaft/Bodenkonten/Arsenale |
| `START_PROMPT_NEUER_CHAT.txt` | Rollen, vier bindende Arbeitsregeln |
| `Befehlsblatt_ROMAN_EU_Zug5 (1).pdf` | EU Blatt 1/2, ausgefüllt (6 Befehle, Regler) |
| `Blatt3_BODEN_ROMAN_EU_Zug5 (1).pdf` | EU Blatt 3 ZH-01, ausgefüllt + VORGABE-Keywords |
| `Blatt4_RECHENWERK_ROMAN_EU_Zug5 (2).pdf` | EU Blatt 4 DW-01/FO-01, ausgefüllt |
| `Entscheidungen von Europa für Zug 5.docx` | Romans Klartext-Befehle (auf Blatt 3 für verbindlich erklärt) |
| `Zug 5 Indien.docx` | Jakobs Indien-Befehle |

## B. NICHT im Repository (laut UEBERGABE §8 Pflichtbestandteil des Pakets)
`gamestate.json` · `erde01_state_schwarzesee.json` · `config.json` · `journal.jsonl` (104 Einträge)
`work/` (Hausformulare B-19/B-20/B-23) · `work/sv01/` (NPC-Befehlssätze, Profilhistorien)
`sitreps/` · `snapshots/` · `saves/` · `blaetter/zug5/` (China- und Indien-Blätter) · `forschung/wachstumsbuch/`

Folge: `resolve_round.py`, `erde01_engine.py`, `eh01.py spiel zug`, `wn01_validator.py`
und `zh01.py pruefe` können **nicht gegen den echten Stand** laufen. Alles, was unten
gerechnet wird, ist aus A. plus Skill-Kanondaten abgeleitet und als solches markiert.

## C. Belegte Zahlen (Quelle in Klammern)
- Scoring: China LEO·MEO·HEO·SSO·GEO, Serie **2**; USA earthSurface, Serie 0; EU/Indien/Russland/Rest 0 (UEBERGABE §4)
- Wirtschaft Ende 2029: China 15,0587 · EU 19,1162 · Indien 4,0870 Bio USD (UEBERGABE §4)
- Bodenkonten Zug 5: China 2232,5 t (Tranche 334,9) · EU 1602,6 t (240,4) · Indien 601,0 t (90,2) ·
  USA 7463,6 t (1119,5) · Russland 1079,8 t (162,0) (UEBERGABE §4; EU zusätzlich aus PDF-Keywords ZH01VORGABE)
- Arsenale: China 726 (+50 in Indien) · EU 290 · Indien 199 · USA 3700 · Russland 4309 (UEBERGABE §4)
- Qualität: China Heer/SAM/Marine future, Luft legacy · EU alle legacy · Indien Heer future ·
  USA SAM modern · Russland Heer future (UEBERGABE §4)
- RP/Prüfer: China 20/P0 · EU 8/P0 · Indien 3/P0 · USA 55/P0 · Russland 1/P0 (UEBERGABE §4; EU aus Blatt 4)
- Doktrinen: China `ambiguitaet` · Indien `de_eskalationsschlag` · EU keine erklärt (UEBERGABE §4);
  EU-Blatt trägt `status_quo` ein (Befehlsblatt-Feld eu_doktrin)
- EU-Latenz L3 (PDF-Keywords ZH01VORGABE)

## D. Unbelegt / offen (nicht geraten, sondern gemeldet)
- Delta-V-Flottenbestand, Bahnobjekte, Δv-Vorräte aller Fraktionen
- cyberLevel je Fraktion (Infowar-Teil des Earth-Surface-Best-of-3)
- Eskalationsstufen je Fraktionspaar (außer Russland, siehe unten)
- Implosionspunkte-Stand Chinas C-7-Zündung
- Geheimdienst-/Force-Projection-/Modernisierungs-%-Sätze der NPCs
- Stärkepunkte je Schauplatz (BD-01 groundForces)
- Profilvektoren aus `work/sv01/` (für V2-Vertretung Chinas und die NPC-Züge)

## E. Ukraine / Russland
Kein Eintrag im vorliegenden Material beendet den Krieg in der Ukraine; die EU führt in Zug 5
"harte Sanktionen gegen Moskau fortsetzen". Der Host hat für Zug 5 ausdrücklich gesetzt:
**Russland steht, solange der Krieg andauert, auf Eskalationsstufe "Incursion".**
Das ist die Eingangsgröße für die Force-Projection-Regel des Erd-Scorings.
