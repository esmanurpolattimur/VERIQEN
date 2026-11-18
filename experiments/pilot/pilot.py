"""
VERIQEN pilot deneyi — sentetik iade senaryosu.

Amaç: Risk-uyarlamalı doğrulamanın "doğrulama düşürme" saldırısına açık olup
olmadığını ve "güvenilir kaynak" ile "güvenilir anahtar" ayrımının etkisini ölçmek.

Bu bir PİLOT çalışmadır: veriler sentetik, parametreler varsayımsaldır,
ön kayıt yapılmamıştır. Sonuçlar hipotez üretmek içindir, kanıt değildir.
"""
import json
import numpy as np

# ---------------------------------------------------------------------------
# Sabitler (varsayımsal; results/config.json'a yazılır)
# ---------------------------------------------------------------------------
CFG = dict(
    n_customers=5000, fraud_share=0.06, n_train=6000, n_cal=6000, n_test=10000,
    n_attack=3000, review_threshold=300.0, hard_limit=1000.0,
    cost_carrier=1.0, cost_fraud=4.0,
    p_carrier_detect=0.95, p_fraud_detect=0.92,
    fp_carrier=0.005, fp_fraud=0.01, p_human_catch=0.85,
    opportunistic_rate=0.03, loyal_pool_size=30,
    floor_new_account_months=6.0, floor_amount_p1=150.0,
    target_extra_uaer=0.01, seeds=[11, 22, 33, 44, 55], n_boot=2000,
)
P0, P1, P2 = 0, 1, 2          # P0: ek doğrulama yok, P1: kargo, P2: kargo + dolandırıcılık
PLAN_COST = {P0: 0.0, P1: CFG["cost_carrier"], P2: CFG["cost_carrier"] + CFG["cost_fraud"]}


# ---------------------------------------------------------------------------
# Dünya: müşteriler (güvenilir veritabanı) ve istekler
# ---------------------------------------------------------------------------
def make_customers(rng):
    n = CFG["n_customers"]
    fraud = rng.random(n) < CFG["fraud_share"]
    tenure = np.where(fraud, rng.gamma(1.0, 4.0, n), rng.gamma(2.0, 18.0, n))
    refunds90 = np.where(fraud, rng.poisson(1.5, n), rng.poisson(0.3, n))
    vip = (~fraud) & (tenure > 36) & (rng.random(n) < 0.6)
    return dict(fraud=fraud, tenure=tenure, refunds90=refunds90, vip=vip)


def make_requests(rng, C, n, kind="natural"):
    """kind='natural': gerçek trafik; kind='attack': dolandırıcının ≤ inceleme eşiği istekleri."""
    nC = len(C["fraud"])
    if kind == "natural":
        cust = rng.integers(0, nC, n)
    else:
        fraud_ids = np.flatnonzero(C["fraud"])
        cust = rng.choice(fraud_ids, n)
    is_fraud = C["fraud"][cust]
    amount = np.where(is_fraud, rng.lognormal(4.8, 0.6, n), rng.lognormal(4.2, 0.8, n))
    amount = np.clip(amount, 5, 1500)
    if kind == "attack":
        amount = np.clip(amount, 5, CFG["review_threshold"])  # saldırgan inceleme eşiğinin altında kalır
    # Gerçek durum ve iddia
    opportunistic = (~is_fraud) & (rng.random(n) < CFG["opportunistic_rate"])
    unsafe = is_fraud | opportunistic
    legit_reason = rng.choice(["not_delivered", "damaged", "other"], n, p=[0.3, 0.5, 0.2])
    fraud_reason = rng.choice(["not_delivered", "damaged"], n, p=[0.8, 0.2])
    claim = np.where(is_fraud, fraud_reason, np.where(opportunistic, "not_delivered", legit_reason))
    false_nd_claim = unsafe & (claim == "not_delivered")   # kargo kontrolünün yakalayabileceği yalan
    # Ajanın beyanları (güvenilmez kanal)
    true_vip = C["vip"][cust]
    declared_vip = np.where(is_fraud, rng.random(n) < 0.10,
                            np.where(rng.random(n) < 0.9, true_vip, ~true_vip))
    inj = np.where(is_fraud, rng.beta(1.5, 15, n), rng.beta(1.0, 25, n))
    return dict(cust=cust, key=cust.copy(), amount=amount, unsafe=unsafe, is_fraud=is_fraud,
                claim=claim, false_nd_claim=false_nd_claim, declared_vip=declared_vip.astype(bool),
                declared_reason=claim.copy(), inj=inj)


# ---------------------------------------------------------------------------
# Özellikler ve risk modeli
# ---------------------------------------------------------------------------
def features(R, C, fset):
    """fset: 'naive' (tümü, ajan anahtarıyla), 'T' (güvenilir kaynak, ajan anahtarıyla),
    'TK' (güvenilir kaynak, oturum anahtarıyla)."""
    key = R["cust"] if fset == "TK" else R["key"]
    cols = [np.log(R["amount"]), np.log1p(C["tenure"][key]), C["refunds90"][key].astype(float)]
    if fset == "naive":
        cols += [R["declared_vip"].astype(float),
                 (R["declared_reason"] == "not_delivered").astype(float), R["inj"] * 10]
    X = np.column_stack(cols)
    return np.column_stack([np.ones(len(X)), X])


def fit_logreg(X, y, l2=1e-2, iters=3000, lr=0.1):
    mu, sd = X[:, 1:].mean(0), X[:, 1:].std(0) + 1e-9
    Z = X.copy(); Z[:, 1:] = (Z[:, 1:] - mu) / sd
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        g = Z.T @ (p - y) / len(y) + l2 * np.r_[0, w[1:]]
        w -= lr * g
    return dict(w=w, mu=mu, sd=sd)


def predict(m, X):
    Z = X.copy(); Z[:, 1:] = (Z[:, 1:] - m["mu"]) / m["sd"]
    return 1 / (1 + np.exp(-Z @ m["w"]))


# ---------------------------------------------------------------------------
# Karar: taban + plan + doğrulayıcılar (beklenen değer hesabı)
# ---------------------------------------------------------------------------
def exec_probs(R, plans, use_floor_checks=True):
    """Her vaka için (yürütülme olasılığı, REVIEW mi, güvenli-ama-engellenme olasılığı)."""
    n = len(R["amount"])
    review = (R["amount"] > CFG["review_threshold"]) & use_floor_checks
    hard_block = (R["amount"] > CFG["hard_limit"]) & use_floor_checks
    has_carrier = plans >= P1
    has_fraud = plans >= P2
    # Güvensiz vaka: her doğrulayıcının kaçırma olasılığı çarpılır
    miss = np.ones(n)
    miss *= np.where(has_carrier & R["false_nd_claim"], 1 - CFG["p_carrier_detect"], 1.0)
    miss *= np.where(has_fraud & R["is_fraud"], 1 - CFG["p_fraud_detect"], 1.0)
    miss *= np.where(review, 1 - CFG["p_human_catch"], 1.0)
    # Güvenli vaka: yanlış pozitif ile engellenme
    pass_safe = np.ones(n)
    pass_safe *= np.where(has_carrier, 1 - CFG["fp_carrier"], 1.0)
    pass_safe *= np.where(has_fraud, 1 - CFG["fp_fraud"], 1.0)
    p_exec = np.where(R["unsafe"], miss, pass_safe)
    p_exec = np.where(hard_block, 0.0, p_exec)
    p_false_block = np.where(R["unsafe"], 0.0, np.where(hard_block, 1.0, 1 - pass_safe))
    return p_exec, review, p_false_block


def apply_floor(plans, R, C):
    """Monoton taban (yalnızca oturum anahtarlı güvenilir bilgiyle)."""
    p = plans.copy()
    p = np.where(C["tenure"][R["cust"]] < CFG["floor_new_account_months"], np.maximum(p, P2), p)
    p = np.where(R["amount"] > CFG["floor_amount_p1"], np.maximum(p, P1), p)
    return p


def worst_case(R):
    """Yönlendirmeyi değiştiremeyen saldırganın yapabileceği en kötü şey: manipüle edilebilir
    doğrulayıcıyı (kargo) etkisiz bırakmak. Yalnızca yönlendirme saldırgandan bağımsızsa geçerlidir."""
    r = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in R.items()}
    r["false_nd_claim"][:] = False
    r["claim"] = np.where(r["unsafe"], "damaged", r["claim"])
    return r


class Router:
    def __init__(self, name, fset, floor, worst_case_cal=False):
        self.name, self.fset, self.floor, self.wc = name, fset, floor, worst_case_cal

    def fit(self, Rtr, Rcal, C, target_uaer, wc_target=None):
        self.m = fit_logreg(features(Rtr, C, self.fset), Rtr["unsafe"].astype(float))
        r = predict(self.m, features(Rcal, C, self.fset))
        qs = np.quantile(r, np.linspace(0, 1, 41))
        best = None
        for i, t1 in enumerate(qs):
            for t2 in qs[i:]:
                plans = self._plans(r, t1, t2, Rcal, C)
                pe, _, _ = exec_probs(Rcal, plans)
                u = pe[Rcal["unsafe"]].mean()
                ok = u <= target_uaer
                if self.wc:   # saldırı altı riski temiz kalibrasyon verisinden kestir (değişmezlik sayesinde)
                    W = worst_case(Rcal); sub = W["unsafe"] & (W["amount"] <= CFG["review_threshold"])
                    pw, _, _ = exec_probs(W, plans)
                    ok = ok and pw[sub].mean() <= wc_target
                cost = np.mean([PLAN_COST[x] for x in plans])
                if ok and (best is None or cost < best[0]):
                    best = (cost, t1, t2)
        if best is None:                      # hedef tutturulamazsa en güvenli plan
            best = (None, -1.0, -1.0)
        _, self.t1, self.t2 = best
        return self

    def _plans(self, r, t1, t2, R, C):
        plans = np.where(r >= t2, P2, np.where(r >= t1, P1, P0))
        return apply_floor(plans, R, C) if self.floor else plans

    def plans(self, R, C):
        return self._plans(predict(self.m, features(R, C, self.fset)), self.t1, self.t2, R, C)


class Fixed:
    def __init__(self, name, plan, floor_checks=True):
        self.name, self.plan, self.floor_checks = name, plan, floor_checks

    def plans(self, R, C):
        return np.full(len(R["amount"]), self.plan)


# ---------------------------------------------------------------------------
# Beyaz kutu saldırgan
# ---------------------------------------------------------------------------
def manipulate(R, combo, victim, inj_low, inj_high):
    """combo ⊆ {D1, D2, D5}. Tüm vakalar için değiştirilmiş kopya döndürür (vektörel)."""
    r = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in R.items()}
    uses_injection = ("D1" in combo) or ("D5" in combo)
    if "D1" in combo:                                  # beyan manipülasyonu
        r["declared_reason"][:] = "damaged"; r["declared_vip"][:] = True
        r["claim"][:] = "damaged"; r["false_nd_claim"][:] = False   # kargo kontrolü artık yakalayamaz
    if "D5" in combo:                                  # anahtar kaydırma: başka müşterinin kaydı okunur
        r["key"][:] = victim
    if uses_injection:
        r["inj"] = (inj_low if "D2" in combo else inj_high).copy()
    return r


COMBOS = [(), ("D1",), ("D5",), ("D1", "D5"), ("D1", "D2"), ("D2", "D5"), ("D1", "D2", "D5")]


def attack(system, R, C, loyal, rng_inj):
    """Her vaka için başarı olasılığını maksimize eden manipülasyonu seçer (beyaz kutu)."""
    n = len(R["amount"])
    inj_low, inj_high = rng_inj.beta(1.0, 15, n), rng_inj.beta(6, 4, n)
    best_p = np.full(n, -1.0); best_plan = np.zeros(n, int); best_combo = np.empty(n, dtype=object)
    fc = getattr(system, "floor_checks", True)
    for combo in COMBOS:
        victims = loyal if "D5" in combo else [None]
        for v in victims:
            r = manipulate(R, combo, v, inj_low, inj_high)
            pl = system.plans(r, C)
            pe, _, _ = exec_probs(r, pl, fc)
            better = (pe > best_p + 1e-12) | ((np.abs(pe - best_p) <= 1e-12) & (pl < best_plan))
            best_p = np.where(better, pe, best_p)
            best_plan = np.where(better, pl, best_plan)
            for i in np.flatnonzero(better):
                best_combo[i] = combo
    return best_p, best_plan, list(best_combo)


# ---------------------------------------------------------------------------
# Deney
# ---------------------------------------------------------------------------
def boot_ci(x, rng, n_boot):
    idx = rng.integers(0, len(x), (n_boot, len(x)))
    m = x[idx].mean(1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    C = make_customers(rng)
    Rtr, Rcal, Rte = (make_requests(rng, C, CFG[k]) for k in ("n_train", "n_cal", "n_test"))
    Ratt = make_requests(rng, C, CFG["n_attack"], kind="attack")
    loyal = rng.choice(np.flatnonzero(C["vip"]), CFG["loyal_pool_size"], replace=False)

    b3 = Fixed("B3 sabit tam doğrulama", P2)
    pe_b3_cal, _, _ = exec_probs(Rcal, b3.plans(Rcal, C))
    target = pe_b3_cal[Rcal["unsafe"]].mean() + CFG["target_extra_uaer"]
    W = worst_case(Rcal); sub = W["unsafe"] & (W["amount"] <= CFG["review_threshold"])
    pw_b3, _, _ = exec_probs(W, b3.plans(W, C))
    wc_target = pw_b3[sub].mean() + CFG["target_extra_uaer"]

    systems = [
        Fixed("B0 korumasız", P0, floor_checks=False),
        Fixed("B1 yalnız kurallar", P0),
        b3,
        Router("B4-naif", "naive", False).fit(Rtr, Rcal, C, target),
        Router("B4-T (güvenilir kaynak)", "T", False).fit(Rtr, Rcal, C, target),
        Router("B4-TK (güvenilir kaynak+anahtar)", "TK", False).fit(Rtr, Rcal, C, target),
        Router("VERIQEN (TK + monoton taban)", "TK", True).fit(Rtr, Rcal, C, target),
        Router("VERIQEN-K (TK + taban + kötü durum kalibrasyonu)", "TK", True, True).fit(Rtr, Rcal, C, target, wc_target),
        Router("B4-naif + kötü durum kalibrasyonu", "naive", False, True).fit(Rtr, Rcal, C, target, wc_target),
    ]
    out = {}
    for s in systems:
        fc = getattr(s, "floor_checks", True)
        pl = s.plans(Rte, C)
        pe, rev, pfb = exec_probs(Rte, pl, fc)
        safe = ~Rte["unsafe"]
        ap, aplan, acombo = attack(s, Ratt, C, loyal, np.random.default_rng(seed + 1))
        down = (aplan < P2).astype(float) * ap      # tam doğrulama atlanıp yürütülen
        combos = {}
        for c in acombo:
            k = "+".join(c) if c else "yok"
            combos[k] = combos.get(k, 0) + 1
        out[s.name] = dict(
            cost=float(np.mean([PLAN_COST[x] for x in pl])),
            uaer_natural=float(pe[Rte["unsafe"]].mean()),
            fbr=float(pfb[safe].mean()),
            her=float(rev.mean()),
            uaer_attack=float(ap.mean()),
            uaer_attack_ci=boot_ci(ap, np.random.default_rng(seed + 2), CFG["n_boot"]),
            downgrade_asr=float(down.mean()),
            attack_full_plan_share=float((aplan == P2).mean()),
            attacker_choice=combos,
            _ap=ap,
        )
    return out


def main():
    all_runs = {s: run_seed(s) for s in CFG["seeds"]}
    names = list(next(iter(all_runs.values())).keys())
    summary = {}
    for n in names:
        rows = [all_runs[s][n] for s in CFG["seeds"]]
        agg = {}
        for k in ["cost", "uaer_natural", "fbr", "her", "uaer_attack", "downgrade_asr", "attack_full_plan_share"]:
            v = np.array([r[k] for r in rows])
            agg[k] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)))
        pooled = np.concatenate([r["_ap"] for r in rows])
        agg["uaer_attack_pooled_ci"] = boot_ci(pooled, np.random.default_rng(0), CFG["n_boot"])
        choice = {}
        for r in rows:
            for k, v in r["attacker_choice"].items():
                choice[k] = choice.get(k, 0) + v
        agg["attacker_choice"] = choice
        summary[n] = agg
    # Eşleştirilmiş fark: VERIQEN − B3 (saldırı altı UAER), vaka düzeyinde havuzlanmış bootstrap
    for nm in ["VERIQEN (TK + monoton taban)", "VERIQEN-K (TK + taban + kötü durum kalibrasyonu)"]:
        diffs = np.concatenate([all_runs[s][nm]["_ap"] - all_runs[s]["B3 sabit tam doğrulama"]["_ap"] for s in CFG["seeds"]])
        summary["_paired_" + nm + "_minus_B3"] = dict(
            mean=float(diffs.mean()), ci=boot_ci(diffs, np.random.default_rng(1), CFG["n_boot"]))
    json.dump(dict(config=CFG, summary=summary), open("results/summary.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return summary


if __name__ == "__main__":
    S = main()
    for n, a in S.items():
        if n.startswith("_"):
            print(n, a); continue
        print(f"{n:38s} maliyet={a['cost']['mean']:.2f} UAER_doğal={a['uaer_natural']['mean']:.3f} "
              f"UAER_saldırı={a['uaer_attack']['mean']:.3f} CI={tuple(round(x,3) for x in a['uaer_attack_pooled_ci'])} "
              f"DASR={a['downgrade_asr']['mean']:.3f} FBR={a['fbr']['mean']:.4f} HER={a['her']['mean']:.3f}")
        print("   saldırgan seçimleri:", a["attacker_choice"])
