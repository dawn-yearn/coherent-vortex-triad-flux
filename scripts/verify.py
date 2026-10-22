"""Lightweight exact audit of exported certificates, not a full residual replay."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import subprocess
import sys
import os

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"
checks=0
def require(condition,label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks+=1
def read(name):
    return json.loads((E/name).read_text("utf-8"))
def record(x):
    if isinstance(x,dict):
        if {"center","radius","interval"} <= x.keys():
            c,r=F(x["center"]),F(x["radius"])
            require([c-r,c+r]==list(map(F,x["interval"])),"rational endpoints")
            if "outward_decimal" in x:
                lo,hi=map(F,x["outward_decimal"])
                require(lo<=c-r and c+r<=hi,"outward rounding")
        for v in x.values(): record(v)
    elif isinstance(x,list):
        for v in x: record(v)

for filename,item in read("source_manifest.json").items():
    require(hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==item["sha256"],
            "source hash "+filename)

temp=ROOT/"tmp"
temp.mkdir(exist_ok=True)
output=temp/"baseline_replayed.json"
subprocess.run([sys.executable,str(ROOT/"scripts/baseline_exact.py"),"--output",str(output)],
               check=True,timeout=58,capture_output=True,text=True,encoding="utf-8",
               env={**os.environ,"PYTHONIOENCODING":"utf-8"})
require(json.loads(output.read_text("utf-8"))==read("baseline.json"),"baseline replay")

full=read("full_certificate.json")
ind=read("full_independent.json")
m=read("mechanism.json")
levels=[read(f"sideband_{d}.json") for d in range(4)]
si=read("sideband_independent.json")
for item in [m,*levels,si]: record(item)
for c in [full,ind]:
    radius=F(c["radius"])
    require(sum(F(c[k]) for k in ["E_solve","E_tail_and_pruning","E_round"])==radius,
            "complete error-budget sum")
    require(radius<F("4.78e-9"),"absolute radius")
    for key,display in [("F",["-0.003965854562651","-0.003965845004717"]),
                        ("Delta",["0.000478589881793","0.000478599439728"])]:
        center=F(c[key+"_center"])
        lo,hi=map(F,c[key+"_interval"])
        require((lo,hi)==(center-radius,center+radius),"full endpoints")
        require(F(display[0])<=lo<=hi<=F(display[1]),"published outward enclosure")
    require(F(c["F_interval"][1])<0<F(c["Delta_interval"][0]),"certified signs")
    require(F(c["Delta_center"])==F(c["F_center"])+F(1,225),"exact baseline shift")
require(full["F_center"]==ind["F_center"],"independent full center")
require(full["candidate_sha256"]==ind["candidate_sha256"],"independent candidate binding")
require(F(full["E_spatial_exterior"])+F(full["E_pruning"])==F(full["E_tail_and_pruning"]),
        "tail/pruning split")
for g in m["groups"].values():
    require(F(g["connected"]["center"])+F(g["mean"]["center"])==F(g["raw"]["center"]),
            "raw = connected + mean")
for kind in ["raw","mean","connected"]:
    require(sum(F(m["groups"][g][kind]["center"]) for g in ["original","other"])
            ==F(m["groups"]["total"][kind]["center"]),"original + complement")
require(F(m["groups"]["total"]["raw"]["center"])==F(full["F_center"]),"mechanism/full binding")
sd=m["shift_decomposition"]
require(sum(F(sd[k]["center"]) for k in ["original_connected_change","other_connected","mean_total"])
        ==F(full["Delta_center"]),"three-way shift identity")
mean_lo,mean_hi=map(F,sd["mean_total"]["percent_of_Delta_interval"])
require(F("0.563853")<=mean_lo<=mean_hi<=F("0.563872"),"mean share")
require(100-mean_hi>F("99.43"),"connected share")
delta_lo,delta_hi=map(F,full["Delta_interval"])
require(F("10.768272")<=22500*delta_lo<=22500*delta_hi<=F("10.768488"),"attenuation")
positive=m["cancellation_masks"]["other_candidate_positive_raw"]["raw"]
negative=m["cancellation_masks"]["other_candidate_negative_raw"]["raw"]
require(F(positive["center"])+F(negative["center"])==F(m["groups"]["other"]["raw"]["center"]),
        "candidate signed cancellation; unlisted candidate zero")

modes={(3,0),(-3,0),(-2,1),(2,-1),(1,1),(-1,-1)}
for d,cert in enumerate(levels):
    require(set(map(tuple,cert["modes"]))==modes,f"reachable support {d}")
    require(cert["mode_count"]==[6,20,38,62][d],f"mode count {d}")
    classifications=[]
    for target,v in cert["targets"].items():
        s,rs=F(v["reduced"]["center"]),F(v["reduced"]["radius"])
        f,rf=F(v["full"]["center"]),F(v["full"]["radius"])
        require(abs(f)>rf,"nonzero full target")
        upper=(abs(s-f)+rs+rf)/(abs(f)-rf)
        lower=max(F(0),abs(s-f)-rs-rf)/(abs(f)+rf)
        require(upper==F(v["relative_error_upper"]) and lower==F(v["relative_error_lower"]),
                "target error interval "+target)
        classifications.append((lower,upper))
        if d==3:
            require(upper<F("0.0008530"),"all targets < 0.08530 percent")
            require(v["reduced"]==si["targets"][target]["reduced"],"independent reduced target")
    require(all(u<F("0.05") for l,u in classifications) if d==3
            else any(l>F("0.05") for l,u in classifications),"family acceptance/rejection")
    next_modes=set(modes)
    for x,y in modes:
        for a,b in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (x+a)**2+(y+b)**2>1 and a*y-b*x:
                next_modes.add((x+a,y+b))
    modes=next_modes
require(F(levels[2]["targets"]["other_candidate_negative_raw"]["relative_error_lower"])
        >F("0.051264"),"depth 2 strict rejection")
require(F(levels[3]["raw_error"])<F("9.44e-15"),"finite solve radius")
print(json.dumps({"status":"PASS","exact_checks":checks,"baseline_replayed":True,
    "mode_counts":[6,20,38,62],"passing_depth":3,
    "scope":"exported arithmetic and source integrity; not a full candidate/residual replay"}))
