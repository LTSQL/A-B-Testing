"""
Simulates an A/B test of a new checkout page design.
Control = existing checkout. Treatment = redesigned checkout with fewer steps.
True effect is baked in (~1.8 percentage point lift in conversion) so the
analysis has a real, known signal to try to recover.
"""
import os
import numpy as np
import pandas as pd

# All files (data, charts) are saved right next to this script, so there's
# no folder structure to worry about — this works no matter what the repo
# folder is named or where it's cloned/extracted to.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

np.random.seed(123)

n_control = 8000
n_treatment = 8000

true_conversion_control = 0.112
true_conversion_treatment = 0.130  # ~1.8pp lift

control = np.random.binomial(1, true_conversion_control, n_control)
treatment = np.random.binomial(1, true_conversion_treatment, n_treatment)

# add a plausible confound: treatment was rolled out slightly more on mobile
device_control = np.random.choice(["mobile", "desktop"], n_control, p=[0.55, 0.45])
device_treatment = np.random.choice(["mobile", "desktop"], n_treatment, p=[0.62, 0.38])

df = pd.concat([
    pd.DataFrame({"user_id": range(1, n_control + 1), "group": "control",
                  "converted": control, "device": device_control}),
    pd.DataFrame({"user_id": range(n_control + 1, n_control + n_treatment + 1), "group": "treatment",
                  "converted": treatment, "device": device_treatment}),
])
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

out_path = os.path.join(SCRIPT_DIR, "checkout_experiment.csv")
df.to_csv(out_path, index=False, encoding="utf-8")
print(f"Generated {len(df)} rows -> {out_path}")
