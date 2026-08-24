from pathlib import Path
import pandas as pd

from feature_extractor import extract_features

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "processed" / "clean_urls.csv")

# 1. Training data ke benign URLs kaisi dikhti hain?
print("=" * 60)
print("SAFE URLs ke examples (label=0):")
print(df[df["label"] == 0]["url"].head(15).to_string())

print("\n" + "=" * 60)
print("DANGEROUS URLs ke examples (label=1):")
print(df[df["label"] == 1]["url"].head(15).to_string())

# 2. Dono groups ke features ka average nikalo
print("\n" + "=" * 60)
features = pd.DataFrame([extract_features(u) for u in df["url"]])
features["label"] = df["label"].values

comparison = features.groupby("label").mean().T
comparison.columns = ["Safe (0)", "Dangerous (1)"]
print("Feature averages:")
print(comparison.round(2).to_string())

# 3. Kitni benign URLs chhoti aur simple hain?
safe_urls = df[df["label"] == 0]["url"]
short_clean = safe_urls[safe_urls.str.count("/") <= 2]
print(f"\nSafe URLs with <=2 slashes: {len(short_clean)} / {len(safe_urls)}")
print(f"Percentage: {len(short_clean)/len(safe_urls)*100:.1f}%")