#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v5.22-HE Schritt 2: alle drei Optionen fuer powerUsed < 50 kW durchgerechnet.

SKILL.md Schritt 2 woertlich:
  "powerUsed < 50 kW -> the game rule does NOT apply. State this in notes. The calculator
   still offers only x3 or cm x np; pick the state closest to the rule, record the difference
   as [S] with rule citation in customData.highEnergy, and declare the mismatch as RULES-GAP
   to the player (options: calculator default x3 / ctxNoHE cm x np / house-rule flat base
   marked [S])."
"""
import importlib.util
OW=("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
    "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
sp=importlib.util.spec_from_file_location("nb",OW); nb=importlib.util.module_from_spec(sp); sp.loader.exec_module(nb)

def cm_basis(np_): return 1.0 if np_<=0 else (2.0 if np_==1 else float(np_))
OPT={
 "a) Kalkulator x3":  lambda np_: cm_basis(np_)*(1.0 if np_<=0 else 3.0),
 "b) ctxNoHE cm x np": lambda np_: cm_basis(np_)*(1.0 if np_<=0 else np_),
 "c) Hausregel flach": lambda np_: cm_basis(np_),
}
SCH={
 "Feldzeichen":   dict(anker=2000.0, base=50.0, adv=2, maxdis=3, isp=315, prop="mmh_nto",
   dv=1000.0, ld=2.5, house=3.6, batt=1.2,
   eng=[dict(thrust_n=490,mass_kg=16,count=1),dict(thrust_n=22,mass_kg=6,count=4)]),
 "Himmelsauge":   dict(anker=3600.0, base=1000.0, adv=2, maxdis=4, isp=230, prop="hydrazine",
   dv=50.0, ld=2.5, house=11.0, batt=0.6, eng=[dict(thrust_n=22,mass_kg=6,count=4)]),
 "Himmelsbruecke":dict(anker=5000.0, base=150.0, adv=3, maxdis=2, isp=1600, prop="xenon",
   dv=750.0, ld=2.6, house=15.0, batt=1.2,
   eng=[dict(thrust_n=0.083,mass_kg=45,count=4,p_kw=1.35,p_count=2,waste_kw=0.54)]),
}
HK={"pay_dry":(6.8,58.2),"paybus_dry":(17.7,78.2),"struct_dry":(10.7,20.6),
    "dry_wet":(40.2,93.3),"pp_dry":(5.0,15.0)}
def bau(s,pay,a,d,bus):
    return nb.build(dict(struct_class="ruggedized",adv=a,disadv=d,payload_kg=pay,misc_kg=bus,
      house_kw=s["house"],pp_type="solar",pp_alpha=15.0,au=1.0,batt_hours=s["batt"],batt_alpha=5,
      rad_alpha=5.0,ld=s["ld"],isp=s["isp"],prop=s["prop"],dv_target=s["dv"],engines=s["eng"]))
def loese(s,pay,a,d):
    lo,hi=-s["anker"]*4,s["anker"]*4
    for _ in range(200):
        m=(lo+hi)/2
        if bau(s,pay,a,d,max(m,0.0) if m>=0 else m)["wet"]<s["anker"]: lo=m
        else: hi=m
    return (lo+hi)/2

for name,s in SCH.items():
    print(f"\n{'='*104}\n{name}   Anker {s['anker']:.0f} kg · Basis {s['base']:.0f} kg · "
          f"{s['adv']} Vorteile · hoechstens {s['maxdis']} ehrliche Nachteile\n{'='*104}")
    print(f"{'Option':<20}{'Nach':>5}{'np':>4}{'Faktor':>8}{'Nutzlast':>10}{'nass min':>11}"
          f"{'Bus':>9}  Huellkurve")
    for lab,f in OPT.items():
        for d in range(0, s["maxdis"]+1):
            np_=3+s["adv"]-d; M=f(np_); pay=s["base"]*M
            bus=loese(s,pay,s["adv"],d); r=bau(s,pay,s["adv"],d,max(bus,0))
            if bus<0:
                print(f"{lab:<20}{d:>5}{np_:>4}{M:>8.0f}{pay:>10.0f}{r['wet']:>11.1f}"
                      f"{'  —':>9}  zu schwer {r['wet']/s['anker']:.2f}x"); continue
            k=dict(pay_dry=100*pay/r["dry"],paybus_dry=100*(pay+bus)/r["dry"],
                   struct_dry=100*r["struct_kg"]/r["dry"],dry_wet=100*r["dry"]/r["wet"],
                   pp_dry=100*(r["pp_mass"]+r["batt_mass"])/r["dry"])
            aus=[n for n,(lo,hi) in HK.items() if not lo<=k[n]<=hi]
            print(f"{lab:<20}{d:>5}{np_:>4}{M:>8.0f}{pay:>10.0f}{r['wet']:>11.1f}{bus:>9.1f}  "
                  f"{5-len(aus)}/5" + (f" · {','.join(aus)}" if aus else " ALLE INNEN"))
        print()
