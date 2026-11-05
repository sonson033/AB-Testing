"""
Aufgabe 1: Synthetische Daten für den Headline-CTR-A/B-Test.

Wir simulieren 1500 Impressionen auf drei Headline-Varianten:
  A = Neutral/faktisch        (45 %, n=675)  -> wahre CTR 4.0 %
  B = Emotional/Curiosity     (35 %, n=525)  -> wahre CTR 5.0 % (soll gewinnen)
  C = KI-generiert            (20 %, n=300)  -> wahre CTR 4.5 %

Wichtig: Wir bauen absichtlich einen "Clickbait-Tax"-Trade-off ein.
Variante B klickt sich zwar am besten, liefert danach aber die
schlechteste Engagement-Qualität (niedrigste Scroll-Tiefe, kürzeste
Verweildauer, höchste Bounce-Rate). Das ist der Kern der Story:
"Mehr Klicks kosten Qualität" -> die spätere Analyse muss das zeigen.
"""

import numpy as np
import pandas as pd

# Seed fix, damit die Daten reproduzierbar sind (jeder Lauf liefert
# denselben Datensatz -- wichtig für Nachvollziehbarkeit der Analyse).
rng = np.random.default_rng(42)

N_TOTAL = 1500

# ---------------------------------------------------------------------------
# 1) Varianten-Zuordnung (feste Fallzahlen statt zufälligem Sampling der
#    Gruppenzugehörigkeit, damit die Anteile exakt 45/35/20 % treffen und
#    nicht nur "im Erwartungswert")
# ---------------------------------------------------------------------------
VARIANT_CONFIG = {
    "A": {"share": 0.45, "n": 675, "true_ctr": 0.040},
    "B": {"share": 0.35, "n": 525, "true_ctr": 0.050},
    "C": {"share": 0.20, "n": 300, "true_ctr": 0.045},
}
assert sum(v["n"] for v in VARIANT_CONFIG.values()) == N_TOTAL

variant_list = []
for name, cfg in VARIANT_CONFIG.items():
    variant_list.extend([name] * cfg["n"])
variant_arr = np.array(variant_list)
rng.shuffle(variant_arr)  # zufällige Reihenfolge, damit die Zeitachse nicht nach Variante sortiert ist

# ---------------------------------------------------------------------------
# 2) Zeitachse: Impressionen gleichmäßig (mit leichtem Rauschen) über
#    14 Tage verteilt, chronologisch sortiert -> "sequence" ist die
#    laufende Nummer der Impression in dieser Zeitreihe.
# ---------------------------------------------------------------------------
start = pd.Timestamp("2026-08-01 00:00:00")
# gleichverteilte Sekunden-Offsets über 14 Tage
offsets_sec = rng.uniform(0, 14 * 24 * 3600, size=N_TOTAL)
offsets_sec.sort()
impression_ts = start + pd.to_timedelta(offsets_sec, unit="s")

sequence = np.arange(1, N_TOTAL + 1)
user_id = [f"u{100000 + i}" for i in sequence]

df = pd.DataFrame(
    {
        "user_id": user_id,
        "sequence": sequence,
        "impression_ts": impression_ts,
        "variant": variant_arr,
        "impression": 1,
    }
)

# ---------------------------------------------------------------------------
# 3) Conversion (= Klick auf die Headline): Bernoulli-Ziehung je nach
#    wahrer CTR der Variante. Das ist die eigentliche Zielgröße des Tests.
# ---------------------------------------------------------------------------
true_ctr_map = {k: v["true_ctr"] for k, v in VARIANT_CONFIG.items()}
p_click = df["variant"].map(true_ctr_map).to_numpy()
df["conversion"] = rng.binomial(1, p_click)

# ---------------------------------------------------------------------------
# 4) Engagement-Metriken NACH dem Klick: scroll_depth_pct, time_on_page_sec,
#    bounced. Diese Werte ergeben nur Sinn, wenn tatsächlich geklickt wurde
#    (conversion=1) -- sonst gibt es keinen Seitenaufruf, also NaN.
#
#    Hier steckt der "Clickbait-Tax"-Effekt: B hat die höchste CTR, aber die
#    schwächste Engagement-Qualität (Neugierlücke wird nicht eingelöst).
# ---------------------------------------------------------------------------
ENGAGEMENT_CONFIG = {
    # scroll_depth: Beta-Verteilung skaliert auf 0-100 (natürlich begrenzt)
    # time_on_page: Lognormal (rechtsschief, realistisch für Verweildauern)
    # bounce_prob: Wahrscheinlichkeit für sofortiges Verlassen der Seite
    "A": {"scroll_mean": 68, "scroll_sd": 12, "time_mu": np.log(140), "time_sigma": 0.5, "bounce_prob": 0.22},
    "B": {"scroll_mean": 42, "scroll_sd": 15, "time_mu": np.log(70), "time_sigma": 0.6, "bounce_prob": 0.48},
    "C": {"scroll_mean": 55, "scroll_sd": 13, "time_mu": np.log(100), "time_sigma": 0.55, "bounce_prob": 0.33},
}


def sample_scroll_depth(mean, sd, size):
    # Beta-Parametrisierung über Mean/Varianz, dann auf 0-100 skaliert.
    # Beta erzeugt realistisches, auf [0,1] begrenztes Rauschen ohne
    # unplausible Werte < 0 % oder > 100 % (im Gegensatz zu einer Normal-
    # verteilung, die wir künstlich clippen müsste).
    m = mean / 100
    var = (sd / 100) ** 2
    # Momentenmethode: alpha/beta aus Mean & Varianz einer Beta-Verteilung
    common = m * (1 - m) / var - 1
    alpha = max(m * common, 0.5)
    beta = max((1 - m) * common, 0.5)
    return rng.beta(alpha, beta, size=size) * 100


n_rows = len(df)
scroll_depth = np.full(n_rows, np.nan)
time_on_page = np.full(n_rows, np.nan)
bounced = np.full(n_rows, np.nan)

converted_mask = df["conversion"].to_numpy() == 1
for variant, cfg in ENGAGEMENT_CONFIG.items():
    mask = converted_mask & (df["variant"].to_numpy() == variant)
    n = mask.sum()
    if n == 0:
        continue
    scroll_depth[mask] = sample_scroll_depth(cfg["scroll_mean"], cfg["scroll_sd"], n)
    time_on_page[mask] = rng.lognormal(cfg["time_mu"], cfg["time_sigma"], size=n)
    bounced[mask] = rng.binomial(1, cfg["bounce_prob"], size=n)

df["scroll_depth_pct"] = np.round(scroll_depth, 1)
df["time_on_page_sec"] = np.round(time_on_page, 1)
df["bounced"] = pd.array(bounced, dtype="Int64")  # nullable int: 0/1 oder <NA>

# Reihenfolge der Spalten wie in der Aufgabenstellung
df = df[
    [
        "user_id",
        "sequence",
        "impression_ts",
        "variant",
        "impression",
        "conversion",
        "scroll_depth_pct",
        "time_on_page_sec",
        "bounced",
    ]
]

out_path = "headline_ab_test_synthetic.csv"
df.to_csv(out_path, index=False)

print(f"Gespeichert: {out_path}  ({len(df)} Zeilen)")
print("\nVerteilung Varianten:")
print(df["variant"].value_counts())
print("\nBeobachtete CTR je Variante (zur Kontrolle gegen die wahren Raten):")
print(df.groupby("variant")["conversion"].mean().round(4))
print("\nEngagement bei Klick (Mittelwerte, nur conversion=1):")
print(
    df[df["conversion"] == 1]
    .groupby("variant")[["scroll_depth_pct", "time_on_page_sec", "bounced"]]
    .mean()
    .round(2)
)
