from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# 1. Data load karo
df = pd.read_csv(ROOT / "data" / "raw" / "Malicious URL v3.csv")
print("Original shape:", df.shape)

# 2. Duplicates hatao
df = df.drop_duplicates(subset=["url"])
print("After removing duplicates:", df.shape)

# 3. Sirf benign aur phishing rakho
#    (defacement = hacked sites, malware = alag problem)
df = df[df["type"].isin(["benign", "phishing"])]
print("After keeping benign + phishing:", df.shape)

# 4. Binary label
df["label"] = df["type"].apply(lambda x: 0 if x == "benign" else 1)

print("\nLabel distribution:")
print(df["label"].value_counts())
print("\nPercentage:")
print((df["label"].value_counts(normalize=True) * 100).round(2))

# 5. Save
out_path = ROOT / "data" / "processed" / "clean_urls.csv"
df[["url", "label"]].to_csv(out_path, index=False)
print(f"\nSaved to {out_path}")