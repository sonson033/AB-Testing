# Headline CTR A/B Test — Speaking Notes (English, short version ~5 min)

*Read this out loud, roughly as written. Three slides, ~1.5 min each.*

---

## Slide 1 — What we tested, and why

We ran an A/B test on headline style because our click-through rate had stalled, and we wanted to know if the way we phrase a headline — not the content itself — can move it.

We tested three variants: A, our current neutral, factual headlines; B, emotional, curiosity-driven headlines; and C, AI-generated headlines. Our hypothesis: closing the curiosity gap increases the perceived reward of clicking, so B should win on CTR — but we worried about a "clickbait tax": if a headline over-promises, readers click and then bounce. So we tracked not just clicks, but scroll depth, time on page, and bounce rate too.

We collected 1,500 impressions over two weeks, split 45/35/20 across A, B, and C, and fixed our sample size target and stopping rule before looking at any results.

---

## Slide 2 — What we found

Observed CTR: 3.4% for A, 5.3% for B, 4.0% for C. B looks like the clear winner. But a standard two-proportion z-test found the A-vs-B difference not statistically significant — p is about 0.10 — because with only 300 to 675 impressions per arm, we're well under the roughly 10,300 per arm a properly powered test needs. A Bayesian analysis gives a more useful number: 95% probability B is genuinely better than A. So there's a real signal, just not yet a confirmed one.

We can also show why patience matters here: replaying the data like a live dashboard, the "leading" variant flipped six times in just the first 300 impressions. Stopping early would likely have picked the wrong winner.

Meanwhile, the trade-off we predicted showed up exactly as expected: clicks on B bounce 43% of the time versus 13% for A, scroll through only 37% of the article versus 67%, and spend 85 seconds on the page versus 164. B wins the click, but loses the reader.

---

## Slide 3 — Recommendation

Our recommendation: iterate — don't roll out, and don't drop it either. The 95% Bayesian signal is promising but not statistically confirmed, and it comes with a real engagement cost.

Concretely: extend the test to the roughly 10,300 impressions per arm we need, and don't stop early based on interim results — we just showed those can flip and mislead. Only stop early if a guardrail metric, like bounce rate, spikes clearly. In parallel, refine variant B's article content so it actually delivers on the curiosity the headline promises, cutting the bounce penalty without losing the CTR gain. And going forward, track scroll depth, time on page, and bounce rate on every headline test — CTR alone would have told us to ship something that quietly erodes reader trust.
