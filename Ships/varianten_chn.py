#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variantenrechnung: was kostet Haertung? Volle Penaltykette, Anker fest."""
import math, importlib.util, json
OW=("/root/.claude/skills/synced/2c0e114f-f980-4879-be59-84347099c9f5_"
    "db129feb-ec7e-452e-ac0f-412f398c1773/orbitalwerk/scripts/nachbau.py")
sp=importlib.util.spec_from_file_location("nb",OW); nb=importlib.util.module_from_spec(sp); sp.loader.exec_module(nb)

def k2(base, adv, dis):
    np_=3+adv-dis
    if np_<=0:  cm,x3=1.0,1.0
    elif np_==1: cm,x3=2.0,3.0
    else:        cm,x3=float(np_),3.0
    return np_, cm, x3, base*cm*x3

SCHIFFE = {
 "Himmelsauge (Aufklaerer, LEO 600 km)": dict(
   anker=2000.0, base=1000.0, isp=230, prop="hydrazine", dv=50.0, ld=2.5, house=6.0, batt=0.6,
   eng=[dict(thrust_n=22, mass_kg=6, count=4)], sc="ruggedized"),
 "Feldzeichen (Scorer, LEO..GEO)": dict(
   anker=2000.0, base=1000.0, isp=315, prop="mmh_nto", dv=1000.0, ld=2.5, house=3.6, batt=1.2,
   eng=[dict(thrust_n=490, mass_kg=16, count=1), dict(thrust_n=22, mass_kg=6, count=4)], sc="ruggedized"),
 "Himmelsbruecke (Relais, GEO)": dict(
   anker=5000.0, base=150.0, isp=1600, prop="xenon", dv=750.0, ld=2.6, house=15.0, batt=1.2,
   eng=[dict(thrust_n=0.083, mass_kg=45, count=4, p_kw=1.35, p_count=2, waste_kw=0.54)], sc="ruggedized"),
}

def bau(s, pay, adv, dis, bus):
    return nb.build(dict(struct_class=s["sc"], adv=adv, disadv=dis, payload_kg=pay,
        misc_kg=bus, house_kw=s["house"], pp_type="solar", pp_alpha=15.0, au=1.0,
        batt_hours=s["batt"], batt_alpha=5, rad_alpha=5.0, ld=s["ld"], isp=s["isp"],
        prop=s["prop"], dv_target=s["dv"], engines=s["eng"]))

def min_masse(s, pay, adv, dis):
    """Untergrenze: Bus = 0."""
    return bau(s, pay, adv, dis, 0.0)["wet"]

VAR = [(a,d) for a in (0,1,2,3) for d in (0,1,2,3,4,5)]
for name, s in SCHIFFE.items():
    print(f"\n{'='*96}\n{name}   Anker {s['anker']:.0f} kg · Basisnutzlast {s['base']:.0f} kg · "
          f"Isp {s['isp']} · dv {s['dv']:.0f} m/s\n{'='*96}")
    print(f"{'Vort':>4}{'Nach':>5}{'np':>4}{'cm':>4}{'HE':>4}{'Nutzlast':>10}{'Struktur':>10}"
          f"{'nass min':>11}{'  Urteil':<24}")
    for a,d in VAR:
        np_,cm,x3,pay = k2(s["base"], a, d)
        w = min_masse(s, pay, a, d)
        passt = w <= s["anker"]+1e-6
        rest = s["anker"]-w
        urteil = f"PASST, Bus frei {rest:7.1f} kg" if passt else f"zu schwer {w/s['anker']:5.2f}x Anker"
        print(f"{a:>4}{d:>5}{np_:>4}{cm:>4.0f}{x3:>4.0f}{pay:>10.0f}"
              f"{15+max(0,a-d):>8.0f} %{w:>11.1f}  {urteil:<24}")
