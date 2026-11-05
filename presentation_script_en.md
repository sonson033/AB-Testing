# Headline CTR A/B Test — Speaking Notes (English)

*Read this out loud, roughly as written. Three slides.*

---

## Slide 1 — What we tested, and why

We ran an A/B test on headline style for our articles, because click-through rate has been flat and we wanted to know whether the *way* we phrase a headline — not the content itself — can move it.

We tested three variants. Variant A is our current style: neutral, factual headlines. Variant B replaces them with emotional, curiosity-driven headlines — the kind that opens a "curiosity gap" instead of stating the fact outright. Variant C is an AI-generated headline, as a check on whether an LLM can match or beat our editorial team without extra guidance.

Our hypothesis was that closing that curiosity gap increases the perceived reward of clicking, so variant B should win on click-through rate. But we were equally interested in the trade-off: if a headline over-promises, readers may click and then bounce immediately, because the article doesn't deliver what the headline implied. We call that the "clickbait tax," and we built our analysis specifically to catch it — not just to look at clicks in isolation.

We collected 1,500 impressions over two weeks, split roughly 45% A, 35% B, and 20% C, and measured not just clicks but what happened after the click: scroll depth, time on page, and bounce rate.

Before looking at any results, we also fixed two things in advance. First, the sample size: for a 4% baseline CTR and a 20% relative minimum detectable effect, a properly powered test needs about 10,300 impressions per arm — we set that as our target. Second, the stopping rule: we agreed not to call a winner before hitting that target, and to only stop a variant early if it caused clear harm, like a bounce rate spike. Both of those decisions matter for how you should read the next slide.

---

## Slide 2 — What we found

Starting with the headline number: the observed click-through rate was 3.4% for A, 5.3% for B, and 4.0% for C. So on the surface, B — the emotional, curiosity-driven variant — is the clear winner, exactly as we hypothesized.

But when we ran a standard statistical significance test — a two-proportion z-test — the difference between A and B was *not* statistically significant, with a p-value of about 0.10. The same was true comparing A and C. In plain terms: with the amount of traffic we had, we can't yet rule out that this difference happened by chance.

That said, we also ran a Bayesian analysis, which asks a more useful question for decision-making: given the data, what's the probability that B is actually better than A? That answer was 95%. So there's a strong signal here, even though it doesn't clear the traditional significance bar yet — which makes sense, because remember, we're only at 300 to 675 impressions per arm against a target of 10,300. This test is directionally promising, but underpowered.

That underpowered stage is exactly where premature conclusions get dangerous, and we can actually show it: we re-ran the analysis as if we were watching a live dashboard, checkpoint by checkpoint, from the very first impressions onward. In just the first 300 impressions, the "leading" variant by cumulative click-through rate flipped six times — C led early, then A, then B, back and forth — before it settled down into the pattern we see now. If we'd stopped at any one of those early checkpoints and trusted what we saw, we could easily have shipped the wrong variant. That's exactly why we fixed the sample size and stopping rule before we started.

And here's the trade-off we predicted: variant B did win on clicks, but it lost badly on everything downstream. Readers who clicked on B bounced 43% of the time, versus 13% for A. They scrolled through only 37% of the article on average, versus 67% for A. And they spent 85 seconds on the page, versus 164 seconds for A. That's the clickbait tax showing up exactly where we expected it.

---

## Slide 3 — Recommendation

Our recommendation is: don't roll out variant B as-is, and don't dismiss it either. The click-through lift is real-looking — 95% probability of being genuinely better, by our Bayesian estimate — but it's not statistically confirmed yet, and it comes with a real cost in reader engagement.

Concretely, we recommend three things. First, extend the test to reach the roughly 10,300 impressions per arm we'd need for a conclusive result, and resist the urge to call it early — we just showed that the apparent leader can flip repeatedly in the first few hundred impressions, so an interim glance is not a decision point. The only thing that should trigger an early stop is a guardrail breach, like a variant's bounce rate spiking well past baseline. Second, in parallel, iterate on variant B so the headline's promise is actually paid off by the article — the goal is to keep the curiosity-driven framing without the bounce penalty, not to abandon it. Third, going forward, we should track scroll depth, time on page, and bounce rate as guardrail metrics on every headline test, not just click-through rate — because CTR alone would have told us to ship a headline style that quietly damages reader trust and engagement.
