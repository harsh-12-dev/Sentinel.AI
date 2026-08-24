from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(ROOT / "data" / "processed" / "clean_urls.csv")
print("Before:", df.shape)

# Benign URLs se homepage versions banao
# mp3raid.com/music/xyz.html  ->  mp3raid.com
benign = df[df["label"] == 0]["url"]
homepages = benign.str.replace(r"^https?://", "", regex=True)
homepages = homepages.str.split("/").str[0]
homepages = homepages[homepages.str.contains(r"\.")].drop_duplicates()

print(f"Extracted {len(homepages)} unique homepages")

# Inko benign ke roop me add karo
extra = pd.DataFrame({"url": homepages, "label": 0})
df = pd.concat([df, extra], ignore_index=True).drop_duplicates(subset=["url"])

print("After:", df.shape)
print(df["label"].value_counts())

df.to_csv(ROOT / "data" / "processed" / "clean_urls.csv", index=False)
print("Saved.")