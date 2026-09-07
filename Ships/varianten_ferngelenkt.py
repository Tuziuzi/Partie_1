#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spielerentscheid: Strukturtonne weglassen -> die Schiffe sind FERNGELENKT.

construction.md §"Struktur = Autonomie (Kernregel)":
  "Die Strukturtonne kauft nicht Rumpf, sondern Autonomie: Bordrechner,
   Selbststeuerung, eigene Feuerleitung. Sie ist ein Bauentscheid und muss
   explizit verbaut sein — ab 10 t gratis (Synergieregel), darunter 1 t."
  Ferngelenkt = Strukturtonne fehlt -> permanenter Kommandolink zwingend.

Sie IST ein Nutzlastposten (comps shipframe 1000 kg) und geht damit in die
K2-Basis ein. Weglassen senkt die Basis um 1000 kg — das ist der Hebel.

Zusaetzlich geprueft: Werftdurchsatz nach BZ-01 §1
  Kosten = Masse x Kostenmultiplikator (P0n = 4,0), bezahlt aus
  industrial.capacity_t_year. China: 40,0 t/a.
"""
import importlib.util, json
OW=("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
    "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
sp=importlib.util.spec_from_file_location("nb",OW); nb=importlib.util.module_from_spec(sp)
sp.loader.exec_module(nb)

def k2(base,a,d):
    np_=3+a-d
    if np_<=0:  cm,x3=1.0,1.0
    elif np_==1: cm,x3=2.0,3.0
    else:        cm,x3=float(np_),3.0
    return np_,cm,x3,base*cm*x3

SCO=dict(isp=315,prop="mmh_nto",dv=1000.0,ld=2.5,house=3.6,batt=1.2,
  eng=[dict(thrust_n=490,mass_kg=16,count=1),dict(thrust_n=22,mass_kg=6,count=4)])
AUF=dict(isp=230,prop="hydrazine",dv=50.0,ld=2.5,house=6.0,batt=0.6,
  eng=[dict(thrust_n=22,mass_kg=6,count=4)])

def masse(s,pay,a,d,bus=0.0):
    return nb.build(dict(struct_class="ruggedized",adv=a,disadv=d,payload_kg=pay,misc_kg=bus,
      house_kw=s["house"],pp_type="solar",pp_alpha=15.0,au=1.0,batt_hours=s["batt"],
      batt_alpha=5,rad_alpha=5.0,ld=s["ld"],isp=s["isp"],prop=s["prop"],
      dv_target=s["dv"],engines=s["eng"]))["wet"]

HAERT=["Strahlungs-Haertung","Thermischer Betrieb"]
print("="*104)
print("A) FELDZEICHEN (Scorer) — Strukturtonne weg, damit ferngelenkt. Sensor hatte er nie.")
print("="*104)
print(f"{'Basisnutzlast':<34}{'Vort':>5}{'Nach':>5}{'np':>4}{'Nutzl':>8}{'nass min':>11}{'  Urteil'}")
for lab,base in [("keine (nur Tank + Triebwerk)",0.0),
                 ("Ops-Paket 20 kg",20.0),("Ops-Paket 50 kg",50.0),
                 ("MIT Strukturtonne 1000 kg",1000.0)]:
    for a,d in [(2,0),(2,1),(0,3)]:
        np_,cm,x3,pay=k2(base,a,d); w=masse(SCO,pay,a,d)
        print(f"{lab:<34}{a:>5}{d:>5}{np_:>4}{pay:>8.0f}{w:>11.1f}"
              f"  {'PASST, Bus frei %6.1f kg'%(2000-w) if w<=2000 else 'zu schwer %.2fx'%(w/2000)}")
    print()

print("="*104)
print("B) HIMMELSAUGE (Aufklaerer) — Strukturtonne weg; der Sensor bleibt, er IST die Mission.")
print("   construction.md §2 Sensoren: 'Bis GEO alles aufdecken | 1 t' · kleinere Klassen 500/200/100/10/5/1 kg")
print("="*104)
print(f"{'Sensorklasse':<34}{'Vort':>5}{'Nach':>5}{'np':>4}{'Nutzl':>8}{'nass min':>11}{'  Urteil'}")
for lab,base in [("bis GEO alles aufdecken 1000 kg",1000.0),
                 ("Init-Angreifer 500 kg",500.0),("Init-Angreifer 200 kg",200.0),
                 ("Init-Angreifer 100 kg",100.0)]:
    for a,d in [(2,0),(2,1),(2,2)]:
        np_,cm,x3,pay=k2(base,a,d); w=masse(AUF,pay,a,d)
        print(f"{lab:<34}{a:>5}{d:>5}{np_:>4}{pay:>8.0f}{w:>11.1f}"
              f"  {'PASST, Bus frei %6.1f kg'%(2000-w) if w<=2000 else 'zu schwer %.2fx'%(w/2000)}")
    print()
