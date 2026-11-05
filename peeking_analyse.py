"""
Peeking-Problem: Warum ein zu frühes Auswerten des Tests irreführend ist.

Idee: Wir sortieren die Daten chronologisch (nach `sequence`, das ist die
laufende Nummer der Impression in der Zeitreihe -- äquivalent zu einer
Sortierung nach impression_ts) und schauen uns an, wie sich die kumulative
CTR pro Variante entwickelt, je mehr Daten "hereinkommen". Dabei rechnen
wir an mehreren Zwischenständen auch den p-Wert des z-Tests aus A vs. B.

Erwartung: Bei kleinen Stichproben schwankt die kumulative CTR stark, die
"führende" Variante kann mehrfach wechseln (flippen), und der p-Wert kann
zwischendurch unter 0.05 fallen, obwohl das Endergebnis (mit allen Daten)
nicht signifikant ist. Wer an so einem Zwischenpunkt stoppt ("Peeking"),
begeht einen klassischen Fehler: wiederholtes Testen ohne Korrektur
erhöht die tatsächliche Falsch-Positiv-Rate weit über die nominalen 5 %.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("headline_ab_test_synthetic.csv")

# ---------------------------------------------------------------------------
# 1) Chronologisch sortieren. `sequence` ist bereits die laufende Nummer in
#    der Zeitreihe (identisch zur Sortierung nach impression_ts), wir
#    sortieren trotzdem explizit, um von der Reihenfolge in der CSV
#    unabhängig zu sein.
# ---------------------------------------------------------------------------
df = df.sort_values("sequence").reset_index(drop=True)

# ---------------------------------------------------------------------------
# 2) Kumulative Conversion-Rate pro Variante über die Zeit.
#
#    Trick: cumsum() eines Indikators "ist diese Zeile Variante X" liefert
#    an jeder Position die kumulative Impressionszahl von X bis dorthin.
#    Da der Indikator bei allen anderen Zeilen 0 ist, bleibt der
#    kumulative Wert zwischen zwei X-Beobachtungen automatisch konstant --
#    genau das gewünschte "Stufenverhalten" einer laufenden Kennzahl.
# ---------------------------------------------------------------------------
variants = ["A", "B", "C"]
for v in variants:
    is_v = (df["variant"] == v).astype(int)
    cum_impressions = is_v.cumsum()
    cum_conversions = (df["conversion"] * is_v).cumsum()
    df[f"cum_ctr_{v}"] = cum_conversions / cum_impressions.replace(0, np.nan)
    df[f"cum_n_{v}"] = cum_impressions
    df[f"cum_x_{v}"] = cum_conversions

# ---------------------------------------------------------------------------
# 3) Plot: kumulative CTR A vs. B (und C) über die Zeit (sequence)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
colors = {"A": "#4C72B0", "B": "#DD8452", "C": "#55A868"}
for v in variants:
    ax.plot(df["sequence"], df[f"cum_ctr_{v}"], label=f"Variante {v}", color=colors[v], linewidth=1.8)

ax.set_xlabel("Impression # (chronologisch)")
ax.set_ylabel("Kumulative CTR")
ax.set_title("Peeking-Problem: Kumulative CTR pro Variante über die Zeit")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("peeking_cumulative_ctr.png", dpi=150)
print("Plot gespeichert: peeking_cumulative_ctr.png")

# ---------------------------------------------------------------------------
# 4) Wo flippt die "führende" Variante (A vs. B)? Vorzeichenwechsel von
#    (cum_ctr_B - cum_ctr_A) über die Zeit, ab dem Punkt, an dem beide
#    Varianten mindestens einmal beobachtet wurden.
# ---------------------------------------------------------------------------
diff = df["cum_ctr_B"] - df["cum_ctr_A"]
valid = diff.notna()
sign = np.sign(diff[valid])
flips = sign.ne(sign.shift()).to_numpy().nonzero()[0]
flip_positions = df.loc[valid].iloc[flips]["sequence"].tolist()

print(f"\nAnzahl Führungswechsel (A vs. B) über den Testverlauf: {max(len(flip_positions) - 1, 0)}")
print(f"Zeitpunkte (Impression #) der Führungswechsel: {flip_positions[1:]}")

# ---------------------------------------------------------------------------
# 5) p-Wert des z-Tests A vs. B an mehreren Zwischenständen ("was wäre,
#    wenn wir an diesem Punkt gestoppt hätten?")
# ---------------------------------------------------------------------------
def two_proportion_ztest(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return p_value


checkpoints = np.unique(np.concatenate([np.arange(20, 300, 20), np.arange(300, len(df) + 1, 100)]))
print("\nZwischenstände (A vs. B) -- 'was wäre, wenn wir hier gestoppt hätten?':")
print(f"{'Impr. #':>8} | {'n_A':>5} {'n_B':>5} | {'CTR A':>7} {'CTR B':>7} | {'p-Wert':>8} | Führung")
had_significant_peek = False
for cp in checkpoints:
    row = df.iloc[cp - 1]
    n_a, x_a = row["cum_n_A"], row["cum_x_A"]
    n_b, x_b = row["cum_n_B"], row["cum_x_B"]
    if n_a < 5 or n_b < 5 or x_a == 0 or x_b == 0:
        continue
    p_val = two_proportion_ztest(x_a, n_a, x_b, n_b)
    leader = "B" if row["cum_ctr_B"] > row["cum_ctr_A"] else "A"
    flag = "  <-- p<0.05 (Peeking-Falle!)" if p_val < 0.05 else ""
    if p_val < 0.05:
        had_significant_peek = True
    print(f"{cp:>8} | {int(n_a):>5} {int(n_b):>5} | {row['cum_ctr_A']:>6.2%} {row['cum_ctr_B']:>6.2%} | "
          f"{p_val:>8.4f} | {leader}{flag}")

final = df.iloc[-1]
final_p = two_proportion_ztest(final["cum_x_A"], final["cum_n_A"], final["cum_x_B"], final["cum_n_B"])

print("\n" + "=" * 70)
print("DISKUSSION")
print("=" * 70)
print(f"Finaler p-Wert (alle {len(df)} Impressionen): {final_p:.4f} "
      f"({'signifikant' if final_p < 0.05 else 'nicht signifikant'} bei alpha=0.05)")
if had_significant_peek and final_p >= 0.05:
    print(
        "-> Klassische Peeking-Falle: An mindestens einem Zwischenpunkt lag der p-Wert\n"
        "   unter 0.05, obwohl das Endergebnis mit der vollen Stichprobe nicht signifikant\n"
        "   ist. Wer an so einem Punkt gestoppt hätte, hätte sich für ein 'signifikantes'\n"
        "   Ergebnis entschieden, das reines Stichproben-Rauschen war."
    )
if not had_significant_peek:
    print(
        f"-> In diesem Lauf hat der p-Wert nie die 0.05-Schwelle unterschritten -- aber die\n"
        f"   'gefuehlte' Fuehrung (die Variante mit der aktuell hoeheren kumulativen CTR) ist\n"
        f"   trotzdem {max(len(flip_positions) - 1, 0)}-mal umgesprungen, allein in den ersten ~300\n"
        f"   Impressionen (siehe Tabelle: A -> B -> A -> B -> A -> B). Ein Team, das nur auf ein\n"
        f"   Live-Dashboard schaut (ohne formalen Test), haette also je nach Zufallszeitpunkt\n"
        f"   des Blicks eine andere Variante zum 'Gewinner' erklaert -- das ist die informelle,\n"
        f"   aber genauso gefaehrliche Variante des Peeking-Problems."
    )
print(
    "-> Jeder Blick auf ein Zwischenergebnis ist im Grunde ein weiterer statistischer\n"
    "   Test. Ohne Korrektur (z.B. Sequential Testing / Alpha-Spending, oder schlicht:\n"
    "   vorher fixierte Stichprobengröße und genau EIN Auswertungszeitpunkt) steigt die\n"
    "   tatsächliche Falsch-Positiv-Rate weit über die nominalen 5 %, je öfter man\n"
    "   zwischendurch hinschaut."
)
