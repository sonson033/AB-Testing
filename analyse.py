"""
Aufgabe 2: Analyse des Headline-CTR-A/B-Tests.

Läuft auf Basis der selbst generierten CSV (headline_ab_test_synthetic.csv).
Bei jedem Analyseschritt wird kurz erklärt, WARUM diese Methode gewählt
wurde und welche Alternativen es gegeben hätte.

Nur numpy/pandas/scipy werden verwendet (kein statsmodels nötig) --
Wilson-CI, z-Test und die Sample-Size-Formel lassen sich direkt aus der
Normalverteilung (scipy.stats.norm) ableiten.
"""

import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("headline_ab_test_synthetic.csv")

# ---------------------------------------------------------------------------
# Rohzahlen je Variante
# ---------------------------------------------------------------------------
summary = df.groupby("variant").agg(n=("impression", "sum"), clicks=("conversion", "sum"))
summary["ctr"] = summary["clicks"] / summary["n"]

print("=" * 70)
print("ROHZAHLEN")
print("=" * 70)
print(summary)

# ---------------------------------------------------------------------------
# 1) Wilson-95%-Konfidenzintervalle für die CTR je Variante
#
#    WARUM Wilson und nicht die "normale" Wald-CI (p +/- z*SE)?
#    - Die Wald-CI basiert auf einer Normalapproximation, die bei kleinen
#      Stichproben und/oder Anteilen nahe 0 (hier: CTR ~4-5 %) schlecht
#      funktioniert. Sie kann sogar negative untere Grenzen liefern, was
#      für eine Wahrscheinlichkeit unsinnig ist.
#    - Wilson invertiert stattdessen den z-Test direkt und liefert damit
#      auch bei kleinem n und niedrigem p eine deutlich bessere
#      Abdeckung (closer to nominal 95 %). Deshalb ist Wilson der
#      Standard für CTR/Konversionsraten in der Praxis.
#    Alternative: Clopper-Pearson (exakt, aber konservativer/breiter) oder
#    Bootstrap-CI (rechenintensiver, ohne Verteilungsannahme).
# ---------------------------------------------------------------------------
def wilson_ci(successes, n, confidence=0.95):
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = (z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return center - margin, center + margin


print("\n" + "=" * 70)
print("1) CTR MIT WILSON-95%-KONFIDENZINTERVALL")
print("=" * 70)
for variant, row in summary.iterrows():
    lo, hi = wilson_ci(row["clicks"], row["n"])
    print(f"  {variant}: CTR={row['ctr']:.4f}  (n={int(row['n'])}, Klicks={int(row['clicks'])})  "
          f"95%-CI Wilson=[{lo:.4f}, {hi:.4f}]")

# ---------------------------------------------------------------------------
# 2) Zwei-Proportionen-z-Test: A vs. B, A vs. C
#
#    WARUM z-Test?
#    - Klassischer, weit verbreiteter Test für den Vergleich zweier
#      Anteile (Konversionsraten) unter H0: p1 = p2. Er nutzt die
#      gepoolte Varianz unter H0 und die Normalapproximation der
#      Binomialverteilung (bei unseren n's von 300-675 gerechtfertigt).
#    - Ergebnis ist ein p-Wert: Wahrscheinlichkeit, einen mindestens so
#      extremen Unterschied zu beobachten, WENN es in Wahrheit keinen
#      Unterschied gibt.
#    Alternativen:
#      - Chi-Quadrat-Test (mathematisch äquivalent zum zweiseitigen
#        z-Test bei 2x2-Tabellen)
#      - Fisher's Exact Test (exakt statt approximiert, besser bei sehr
#        kleinen Zellhäufigkeiten -- hier nicht nötig, da n und
#        erwartete Zellhäufigkeiten ausreichend groß sind)
# ---------------------------------------------------------------------------
def two_proportion_ztest(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value


print("\n" + "=" * 70)
print("2) ZWEI-PROPORTIONEN-Z-TEST")
print("=" * 70)
a = summary.loc["A"]
b = summary.loc["B"]
c = summary.loc["C"]

z_ab, p_ab = two_proportion_ztest(a["clicks"], a["n"], b["clicks"], b["n"])
z_ac, p_ac = two_proportion_ztest(a["clicks"], a["n"], c["clicks"], c["n"])
print(f"  A vs. B: z={z_ab:.3f}, p-Wert={p_ab:.4f}  "
      f"-> {'signifikant (p<0.05)' if p_ab < 0.05 else 'NICHT signifikant (p>=0.05)'}")
print(f"  A vs. C: z={z_ac:.3f}, p-Wert={p_ac:.4f}  "
      f"-> {'signifikant (p<0.05)' if p_ac < 0.05 else 'NICHT signifikant (p>=0.05)'}")

# ---------------------------------------------------------------------------
# 3) Bayesianische Analyse: Beta-Binomial-Modell
#
#    WARUM Bayesianisch zusätzlich zum z-Test?
#    - Der z-Test beantwortet nur "ist der Unterschied überzufällig?"
#      (p-Wert). Die Bayesianische Sicht beantwortet die eigentlich
#      interessantere Business-Frage: "Mit welcher Wahrscheinlichkeit
#      ist B tatsächlich besser als A?" (P(B>A)) -- direkt
#      interpretierbar für Stakeholder, ohne die häufige
#      Fehlinterpretation von p-Werten.
#    - Beta ist der konjugierte Prior zur Binomial-Likelihood: die
#      Posterior ist wieder eine Beta-Verteilung, geschlossene Form,
#      kein Sampling-Verfahren (MCMC) nötig.
#    - Prior Beta(1,1) = Gleichverteilung auf [0,1], also "uninformativ"
#      (wir wollen die Daten für sich sprechen lassen, keine Vorannahme
#      über die CTR einbringen).
#    Alternative Priors: schwach informativ, z.B. Beta(4,96) passend zu
#      einer historisch bekannten Baseline-CTR von ~4 % -- würde die
#      Posterior bei kleinen Stichproben stärker "einziehen".
#    Für P(B>A)/P(C>A) selbst: Monte-Carlo-Sampling aus den Posteriors
#      (einfach, robust) statt numerischer Integration der Differenz
#      zweier Beta-Verteilungen (exakter, aber komplexer herzuleiten).
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
N_SAMPLES = 200_000

prior_alpha, prior_beta = 1, 1


def posterior_samples(clicks, n):
    alpha = prior_alpha + clicks
    beta_param = prior_beta + (n - clicks)
    return rng.beta(alpha, beta_param, size=N_SAMPLES)


samples_a = posterior_samples(a["clicks"], a["n"])
samples_b = posterior_samples(b["clicks"], b["n"])
samples_c = posterior_samples(c["clicks"], c["n"])

p_b_gt_a = np.mean(samples_b > samples_a)
p_c_gt_a = np.mean(samples_c > samples_a)

print("\n" + "=" * 70)
print("3) BAYESIANISCHE ANALYSE (Beta-Binomial, Prior Beta(1,1))")
print("=" * 70)
print(f"  P(B > A) = {p_b_gt_a:.4f}")
print(f"  P(C > A) = {p_c_gt_a:.4f}")
print(f"  Erwartete relative Verbesserung B vs. A (Median der Posterior-Differenz): "
      f"{np.median((samples_b - samples_a) / samples_a):.2%}")

# ---------------------------------------------------------------------------
# 4) Sample-Size-Check: wie viele Impressionen/Arm für einen sauber
#    gepowerten Test?
#
#    WARUM diese Formel?
#    - Standardformel für den Vergleich zweier Anteile (z-Test-basiert,
#      gepoolte Varianz), die aus der gewünschten Power (1-beta) und dem
#      Signifikanzniveau (alpha) die nötige Stichprobengröße pro Arm
#      herleitet: n = (z_a/2 + z_b)^2 * (p1(1-p1)+p2(1-p2)) / (p2-p1)^2
#    - Baseline p1=4.0 %, relative MDE 20 % -> p2 = 4.0 % * 1.20 = 4.8 %
#      (absolute MDE = 0.8 Prozentpunkte). Wir testen zweiseitig (alpha
#      = 0.05, also z_a/2 = 1.96) mit Power 80 % (z_b = 0.84).
#    Alternative: Simulationsbasierte Power-Analyse (Power per Monte-
#      Carlo aus vielen simulierten Experimenten geschätzt) -- robuster
#      bei komplexeren Designs, hier aber unnötig, da die geschlossene
#      Formel für einfache Anteilsvergleiche exakt genug ist.
# ---------------------------------------------------------------------------
def sample_size_two_proportions(p1, relative_mde, alpha=0.05, power=0.80):
    p2 = p1 * (1 + relative_mde)
    z_alpha2 = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    n = (z_alpha2 + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2
    return n, p2


n_required, p2 = sample_size_two_proportions(p1=0.04, relative_mde=0.20)
print("\n" + "=" * 70)
print("4) SAMPLE-SIZE-CHECK (Baseline 4.0 %, 20 % relative MDE, alpha=0.05, power=0.80)")
print("=" * 70)
print(f"  Ziel-CTR der Variante (p2): {p2:.4f}")
print(f"  Benötigte Impressionen PRO ARM: {np.ceil(n_required):.0f}")
print(f"  Tatsächliches n: A={int(a['n'])}, B={int(b['n'])}, C={int(c['n'])}")
if a["n"] < n_required or b["n"] < n_required:
    print("  -> A/B ist UNTERPOWERT für eine 20%-relative-MDE-Detektion bei 4% Baseline;")
    print("     das (nicht signifikante Ergebnis trotz sichtbarem Unterschied) passt dazu.")
if a["n"] < n_required or c["n"] < n_required:
    print("  -> A/C ist ebenfalls unterpowert (C hat mit n=300 die kleinste Stichprobe).")
