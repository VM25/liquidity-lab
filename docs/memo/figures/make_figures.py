"""Figures for the research memo (docs/memo/liquidity_paradox.tex), drawn only from frozen result files.

Every plotted number is read from a committed artifact: the discovery reports' JSON/CSV outputs and the held-out
close-out analysis (results/closeout/closeout_analysis.json). Nothing is recomputed from market data, and no new
statistic of the held-out sessions is formed: test values are the frozen analysis's session values and means.

Usage (any Python with matplotlib; the project environment does not ship it):
    python3 docs/memo/figures/make_figures.py
"""

import csv
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CLOSE = json.loads((ROOT / "results/closeout/closeout_analysis.json").read_text())
E001 = json.loads((ROOT / "results/e001/e001_discovery.json").read_text())
E003 = json.loads((ROOT / "results/e003/e003_analysis.json").read_text())
E004 = json.loads((ROOT / "results/e004/e004_analysis.json").read_text())

# Two categorical slots of the reference palette (validated: adjacent CVD dE 24.7, normal-vision dE 33.6, >= 3:1 contrast)
DISC, TEST = "#eb6834", "#2a78d6"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8c8b86", "#e6e5e1"
TEST_DAYS = ["2026-06-01", "2026-07-01", "2026-08-01", "2026-09-01", "2026-10-01"]

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True,
    "font.size": 8.5, "axes.titlesize": 8.5, "axes.labelsize": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
})


def check(exp, cid):
    return next(c for c in CLOSE["experiments"][exp]["checks"] if c["id"] == cid)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------------------------- Figure 1: design
def fig_design():
    days = [f"{y}-{m:02d}-01" for y, m in [(2025, m) for m in range(3, 13)] + [(2026, m) for m in range(1, 11)]]
    fig, ax = plt.subplots(figsize=(6.3, 1.85))
    rows = [("E001, E002: all 15 discovery sessions", 2.0), ("E003, E004: walk-forward (fit on s1..s(k-1), evaluate s6..s15)", 1.0),
            ("Held-out evaluation: once, after the freeze", 0.0)]
    for i, d in enumerate(days):
        k = i + 1
        test = k > 15
        ax.scatter(i, 2.0, s=26, color=TEST if test else DISC, alpha=0.18 if test else 1, edgecolor="none", zorder=3)
        if not test:
            ax.scatter(i, 1.0, s=26, facecolor=DISC if k >= 6 else "white", edgecolor=DISC, linewidth=1.0, zorder=3)
        ax.scatter(i, 0.0, s=26, color=TEST if test else MUTED, alpha=1 if test else 0.25, edgecolor="none", zorder=3)
    for y, (label, _) in zip((2.0, 1.0, 0.0), rows):
        ax.text(-0.6, y + 0.32, label, fontsize=7.5, color=INK2, va="bottom", ha="left")
    ax.axvspan(-0.5, 9.5, color=DISC, alpha=0.05, lw=0)
    ax.axvspan(9.5, 14.5, color=DISC, alpha=0.11, lw=0)
    ax.axvspan(14.5, 19.5, color=TEST, alpha=0.09, lw=0)
    for x, t in ((4.5, "train (10)"), (12.0, "validation (5)"), (17.0, "held-out test (5)")):
        ax.text(x, -0.75, t, ha="center", fontsize=7.5, color=INK2)
    ticks = [0, 9, 14, 19]
    ax.set_xticks(ticks, [days[t][:7] for t in ticks])
    ax.set_yticks([])
    ax.set_ylim(-0.95, 2.7)
    ax.set_xlim(-0.8, 19.6)
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    save(fig, "fig1_design")


# ---------------------------------------------------------------------------------------------- Figure 2: E001 markouts
def fig_markouts():
    prim = {r["metric"]: r for r in E001["primary"] if r.get("spec") == "primary" and r.get("cell") == "all"}
    dsec = {r["metric"]: r["mean_of_session_means"] for r in CLOSE["experiments"]["E001"]["discovery_side"]["descriptive"]["secondary_horizons"]}
    tsec = {r["metric"]: r["mean_of_session_means"] for r in CLOSE["experiments"]["E001"]["reported_only"]["descriptive"]["secondary_horizons"]}
    hs = [0.1, 1, 5, 30, 60]
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.35))
    for ax, m, title in ((axes[0], "mo", r"Midpoint markout $mo(h)$, aggressor direction"),
                         (axes[1], "rs", r"Realized spread $rs(h)$ (passive side: $rs/2$)")):
        dv = [dsec[f"{m}_0.1s"], prim[f"{m}_1s"]["mean_of_session_means"], prim[f"{m}_5s"]["mean_of_session_means"],
              prim[f"{m}_30s"]["mean_of_session_means"], dsec[f"{m}_60s"]]
        tv = [tsec[f"{m}_0.1s"]] + [check("E001", f"E001 {m}_{h}s")["components"][f"{m}_{h}s"]["mean"] for h in (1, 5, 30)] + [tsec[f"{m}_60s"]]
        ax.axhline(0, color=MUTED, lw=0.7, zorder=1)
        ax.plot(hs, dv, color=DISC, lw=1.6, marker="o", ms=4, label="discovery (15 sessions)", zorder=3)
        ax.plot(hs, tv, color=TEST, lw=1.6, marker="o", ms=4, label="held-out test (5 sessions)", zorder=4)
        for h in (1, 5, 30):
            r = prim[f"{m}_{h}s"]
            ax.errorbar(h * 0.86, r["mean_of_session_means"], yerr=[[r["mean_of_session_means"] - r["ci95_lo"]], [r["ci95_hi"] - r["mean_of_session_means"]]],
                        color=DISC, lw=0.9, capsize=0, zorder=2)
            sv = check("E001", f"E001 {m}_{h}s")["components"][f"{m}_{h}s"]["session_values"]
            ax.scatter([h * 1.16] * len(sv), list(sv.values()), s=9, color=TEST, alpha=0.55, edgecolor="none", zorder=2)
        ax.set_xscale("log")
        ax.set_xticks(hs, ["0.1", "1", "5", "30", "60"])
        ax.minorticks_off()
        ax.set_xlabel("horizon $h$ (s)")
        ax.set_ylabel("bp of pre-event mid")
        ax.set_title(title, loc="left", color=INK)
    axes[0].legend(frameon=False, loc="lower right")
    fig.tight_layout(w_pad=2.0)
    save(fig, "fig2_markouts")


# ---------------------------------------------------------------------------------------------- Figure 3: fees vs fill models
def fig_fees():
    rows = [r for r in csv.DictReader((ROOT / "results/e002/e002_net_by_session.csv").open()) if r["policy"] == "P0" and r["latency"] == "tokyo"]
    sched = [("vip0", "VIP0, 10 / 10 bp (attainable)"), ("vip0_bnb", "VIP0 + BNB, 7.5 / 7.5 bp*"), ("vip9", "VIP9, 1.1 / 2.3 bp*"),
             ("lp_tier1", "LP tier 1, 0 / 2.3 bp*"), ("lp_tier4", "LP tier 4, $-$0.8 / 2.3 bp*")]
    fig, ax = plt.subplots(figsize=(6.3, 1.95))
    for i, (s, label) in enumerate(sched):
        means = []
        for fm in ("conservative", "intermediate", "optimistic"):
            v = [float(r["net_bp_per_notional"]) for r in rows if r["fee_schedule"] == s and r["fill_model"] == fm and r["net_bp_per_notional"]]
            means.append(statistics.mean(v))
        y = len(sched) - 1 - i
        ax.plot([min(means), max(means)], [y, y], color=DISC, lw=5, solid_capstyle="round", zorder=3)
        right = max(means) < -4
        ax.text(max(means) + 0.25 if right else min(means) - 0.25, y, f"${min(means):.1f}$ to ${max(means):.1f}$",
                ha="left" if right else "right", va="center", fontsize=7.5, color=INK2)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_yticks(range(len(sched)), [label for _, label in reversed(sched)])
    ax.set_xlim(-13.6, 0.6)
    ax.set_xlabel("net P&L, bp of traded notional (liquidation-adjusted)")
    ax.grid(axis="y", visible=False)
    save(fig, "fig3_fees")


# ---------------------------------------------------------------------------------------------- Figure 4: participation, not alpha
def fig_turnover():
    disc = E003["participation"]["policies"]
    test = CLOSE["experiments"]["E003"]["policies_vip0_descriptive"]["policies"]
    names = {"P0": "P0", "P1": "P1", "P3_M1": None, "P3_M2": "P3[M1], P3[M2]", "P3_negM2": "P3[$-$M2]", "P3F": "P3F, P4 (abstain)", "P4": None}
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.7), sharey=False)
    for ax, data, tkey, nkey, color, title in ((axes[0], disc, "turnover_per_hour", "mean", DISC, "Discovery (10 walk-forward sessions)"),
                                                (axes[1], test, "turnover_per_hour", "mean_net_per_hour", TEST, "Held-out test (5 sessions)")):
        xmax = max(v[tkey] for v in data.values()) * 1.12
        xs = [0, xmax]
        for bp, style in ((-10, (0, (4, 3))), (-12, (0, (1, 2)))):
            ax.plot(xs, [x * bp / 1e4 for x in xs], color=MUTED, lw=0.8, ls=style, zorder=1)

        for k, v in data.items():
            x, y = v[tkey], v[nkey]
            ax.scatter(x, y, s=30, color=color, edgecolor="white", linewidth=1.0, zorder=3)
            if names[k]:
                dx, dy, ha = xmax * 0.025, 0.0, "left"
                if k in ("P0", "P1", "P3_negM2"):
                    dx, ha = -xmax * 0.025, "right"
                    dy = {"P0": -0.035, "P1": 0.035, "P3_negM2": 0.0}[k] * abs(min(v2[nkey] for v2 in data.values()))
                ax.text(x + dx, y + dy, names[k], fontsize=7, color=INK2, ha=ha, va="center")
        ax.set_xlim(-xmax * 0.03, xmax)
        ax.legend(handles=[plt.Line2D([], [], color=MUTED, lw=0.8, ls=(0, (4, 3)), label="net $-$10 bp of notional"),
                           plt.Line2D([], [], color=MUTED, lw=0.8, ls=(0, (1, 2)), label="net $-$12 bp of notional")],
                  loc="lower left", frameon=False, handlelength=2.6)
        ax.set_xlabel("turnover, USDT of notional per valid hour")
        ax.set_title(title, loc="left")
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1e3:.0f}k"))
    axes[0].set_ylabel("net P&L at VIP0, USDT per valid hour")
    fig.tight_layout(w_pad=2.5)
    save(fig, "fig4_turnover")


# ---------------------------------------------------------------------------------------------- Figure 5: held-out checks
def fig_holdout():
    e3, e4 = E003, E004["primary"]
    panels = [
        ("E001 $rs(h)$, $h$ = 1, 5, 30 s (bp)", "e001"),
        ("E003 H1-F: $R^2_{\mathrm{OS}}$ of M2 at 5 s (%)", "h1f"),
        ("E003 H1-T: $D$, gross (bp)", "h1t"),
        ("E003 H3: P4 $-$ P3F, net/h (USDT)*", "h3"),
        ("E004 H4-W[P0]: $D_W$ (bp)", "h4p0"),
        ("E004 H4-W[P3[M2]]: $D_W$ (bp)", "h4p3"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(6.3, 4.1))
    for ax, (title, key) in zip(axes.flat, panels):
        ax.axhline(0, color=MUTED, lw=0.7, zorder=1)
        if key == "e001":
            prim = {r["metric"]: r for r in E001["primary"] if r.get("spec") == "primary" and r.get("cell") == "all"}
            for j, h in enumerate((1, 5, 30)):
                r = prim[f"rs_{h}s"]
                c = check("E001", f"E001 rs_{h}s")["components"][f"rs_{h}s"]
                draw(ax, j, r["mean_of_session_means"], (r["ci95_lo"], r["ci95_hi"]), c)
            ax.set_xticks([0, 1, 2], ["1 s", "5 s", "30 s"])
            ax.set_xlim(-0.6, 2.6)
            continue
        if key == "h1f":
            d = e3["H1"]["H1-F"]
            draw(ax, 0, d["mean"] * 100, [x * 100 for x in d["ci95"]], check("E003", "H1-F")["components"]["r2_os"], scale=100)
        elif key == "h1t":
            d = e3["H1"]["H1-T"]
            draw(ax, 0, d["mean"], d["ci95"], check("E003", "H1-T")["components"]["D_bp"])
            threshold(ax, 0.5, r"$\delta$ = 0.5 bp")
        elif key == "h3":
            d = e3["H3"]["net_per_hour_diff"]
            draw(ax, 0, d["mean"], d["ci95"], check("E003", "H3")["components"]["net_per_hour_diff"])
            threshold(ax, -e3["H3"]["noninferiority_margin"], r"$-\delta_h$")
        else:
            cid = "H4-W[P0]" if key == "h4p0" else "H4-W[P3_M2]"
            d = e4[cid]["D_W_bp"]
            draw(ax, 0, d["mean"], d["ci95"], check("E004", cid)["components"]["D_W_bp"])
            threshold(ax, 1.0, r"$\delta$ = 1 bp")
        ax.set_xticks([])
        ax.set_xlim(-0.8, 0.8)
    for ax, (title, _) in zip(axes.flat, panels):
        ax.set_title(title, loc="left", fontsize=7.8)
    h = [plt.Line2D([], [], color=DISC, marker="o", ms=4, lw=1.0, label="discovery mean, 95% session-bootstrap interval"),
         plt.Line2D([], [], color=TEST, marker="D", ms=4.5, lw=0, label="test mean (5 sessions)"),
         plt.Line2D([], [], color=TEST, marker="o", ms=3, lw=0, alpha=0.55, label="test session values"),
         plt.Line2D([], [], color=INK2, lw=0.8, ls=(0, (4, 3)), label="pre-registered threshold")]
    fig.legend(handles=h, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(h_pad=1.6, w_pad=1.4, rect=(0, 0.07, 1, 1))
    save(fig, "fig5_holdout")


def draw(ax, x, dmean, dci, comp, scale=1.0):
    ax.errorbar(x - 0.22, dmean, yerr=[[dmean - dci[0]], [dci[1] - dmean]], color=DISC, marker="o", ms=4, lw=1.0, capsize=0, zorder=3)
    sv = [v * scale for v in comp["session_values"].values()]
    offs = [-0.08, -0.04, 0.0, 0.04, 0.08][:len(sv)]
    ax.scatter([x + 0.22 + o for o in offs], sv, s=10, color=TEST, alpha=0.55, edgecolor="none", zorder=2)
    ax.scatter([x + 0.22], [comp["mean"] * scale], s=26, marker="D", color=TEST, edgecolor="white", linewidth=0.8, zorder=4)


def threshold(ax, y, label):
    ax.axhline(y, color=INK2, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.text(0.97, y, label, transform=ax.get_yaxis_transform(), fontsize=7, color=INK2, ha="right", va="top" if y > 0 else "bottom")


if __name__ == "__main__":
    assert CLOSE["mode"] == "test" and sorted(CLOSE["sessions"]["E001"]) == TEST_DAYS
    for f in (fig_design, fig_markouts, fig_fees, fig_turnover, fig_holdout):
        f()
    print("figures written to", OUT)
