"""Build the website's data bundles from frozen research artifacts.

Writes web/src/data/core.json (prose numbers, research figures, the held-out label table) and web/src/data/lab.json
(the Scenario Lab grids). Every number is a record carrying its value, display precision, verbatim status, sample,
held-out label where one applies, and a `src` pointer that resolves back to the frozen file (registry.resolve).
Nothing is recomputed from market data and no new statistic of the held-out sessions is formed.

Usage:
    python3 web/export/build_bundle.py          # write the bundles
    python3 web/export/build_bundle.py --check  # fail if the committed bundles differ from a fresh build
"""

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry as R  # noqa: E402

OUT = R.ROOT / "web" / "src" / "data"
CLOSE = "/experiments"
STATUS_OBS, STATUS_MOD = "observed", "modeled historical replay"
FEE_STATUS = {"vip0": "attainable", "vip0_bnb": "hypothetical", "vip9": "hypothetical", "lp_tier1": "hypothetical",
              "lp_tier4": "hypothetical"}
FEE_LABEL = {"vip0": "VIP0", "vip0_bnb": "VIP0 + BNB", "vip9": "VIP9", "lp_tier1": "LP tier 1", "lp_tier4": "LP tier 4"}
POLICIES = ["NT", "P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4"]
CODE = {"NT": "NT", "P0": "P0", "P1": "P1", "P3_M1": "P3[M1]", "P3_M2": "P3[M2]", "P3_negM2": "P3[−M2]", "P3F": "P3F",
        "P4": "P4"}
LAB_METRICS = ["net_per_hour", "gross_per_hour", "net_bp_per_notional", "gross_bp_per_notional", "turnover_per_hour",
               "inc_es", "max_drawdown", "tw_abs_inventory_avg", "max_abs_inventory", "quote_presence_both",
               "fill_rate", "own_markout_1s_bp", "own_markout_5s_bp", "own_markout_30s_bp"]


def display_label(label, basis):
    """The held-out label as CLOSEOUT_report.md prints it: "confirmed (point estimate, 5 of 5 defined)"."""
    if not basis:
        return label
    return f"{label.split(' (')[0]} ({basis})"


class Bundle:
    def __init__(self):
        self.values = {}

    def rec(self, rid, key, pointer, unit, d, st, smp, signed=False, pct=False, lab=None, scale=1.0, note=None):
        raw = R.json_pointer(R.load(key), pointer)
        v = None if raw is None else raw * scale
        r = {"v": v, "u": unit, "d": d, "st": st, "smp": smp, "src": f"{R.path_of(key)}#{pointer}"}
        if signed:
            r["s"] = True
        if pct:
            r["pct"] = True
        if scale != 1.0:
            r["scale"] = scale
        if lab:
            r["lab"] = lab
        if note:
            r["note"] = note
        self._put(rid, r)
        return r

    def paper(self, rid, fragment, value, unit, d, st, smp, signed=False, lab=None, printed=None):
        """A number printed in the frozen paper. `printed` (default: the formatted value) must appear on that line."""
        line = R.paper_line(fragment)
        r = {"v": value, "u": unit, "d": d, "st": st, "smp": smp, "src": f"{R.path_of('paper')}#L{line}",
             "frag": fragment, "printed": printed if printed is not None else fragment}
        if signed:
            r["s"] = True
        if lab:
            r["lab"] = lab
        self._put(rid, r)
        return r

    def param(self, rid, key, pointer, unit, d, scale=1.0):
        raw = R.json_pointer(R.load(key), pointer)
        r = {"v": raw * scale, "u": unit, "d": d, "st": "parameter", "smp": "parameter",
             "src": f"{R.path_of(key)}#{pointer}"}
        if scale != 1.0:
            r["scale"] = scale
        self._put(rid, r)
        return r

    def _put(self, rid, r):
        if rid in self.values:
            raise KeyError(f"duplicate record {rid}")
        self.values[rid] = r


def index_of(rows, **match):
    hits = [i for i, r in enumerate(rows) if all(r.get(k) == v for k, v in match.items())]
    if len(hits) != 1:
        raise LookupError(f"{match}: {len(hits)} rows")
    return hits[0]


def check_index(exp, cid):
    return index_of(R.load("close")["experiments"][exp]["checks"], id=cid)


# --------------------------------------------------------------------------------------------- E001
def e001(b):
    prim = R.load("e001")["primary"]
    close = R.load("close")["experiments"]["E001"]
    out = {"horizons": [], "held_sessions": {}}
    for m in ("mo", "rs", "es"):
        hs = ("",) if m == "es" else ("_1s", "_5s", "_30s")
        for h in hs:
            metric = m + h
            i = index_of(prim, metric=metric, spec="primary", cell="all")
            base = f"/primary/{i}"
            b.rec(f"e001.{metric}.disc", "e001", f"{base}/mean_of_session_means", "bp", 2, STATUS_OBS, "discovery", signed=True)
            b.rec(f"e001.{metric}.disc_lo", "e001", f"{base}/ci95_lo", "bp", 2, STATUS_OBS, "discovery", signed=True)
            b.rec(f"e001.{metric}.disc_hi", "e001", f"{base}/ci95_hi", "bp", 2, STATUS_OBS, "discovery", signed=True)
            b.rec(f"e001.{metric}.disc_pos", "e001", f"{base}/sessions_positive", "sessions", 0, STATUS_OBS, "discovery")
            if m == "es":
                lab = display_label(close["es"]["label"], close["es"]["label_basis"])
                b.rec("e001.es.held", "close", f"{CLOSE}/E001/es/components/es/mean", "bp", 2, STATUS_OBS, "heldout", signed=True, lab=lab)
                continue
            j = check_index("E001", f"E001 {metric}")
            chk = close["checks"][j]
            lab = display_label(chk["label"], chk["label_basis"])
            cp = f"{CLOSE}/E001/checks/{j}/components/{metric}"
            b.rec(f"e001.{metric}.held", "close", f"{cp}/mean", "bp", 2, STATUS_OBS, "heldout", signed=True, lab=lab)
            b.rec(f"e001.{metric}.held_neg", "close", f"{cp}/negative", "sessions", 0, STATUS_OBS, "heldout", lab=lab)
            b.rec(f"e001.{metric}.held_pos", "close", f"{cp}/positive", "sessions", 0, STATUS_OBS, "heldout", lab=lab)
            out["held_sessions"][metric] = {day: b.rec(f"e001.{metric}.held.{day}", "close", f"{cp}/session_values/{day}", "bp", 3, STATUS_OBS, "heldout", signed=True, lab=lab)["v"]
                                            for day in chk["components"][metric]["session_values"]}
    j = check_index("E001", "E001 rs_1s")
    b.rec("e001.rs_1s.held_tlo", "close", f"{CLOSE}/E001/checks/{j}/components/rs_1s/t_interval_95_descriptive_not_used/0", "bp", 2, STATUS_OBS, "heldout", signed=True, lab="descriptive, not used")
    b.rec("e001.rs_1s.held_thi", "close", f"{CLOSE}/E001/checks/{j}/components/rs_1s/t_interval_95_descriptive_not_used/1", "bp", 2, STATUS_OBS, "heldout", signed=True, lab="descriptive, not used")
    # secondary horizons (descriptive) on both sides, as the paper's Figure 2 draws them
    for side, block, smp in (("disc", "discovery_side", "discovery"), ("held", "reported_only", "heldout")):
        rows = close[block]["descriptive"]["secondary_horizons"]
        for metric in ("mo_0.1s", "mo_60s", "rs_0.1s", "rs_60s"):
            i = index_of(rows, metric=metric)
            b.rec(f"e001.{metric}.{side}", "close", f"{CLOSE}/E001/{block}/descriptive/secondary_horizons/{i}/mean_of_session_means",
                  "bp", 2, STATUS_OBS, smp, signed=True, lab="secondary horizon, descriptive")
    b.rec("e001.events.disc", "e001", "/events_primary", "events", 0, STATUS_OBS, "discovery")
    b.rec("e001.events.held", "close_e001", "/events_primary", "events", 0, STATUS_OBS, "heldout")
    b.paper("e001.rs_share_5_30", "52 and 56\\% of discovery size", None, "", 0, STATUS_OBS, "heldout", printed="52 and 56%")
    out["tally"] = close["tally"]
    out["family"] = close["family"]
    return out


# --------------------------------------------------------------------------------------------- E002
def e002(b):
    cfg = R.load("cfg_e002")["fees"]
    fees = []
    rows = R.load("e002_net")
    for sid in ("vip0", "vip0_bnb", "vip9", "lp_tier1", "lp_tier4"):
        b.param(f"fee.{sid}.maker", "cfg_e002", f"/fees/{sid}/maker", "bp", 1, scale=1e4)
        b.param(f"fee.{sid}.taker", "cfg_e002", f"/fees/{sid}/taker", "bp", 1, scale=1e4)
        means = {}
        for fm in ("conservative", "intermediate", "optimistic"):
            v = [float(r["net_bp_per_notional"]) for r in rows
                 if r["policy"] == "P0" and r["latency"] == "tokyo" and r["fee_schedule"] == sid and r["fill_model"] == fm and r["net_bp_per_notional"]]
            means[fm] = statistics.mean(v)
        fees.append({"id": sid, "label": FEE_LABEL[sid], "status": FEE_STATUS[sid], "cfg_label": cfg[sid]["label"],
                     "by_fill": means, "lo": min(means.values()), "hi": max(means.values()),
                     "src": f"{R.path_of('e002_net')}?policy=P0&latency=tokyo&fee_schedule={sid}#net_bp_per_notional",
                     "op": "mean over discovery sessions per fill model, as docs/memo/figures/make_figures.py (fig_fees)"})
    h2 = R.load("e002")
    hc = R.load("close")["experiments"]["E002"]["reported_only"]["scenario_table"]
    matrix = []
    for i, r in enumerate(h2["scenario_table"]):
        j = index_of(hc, policy=r["policy"], fill_model=r["fill_model"], latency=r["latency"])
        matrix.append({"policy": r["policy"], "fill": r["fill_model"], "latency": r["latency"],
                       "disc": r["mean"], "disc_lo": r["ci95_lo"], "disc_hi": r["ci95_hi"], "disc_n": r["sessions_defined"],
                       "held": hc[j]["mean"], "held_n": hc[j]["sessions_defined"],
                       "src_disc": f"{R.path_of('e002')}#/scenario_table/{i}",
                       "src_held": f"{R.path_of('close')}#{CLOSE}/E002/reported_only/scenario_table/{j}"})
    b.paper("e002.range.disc", "lay between $-11.07$ and $-11.87$", None, "bp", 2, STATUS_MOD, "discovery", printed="−11.87 to −11.07")
    b.paper("e002.range.held", "lay between $-10.99$ and $-11.95$", None, "bp", 2, STATUS_MOD, "heldout", printed="−11.95 to −10.99",
            lab="reported only, no confirmation claim")
    b.paper("e002.fill_diff", "0.16 to 0.55\\bp, all below the 1.0\\bp{} threshold", None, "bp", 2, STATUS_MOD, "discovery", printed="0.16 to 0.55")
    return {"fees": fees, "matrix": matrix, "status": "modeled historical replay; VIP0 attainable, other schedules hypothetical",
            "heldout_label": "reported only, no confirmation claim", "note": R.load("close")["experiments"]["E002"]["note"]}


# --------------------------------------------------------------------------------------------- E003
def e003(b):
    e3 = R.load("e003")
    close = R.load("close")["experiments"]["E003"]
    for cid in ("H1-F", "H1-T", "H3"):
        j = check_index("E003", cid)
        chk = close["checks"][j]
        lab = display_label(chk["label"], chk["label_basis"])
        if cid == "H1-F":
            b.rec("e003.h1f.disc", "e003", "/H1/H1-F/mean", "%", 2, STATUS_OBS, "discovery_walkforward", pct=True)
            b.rec("e003.h1f.disc_lo", "e003", "/H1/H1-F/ci95/0", "%", 2, STATUS_OBS, "discovery_walkforward", pct=True)
            b.rec("e003.h1f.disc_hi", "e003", "/H1/H1-F/ci95/1", "%", 2, STATUS_OBS, "discovery_walkforward", pct=True)
            b.rec("e003.h1f.held", "close", f"{CLOSE}/E003/checks/{j}/components/r2_os/mean", "%", 2, STATUS_OBS, "heldout", pct=True, lab=lab)
            sv = chk["components"]["r2_os"]["session_values"]
        elif cid == "H1-T":
            st = "modeled historical replay (gross, fee-free)"
            b.rec("e003.h1t.disc", "e003", "/H1/H1-T/mean", "bp", 2, st, "discovery_walkforward", signed=True)
            b.rec("e003.h1t.disc_lo", "e003", "/H1/H1-T/ci95/0", "bp", 2, st, "discovery_walkforward", signed=True)
            b.rec("e003.h1t.disc_hi", "e003", "/H1/H1-T/ci95/1", "bp", 2, st, "discovery_walkforward", signed=True)
            b.rec("e003.h1t.disc_pos", "e003", "/H1/H1-T/positive", "sessions", 0, st, "discovery_walkforward")
            cp = f"{CLOSE}/E003/checks/{j}/components/D_bp"
            b.rec("e003.h1t.held", "close", f"{cp}/mean", "bp", 2, st, "heldout", signed=True, lab=lab)
            b.rec("e003.h1t.held_neg", "close", f"{cp}/negative", "sessions", 0, st, "heldout", lab=lab)
            b.rec("e003.h1t.held_tlo", "close", f"{cp}/t_interval_95_descriptive_not_used/0", "bp", 2, st, "heldout", signed=True, lab="descriptive, not used")
            b.rec("e003.h1t.held_thi", "close", f"{cp}/t_interval_95_descriptive_not_used/1", "bp", 2, st, "heldout", signed=True, lab="descriptive, not used")
            b.rec("e003.h1t.delta", "e003", "/H1/H1-T/margin_bp", "bp", 1, "parameter", "parameter")
            sv = chk["components"]["D_bp"]["session_values"]
        else:
            st = "modeled historical replay; LP tier 4 fees are hypothetical, not attainable"
            for comp, d in (("es_diff", 2), ("drawdown_diff", 1), ("net_per_hour_diff", 2)):
                b.rec(f"e003.h3.{comp}.disc", "e003", f"/H3/{comp}/mean", "USDT" if comp != "net_per_hour_diff" else "USDT/h", d, st, "discovery_walkforward", signed=True)
                b.rec(f"e003.h3.{comp}.disc_lo", "e003", f"/H3/{comp}/ci95/0", "USDT" if comp != "net_per_hour_diff" else "USDT/h", d, st, "discovery_walkforward", signed=True)
                b.rec(f"e003.h3.{comp}.disc_hi", "e003", f"/H3/{comp}/ci95/1", "USDT" if comp != "net_per_hour_diff" else "USDT/h", d, st, "discovery_walkforward", signed=True)
                b.rec(f"e003.h3.{comp}.held", "close", f"{CLOSE}/E003/checks/{j}/components/{comp}/mean", "USDT" if comp != "net_per_hour_diff" else "USDT/h", d, st, "heldout", signed=True, lab=lab)
            b.rec("e003.h3.margin", "e003", "/H3/noninferiority_margin", "USDT/h", 2, st, "discovery_walkforward")
            sv = chk["components"]["net_per_hour_diff"]["session_values"]
        b.values[f"e003.{cid.lower().replace('-', '')}.held_sessions"] = {
            "v": None, "u": "", "d": 0, "st": chk["status"], "smp": "heldout", "lab": lab,
            "src": f"{R.path_of('close')}#{CLOSE}/E003/checks/{j}/components", "sessions": sv}
    # P3[M2] − P0 (fill avoidance), discovery interval and the held-out fee split
    b.rec("e003.p3m2_p0.disc", "e003", "/H1/reported/P3_M2_minus_P0_net_per_hour/mean", "USDT/h", 0, STATUS_MOD, "discovery_walkforward", signed=True)
    b.rec("e003.p3m2_p0.disc_lo", "e003", "/H1/reported/P3_M2_minus_P0_net_per_hour/ci95/0", "USDT/h", 0, STATUS_MOD, "discovery_walkforward")
    b.rec("e003.p3m2_p0.disc_hi", "e003", "/H1/reported/P3_M2_minus_P0_net_per_hour/ci95/1", "USDT/h", 0, STATUS_MOD, "discovery_walkforward")
    b.rec("e003.p3m2_p0.disc_pos", "e003", "/H1/reported/P3_M2_minus_P0_net_per_hour/positive", "sessions", 0, STATUS_MOD, "discovery_walkforward")
    held_lab = "reported only, descriptive (no confirmation claim)"
    b.rec("e003.p3m2_p0.held", "close", f"{CLOSE}/E003/reported_only/H1_reported/P3_M2_minus_P0_net_per_hour/mean", "USDT/h", 1, STATUS_MOD, "heldout", signed=True, lab=held_lab)
    b.rec("e003.p3m2_p0.held_pos", "close", f"{CLOSE}/E003/reported_only/H1_reported/P3_M2_minus_P0_net_per_hour/positive", "sessions", 0, STATUS_MOD, "heldout", lab=held_lab)
    b.rec("e003.p3m2_p0.held_fee_saving", "close", f"{CLOSE}/E003/reported_only/fee_split_per_hour_vip0/P3_M2_minus_P0_net_per_hour/maker_fees_per_hour_mean_mechanical",
          "USDT/h", 1, STATUS_MOD, "heldout", lab=held_lab, scale=-1.0, note="maker fees not paid (mechanical): the frozen maker-fee difference with its sign reversed")
    b.rec("e003.p3m2_p0.held_gross", "close", f"{CLOSE}/E003/reported_only/fee_split_per_hour_vip0/P3_M2_minus_P0_net_per_hour/gross_per_hour_mean",
          "USDT/h", 1, STATUS_MOD, "heldout", lab=held_lab)
    # P0 gross and net per notional at the primary scenario (the fee link of the homepage chain)
    sc = e3["descriptive"]["scenarios"]
    i = index_of(sc, policy="P0", fill_model="intermediate", latency="regional", fee_schedule="vip0")
    b.rec("e003.p0_primary.gross_bp", "e003", f"/descriptive/scenarios/{i}/gross_bp_per_notional", "bp", 2, "modeled historical replay (gross, fee-free)", "discovery_walkforward", signed=True)
    b.rec("e003.p0_primary.net_bp", "e003", f"/descriptive/scenarios/{i}/net_bp_per_notional", "bp", 2, STATUS_MOD, "discovery_walkforward", signed=True)
    hs = close["reported_only"]["descriptive"]["scenarios"]
    k = index_of(hs, policy="P0", fill_model="intermediate", latency="regional", fee_schedule="vip0")
    hp = f"{CLOSE}/E003/reported_only/descriptive/scenarios/{k}"
    b.rec("e003.p0_primary.held_gross_bp", "close", f"{hp}/gross_bp_per_notional", "bp", 2, "modeled historical replay (gross, fee-free)", "heldout", signed=True, lab=held_lab)
    b.rec("e003.p0_primary.held_net_bp", "close", f"{hp}/net_bp_per_notional", "bp", 2, STATUS_MOD, "heldout", signed=True, lab=held_lab)
    # forecast skill by model and horizon
    skill = []
    for side, base, smp in (("disc", "/descriptive/forecasts", "discovery_walkforward"), ("held", f"{CLOSE}/E003/reported_only/descriptive/forecasts", "heldout")):
        key = "e003" if side == "disc" else "close"
        rows = R.json_pointer(R.load(key), base)
        for k, r in enumerate(rows):
            skill.append({"side": side, "model": r["model"], "h": r["horizon_s"], "r2": r["r2_os"], "ic": r["ic"], "hit": r["hit_rate"],
                          "src": f"{R.path_of(key)}#{base}/{k}", "smp": smp})
    # the eight policies at VIP0, primary scenario (paper Table 5; Figure 4)
    part = e3["participation"]["policies"]
    pv = close["policies_vip0_descriptive"]["policies"]
    pol = []
    for p in POLICIES:
        if p == "NT":
            continue
        pol.append({"policy": p, "code": CODE[p],
                    "disc_net": part[p]["mean"], "disc_lo": part[p]["ci95"][0], "disc_hi": part[p]["ci95"][1], "disc_turnover": part[p]["turnover_per_hour"],
                    "disc_pos": part[p]["positive"],
                    "held_net": pv[p]["mean_net_per_hour"], "held_turnover": pv[p]["turnover_per_hour"], "held_gross": pv[p]["gross_per_hour"],
                    "held_maker": pv[p]["maker_fees_per_hour_mechanical"], "held_taker": pv[p]["taker_fees_per_hour"],
                    "held_with_trades": pv[p]["sessions_with_trades"], "held_sessions": pv[p]["session_values"],
                    "src_disc": f"{R.path_of('e003')}#/participation/policies/{p}",
                    "src_held": f"{R.path_of('close')}#{CLOSE}/E003/policies_vip0_descriptive/policies/{p}"})
    return {"skill": skill, "policies_vip0": pol, "tally": close["tally"],
            "policies_status": close["policies_vip0_descriptive"]["status"], "policies_note": close["policies_vip0_descriptive"]["note"]}


def _has(obj, pointer):
    try:
        R.json_pointer(obj, pointer)
        return True
    except (KeyError, IndexError, TypeError):
        return False


# --------------------------------------------------------------------------------------------- E004
def e004(b):
    e4 = R.load("e004")
    close = R.load("close")["experiments"]["E004"]
    st = "modeled historical replay under stress test"
    out = {"tally": close["tally"], "scope_note": close["scope_note"]}
    for cid, key in (("H4-W[P0]", "p0"), ("H4-W[P3_M2]", "p3m2")):
        j = check_index("E004", cid)
        chk = close["checks"][j]
        lab = display_label(chk["label"], chk["label_basis"]) + ": " + chk["interpretation"]
        b.rec(f"e004.{key}.disc", "e004", f"/primary/{cid}/D_W_bp/mean", "bp", 2, st, "discovery_walkforward", signed=True)
        b.rec(f"e004.{key}.disc_lo", "e004", f"/primary/{cid}/D_W_bp/ci95/0", "bp", 2, st, "discovery_walkforward", signed=True)
        b.rec(f"e004.{key}.disc_hi", "e004", f"/primary/{cid}/D_W_bp/ci95/1", "bp", 3 if key == "p3m2" else 2, st, "discovery_walkforward", signed=True)
        cp = f"{CLOSE}/E004/checks/{j}/components/D_W_bp"
        b.rec(f"e004.{key}.held", "close", f"{cp}/mean", "bp", 2, st, "heldout", signed=True, lab=lab)
        b.rec(f"e004.{key}.held_neg", "close", f"{cp}/negative", "sessions", 0, st, "heldout", lab=lab)
        b.rec(f"e004.{key}.held_below", "close", f"{CLOSE}/E004/checks/{j}/sign_count_below_delta", "sessions", 0, st, "heldout", lab=lab)
        b.values[f"e004.{key}.held_sessions"] = {"v": None, "u": "", "d": 0, "st": st, "smp": "heldout", "lab": lab,
                                                 "src": f"{R.path_of('close')}#{cp}/session_values", "sessions": chk["components"]["D_W_bp"]["session_values"]}
        out[f"{key}_interpretation"] = chk["interpretation"]
    yv = close["h4f_y_view"]
    for cell in ("D1_S", "D3"):
        c = yv["cells"][cell]
        lab = display_label(c["label"], c["label_basis"])
        b.rec(f"e004.yview.{cell}.held", "close", f"{CLOSE}/E004/h4f_y_view/cells/{cell}/rho_A", "", 3, "stress test", "heldout", lab=lab)
        b.rec(f"e004.yview.{cell}.disc", "close", f"{CLOSE}/E004/h4f_y_view/cells/{cell}/discovery_rho_A", "", 3, "stress test", "discovery_walkforward")
    out["yview"] = {"row_label": yv["row_label"], "note": yv["note"], "secondary": yv["secondary"]}
    for cell in ("D1_S", "D3"):
        b.rec(f"e004.yk.{cell}.held", "close", f"{CLOSE}/E004/reported_only/h4f_other/{cell}:y_k/rho_A", "", 2, "stress test", "heldout", lab="reported only")
        b.rec(f"e004.yk.{cell}.projection", "close", f"{CLOSE}/E004/reported_only/h4f_other/{cell}:y_k/projection/rho_a", "", 2, "stress test", "parameter")
    b.paper("e004.yk.disc", "$\\rho_A=0.57$; \\emph{inconclusive}", 0.57, "", 2, "stress test", "discovery_walkforward")
    b.rec("e004.h40.disc", "e004", "/secondary/H4-0/difference_pp/mean", "pp", 2, "observed (model trained under stress test)", "discovery_walkforward", signed=True)
    b.rec("e004.h40.held", "close", f"{CLOSE}/E004/reported_only/H4_0/difference_pp/mean", "pp", 3, "observed (model trained under stress test)", "heldout", signed=True, lab="reported only")
    out["h40_label"] = e4["secondary"]["H4-0"]["label"]
    return out


# --------------------------------------------------------------------------------------------- held-out evaluation
def holdout(b):
    close = R.load("close")
    ledger = R.load("ledger")
    meta = R.load("close_meta")
    ticks = {day: b.rec(f"holdout.tick.{day}", "close", f"/relative_tick_bp/{day}", "bp", 2, "observed", "heldout")["v"] for day in close["relative_tick_bp"]}
    return {"ledger": ledger, "attempt": meta["attempt"], "freeze_record_sha256": meta["freeze_record_sha256"],
            "relative_tick_bp": ticks, "tallies": {e: close["experiments"][e].get("tally") for e in ("E001", "E002", "E003", "E004")},
            "not_refutation": close["not_refutation"], "fee_attainability": close["fee_attainability"],
            "undefined_sessions": close["undefined_sessions"], "sessions": close["sessions"]["E001"]}


# --------------------------------------------------------------------------------------------- label table (paper Tables 6 and 7)
def labels():
    close = R.load("close")["experiments"]
    rows = []

    def chk(exp, cid, title, status, disc, test, extra=None):
        j = check_index(exp, cid)
        c = close[exp]["checks"][j]
        rows.append({"exp": exp, "id": cid, "title": title, "status": status, "rule": c["rule"], "discovery": disc, "heldout": test,
                     "label": display_label(c["label"], c["label_basis"]), "interpretation": c.get("interpretation"),
                     "comment": extra, "kind": "check", "src": f"{R.path_of('close')}#{CLOSE}/{exp}/checks/{j}"})

    for m in ("mo_1s", "mo_5s", "mo_30s", "rs_1s", "rs_5s", "rs_30s"):
        chk("E001", f"E001 {m}", f"{m.split('_')[0]} {m.split('_')[1][:-1]} s", "observed", {"ids": [f"e001.{m}.disc"]}, {"ids": [f"e001.{m}.held"]})
    chk("E003", "H1-F", "H1-F forecast skill", "observed", {"ids": ["e003.h1f.disc"]}, {"ids": ["e003.h1f.held"]}, "sign of a mean only")
    chk("E003", "H1-T", "H1-T translation", "modeled historical replay (gross, fee-free)", {"ids": ["e003.h1t.disc"]}, {"ids": ["e003.h1t.held"]},
        "by a margin of 0.01 bp; weakest label")
    chk("E003", "H3", "H3 risk components (P4 − P3F)", "modeled historical replay; LP tier 4 fees hypothetical", {"ids": ["e003.h3.es_diff.disc", "e003.h3.drawdown_diff.disc", "e003.h3.net_per_hour_diff.disc"]},
        {"ids": ["e003.h3.es_diff.held", "e003.h3.drawdown_diff.held", "e003.h3.net_per_hour_diff.held"]}, "hypothetical fees; net gain about a fifth of discovery")
    chk("E004", "H4-W[P0]", "H4-W[P0] stale-window fill quality", "modeled historical replay under stress test", {"ids": ["e004.p0.disc"]}, {"ids": ["e004.p0.held"]})
    chk("E004", "H4-W[P3_M2]", "H4-W[P3[M2]] stale-window fill quality", "modeled historical replay under stress test", {"ids": ["e004.p3m2.disc"]}, {"ids": ["e004.p3m2.held"]})
    yv = close["E004"]["h4f_y_view"]
    rows.append({"exp": "E004", "id": "H4-F y_view", "title": "H4-F y_view, D1-S and D3 (secondary)", "status": "stress test",
                 "rule": yv["cells"]["D1_S"]["rule"], "discovery": {"ids": ["e004.yview.D1_S.disc", "e004.yview.D3.disc"]},
                 "heldout": {"ids": ["e004.yview.D1_S.held", "e004.yview.D3.held"]},
                 "label": display_label(yv["cells"]["D1_S"]["label"], yv["cells"]["D1_S"]["label_basis"]), "interpretation": None,
                 "comment": "secondary, outside the tally; largely implied by the target choice", "kind": "secondary",
                 "src": f"{R.path_of('close')}#{CLOSE}/E004/h4f_y_view"})
    reported = [
        {"exp": "E001", "id": "es", "title": "E001 effective spread", "status": "observed", "discovery": {"ids": ["e001.es.disc"]}, "heldout": {"ids": ["e001.es.held"]},
         "label": "reported only", "comment": "close to mechanical; no confirmatory weight"},
        {"exp": "E002", "id": "H2", "title": "E002 H2 execution sensitivity", "status": "modeled historical replay", "discovery": {"text": "not supported"},
         "heldout": {"ids": ["e002.range.held"]}, "label": "reported only, no confirmation claim", "comment": "E002 §10.10"},
        {"exp": "E003", "id": "participation", "title": "E003 participation at VIP0", "status": "modeled historical replay", "discovery": {"text": "no policy's interval above zero; abstention rational"},
         "heldout": {"text": "every policy that trades lost in 5 of 5 sessions; P3F and P4 abstained"}, "label": "descriptive, no label or rule", "comment": None},
        {"exp": "E004", "id": "H4-F y_k", "title": "E004 H4-F y_k, D1-S and D3", "status": "stress test", "discovery": {"ids": ["e004.yk.disc"], "text": "inconclusive"},
         "heldout": {"ids": ["e004.yk.D1_S.held", "e004.yk.D3.held"]}, "label": "reported only", "comment": "reported against the projection"},
        {"exp": "E004", "id": "H4-0", "title": "E004 H4-0 do-no-harm on clean data", "status": "observed (model trained under stress test)",
         "discovery": {"ids": ["e004.h40.disc"], "text": "harmless"}, "heldout": {"ids": ["e004.h40.held"]}, "label": "reported only", "comment": None},
    ]
    for r in reported:
        r["kind"] = "reported"
    return rows + reported


# --------------------------------------------------------------------------------------------- sample and parameters
def sample(b):
    # paper Table 1 (sample); every value is printed in the frozen paper
    for rid, frag, v, d in (("sample.disc.sessions", "Sessions & 15 & 10 & 5", 15, 0), ("sample.wf.sessions", "Sessions & 15 & 10 & 5", 10, 0),
                            ("sample.held.sessions", "Sessions & 15 & 10 & 5", 5, 0), ("sample.disc.episodes", "Episodes & 29 & 19 & 20", 29, 0),
                            ("sample.wf.episodes", "Episodes & 29 & 19 & 20", 19, 0), ("sample.held.episodes", "Episodes & 29 & 19 & 20", 20, 0),
                            ("sample.disc.hours", "Valid hours & 347.5 & 227.9 & 119.7", 347.5, 1), ("sample.wf.hours", "Valid hours & 347.5 & 227.9 & 119.7", 227.9, 1),
                            ("sample.held.hours", "Valid hours & 347.5 & 227.9 & 119.7", 119.7, 1)):
        b.paper(rid, frag, v, "", d, "metadata", "paper", printed=frag)
    b.paper("sample.disc.tick", "Relative tick (bp) & 0.46--1.20", None, "bp", 2, "metadata", "paper", printed="0.46–1.20")
    b.paper("sample.held.tick", "& --- & 0.85--1.38", None, "bp", 2, "metadata", "paper", printed="0.85–1.38")
    cfg = R.load("cfg_e002")["latency"]
    for lat in ("tokyo", "regional", "distant"):
        b.param(f"lat.{lat}.entry_ms", "cfg_e002", f"/latency/{lat}/entry_us", "ms", 0, scale=1e-3)
        b.param(f"lat.{lat}.md_ms", "cfg_e002", f"/latency/{lat}/md_delay_us", "ms", 0, scale=1e-3)
    for k, rid, d in (("size", "pol.size", 0), ("inventory_limit", "pol.limit", 0), ("p1_threshold", "pol.p1", 0), ("p4_kappa_ticks_per_unit", "pol.kappa", 2)):
        b.param(rid, "cfg_e003", f"/policies/{k}", "SOL" if k != "p4_kappa_ticks_per_unit" else "tick/SOL", d)
    b.param("pacing.rate", "cfg_e003", "/pacing/rate_per_s", "orders/s per side", 2)
    splits = R.load("cfg_research")["splits"]
    return {"latency_labels": {k: v["label"] for k, v in cfg.items()},
            "splits": {k: splits[k] for k in ("train", "validation", "test")},
            "splits_src": f"{R.path_of('cfg_research')}#/splits",
            "walkforward": R.load("e003")["evaluation_sessions"]}


# --------------------------------------------------------------------------------------------- the frozen paper files
def paper_files():
    pins = dict(reversed(line.split(maxsplit=1)) for line in R.load("memo_frozen").splitlines() if line.strip())
    out = []
    for key, title in (("paper_pdf", "The Liquidity Paradox (paper, PDF)"), ("supplement_pdf", "Reproducibility supplement (PDF)")):
        path = R.path_of(key)
        assert R.sha256(key) == pins[path], path
        out.append({"title": title, "path": path, "file": path.split("/")[-1], "sha256": pins[path], "bytes": len(R.raw_bytes(key))})
    return {"files": out, "frozen": [{"path": p, "sha256": h} for p, h in pins.items()],
            "frozen_src": R.path_of("memo_frozen")}


# --------------------------------------------------------------------------------------------- Scenario Lab
def lab():
    e3 = R.load("e003")
    close = R.load("close")["experiments"]
    grid = {"disc": {}, "held": {}}
    for side, rows in (("disc", e3["descriptive"]["scenarios"]), ("held", close["E003"]["reported_only"]["descriptive"]["scenarios"])):
        for s in rows:
            grid[side][f'{s["policy"]}|{s["fill_model"]}|{s["latency"]}|{s["fee_schedule"]}'] = [s[m] for m in LAB_METRICS]
    sess = {}
    for r in R.load("e003_net"):
        k = f'{r["policy"]}|{r["fill_model"]}|{r["latency"]}|{r["fee_schedule"]}'
        sess.setdefault(k, {})[r["day"]] = [None if not r["net_per_hour"] else float(r["net_per_hour"]),
                                            None if not r["turnover_per_hour"] else float(r["turnover_per_hour"])]
    part = {p: {"lo": v["ci95"][0], "hi": v["ci95"][1]} for p, v in e3["participation"]["policies"].items()}
    pv = close["E003"]["policies_vip0_descriptive"]["policies"]
    held_sess = {p: v["session_values"] for p, v in pv.items()}
    e4 = R.load("e004")["descriptive"]
    c4 = close["E004"]["reported_only"]["descriptive"]
    keep = ("delta_gross_bp", "delta_net_per_hour_vip0", "delta_net_per_hour_lp_tier4", "fee_saving_per_hour_vip0_mechanical")

    def contrasts(block):
        return {base: {c: {k: block[base][c][k] for k in keep if k in block[base][c]} for c in ("U-P", "U-N", "P-N")} for base in ("P0", "P3_M2")}

    return {
        "metrics": LAB_METRICS, "policies": POLICIES, "codes": CODE, "fees": FEE_LABEL, "fee_status": FEE_STATUS,
        "grid": grid, "grid_src": {"disc": f"{R.path_of('e003')}#/descriptive/scenarios", "held": f"{R.path_of('close')}#{CLOSE}/E003/reported_only/descriptive/scenarios"},
        "disc_sessions": sess, "disc_sessions_src": R.path_of("e003_net"), "disc_sessions_cols": ["net_per_hour", "turnover_per_hour"],
        "disc_ci_primary_vip0": part, "disc_ci_src": f"{R.path_of('e003')}#/participation/policies",
        "held_sessions_primary_vip0": held_sess, "held_sessions_src": f"{R.path_of('close')}#{CLOSE}/E003/policies_vip0_descriptive/policies",
        "held_label": "reported only, descriptive (no confirmation claim)",
        "e004": {"status": "modeled historical replay under stress test",
                 "disc_window": e4["window_quality"], "held_window": c4["window_quality"],
                 "disc_contrasts": contrasts(e4["policy_D1_E"]), "held_contrasts": contrasts(c4["policy_D1_E"]),
                 "src_disc": f"{R.path_of('e004')}#/descriptive", "src_held": f"{R.path_of('close')}#{CLOSE}/E004/reported_only/descriptive",
                 "held_label": "descriptive test replication, never a confirmation"},
        "untested": {
            "fill_naive": "the naive fill model is an E002 reference, outside the pre-registered E003 runs",
            "fee_untested": "VIP0 + BNB and LP tier 1 were run for E002 only, not for the E003 policies",
            "e004_latency": "E004 was run at regional latency only",
            "e004_fill": "the D1-S condition was run with the intermediate fill model only",
            "limits": "inventory limits were fixed per policy and never varied",
            "paths": "not exported as frozen artifacts; high-frequency data rights unresolved",
        },
    }


# --------------------------------------------------------------------------------------------- build
def build():
    b = Bundle()
    core = {
        "e001": e001(b), "e002": e002(b), "e003": e003(b), "e004": e004(b), "holdout": holdout(b),
        "labels": labels(), "sample": sample(b), "paper": paper_files(),
    }
    core["values"] = b.values
    labd = lab()
    used = sorted({key for key in R.SOURCES if R.path_of(key) in R._cache})
    meta = {"generator": "web/export/build_bundle.py", "sources": {R.path_of(k): R.sha256(k) for k in used},
            "note": "Frozen values only. Held-out values come from the frozen close-out analysis and pre-outcome metadata."}
    core["meta"] = meta
    labd["meta"] = meta
    return core, labd


def dump(obj):
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def main(argv):
    core, labd = build()
    files = {OUT / "core.json": dump(core), OUT / "lab.json": dump(labd)}
    if "--check" in argv:
        stale = [p.name for p, text in files.items() if not p.exists() or p.read_text() != text]
        if stale:
            print("stale bundles:", ", ".join(stale), "(run: npm run export)")
            return 1
        print("bundles up to date")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for p, text in files.items():
        p.write_text(text)
        print(f"wrote {p.relative_to(R.ROOT)} ({len(text):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
