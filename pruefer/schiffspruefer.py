#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SP-01 SCHIFFSPRUEFER — Regelgatter fuer Delta-V-Entwuerfe und ihre Buchung.

Entstanden aus vier echten Fehlern der Kampagne SCHWARZE SEE (Journal Z5-057
bis Z5-072). Jedes Gatter unten haelt genau einen davon fest. Der Pruefer
liest NUR, er aendert nichts.

    python3 pruefer/schiffspruefer.py [--state stand/gamestate.json] [--json]

Rueckgabe 0 = keine FEHLER, 1 = mindestens ein FEHLER.
Regelstellen sind an jedem Gatter woertlich zitiert.
"""
import json, math, argparse, sys, unicodedata

G0 = 9.80665

# --- launch_c2.md §1.1 -------------------------------------------------------
ZONENFAKTOR = {"LEO": 1, "SSO": 1, "MEO": 2, "GTO": 3, "HEO": 3, "GEO": 4,
               "GEO_GSO": 4, "EML": 5, "MONDORBIT": 6, "MONDOBERFLAECHE": 8}
# --- launch_c2.md §2 Tabelle 2 ----------------------------------------------
C2_BASIS = {"USA": 24, "CHN": 12, "EU": 8, "RUS": 5, "JPN": 4, "IND": 3,
            "REST": 20}   # REST = JPN 4 + 4x2 + 8x1
# --- research.md §Techstufen ------------------------------------------------
L_FREISCHALTUNG = {"L1": 2035, "L2": 2046, "L3": 2058}
# --- payload_catalog.md §Advantages (26) / §Disadvantages (7) ----------------
VORTEILE = {"Thermischer Betrieb","Saeure-Resistenz","Strahlungs-Haertung","Druck/Untersee",
  "Staub/Feuchte","Magnetfeld-Toleranz","Bestrahlbarkeit","Aero-/Magnetobrake","ISRU",
  "Landefaehigkeit","Wiederverwendbarkeit","Intra-atm Manoever","Fliegen","Schweben",
  "Hypersonic","Schwimmen","Fahren","Blimp","Eigenstart","Low-Pressure-Flight",
  "Flug ohne Oxidator","All-Terrain","Radar Suite","Lidar Suite","Soundranging Suite",
  "Supersonar Suite"}
NACHTEILE = {"Single-Use","Nur Sabotage","Fragile Radiatoren","Hoher EM-Abdruck",
  "Kryo-Boil-off","Verengte Schusssektoren","Doktrinaer gebunden"}

def norm(s):
    s = str(s).replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    return unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().strip()

NORM_V = {norm(x) for x in VORTEILE}
NORM_N = {norm(x) for x in NACHTEILE}

class Bericht:
    def __init__(self): self.p = []
    def add(self, stufe, gatter, betrifft, text, regel):
        self.p.append(dict(stufe=stufe, gatter=gatter, betrifft=betrifft, text=text, regel=regel))
    def fehler(self,*a): self.add("FEHLER",*a)
    def warnung(self,*a): self.add("WARNUNG",*a)
    def hinweis(self,*a): self.add("HINWEIS",*a)
    @property
    def n_fehler(self): return sum(1 for x in self.p if x["stufe"]=="FEHLER")


def cm_regel(np_):
    """payload_catalog.md: np>=2 -> np ; np==1 -> 2 ; np<=0 -> 1 (geklemmt, kein x3)."""
    if np_ <= 0: return 1.0, 1.0
    if np_ == 1: return 2.0, 3.0
    return float(np_), 3.0


def pruefe(g, b):
    jahr = g.get("state", {}).get("currentYear")

    # ---------------- S-Gatter: Entwuerfe ----------------------------------
    for fk, fd in g.get("factions", {}).items():
        res = fd.get("research", {}) or {}
        hat_L = {s: bool(res.get("completed"+s)) for s in ("L1","L2","L3")}
        for did, d in (fd.get("designs") or {}).items():
            ref = f"{fk}/{did}"

            # S-1 — Auslegungsmodus deklariert, Nachbau-Ausnahme belegt
            modus = d.get("designMode")
            if not modus:
                b.fehler("S-1", ref, "Kein designMode deklariert. Ohne Deklaration gilt der "
                    "Normalfall: Weight Penalty 3 MUSS aufgeschlagen werden.",
                    'construction.md §Weight Penalty 3: "Ohne diese Deklaration gilt der Normalfall."')
            elif norm(modus).upper() in ("A","RECONSTRUCTION","REKONSTRUKTION"):
                if not (d.get("realSystem") and d.get("realLaunchMass_kg")):
                    b.fehler("S-1", ref, "Modus A beansprucht die Nachbau-Ausnahme, nennt aber kein "
                        "reales Vorbild mit veroeffentlichter Startmasse (realSystem + "
                        "realLaunchMass_kg). Eine GM-Buchung ist keine veroeffentlichte Startmasse.",
                        'construction.md: Ausnahme nur bei designMode "reconstruction" '
                        '(veroeffentlichte Startmasse eines realen Systems).')

            vor = d.get("vorteile", []); nach = d.get("nachteile", [])
            def namen(x): return [e["name"] if isinstance(e, dict) else e for e in x]
            nv, nn = namen(vor), namen(nach)

            # S-3 — benannt statt gezaehlt, jede Zuschreibung begruendet
            if isinstance(vor, int) or isinstance(nach, int):
                b.fehler("S-3", ref, "Vor-/Nachteile stehen als blosse Zahl. Eine Zahl ist nicht "
                    "nachpruefbar.", 'nachbau_regeln.md §2: "Immer die konkreten Presets eintragen".')
            for n in nv:
                if norm(n) not in NORM_V:
                    b.fehler("S-3", ref, f"Vorteil '{n}' steht in keinem der 26 Presets.",
                             "payload_catalog.md §Advantages (26)")
            for n in nn:
                if norm(n) not in NORM_N:
                    b.fehler("S-3", ref, f"Nachteil '{n}' steht in keinem der 7 Presets.",
                             "payload_catalog.md §Disadvantages (7)")
            for e in list(vor)+list(nach):
                if isinstance(e, dict) and not (e.get("begruendung") and e.get("spielwirkung")):
                    b.fehler("S-3", ref, f"'{e.get('name')}' ohne Begruendung oder ohne Spielwirkung. "
                        "Ein Vorteil ohne Wirkung ist Zierrat, ein Nachteil ohne Wirkung ist geschenkt.",
                        "nachbau_regeln.md §2 · construction.md §Nachteile")

            # S-2 — Penaltykette bei Modus B vollstaendig und richtig gerechnet
            if modus and norm(modus).upper() in ("B","NEU","NEUKONSTRUKTION"):
                k = d.get("k2_penaltykette")  # noqa: F841 (oben schon gelesen)
                if not k:
                    b.fehler("S-2", ref, "Modus B ohne k2_penaltykette. Der Nutzlastmultiplikator "
                        "ist der Kanal, der bei Modus A entfaellt — in Modus B muss er belegt sein.",
                        "design_modes.md §1: Modus B wendet K1, K2 und K3 vollstaendig an.")
                else:
                    np_soll = 3 + len(nv) - len(nn)
                    cm_soll, x3_soll = cm_regel(np_soll)
                    # HAUSENTSCHEIDUNG HE-29: ohne Hochenergie gilt cm = np, sonst nichts.
                    # nachbau_regeln.md §1 und construction.md stimmen darin ueberein.
                    # payload_catalog.md beschreibt fuer ctxNoHE ein cm = np x np — das ist ab
                    # np 4 teurer als MIT Hochenergie und bestraft das Fehlen eines 50-kW-
                    # Systems staerker als sein Vorhandensein. Werkzeugartefakt, keine Regel.
                    if k.get("ctxNoHE") and np_soll >= 1:
                        x3_soll = 1.0
                    if k.get("np") != np_soll:
                        b.fehler("S-2", ref, f"np ist {k.get('np')}, muss 3 + {len(nv)} - {len(nn)} "
                            f"= {np_soll} sein.", "payload_catalog.md: np = 3 + adv - disadv")
                    if abs((k.get("cm") or 0) - cm_soll) > 1e-9:
                        b.fehler("S-2", ref, f"cm ist {k.get('cm')}, muss bei np={np_soll} "
                            f"{cm_soll:.0f} sein"
                            f"{' (ctxNoHE: cm zusaetzlich x np)' if k.get('ctxNoHE') else ''}.",
                            "nachbau_regeln.md §1 (HE-29): cm = np; np==1 -> 2; np<=0 -> 1")
                    if abs((k.get("hochenergie_faktor") or 0) - x3_soll) > 1e-9:
                        b.fehler("S-2", ref, f"Hochenergie-Faktor ist {k.get('hochenergie_faktor')}, "
                            f"muss {x3_soll:.0f} sein"
                            f"{' (ctxNoHE deklariert)' if k.get('ctxNoHE') else ''}.",
                            "payload_catalog.md: dann x3, ausser ctxNoHE; mit ctxNoHE entfaellt "
                            "das x3 und cm wird zusaetzlich mit np multipliziert; bei np<=0 geklemmt")
                    soll = (k.get("basis_kg") or 0)*(k.get("cm") or 0)*(k.get("disc") or 1) \
                           *(1+(k.get("env") or 0))*(k.get("hochenergie_faktor") or 1)
                    if abs(soll - (k.get("nutzlast_final_kg") or 0)) > 1e-6:
                        b.fehler("S-2", ref, f"Nutzlast endgueltig {k.get('nutzlast_final_kg')} kg "
                            f"passt nicht zur Kette (gerechnet {soll:.4f} kg).",
                            "payload_catalog.md: final = basis x cm x disc x (1+env) x HE")

            # S-6 — Penalty-Reduktion durch Forschung nur wenn wirklich beherrscht
            for stufe, jahr_frei in L_FREISCHALTUNG.items():
                if d.get("penalty_reduktion_"+stufe.lower()) or stufe in str(d.get("penalty_quelle","")):
                    if not hat_L[stufe]:
                        b.fehler("S-6", ref, f"Penalty-Reduktion aus {stufe} beansprucht, aber "
                            f"factions.{fk}.research.completed{stufe} ist leer.",
                            "construction.md §Penalty reduzieren · research.md §Techstufen")
                    elif jahr and jahr < jahr_frei:
                        b.fehler("S-6", ref, f"{stufe} beansprucht im Jahr {jahr}, freigeschaltet "
                            f"erst ab {jahr_frei}.", "research.md §Techstufen")

            # S-8 — Hochenergie ist eine Tatsache ueber das Schiff, keine Wahl.
            # construction.md: "High-Energy-Systeme (ab ~50 kW, z.B. Laser): ... Zusaetzlich:
            # Dv / 3 UND 3x Gewicht" — die Strafe hat ZWEI Haelften und gilt erst ab ~50 kW.
            k = d.get("k2_penaltykette") or {}
            leist = d.get("spitzenlast_kw")
            if k and leist is not None:
                he = (k.get("hochenergie_faktor") or 1) > 1
                if leist < 50 and he:
                    b.fehler("S-8", ref, f"Hochenergie-Faktor x{k.get('hochenergie_faktor')} "
                        f"aufgeschlagen, aber die Spitzenlast betraegt nur {leist:.2f} kW. Die "
                        "Strafe gilt erst ab ~50 kW — hier ist ctxNoHE zu deklarieren.",
                        'construction.md §Weight Penalty 3: "High-Energy-Systeme (ab ~50 kW, '
                        'z.B. Laser)"')
                if leist >= 50 and he and not d.get("dv_hochenergie_geteilt"):
                    b.fehler("S-8", ref, f"Hochenergie mit {leist:.2f} kW zu Recht angesetzt, aber "
                        "nur die Gewichtshaelfte gebucht. Die Strafe hat zwei Haelften: 3x Gewicht "
                        "UND Dv / 3. Entweder beide oder keine.",
                        'construction.md: "Zusaetzlich: Dv / 3 und 3x Gewicht"')
                if leist >= 50 and not he and not k.get("ctxNoHE"):
                    b.warnung("S-8", ref, f"Spitzenlast {leist:.2f} kW liegt ueber der Schwelle, "
                        "aber es ist weder Hochenergie noch ctxNoHE gebucht — Zustand unklar.",
                        "construction.md §Weight Penalty 3")

            # S-7 — Autonomie ist ein Bauentscheid und muss dastehen
            st = norm(d.get("steuerung","")).lower()
            if st not in ("autonom","ferngelenkt"):
                b.fehler("S-7", ref, "Keine Steuerung deklariert. Die Strukturtonne ist ein "
                    "Bauentscheid: mit ihr autonom, ohne sie ferngelenkt. Beides hat Folgen im "
                    "Spiel, also muss dastehen, welches gilt.",
                    'construction.md §"Struktur = Autonomie (Kernregel)": "Sie ist ein '
                    'Bauentscheid und muss explizit verbaut sein."')
            elif st == "ferngelenkt" and not d.get("steuerungBegruendung"):
                b.warnung("S-7", ref, "Ferngelenkt erklaert, aber die Folgen sind nicht "
                    "hinterlegt. Ohne aktiven Link ist das Schiff handlungsunfaehig und im "
                    "Kampf wehrloses Ziel — das gehoert an den Entwurf.",
                    "construction.md §Ferngelenkte Fahrzeuge")
            elif st == "autonom" and modus and norm(modus).upper() in ("B","NEU","NEUKONSTRUKTION"):
                k = d.get("k2_penaltykette") or {}
                nl = str(d.get("nutzlastHerkunft","")).lower()
                if k and "shipframe" not in nl and (d.get("masse_t") or 0) < 10:
                    b.fehler("S-7", ref, "Autonom erklaert, aber unter 10 t und ohne die "
                        "Strukturtonne in der Nutzlast. Gratis gibt es sie erst ab 10 t.",
                        'construction.md: "ab 10 t gratis (Synergieregel), darunter 1 t"')

            # S-4 — Massenschluss und Ziolkowski
            dry, prop, nass = d.get("dryMass_t"), d.get("propellantMass_t"), d.get("nassMasse_t")
            if None not in (dry, prop, nass):
                if abs(dry+prop-nass) > 1e-3:
                    b.fehler("S-4", ref, f"trocken {dry} + Treibstoff {prop} = {dry+prop:.4f} t, "
                        f"eingetragen ist nass {nass} t.", "Erhaltungssatz")
                isp, dv = d.get("isp_s"), d.get("dv_total_kms")
                if isp and dv is not None and dry > 0:
                    soll = isp*G0*math.log(nass/dry)/1000
                    if abs(soll-dv) > max(0.001, 0.005*abs(dv)):
                        b.fehler("S-4", ref, f"dv_total {dv} km/s passt nicht zu Isp {isp} und "
                            f"dem Massenverhaeltnis (Ziolkowski: {soll:.4f} km/s).", "Ziolkowski")
            # S-5 — Entwurf und gebuchte Startmasse muessen uebereinstimmen
            if nass is not None and d.get("masse_t") is not None:
                gebucht = d["masse_t"]
                if nass - gebucht > 1e-3:
                    b.fehler("S-5", ref, f"Konstruierte Nassmasse {nass} t ist GROESSER als die "
                        f"gebuchte Startmasse {gebucht} t. Es fliegt mehr, als bezahlt wurde.",
                        "ZH-01 Bodenkonto / launch_c2.md §5.2")
                elif gebucht - nass > max(1e-3, 0.01*gebucht):
                    b.hinweis("S-5", ref, f"Gebucht sind {gebucht} t, konstruiert {nass} t — "
                        f"{gebucht-nass:.4f} t zu viel bezahlt. Kein Regelverstoss, nur teuer.",
                        "launch_c2.md §5.2")

    # ---------------- D-Gatter: Delta-v-Buchfuehrung -------------------------
    ctrl = (g.get("scoring") or {}).get("zonen_controller") or {}
    for fk, fd in g.get("factions", {}).items():
        designs = fd.get("designs") or {}
        for sk, sw in (fd.get("swarms") or {}).items():
            d = designs.get(sw.get("design"))
            if not d: continue
            dv_bau = d.get("dv_total_kms")
            if dv_bau is not None and (sw.get("dv_kms") or 0) - dv_bau > 1e-9:
                b.fehler("D-1", f"{fk}/{sk}", f"Schwarm fuehrt {sw.get('dv_kms')} km/s, der Entwurf "
                    f"gibt aber nur {dv_bau} km/s her.", "Kein Delta-v aus dem Nichts")
        # D-2 — wer eine Zone haelt, muss dafuer bezahlt haben
        for zone, halter in ctrl.items():
            if halter != fk: continue
            drin = [(k,v) for k,v in (fd.get("swarms") or {}).items()
                    if str(v.get("zone","")).upper() in (zone.upper(), zone.upper().split("_")[0])
                    and (designs.get(v.get("design"),{}).get("dv_manoever_kms") or 0) > 0]
            if drin and all((v.get("dv_kms") or 0) >= designs[v["design"]]["dv_manoever_kms"]
                            for _,v in drin):
                b.warnung("D-2", f"{fk}/{zone}", f"{fk} haelt {zone}, aber kein Schwarm dort hat "
                    "Delta-v abgegeben. Jeder Scoring-Versuch kostet 1 km/s — pruefen, ob die "
                    "Abschreibung fehlt.", "scoring.md §Grundregeln: 1 km/s pro Scoring-Versuch")

    # ---------------- B-Gatter: Bau und Bezahlung ---------------------------
    for e in (g.get("bz01") or {}).get("bauplan", []):
        preis = (e.get("count",0))*(e.get("stueck_masse_t",0))*(e.get("kosten_mult",1))
        if e.get("werft_gebucht_t") is None:
            b.warnung("B-1", f"{e.get('fraktion')}/{e.get('design_ref')}",
                f"Auftrag {e.get('id')} ohne Feld werft_gebucht_t. Faellig waeren "
                f"{preis:.1f} t Werftdurchsatz ({e.get('count')} x {e.get('stueck_masse_t')} t "
                f"x Kostenmultiplikator {e.get('kosten_mult')}).",
                'BZ-01 §1: Kosten = Kaufladenpreis x K(P-Stufe) ... "Werftdurchsatz = '
                'industrial.capacity_t_year. Keine neue Waehrung."')
        elif abs(e["werft_gebucht_t"] - preis) > 1e-6:
            b.fehler("B-1", f"{e.get('fraktion')}/{e.get('design_ref')}",
                f"werft_gebucht_t {e['werft_gebucht_t']} t weicht vom Preis {preis:.1f} t ab.",
                "BZ-01 §1")

    # ---------------- B-2: passt die Summe in die Werft? --------------------
    from collections import defaultdict
    je_fraktion = defaultdict(lambda: [0.0, set()])
    for e in (g.get("bz01") or {}).get("bauplan", []):
        w = e.get("werft_gebucht_t")
        if w is None: continue
        f = e.get("fraktion"); je_fraktion[f][0] += w
        for z in range(int(e.get("gestartet_zug", 0) or 0), int(e.get("fertig_zug", 0) or 0)):
            je_fraktion[f][1].add(z)
    for f, (summe, jahre) in je_fraktion.items():
        kap = (((g.get("factions") or {}).get(f) or {}).get("economy", {})
               .get("resources", {}).get("industrial", {}).get("capacity_t_year"))
        if not kap or not jahre: continue
        deckel = kap * len(jahre)
        if summe > deckel + 1e-6:
            b.fehler("B-2", f, f"Bauauftraege binden {summe:.1f} t Werftdurchsatz, verfuegbar sind "
                f"{deckel:.1f} t ({kap:.1f} t/a x {len(jahre)} Baujahre). Engpass.",
                "BZ-01 §1 · launch_c2.md §5.2 Pkt. 2: im Baujahr den Werftdurchsatz pruefen")
        elif summe > 0.9 * deckel:
            b.hinweis("B-2", f, f"Werft zu {100*summe/deckel:.0f} % ausgelastet "
                f"({summe:.1f} von {deckel:.1f} t) — kein Spielraum fuer weitere Auftraege.",
                "BZ-01 §1")

    # ---------------- C-Gatter: C2-Erhaltungssatz ---------------------------
    for fk, fd in g.get("factions", {}).items():
        c = (fd.get("economy") or {}).get("resources", {}).get("c2")
        if not c: continue
        basis = C2_BASIS.get(fk)
        if basis is None:
            b.hinweis("C-1", fk, "Keine Basiszeile in launch_c2 Tabelle 2 hinterlegt — uebersprungen.",
                      "launch_c2.md §2"); continue
        soll = basis + c.get("ground_stations",0) + c.get("geo_relays",0) + c.get("deep_space_relays",0)
        if abs((c.get("slots_total") or 0) - soll) > 1e-9:
            b.fehler("C-1", fk, f"slots_total {c.get('slots_total')} passt nicht zu Basis {basis} + "
                f"Bodenstationen {c.get('ground_stations',0)} + GEO-Relais {c.get('geo_relays',0)} + "
                f"Deep-Space {c.get('deep_space_relays',0)} = {soll}. Bestand muss gleich "
                "Buchungssumme sein.", "launch_c2.md §2.1 · Erhaltungssatz")
        im_orbit = sum(v.get("count",0) for v in (fd.get("swarms") or {}).values()
                       if "relais" in str(v.get("design","")).lower()
                       and "GEO" in str(v.get("zone","")).upper())
        if im_orbit != c.get("geo_relays",0):
            b.fehler("C-2", fk, f"{im_orbit} GEO-Relais stehen im Orbit, der Zaehler geo_relays sagt "
                f"{c.get('geo_relays',0)}.", "launch_c2.md §2.1")
    return b


# ---------------------------------------------------------------- Selbsttest
# Jeder Fall bildet einen ECHTEN Fehler dieser Kampagne nach. Faengt das Gatter
# ihn nicht mehr, ist das Gatter kaputt — nicht der Fall.
FAELLE = [
 ("Z5-063  Modus A ohne reales Vorbild (Nachbau-Ausnahme zu Unrecht)", "S-1",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "A", "vorteile": [], "nachteile": []}}}}}),
 ("Z5-057  Entwurf ganz ohne designMode (Stub)", "S-1",
  {"factions": {"CHN": {"designs": {"X": {"masse_t": 2}}}}}),
 ("Z5-065  Modus B ohne Penaltykette", "S-2",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "vorteile": [], "nachteile": []}}}}}),
 ("Z5-065  Modus B mit falsch gerechnetem np", "S-2",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "vorteile": [], "nachteile": [],
     "k2_penaltykette": {"basis_kg": 1000, "np": 0, "cm": 1, "hochenergie_faktor": 1,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 1000}}}}}}),
 ("Z5-064  L-Stufe beansprucht, die es 2030 nicht gibt", "S-6",
  {"state": {"currentYear": 2030},
   "factions": {"CHN": {"research": {"completedL1": []}, "designs": {"X": {"designMode": "B",
     "vorteile": [], "nachteile": [], "penalty_quelle": "L1",
     "k2_penaltykette": {"basis_kg": 100, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 900}}}}}}),
 ("Vorteil als blosse Zahl statt als Preset", "S-3",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "vorteile": ["Tarnkappe"],
     "nachteile": [], "k2_penaltykette": {"basis_kg": 100, "np": 4, "cm": 4,
     "hochenergie_faktor": 3, "disc": 1, "env": 0, "nutzlast_final_kg": 1200}}}}}}),
 ("Nachteil ohne Spielwirkung (geschenkt)", "S-3",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "vorteile": [],
     "nachteile": [{"name": "Single-Use"}],
     "k2_penaltykette": {"basis_kg": 100, "np": 2, "cm": 2, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 600}}}}}}),
 ("Massenschluss verletzt", "S-4",
  {"factions": {"IND": {"designs": {"X": {"designMode": "A", "realSystem": "r",
     "realLaunchMass_kg": 1, "dryMass_t": 0.24, "propellantMass_t": 0.017,
     "nassMasse_t": 0.30, "vorteile": [], "nachteile": []}}}}}),
 ("Es fliegt mehr, als bezahlt wurde", "S-5",
  {"factions": {"IND": {"designs": {"X": {"designMode": "A", "realSystem": "r",
     "realLaunchMass_kg": 1, "masse_t": 2.0, "dryMass_t": 2.0, "propellantMass_t": 0.5,
     "nassMasse_t": 2.5, "vorteile": [], "nachteile": []}}}}}),
 ("Schwarm fuehrt mehr Delta-v, als der Entwurf hergibt", "D-1",
  {"factions": {"CHN": {"designs": {"S": {"designMode": "B", "vorteile": [], "nachteile": [],
     "dv_total_kms": 1.0, "dv_manoever_kms": 1.0,
     "k2_penaltykette": {"basis_kg": 100, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 900}}},
    "swarms": {"A": {"design": "S", "zone": "LEO", "dv_kms": 2.0}}}}}),
 ("Z5-067  Zone gehalten, aber kein Delta-v abgeschrieben", "D-2",
  {"scoring": {"zonen_controller": {"LEO": "CHN"}},
   "factions": {"CHN": {"designs": {"S": {"designMode": "B", "vorteile": [], "nachteile": [],
     "dv_total_kms": 1.0, "dv_manoever_kms": 1.0,
     "k2_penaltykette": {"basis_kg": 100, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 900}}},
    "swarms": {"A": {"design": "S", "zone": "LEO", "dv_kms": 1.0}}}}}),
 ("Z5-070  Bauauftrag ohne gebuchten Werftdurchsatz", "B-1",
  {"bz01": {"bauplan": [{"id": "T", "fraktion": "CHN", "design_ref": "X", "count": 2,
                         "stueck_masse_t": 2.0, "kosten_mult": 4.0}]}}),
 ("Z5-084  ctxNoHE mit quadriertem cm (Werkzeugartefakt statt Regel)", "S-2",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "steuerung": "ferngelenkt",
     "steuerungBegruendung": "Link", "spitzenlast_kw": 3.6,
     "vorteile": [{"name": "Strahlungs-Haertung", "spielwirkung": "w", "begruendung": "b"},
                  {"name": "Thermischer Betrieb", "spielwirkung": "w", "begruendung": "b"}],
     "nachteile": [],
     "k2_penaltykette": {"basis_kg": 50, "np": 5, "cm": 25, "hochenergie_faktor": 1,
                         "ctxNoHE": True, "disc": 1, "env": 0, "nutzlast_final_kg": 1250}}}}}}),
 ("Z5-082  Hochenergie-Gewicht ohne Hochenergie-Leistung (unter 50 kW)", "S-8",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "steuerung": "ferngelenkt",
     "steuerungBegruendung": "Link", "spitzenlast_kw": 3.6, "vorteile": [], "nachteile": [],
     "k2_penaltykette": {"basis_kg": 50, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 450}}}}}}),
 ("Z5-082  Hochenergie zu Recht, aber nur die Gewichtshaelfte gebucht", "S-8",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "steuerung": "ferngelenkt",
     "steuerungBegruendung": "Link", "spitzenlast_kw": 200.0, "vorteile": [], "nachteile": [],
     "k2_penaltykette": {"basis_kg": 50, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 450}}}}}}),
 ("Z5-076  Steuerung nicht deklariert (Strukturtonne: Bauentscheid)", "S-7",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "vorteile": [], "nachteile": [],
     "k2_penaltykette": {"basis_kg": 100, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 900}}}}}}),
 ("Autonom unter 10 t ohne Strukturtonne in der Nutzlast", "S-7",
  {"factions": {"CHN": {"designs": {"X": {"designMode": "B", "steuerung": "autonom",
     "masse_t": 2.0, "nutzlastHerkunft": "comps sensor_geo", "vorteile": [], "nachteile": [],
     "k2_penaltykette": {"basis_kg": 100, "np": 3, "cm": 3, "hochenergie_faktor": 3,
                         "disc": 1, "env": 0, "nutzlast_final_kg": 900}}}}}}),
 ("Werftengpass: Auftraege sprengen die Kapazitaet", "B-2",
  {"factions": {"CHN": {"economy": {"resources": {"industrial": {"capacity_t_year": 40.0}}}}},
   "bz01": {"bauplan": [{"id": "T", "fraktion": "CHN", "design_ref": "X", "count": 2,
     "stueck_masse_t": 10.0, "kosten_mult": 4.0, "werft_gebucht_t": 80.0,
     "gestartet_zug": 2026, "fertig_zug": 2027}]}}),
 ("Z5-071  C2-Bestand ungleich Buchungssumme", "C-1",
  {"factions": {"CHN": {"economy": {"resources": {"c2": {"slots_total": 14, "geo_relays": 0,
     "ground_stations": 0, "deep_space_relays": 0}}}}}}),
]

def selbsttest():
    ok = True
    print("SP-01 SELBSTTEST — jeder Fall ist ein echter Fehler dieser Kampagne\n")
    for name, gatter, fixture in FAELLE:
        b = pruefe(fixture, Bericht())
        traf = any(x["gatter"] == gatter for x in b.p)
        print(f"  {'OK    ' if traf else 'VERSAGT'}  {gatter:<4} {name}")
        ok &= traf
    # Gegenprobe: ein sauberer Entwurf darf NICHT anschlagen
    sauber = {"state": {"currentYear": 2030}, "factions": {"CHN": {"research": {},
      "designs": {"X": {"designMode": "B", "masse_t": 2.0, "dryMass_t": 1.4469,
        "propellantMass_t": 0.5531, "nassMasse_t": 2.0, "isp_s": 315, "dv_total_kms": 1.0,
        "vorteile": [], "nachteile": [{"name": "Single-Use", "begruendung": "b", "spielwirkung": "w"},
                                      {"name": "Doktrinaer gebunden", "begruendung": "b", "spielwirkung": "w"},
                                      {"name": "Fragile Radiatoren", "begruendung": "b", "spielwirkung": "w"}],
        "steuerung": "ferngelenkt", "steuerungBegruendung": "Link noetig", "spitzenlast_kw": 3.6,
        "k2_penaltykette": {"basis_kg": 1000, "np": 0, "cm": 1, "hochenergie_faktor": 1,
                            "disc": 1, "env": 0, "nutzlast_final_kg": 1000}}}}}}
    b = pruefe(sauber, Bericht())
    rein = b.n_fehler == 0
    print(f"  {'OK    ' if rein else 'VERSAGT'}  --   Gegenprobe: sauberer Modus-B-Entwurf schlaegt nicht an")
    ok &= rein
    print("\nERGEBNIS:", "BESTANDEN" if ok else "DURCHGEFALLEN")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="SP-01 SCHIFFSPRUEFER")
    ap.add_argument("--state", default="stand/gamestate.json")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selbsttest", action="store_true", help="Gatter gegen die historischen Fehler pruefen")
    a = ap.parse_args()
    if a.selbsttest: return selbsttest()
    try:
        g = json.load(open(a.state))
    except FileNotFoundError:
        print(f"SP-01: {a.state} nicht gefunden — uebersprungen."); return 0
    b = pruefe(g, Bericht())
    if a.json:
        print(json.dumps(dict(befunde=b.p, fehler=b.n_fehler), indent=1, ensure_ascii=False))
    else:
        n = {s: sum(1 for x in b.p if x["stufe"]==s) for s in ("FEHLER","WARNUNG","HINWEIS")}
        print(f"SP-01 SCHIFFSPRUEFER — {a.state}")
        print(f"Befunde: {len(b.p)} (Fehler {n['FEHLER']}, Warnungen {n['WARNUNG']}, "
              f"Hinweise {n['HINWEIS']})")
        print("ERGEBNIS:", "BESTANDEN" if b.n_fehler == 0 else "DURCHGEFALLEN")
        for x in b.p:
            print(f"\n[{x['stufe']:<7}] {x['gatter']}  {x['betrifft']}")
            print(f"  {x['text']}")
            print(f"  Regel: {x['regel']}")
    return 1 if b.n_fehler else 0

if __name__ == "__main__":
    sys.exit(main())
