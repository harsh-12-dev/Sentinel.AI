from pathlib import Path

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from feature_extractor import extract_features

# Project ka root folder (ml/ ka parent)
ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "ml" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Clean data load karo
print("Loading data...")
df = pd.read_csv(ROOT / "data" / "processed" / "clean_urls.csv")
print(f"Rows: {len(df)}")

# 2. Har URL se features nikalo (thoda time lagega)
print("\nExtracting features...")
features_list = [extract_features(url) for url in df["url"]]
X = pd.DataFrame(features_list)
y = df["label"]

print(f"Features shape: {X.shape}")
print(f"Feature names: {X.columns.tolist()}")

# 3. Train-test split
#    stratify=y matlab dono hisso me ratio same rahega
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain: {len(X_train)}, Test: {len(X_test)}")

# 4. Model train karo
print("\nTraining RandomForest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    class_weight="balanced",   # imbalance handle karta hai
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# 5. Test par check karo
y_pred = model.predict(X_test)

print("\n" + "=" * 50)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("(Baseline = 0.7382, isse upar hona chahiye)")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("[[TN FP]")
print(" [FN TP]]")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Safe", "Dangerous"]))

# 6. Kaunsa feature kitna important
print("Top 10 Features:")
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_,
}).sort_values("importance", ascending=False)
print(importance.head(10).to_string(index=False))

# 7. Model save karo
joblib.dump(model, MODELS_DIR / "url_model.pkl")
joblib.dump(X.columns.tolist(), MODELS_DIR / "feature_names.pkl")
print(f"\nModel saved to {MODELS_DIR / 'url_model.pkl'}")