# Experiment Design — Headline-CTR-A/B-Test

## Goal (Ziel)
Die Click-Through-Rate (CTR) auf Artikel-Headlines erhöhen, **ohne** die
redaktionelle Qualität bzw. das Nutzer-Engagement nach dem Klick zu
verschlechtern (Stichwort "Clickbait-Tax").

## Primary KPI
**CTR** = Klicks (`conversion`) / Impressionen. Sekundäre Guardrail-Metriken:
`bounced`, `scroll_depth_pct`, `time_on_page_sec` — diese dürfen sich bei
einer CTR-Verbesserung nicht signifikant verschlechtern.

## Hypothese
*Wenn* wir neutrale, faktische Headlines (A) durch emotionale,
neugierde-getriebene Headlines (B) ersetzen, *dann* steigt die CTR, *weil*
die geöffnete Neugierlücke den wahrgenommenen Reward eines Klicks erhöht —
solange der Artikel das Versprechen der Headline einlöst. Zusätzlich
prüfen wir, ob eine KI-generierte Headline (C) einen ähnlichen Effekt ohne
den Vertrauensverlust von B erzielen kann.

## Varianten
| Variante | Beschreibung | Traffic-Anteil |
|---|---|---|
| A | Neutral / faktisch (Kontrolle) | 45 % |
| B | Emotional / Curiosity-driven | 35 % |
| C | KI-generiert | 20 % |

## Randomisierungsstrategie
Nutzer werden zufällig und unabhängig vom Zeitpunkt einer festen Variante
zugeordnet (feste Ziel-Fallzahlen 675/525/300, zufällig über die
14-Tage-Laufzeit verteilt), damit Tages-/Wochentagseffekte nicht mit einer
bestimmten Variante konfundiert sind. Jeder Nutzer sieht in diesem
Datensatz genau eine Impression/Variante (kein Re-Randomisieren pro
Session).

## Sample-Size-Schätzung
**Tool:** eigene Python-Implementierung (`scipy.stats.norm`, siehe
[analyse.py](analyse.py)) statt eines Web-Rechners — verwendet dieselbe
Standardformel wie Evan Millers und CXLs Sample-Size-Rechner:

```
n = (z_α/2 + z_β)² · [p1(1-p1) + p2(1-p2)] / (p2-p1)²
```

Inputs: Baseline p1 = 4.0 %, relative MDE = 20 % → p2 = 4.8 %, α = 0.05
(zweiseitig), Power = 0.80.

**Ergebnis: ≈ 10.314 Impressionen pro Arm.**
→ Gegenprobe: dieselben Werte (4 %, 20 % relative MDE, 0.05, 0.80) in
Evan Millers oder CXLs Rechner eingetragen liefern dieselbe Größenordnung,
da beide Tools die identische Formel verwenden.

Unser synthetischer Datensatz hat nur 675 (A) / 525 (B) / 300 (C) — der
Test ist also **bewusst unterpowert**, um den Peeking-/Unterpowert-Effekt
im Kurs sichtbar zu machen.

## Stopping Conditions
- **Nicht** vor Erreichen der Ziel-Fallzahl (~10.300/Arm) oder einer
  vorab fixierten Laufzeit abbrechen, auch wenn ein Zwischenergebnis
  signifikant aussieht (siehe Peeking-Analyse, [peeking_analyse.py](peeking_analyse.py)).
- Abbruch nur bei eindeutigem Schaden (z.B. Bounce-Rate einer Variante
  > 2x Baseline über mehrere Tage) — dann sofortiger Stopp dieser
  Variante unabhängig vom CTR-Ergebnis.
- Bei Erreichen der Ziel-Fallzahl: einmalige finale Auswertung, keine
  weiteren Zwischenchecks danach.

## Assumptions & Risks
- **Annahme:** Nutzerverhalten ist über die 14 Tage stabil (keine externen
  Events, die eine Variante bevorzugen).
- **Risiko Clickbait-Tax:** höhere CTR bei B kann durch schlechteres
  Engagement (Bounce, Scroll-Tiefe, Verweildauer) erkauft sein —
  deshalb Guardrail-Metriken zwingend mitlaufen lassen.
- **Risiko Peeking:** wiederholtes Zwischenauswerten ohne Korrektur
  erhöht die Falsch-Positiv-Rate massiv (siehe Peeking-Analyse).
- **Risiko kleine Stichprobe bei C:** n=300 liefert die breitesten
  Konfidenzintervalle — Ergebnis für C ist am unsichersten.

---

## Ergebnisse (aus [analyse.py](analyse.py))

### Conversion per variant (CTR)
| Variante | n | Klicks | CTR | Wilson-95%-CI |
|---|---|---|---|---|
| A | 675 | 23 | 3.41 % | [2.28 %, 5.06 %] |
| B | 525 | 28 | 5.33 % | [3.72 %, 7.60 %] |
| C | 300 | 12 | 4.00 % | [2.30 %, 6.86 %] |

### Uplift
- B vs. A: **+56.5 % relativ** (5.33 % vs. 3.41 %)
- C vs. A: +17.4 % relativ (4.00 % vs. 3.41 %)

### Signifikanz / Bayesianische Wahrscheinlichkeit
- Zwei-Proportionen-z-Test A vs. B: p = 0.10 → **nicht signifikant** (α=0.05)
- Zwei-Proportionen-z-Test A vs. C: p = 0.65 → **nicht signifikant**
- Bayesianisch (Beta-Binomial, Prior Beta(1,1)): **P(B > A) = 95.0 %**,
  P(C > A) = 70.3 %
- Grund für die Diskrepanz: n liegt weit unter dem Sample-Size-Bedarf
  (~10.300/Arm) → der Test ist unterpowert, der frequentistische Test
  ist konservativ, während die Bayesianische Sicht das vorhandene Signal
  direkt als Wahrscheinlichkeit ausdrückt.

### Clickbait-Tax (Guardrails, nur bei conversion=1)
| Variante | Bounce-Rate | Scroll-Tiefe | Time on Page |
|---|---|---|---|
| A | 13 % | 67 % | 164 s |
| B | 43 % | 37 % | 85 s |
| C | 17 % | 56 % | 106 s |

### Empfehlung: Rollout, Iterate oder Revert?
**→ Iterate.** Nicht ausrollen (Signifikanz fehlt, Engagement-Kosten real),
aber auch nicht verwerfen (starkes Bayesianisches Signal, P(B>A)=95 %).
Test bis zur benötigten Fallzahl verlängern und parallel Variante B so
weiterentwickeln, dass die Neugierlücke inhaltlich eingelöst wird
(Bounce-Rate senken), bevor eine finale Rollout-Entscheidung fällt.
