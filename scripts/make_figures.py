"""Render analytic geometry and certified data; no PDE solve."""
from pathlib import Path
import json
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from paper_style import paper_style, COLORS, SIGNED_CMAP, DNS_COLOR

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
def read(name):
    return json.loads((ROOT / "evidence" / name).read_text("utf-8"))

full = read("full_certificate.json")
mech = read("mechanism.json")
levels = [read(f"sideband_{i}.json") for i in range(4)]
keys = ["original_connected_change", "other_connected",
        "other_candidate_positive_raw", "other_candidate_negative_raw", "Delta_total"]
labels = ["Original attenuation", "Other connected net", "Positive raw channels",
          "Negative raw channels", "Total shift"]
errors = [[100 * float(F(x["targets"][k]["relative_error_upper"])) for x in levels] for k in keys]
colors = [DNS_COLOR, COLORS[0], COLORS[1], COLORS[2]]
summary = {
    "scope": "Display-only floats derived from exact rational certificates.",
    "F_center": float(F(full["F_center"])),
    "Delta_center": float(F(full["Delta_center"])),
    "error_radius": float(F(full["radius"])),
    "mode_counts": [x["mode_count"] for x in levels],
    "target_keys": keys, "relative_error_upper_percent": errors,
    "channel_centers_micro": {
        k: float(F(mech["cancellation_masks"][k]["raw"]["center"])) * 1e6
        for k in ["other_candidate_positive_raw", "other_candidate_negative_raw"]},
}
(ROOT / "data/summary.json").write_text(json.dumps(summary, indent=2) + "\n", "utf-8")

with paper_style(font_size=13):
    fig = plt.figure(figsize=(13.8, 4.35))
    grid = fig.add_gridspec(1, 3, width_ratios=[1, 1.15, 1.02], wspace=.43)
    a, b, c = [fig.add_subplot(grid[0, j]) for j in range(3)]
    v = np.linspace(-np.pi, np.pi, 181)
    X, Y = np.meshgrid(v, v)
    W = np.cos(X) + np.cos(Y)
    a.contourf(X, Y, W, levels=np.linspace(-2, 2, 29), cmap=SIGNED_CMAP, vmin=-2, vmax=2)
    a.streamplot(v, v, -np.sin(Y), np.sin(X), density=.64, color="#404040",
                 linewidth=.65, arrowsize=.8)
    a.set(xlim=(-np.pi,np.pi), ylim=(-np.pi,np.pi), aspect="equal",
          xlabel=r"$x$", ylabel=r"$y$")
    a.set_xticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    a.set_yticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    a.set_title("(a) Cellular background", loc="left", fontweight="bold", pad=14)
    a.text(.5, -.25, r"$\omega_{\rm bg}=\cos x+\cos y$", transform=a.transAxes,
           ha="center", fontsize=14)
    nodes = [set(map(tuple, x["modes"])) for x in levels]
    for l in sorted(nodes[-1]):
        for e in [(1,0),(0,1)]:
            k = (l[0]+e[0], l[1]+e[1])
            if k in nodes[-1] and e[0]*l[1]-e[1]*l[0] != 0:
                b.plot([l[0], k[0]], [l[1],k[1]], color="#c8ced3", lw=.8, zorder=1)
    markers=["s","o","^","D"]
    previous=set()
    for i, ns in enumerate(nodes):
        points=np.array(sorted(ns-previous))
        b.scatter(points[:,0],points[:,1],s=43 if i==0 else 34,color=colors[i],
                  marker=markers[i],edgecolor="white",linewidth=.4,zorder=3)
        previous=ns
    b.scatter([0,1,-1,0,0],[0,0,0,1,-1],marker="x",s=24,color="#b0b0b0",linewidth=.8)
    b.set(xlim=(-5.7,5.7),ylim=(-4.6,4.6),aspect="equal",xlabel=r"$k_x$",ylabel=r"$k_y$")
    b.set_xticks([-4,-2,0,2,4]); b.set_yticks([-4,-2,0,2,4])
    b.set_title("(b) Reachable sidebands",loc="left",fontweight="bold",pad=14)
    handles=[Line2D([],[],marker=markers[i],color=colors[i],linestyle="",
                    label=f"Depth {i}") for i in range(4)]
    b.legend(handles=handles,loc="upper center",bbox_to_anchor=(.5,-.23),ncol=2,
             fontsize=11,columnspacing=1.3,handletextpad=.3)
    positive=summary["channel_centers_micro"]["other_candidate_positive_raw"]
    negative=summary["channel_centers_micro"]["other_candidate_negative_raw"]
    net=float(F(mech["groups"]["other"]["raw"]["center"]))*1e6
    values=[positive,negative,net]
    c.barh([2,1,0],values,color=[COLORS[0],COLORS[2],COLORS[1]],height=.55)
    radius=float(F(full["radius"]))*1e6
    c.errorbar(values,[2,1,0],xerr=radius,fmt="none",ecolor=DNS_COLOR,capsize=3,lw=.8)
    c.axvline(0,color=DNS_COLOR,lw=.8)
    c.set_yticks([2,1,0],["Positive","Negative","Raw net"])
    c.set(xlim=(-195,305),ylim=(-.65,2.65),xlabel=r"Flux coefficient $(10^{-6})$")
    c.set_xticks([-150,0,150,300])
    c.spines[["top","right","left"]].set_visible(False)
    c.tick_params(axis="y",length=0)
    for y,value in zip([2,1,0],values):
        c.text(value/2,y,f"{value:+.1f}",ha="center",va="center",color="white",
               fontsize=14,fontweight="bold")
    c.set_title("(c) New channels cancel",loc="left",fontweight="bold",pad=14)
    c.text(.5,-.25,"Fixed signed masks; bounded remainder",transform=c.transAxes,
           ha="center",fontsize=10.5,color="#555555")
    fig.subplots_adjust(left=.05,right=.985,bottom=.24,top=.86)
    for ext in ["png","svg"]:
        fig.savefig(ASSETS/f"mechanism.{ext}",dpi=220,bbox_inches="tight",pad_inches=.12)
    plt.close(fig)

with paper_style(font_size=13):
    fig, ax = plt.subplots(figsize=(9.8,3.7))
    fig.subplots_adjust(left=.10,right=.66,bottom=.23,top=.94)
    linecolors=[DNS_COLOR,COLORS[1],COLORS[0],COLORS[2],COLORS[4]]
    for vals,label,color,marker in zip(errors,labels,linecolors,["o","s","^","D","v"]):
        ax.plot(range(4),vals,label=label,color=color,marker=marker,ms=6,lw=1.5)
    ax.axhline(5,color="#777777",ls="--",lw=1)
    ax.text(.13,6.5,"5% acceptance limit",fontsize=11,color="#555555")
    ax.set_yscale("log")
    ax.set(xlim=(-.12,3.12),ylim=(.0008,200),ylabel="Certified relative error upper (%)")
    ax.set_xticks(range(4),["0\n6 modes","1\n20 modes","2\n38 modes","3\n62 modes"])
    ax.set_xlabel("Sideband depth")
    ax.set_yticks([.001,.01,.1,1,10,100],["0.001","0.01","0.1","1","10","100"])
    ax.grid(axis="y",which="major",alpha=.14)
    ax.legend(loc="center left",bbox_to_anchor=(1.02,.58),fontsize=11.5,labelspacing=1)
    ax.text(1.05,.13,"Depth 3:\nall targets < 0.08530%",transform=ax.transAxes,
            fontsize=12,color=COLORS[1],linespacing=1.5,fontweight="bold")
    for ext in ["png","svg"]:
        fig.savefig(ASSETS/f"convergence.{ext}",dpi=220)
    plt.close(fig)

# Formula images are shared by the print companion; transparent, high resolution.
formulae = {
"model":r"$\omega=A(\cos x+\cos y)+\epsilon\zeta,\qquad \widehat{\zeta}_k=0\quad(|k|\leq1)$",
"observable":r"$T_K(\zeta)=\langle GP_K\zeta,J(G\zeta,\zeta)\rangle,\qquad \mathcal{F}_{K,N}(\epsilon)=\epsilon\mu_{\epsilon,N}(T_K)$",
"uniform":r"$|\mathcal{F}_{K,N}(\epsilon)-\epsilon^2F_{A,K,N}|\leq C\epsilon^4,\qquad F_{A,K,N}\longrightarrow F_{A,K}$",
"decomposition":r"$F_A=t\kappa_{3,A}+t\,\mathrm{Sym}(m_{1,A}\otimes U_A)=F_A^{\mathrm{conn}}+F_A^{\mathrm{mean}}$",
"diagnostic":r"$\Pi_\ell^\parallel=-\sum_{i=1}^{3}\sum_{\alpha=x,y}\tau_{i\alpha}^{\ell}\partial_\alpha\bar{u}_i^\ell,\quad \tau_{i\alpha}^{\ell}=\overline{u_i u_\alpha}^{\,\ell}-\bar{u}_i^\ell\bar{u}_\alpha^\ell$",
}
with paper_style(font_size=15):
    for name,formula in formulae.items():
        fig=plt.figure(figsize=(10,.5))
        fig.text(.5,.5,formula,ha="center",va="center")
        fig.savefig(ASSETS/f"eq-{name}.png",dpi=300,bbox_inches="tight",pad_inches=.05,transparent=True)
        plt.close(fig)
print("Rendered 2 figures (PNG/SVG), 5 formula images and summary.json")
