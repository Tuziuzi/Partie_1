#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entscheidungsrechnung: ferngelenkte Entwuerfe + ctxNoHE + Werftengpass."""
import importlib.util
OW=("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
    "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
sp=importlib.util.spec_from_file_location("nb",OW); nb=importlib.util.module_from_spec(sp)
sp.loader.exec_module(nb)

def k2(base,a,d,no_he=False):
    """payload_catalog.md: mit ctxNoHE entfaellt x3, dafuer cm zusaetzlich x np."""
    np_=3+a-d
    if np_<=0:  return np_,1.0,1.0,base
    cm = 2.0 if np_==1 else float(np_)
    if no_he: return np_, cm*np_, 1.0, base*cm*np_
    return np_, cm, 3.0, base*cm*3.0

SCO=dict(isp=315,prop="mmh_nto",dv=1000.0,ld=2.5,house=3.6,batt=1.2,
  eng=[dict(thrust_n=490,mass_kg=16,count=1),dict(thrust_n=22,mass_kg=6,count=4)])
AUF=dict(isp=230,prop="hydrazine",dv=50.0,ld=2.5,house=6.0,batt=0.6,
  eng=[dict(thrust_n=22,mass_kg=6,count=4)])
def masse(s,pay,a,d):
    return nb.build(dict(struct_class="ruggedized",adv=a,disadv=d,payload_kg=pay,misc_kg=0.0,
      house_kw=s["house"],pp_type="solar",pp_alpha=15.0,au=1.0,batt_hours=s["batt"],
      batt_alpha=5,rad_alpha=5.0,ld=s["ld"],isp=s["isp"],prop=s["prop"],
      dv_target=s["dv"],engines=s["eng"]))["wet"]

print("="*100)
print("HIMMELSAUGE mit ctxNoHE — 'No high-energy' ist ehrlich deklarierbar: 6 kW Bordleistung,")
print("kein Laser, kein System ab 50 kW. Dann entfaellt das x3, dafuer cm x np.")
print("="*100)
print(f"{'Sensor':<28}{'Vort':>5}{'Nach':>5}{'np':>4}{'cm':>5}{'HE':>4}{'Nutzl':>8}{'nass min':>11}  Urteil")
for lab,base in [("bis GEO aufdecken 1000 kg",1000.0),("Init-Angreifer 500 kg",500.0)]:
    for a,d in [(2,0),(2,1),(2,2),(2,3),(2,4)]:
        for he in (False,True):
            np_,cm,x3,pay=k2(base,a,d,he); w=masse(AUF,pay,a,d)
            tag="ctxNoHE" if he else "normal "
            u='PASST, Bus %6.1f kg'%(2000-w) if w<=2000 else 'zu schwer %5.2fx'%(w/2000)
            print(f"{lab+' ['+tag+']':<28}{a:>5}{d:>5}{np_:>4}{cm:>5.0f}{x3:>4.0f}{pay:>8.0f}{w:>11.1f}  {u}")
    print()

print("="*100)
print("WERFTENGPASS — BZ-01 §1: Kosten = Masse x Kostenmultiplikator, bezahlt aus")
print("industrial.capacity_t_year. China: 40,0 t/a · Baufenster 2026-2028 = 3 Jahre = 120,0 t")
print("="*100)
KM=4.0  # P0n Erststueck
print(f"{'Auslegung':<46}{'Aufkl':>8}{'Scorer':>9}{'Relais':>8}{'Masse':>8}{'x4':>9}{'  von 120 t'}")
for lab,ma,ms,mr in [
  ("heute gebucht (2 / 2 / 5 t)",2.0,2.0,5.0),
  ("ferngelenkt, Sensor 1 t behalten (Aufkl 18,2 t)",18.2236,1.5368,5.0),
  ("ferngelenkt, Sensor 100-kg-Klasse",1.6489,1.5368,5.0),
  ("10-t-Klasse (Synergie, autonom)",10.0,10.0,5.0),
  ("np 3 mit 1-t-Sensor (Aufkl 10,8 t)",10.829,1.5368,5.0),
]:
    m=2*ma+5*ms+2*mr; k=m*KM
    print(f"{lab:<46}{2*ma:>8.1f}{5*ms:>9.1f}{2*mr:>8.1f}{m:>8.1f}{k:>9.1f}"
          f"  {'passt (%.0f %%)'%(100*k/120) if k<=120 else 'SPRENGT um %.1f t (%.1f Jahre Werft)'%(k-120,k/40)}")
print("\nHinweis: die Schiffe sind bereits gebaut und geflogen. Neue YARD-Kosten entstehen nur,")
print("wenn die Korrektur die MASSE aendert und damit neu gebucht werden muss.")
