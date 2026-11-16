"""Maliyet–güvenlik eğrisi ve 'tahmin edilen vs gerçekleşen' saldırı riski."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pilot as P

TARGETS = [0.0, 0.0025, 0.005, 0.01, 0.02, 0.04]


def run(seed):
    rng = np.random.default_rng(seed)
    C = P.make_customers(rng)
    Rtr, Rcal, Rte = (P.make_requests(rng, C, P.CFG[k]) for k in ("n_train", "n_cal", "n_test"))
    Ratt = P.make_requests(rng, C, P.CFG["n_attack"], kind="attack")
    loyal = rng.choice(np.flatnonzero(C["vip"]), P.CFG["loyal_pool_size"], replace=False)
    b3 = P.Fixed("B3", P.P2)
    pe_cal, _, _ = P.exec_probs(Rcal, b3.plans(Rcal, C))
    W = P.worst_case(Rcal); sub = W["unsafe"] & (W["amount"] <= P.CFG["review_threshold"])
    pw_b3, _, _ = P.exec_probs(W, b3.plans(W, C))
    rows = []
    for d in TARGETS:
        target = pe_cal[Rcal["unsafe"]].mean() + max(d, P.CFG["target_extra_uaer"])
        wc_target = pw_b3[sub].mean() + d
        for name, fset in [("VERIQEN-K", "TK"), ("Naif-K", "naive")]:
            s = P.Router(name, fset, fset == "TK", True).fit(Rtr, Rcal, C, target, wc_target)
            pl = s.plans(Rte, C)
            cost = float(np.mean([P.PLAN_COST[x] for x in pl]))
            pw, _, _ = P.exec_probs(W, s.plans(W, C))
            predicted = float(pw[sub].mean() - pw_b3[sub].mean())   # B3'e göre fazla risk (temiz veriden)
            ap, _, _ = P.attack(s, Ratt, C, loyal, np.random.default_rng(seed + 1))
            rows.append(dict(seed=seed, delta=d, system=name, cost=cost, _b3=None,
                             predicted_attack_uaer=predicted, realized_attack_uaer=float(ap.mean())))
    b3_attack = None
    for name, s in [("B3", b3), ("B1", P.Fixed("B1", P.P0))]:
        ap, _, _ = P.attack(s, Ratt, C, loyal, np.random.default_rng(seed + 1))
        rows.append(dict(seed=seed, delta=None, system=name,
                         cost=float(np.mean([P.PLAN_COST[x] for x in s.plans(Rte, C)])),
                         predicted_attack_uaer=None, realized_attack_uaer=float(ap.mean())))
    b3r = [r for r in rows if r["system"] == "B3"][0]["realized_attack_uaer"]
    for r in rows:
        if r["predicted_attack_uaer"] is not None:
            r["realized_excess"] = r["realized_attack_uaer"] - b3r
    return rows


if __name__ == "__main__":
    rows = [r for s in P.CFG["seeds"] for r in run(s)]
    json.dump(rows, open("results/sweep.json", "w"), indent=2, ensure_ascii=False)
    summ = json.load(open("results/summary.json"))["summary"]

    def agg(system, d):
        rs = [r for r in rows if r["system"] == system and r["delta"] == d]
        f = lambda k: (np.mean([r[k] for r in rs]), np.std([r[k] for r in rs], ddof=1))
        return f("cost"), f("realized_attack_uaer"), np.mean([r["predicted_attack_uaer"] for r in rs]), np.mean([r["realized_excess"] for r in rs])

    print("delta  sistem      maliyet   UAER_saldırı   fazla_risk_tahmin  fazla_risk_gerçek")
    table = []
    for d in TARGETS:
        for nm in ["VERIQEN-K", "Naif-K"]:
            (c, cs), (u, us), pred, real = agg(nm, d)
            table.append(dict(delta=d, system=nm, cost=c, cost_sd=cs, uaer=u, uaer_sd=us,
                              predicted_excess=pred, realized_excess=real))
            print(f"{d:<6} {nm:10s} {c:6.2f}±{cs:.2f}  {u:.3f}±{us:.3f}   {pred:+.4f}           {real:+.4f}")
    json.dump(table, open("results/sweep_table.json", "w"), indent=2, ensure_ascii=False)

    # Grafik
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    vk = [t for t in table if t["system"] == "VERIQEN-K"]
    nk = [t for t in table if t["system"] == "Naif-K"]
    ax.plot([t["cost"] for t in vk], [t["uaer"] * 100 for t in vk], "o-", color="#1f6f8b", lw=2,
            label="VERIQEN-K (güvenilir kaynak + anahtar + kötü durum kal.)")
    ax.plot([t["cost"] for t in nk], [t["uaer"] * 100 for t in nk], "s-", color="#c0392b", lw=2,
            label="Naif uyarlamalı (aynı kalibrasyonla)")
    pts = {"B3 sabit tam doğrulama": ("B3 sabit tam doğrulama", "#2c3e50", "D"),
           "B4-T (güvenilir kaynak)": ("Yalnız güvenilir kaynak", "#e67e22", "^"),
           "B1 yalnız kurallar": ("B1 yalnız kurallar", "#7f8c8d", "v")}
    for key, (lab, col, mk) in pts.items():
        a = summ[key]
        ax.scatter(a["cost"]["mean"], a["uaer_attack"]["mean"] * 100, color=col, marker=mk, s=70, zorder=5, label=lab)
    ax.set_xlabel("Doğrulama maliyeti (birim / karar, zararsız trafik)")
    ax.set_ylabel("Saldırı altında güvensiz yürütme oranı (%)")
    ax.set_yscale("log"); ax.set_ylim(5, 120)
    ax.set_yticks([5, 8, 10, 20, 50, 100]); ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.grid(alpha=0.3, which="both")
    ax.set_title("Pilot (sentetik): uyarlamalı doğrulama, beyaz kutu saldırgan altında", fontsize=10)
    ax.legend(fontsize=7.5, loc="center right")
    fig.tight_layout(); fig.savefig("results/pilot_tradeoff.png", dpi=160)
    print("grafik kaydedildi")
