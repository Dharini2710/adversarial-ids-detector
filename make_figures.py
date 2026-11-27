"""Figures of the paper.
Figure 1: workflow diagram. Figures 2 to 4: bar charts drawn from the result tables
(values copied from Tables 4, 9 and 10 of the paper: mean and std over 5 seeds).
Run:  python make_figures.py      (needs matplotlib; writes four PNG files to the current folder)
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

# ------------------------------------------------------------------ Figures 2 and 3
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
DS = ["CTU", "BOTNET", "CICIDS2018"]
M = ["Noise sensitivity", "Feature squeezing", "Confidence drop", "Mahalanobis", "Isolation Forest", "ECOD", "Autoencoder (early stop)", "Autoencoder (fixed 40 ep.)", "Ensemble disagreement (proposed)"]
AUROC = {"CTU": [(.504,.015),(.428,.023),(.486,.046),(.387,.003),(.604,.035),(.388,.008),(.481,.097),(.529,.020),(.935,.009)],
         "BOTNET": [(.441,.006),(.455,.030),(.443,.038),(.919,.001),(.602,.014),(.717,.001),(.932,.008),(.925,.015),(.961,.004)],
         "CICIDS2018": [(.444,.042),(.526,.116),(.525,.103),(.752,.012),(.540,.031),(.300,.010),(.987,.003),(.988,.003),(.982,.037)]}
TPR = {"CTU": [(.002,.002),(.001,.002),(.004,.003),(.014,.001),(.050,.036),(.013,.006),(.013,.004),(.025,.020),(.642,.086)],
       "BOTNET": [(.003,.001),(.005,.007),(.001,.003),(.728,.002),(.031,.006),(.035,.003),(.761,.007),(.761,.010),(.905,.018)],
       "CICIDS2018": [(.002,.003),(.125,.208),(.122,.205),(.266,.007),(.184,.104),(.000,.000),(.964,.066),(.994,.004),(.950,.098)]}
COL = ["#bdbdbd", "#9e9e9e", "#7f7f7f", "#e6b17e", "#d98c5f", "#c4676b", "#7aa6c9", "#4f81bd", "#1b3a6b"]
HAT = ["", "//", "..", "", "//", "..", "", "//", ""]
def grouped(data, ylabel, title, fname, ylim, ref=None):
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=300); n = len(M); w = 0.092; x = np.arange(len(DS))
    for i, m in enumerate(M):
        mu = [data[d][i][0] for d in DS]; sd = [data[d][i][1] for d in DS]; prop = (i == n - 1)
        ax.bar(x + (i - (n - 1) / 2) * w, mu, w * 0.94, yerr=sd, capsize=2, color=COL[i], hatch=HAT[i], edgecolor="black", linewidth=1.3 if prop else 0.6, error_kw=dict(lw=0.8, ecolor="#333"), label=m, zorder=3)
    if ref is not None:
        ax.axhline(ref, color="#555", ls="--", lw=0.9, zorder=1)
        ax.annotate(f"chance level ({ref:g})", xy=(1.005, ref), xycoords=("axes fraction", "data"), ha="left", va="center", fontsize=8.5, color="#444", annotation_clip=False)
    ax.set_xticks(x); ax.set_xticklabels(DS, fontsize=11); ax.set_ylim(*ylim); ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=11.5, fontweight="bold"); ax.grid(axis="y", color="#ddd", lw=0.6, zorder=0); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(ncol=3, fontsize=8.6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout(); fig.savefig(fname, facecolor="white", bbox_inches="tight"); plt.close(fig)
grouped(AUROC, "AUROC (higher is better)", "Detection of adversarial flows: AUROC of the proposed detector and existing detectors (mean \u00b1 std, 5 seeds)", "figure2_auroc_comparison.png", (0, 1.08), ref=0.5)
grouped(TPR, "Detection rate at about 5% false alarms", "Detection rate (TPR) of the proposed detector and existing detectors at a threshold set for about 5% false alarms (mean \u00b1 std, 5 seeds)", "figure3_detection_rate_comparison.png", (0, 1.12))

# ------------------------------------------------------------------ Figure 4 (robustness)
D4 = ["BOTNET", "CICIDS2018", "CTU", "NF-ToN-IoT-v2"]; A4 = ["A: black-box vs RF", "B: black-box vs RF and XGBoost", "C: adaptive (knows detector)", "G: gradient attack on surrogate"]
V = {"BOTNET": [(.011,.002),(.012,.002),(.035,.006),(0,0)], "CICIDS2018": [(.001,.001),(0,0),(.002,.003),(0,0)],
     "CTU": [(.525,.071),(.690,.064),(.911,.032),(.143,.108)], "NF-ToN-IoT-v2": [(.407,.100),(.439,.095),(.484,.125),(.100,.072)]}
fig, ax = plt.subplots(figsize=(9.5, 4.3), dpi=300); x = np.arange(len(D4)); w = 0.19; C = ["#1b3a6b", "#4f81bd", "#c4676b", "#9e9e9e"]; H = ["", "//", "..", "xx"]
for i, a in enumerate(A4):
    ax.bar(x + (i - 1.5) * w, [100 * V[d][i][0] for d in D4], w * 0.94, yerr=[100 * V[d][i][1] for d in D4], capsize=2, color=C[i], hatch=H[i], edgecolor="black", lw=0.6, label=a, zorder=3, error_kw=dict(lw=0.8))
ax.set_xticks(x); ax.set_xticklabels(D4, fontsize=11); ax.set_ylabel("Flows that evade the IDS and are not flagged (%)\n(lower is better)", fontsize=10); ax.set_ylim(0, 105)
ax.set_title("Robustness of the detector to stronger attackers (mean \u00b1 std, 5 seeds)", fontsize=11.5, fontweight="bold"); ax.grid(axis="y", color="#ddd", lw=0.6, zorder=0); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.legend(ncol=2, fontsize=9, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.1)); fig.tight_layout(); fig.savefig("figure4_robustness_undetected_evasion.png", facecolor="white", bbox_inches="tight"); plt.close(fig)

# ------------------------------------------------------------------ Figure 1 (workflow)
W, H = 145.0, 59.3
fig = plt.figure(figsize=(14.5, 5.93), dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
FONT = "DejaVu Sans"; CREAM, TAN, WHITE, EDGE, ARR = "#f8f3d4", "#e9e2bd", "#ffffff", "#2b2b2b", "#3a3a3a"
def box(x0, y0, x1, y1, fill=CREAM, lw=1.6):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=1.6", fc=fill, ec=EDGE, lw=lw, zorder=2))
def text(x, y, s, size=15, weight="normal", ha="center", color="#111", style="normal"):
    ax.text(x, y, s, fontsize=size, fontweight=weight, ha=ha, va="center", color=color, family=FONT, fontstyle=style, zorder=5, linespacing=1.25)
def arrow(p0, p1, color=ARR, lw=1.8):
    ax.annotate("", xy=p1, xytext=p0, zorder=4, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=16))
def line(p0, p1): ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=ARR, lw=1.8, zorder=4, solid_capstyle="butt")
box(1, 20, 17, 40, fill="#ddd69b"); text(9, 35.0, "Network\nflow X", 14, "bold"); text(9, 26.0, "CTU, BOTNET,\nCICIDS2018,\nNF-ToN-IoT-v2", 11)
box(20, 19, 42, 41); text(31, 37.0, "Preprocessing", 15, "bold"); text(21.4, 28.5, "\u2022 drop ID/label columns\n\u2022 fill missing values\n\u2022 standardise features", 11.5, ha="left")
box(52, 9, 90, 51, fill=WHITE); text(71, 48.6, "Heterogeneous ensemble", 13.5, "bold"); text(71, 45.9, "(trained on clean flows only)", 11, style="italic")
box(55, 31, 69, 42); text(62, 36.5, "Random\nForest", 13.5); box(55, 16, 69, 27); text(62, 21.5, "XGBoost", 13.5)
box(75, 32.5, 87, 40.5); text(81, 36.5, "P\u2081", 15, "bold"); box(75, 17.5, 87, 25.5); text(81, 21.5, "P\u2082", 15, "bold")
arrow((69, 36.5), (75, 36.5)); arrow((69, 21.5), (75, 21.5)); text(71, 12.4, "P = probability that a flow is malware", 11, style="italic")
box(93, 21, 111, 39); text(102, 34.6, "Disagreement", 14, "bold"); text(102, 31.2, "score", 14, "bold"); text(102, 25.6, "D(X) = |P\u2081 \u2212 P\u2082|", 12.5)
cx, cy, hw = 123, 30, 9.5
ax.add_patch(Polygon([(cx - hw, cy), (cx, cy + hw), (cx + hw, cy), (cx, cy - hw)], closed=True, fc="#c9c18f", ec=EDGE, lw=1.6, zorder=2)); text(cx, cy, "D(X) > \u03c4 ?", 13.5, "bold")
box(137.2, 26.2, 144.6, 33.8); text(140.9, 30, "Clean", 13, "bold"); box(114, 46, 132, 55); text(123, 50.5, "Adversarial", 14, "bold")
box(109, 2.5, 137, 14, fill=TAN); text(123, 10.6, "Threshold calibration", 12.5, "bold"); text(123, 6.2, "\u03c4 = 95th percentile of D on\nclean validation flows", 11)
arrow((17, 30), (20, 30)); line((42, 30), (49, 30)); arrow((49, 30), (55, 36.5)); arrow((49, 30), (55, 21.5))
arrow((87, 36.5), (93, 34.5)); arrow((87, 21.5), (93, 25.5)); arrow((111, 30), (cx - hw, cy))
arrow((cx + hw, cy), (137.2, 30), color="#c62828"); text(134.9, 32.4, "no", 11, color="#c62828", weight="bold")
arrow((cx, cy + hw), (cx, 46), color="#2e7d32"); text(cx + 3.4, 42.6, "yes", 11, color="#2e7d32", weight="bold")
arrow((cx, 14), (cx, cy - hw))
fig.savefig("figure1_workflow.png", dpi=200, facecolor="white"); print("saved four figures")
