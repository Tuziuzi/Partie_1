#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RF-01 — Rückfragen als ausfüllbares Formular mit Kopierblock.

Tischwunsch vom 25.11.2026 (Journal Z6-051): Rückfragen sollen wie die Befehlsblätter Felder zum Ausfüllen
haben; die Antworten kommen als kopierbarer Block zurück und laufen durch den Befehlsprüfer (CLAUDE.md §6).

Eingabe: eine Formularbeschreibung (JSON oder Python-dict, siehe BEISPIEL). Ausgabe: eine HTML-Datei, die
  * jede Frage mit ihren Feldern zeigt (Text, Zahl, Auswahl, Ja/Nein; 16-px-Felder, damit das iPhone nicht zoomt),
  * einen Knopf »Antworten kopieren« hat, der den Block erzeugt
        --- ZH01-ANTWORT ANFANG ---
        {"schema": "zh01-antwort/1", "fraktion": …, "zug": …, "bezug": <Dateistamm>, "felder": {…}}
        --- ZH01-ANTWORT ENDE ---
  * leere Felder weglässt (wie die Befehlsblätter),
  * den Entwurf nur im eigenen Browser zwischenspeichert (Bequemlichkeit, nie Spielstand),
  * die Feldliste als <script id="rf01-felder" type="application/json"> trägt — daraus liest der
    Befehlsprüfer, welche Felder es gibt (AB-6 a: ein unbekanntes Feld wird abgewiesen).

    python3 werkzeuge/rueckfrage_formular.py <beschreibung.json> <ausgabe.html>
"""
import html
import json
import os
import sys

SCHEMA = "zh01-antwort/1"

STIL = """
<style>
:root {
  --papier: #F2F4F3; --karte: #FFFFFF; --tinte: #17202A; --grau: #56616B; --linie: #D3D9DC;
  --akzent: #22456A; --gilt: #1D6646; --gilt-bg: #E2F0E8; --nicht: #A3302B; --nicht-bg: #F6E3E1;
  --frage: #835600; --frage-bg: #F5ECD8; --feld: #FFFFFF;
  --display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --text: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --papier: #11161B; --karte: #182027; --tinte: #E5E9EC; --grau: #98A4AE; --linie: #29323A;
  --akzent: #8DB3DC; --gilt: #72CFA0; --gilt-bg: #15302A; --nicht: #F0897F; --nicht-bg: #3A1D1B;
  --frage: #E7B65C; --frage-bg: #33280F; --feld: #0F1418; color-scheme: dark; } }
:root[data-theme="dark"] {
  --papier: #11161B; --karte: #182027; --tinte: #E5E9EC; --grau: #98A4AE; --linie: #29323A;
  --akzent: #8DB3DC; --gilt: #72CFA0; --gilt-bg: #15302A; --nicht: #F0897F; --nicht-bg: #3A1D1B;
  --frage: #E7B65C; --frage-bg: #33280F; --feld: #0F1418; color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--papier); color: var(--tinte); font-family: var(--text); font-size: 16px; line-height: 1.55; margin: 0; }
.rahmen { max-width: 44rem; margin: 0 auto; padding-block: 1.25rem 7rem;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 1.5rem; }
.leiste { font-family: var(--mono); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--grau); border-top: 3px solid var(--akzent); padding-top: .5rem; display: flex; flex-wrap: wrap; gap: .25rem 1rem; }
.leiste .vs { color: var(--nicht); font-weight: 600; }
h1 { font-family: var(--display); font-weight: 600; font-size: clamp(2rem, 7vw, 2.6rem); line-height: 1.05; margin: .6rem 0 0; }
h2 { font-family: var(--display); font-weight: 600; font-size: 1.4rem; line-height: 1.15; margin: 0 0 .5rem; }
.unter { color: var(--grau); margin: .35rem 0 0; }
.frage { background: var(--karte); border: 1px solid var(--linie); border-radius: 6px; padding: 1rem 1rem 1.1rem;
  display: flex; flex-direction: column; gap: .7rem; }
.frage .nr { font-family: var(--mono); font-size: .72rem; color: var(--grau); letter-spacing: .06em; }
.frage p { margin: 0; }
label.f { display: flex; flex-direction: column; gap: .3rem; }
.lab { font-weight: 600; font-size: .95rem; }
.hilfe { font-size: .85rem; color: var(--grau); }
input[type=text], input[type=number], select, textarea {
  font: inherit; font-size: 16px; color: var(--tinte); background: var(--feld); border: 1px solid var(--linie);
  border-radius: 5px; padding: .6rem .65rem; width: 100%; min-height: 44px; }
textarea { min-height: 5.5rem; resize: vertical; }
.jn { display: flex; gap: .5rem; flex-wrap: wrap; }
.jn label { display: inline-flex; align-items: center; gap: .4rem; border: 1px solid var(--linie); border-radius: 5px;
  padding: .5rem .8rem; min-height: 44px; background: var(--feld); }
.befehlsform { border-left: 3px solid var(--nicht); background: var(--nicht-bg); padding: .7rem .85rem; border-radius: 0 5px 5px 0; font-size: .93rem; }
.kenntnis { margin: 0; padding-left: 1.2rem; display: flex; flex-direction: column; gap: .5rem; }
.leiste-unten { position: fixed; left: 0; right: 0; bottom: 0; background: var(--karte); border-top: 1px solid var(--linie);
  padding: .7rem max(16px, env(safe-area-inset-right, 0px)) calc(.7rem + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px));
  display: flex; gap: .6rem; justify-content: center; }
button { font: inherit; font-weight: 600; border-radius: 6px; border: 1px solid var(--akzent); min-height: 44px; padding: .55rem 1rem; cursor: pointer; }
button.haupt { background: var(--akzent); color: var(--papier); }
button.neben { background: transparent; color: var(--akzent); }
#ausgabe { display: none; flex-direction: column; gap: .5rem; }
#ausgabe.offen { display: flex; }
#ausgabe textarea { font-family: var(--mono); font-size: 13px; min-height: 12rem; }
#meldung { font-size: .9rem; color: var(--gilt); min-height: 1.2em; }
.fuss { font-size: .82rem; color: var(--grau); border-top: 1px solid var(--linie); padding-top: .8rem; }
</style>
"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600'
         '&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&display=swap">')

BEFEHLSFORM = ("<b>Antworten bitte als Wunsch.</b> »Ich möchte …«, »China soll …«, »gegen das Rechenzentrum« — nicht "
               "»China hat …« oder »der Tisch hat beschlossen …«. Ein Befehl bestimmt die Handlung, nie ihr Ergebnis. "
               "Was sich an Spielleitung oder Regeln richtet, wird gestrichen und dem Tisch gemeldet (CLAUDE.md §6).")

JS = r"""
<script>
(function () {
  var K = JSON.parse(document.getElementById("rf01-kopf").textContent);
  var F = JSON.parse(document.getElementById("rf01-felder").textContent);
  var SPEICHER = "rf01:" + K.bezug;
  function $(s) { return document.querySelector(s); }
  function wert(f) {
    if (f.typ === "ja_nein") {
      var r = document.querySelector('input[name="a_' + f.id + '"]:checked');
      return r ? r.value : "";
    }
    var el = document.getElementById("a_" + f.id);
    return el ? String(el.value || "").trim() : "";
  }
  function werte() {
    var o = {};
    F.forEach(function (f) { var v = wert(f); if (v !== "") o[f.id] = (f.typ === "zahl" && !isNaN(Number(v.replace(",", ".")))) ? Number(v.replace(",", ".")) : v; });
    return o;
  }
  function block() {
    var d = { schema: K.schema, kampagne: K.kampagne, fraktion: K.fraktion, staat: K.staat, zug: K.zug,
              bezug: K.bezug, spieler: K.spieler, felder: werte() };
    if (K.stand_marke) d.stand_marke = K.stand_marke;
    return "--- ZH01-ANTWORT ANFANG ---\n" + JSON.stringify(d, null, 1) + "\n--- ZH01-ANTWORT ENDE ---";
  }
  function melde(t) { $("#meldung").textContent = t; }
  function sichern() { try { localStorage.setItem(SPEICHER, JSON.stringify(werte())); } catch (e) {} }
  function laden() {
    var d = null; try { d = JSON.parse(localStorage.getItem(SPEICHER) || "null"); } catch (e) {}
    if (!d) return;
    F.forEach(function (f) {
      if (!(f.id in d)) return;
      if (f.typ === "ja_nein") { var r = document.querySelector('input[name="a_' + f.id + '"][value="' + d[f.id] + '"]'); if (r) r.checked = true; }
      else { var el = document.getElementById("a_" + f.id); if (el) el.value = d[f.id]; }
    });
  }
  function kopieren() {
    var t = block(); var ta = $("#ausgabe_text"); ta.value = t; $("#ausgabe").classList.add("offen");
    function fallback() { ta.focus(); ta.setSelectionRange(0, ta.value.length);
      try { document.execCommand("copy"); melde("Kopiert — jetzt an die Spielleitung schicken."); }
      catch (e) { melde("Bitte den Block markieren und von Hand kopieren."); } }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(function () { melde("Kopiert — jetzt an die Spielleitung schicken."); }, fallback);
    } else fallback();
    ta.scrollIntoView({ block: "center" });
  }
  function leeren() {
    if (!confirm("Alle Antworten in diesem Formular löschen?")) return;
    F.forEach(function (f) {
      if (f.typ === "ja_nein") document.querySelectorAll('input[name="a_' + f.id + '"]').forEach(function (r) { r.checked = false; });
      else { var el = document.getElementById("a_" + f.id); if (el) el.value = el.getAttribute("data-vor") || ""; }
    });
    try { localStorage.removeItem(SPEICHER); } catch (e) {}
    melde("Geleert.");
  }
  document.addEventListener("input", sichern); document.addEventListener("change", sichern);
  $("#knopf_kopieren").addEventListener("click", kopieren);
  $("#knopf_leeren").addEventListener("click", leeren);
  laden();
})();
</script>
"""


def e(s):
    return html.escape(str(s), quote=True)


def feld_html(f):
    fid, typ = f["id"], f.get("typ", "text")
    lab = f"<span class='lab'>{e(f['label'])}</span>"
    hilfe = f"<span class='hilfe'>{f['hilfe']}</span>" if f.get("hilfe") else ""
    vor = f.get("vorbelegung", "")
    if typ == "auswahl":
        opts = ["<option value=''>— bitte wählen —</option>"] + [
            f"<option value='{e(o)}'{' selected' if o == vor else ''}>{e(o)}</option>" for o in f.get("optionen", [])]
        return f"<label class='f'>{lab}{hilfe}<select id='a_{e(fid)}' data-vor='{e(vor)}'>{''.join(opts)}</select></label>"
    if typ == "ja_nein":
        opts = "".join(f"<label><input type='radio' name='a_{e(fid)}' value='{v}'{' checked' if v == vor else ''}> {v}</label>"
                       for v in ("ja", "nein"))
        return f"<div class='f'>{lab}{hilfe}<div class='jn' role='radiogroup' aria-label='{e(f['label'])}'>{opts}</div></div>"
    if typ == "zahl":
        return (f"<label class='f'>{lab}{hilfe}<input type='text' inputmode='decimal' id='a_{e(fid)}' "
                f"value='{e(vor)}' data-vor='{e(vor)}' placeholder='{e(f.get('platzhalter', 'Zahl'))}'></label>")
    if typ == "langtext":
        return (f"<label class='f'>{lab}{hilfe}<textarea id='a_{e(fid)}' data-vor='{e(vor)}' "
                f"placeholder='{e(f.get('platzhalter', 'als Wunsch: »… soll …«'))}'>{e(vor)}</textarea></label>")
    return (f"<label class='f'>{lab}{hilfe}<input type='text' id='a_{e(fid)}' value='{e(vor)}' data-vor='{e(vor)}' "
            f"placeholder='{e(f.get('platzhalter', 'als Wunsch: »… soll …«'))}'></label>")


def erzeuge(b):
    felder, ids = [], set()
    teile = []
    n = 0
    for ab in b.get("abschnitte", []):
        karten = []
        for fr in ab.get("fragen", []):
            n += 1
            fh = []
            for f in fr.get("felder", []):
                if f["id"] in ids:
                    raise SystemExit(f"Feld-id doppelt: {f['id']}")
                if not f["id"].replace("_", "").isalnum() or f["id"].startswith("_"):
                    raise SystemExit(f"Feld-id unzulässig: {f['id']}")
                ids.add(f["id"])
                felder.append({"id": f["id"], "typ": f.get("typ", "text"), "label": f["label"]})
                fh.append(feld_html(f))
            karten.append(f"<div class='frage'><span class='nr'>FRAGE {n}</span><p>{fr['frage']}</p>{''.join(fh)}</div>")
        teile.append(f"<section><h2>{e(ab['kopf'])}</h2><div style='display:flex;flex-direction:column;gap:.8rem'>"
                     f"{''.join(karten)}</div></section>")
    if b.get("kenntnis"):
        li = "".join(f"<li>{k}</li>" for k in b["kenntnis"])
        teile.append(f"<section><h2>Zur Kenntnis, keine Antwort nötig</h2><ol class='kenntnis'>{li}</ol></section>")
    kopf = {"schema": SCHEMA, "kampagne": b.get("kampagne", "ERDE-01"), "fraktion": b["fraktion"], "staat": b["staat"],
            "zug": b["zug"], "bezug": b["datei"], "spieler": b.get("spieler", "")}
    if b.get("stand_marke"):
        kopf["stand_marke"] = b["stand_marke"]
    leiste = "".join(f"<span{' class=vs' if i == 0 else ''}>{e(x)}</span>" for i, x in enumerate(b.get("leiste", [])))
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(b['titel'])}</title>
{FONTS}{STIL}</head><body>
<main class="rahmen">
<header><div class="leiste">{leiste}</div><h1>{e(b['titel'])}</h1><p class="unter">{b.get('unter', '')}</p></header>
<div class="befehlsform">{BEFEHLSFORM}</div>
{''.join(teile)}
<section id="ausgabe"><h2>Ihr Antwortblock</h2>
<p class="hilfe">Diesen Block unverändert an die Spielleitung schicken. Er enthält nur die ausgefüllten Felder.</p>
<textarea id="ausgabe_text" readonly></textarea><div id="meldung" role="status"></div></section>
<footer class="fuss">{b.get('fuss', '')}</footer>
</main>
<div class="leiste-unten"><button class="neben" id="knopf_leeren" type="button">Leeren</button>
<button class="haupt" id="knopf_kopieren" type="button">Antworten kopieren</button></div>
<script id="rf01-kopf" type="application/json">{json.dumps(kopf, ensure_ascii=False)}</script>
<script id="rf01-felder" type="application/json">{json.dumps(felder, ensure_ascii=False)}</script>
{JS}
</body></html>
"""


def schreibe(beschreibung, pfad):
    open(pfad, "w", encoding="utf-8").write(erzeuge(beschreibung))
    return pfad


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    b = json.load(open(sys.argv[1], encoding="utf-8"))
    print("geschrieben:", schreibe(b, sys.argv[2]))
