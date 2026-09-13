# Checkout Redesign A/B Test — Statistical Analysis
 
**Business question:** Does the redesigned checkout page increase conversion enough to justify rolling it out to all users?
 
## Why this project
 
A/B testing is a core data analyst/scientist skill that most student portfolios skip entirely. This project does it properly:
 
- A **pre-experiment power calculation** (not just a post-hoc test)
- A **two-proportion significance test** with confidence intervals
- A **check for confounding**
- A translation of the statistics into a **plain-English stakeholder recommendation**
## Project structure
 
This is a flat project — every script, data file, and output sits in the same folder. No subfolders needed.
 
```
checkout_experiment.csv       # created by generate_experiment_data.py
generate_experiment_data.py
ab_analysis.py
conversion_comparison.png     # created by ab_analysis.py
recommendation.txt            # created by ab_analysis.py
```
 
## Approach
 
**`generate_experiment_data.py`**
Simulates 16,000 users split into control (existing checkout) and treatment (redesigned checkout), with a known true ~1.8pp conversion lift baked in, plus a realistic confound: the treatment group happens to have a slightly higher mobile traffic share.
 
**`ab_analysis.py`**
- **Power calculation** — before looking at results, calculates the minimum sample size needed to reliably detect a lift worth acting on (this is what should happen before running a real test, and most people skip it).
- **Two-proportion z-test** with Wilson confidence intervals on each group's conversion rate.
- **Confound check** — the treatment group's higher mobile share could bias a naive comparison, so the analysis stratifies by device to confirm the lift isn't just an artefact of that imbalance.
- Outputs a **plain-English recommendation**, not just a p-value.
## How to run
 
```bash
pip install pandas numpy statsmodels matplotlib
python generate_experiment_data.py
python ab_analysis.py
```
 
## Key findings (from this run)
 
- Required sample size for 80% power at a 1.5pp minimum detectable effect: **~7,334 per group** — the experiment (8,000 per group) was adequately powered.
- Observed conversion: **control 10.8% vs treatment 12.9%** (+19.9% relative lift), **p < 0.0001**.
- The treatment group had a higher mobile traffic share than control, which could have biased the result — stratifying by device confirmed the lift held in both mobile and desktop segments, ruling that out as the explanation.
- **Recommendation:** ship the redesign to 100% of traffic.
## What I'd do with more time
 
- Add sequential testing / peeking-correction (real experiments are often monitored continuously, which inflates false-positive risk if not corrected for).
- Add a guardrail metric check (e.g. did average order value change, not just conversion).
- Extend the confound check into a full regression-adjusted estimate (logistic regression with device as a covariate) rather than only stratifying.
 
