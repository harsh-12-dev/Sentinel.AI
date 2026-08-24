from pathlib import Path
import joblib
import pandas as pd

from feature_extractor import extract_features

ROOT = Path(__file__).resolve().parent.parent
model = joblib.load(ROOT / "ml" / "models" / "url_model.pkl")
feature_names = joblib.load(ROOT / "ml" / "models" / "feature_names.pkl")

test_urls = [
    "https://www.google.com",
    "https://github.com/user/repo",
    "http://paytm-secure-login.xyz/verify?account=123",
    "signin.eby.de.zukruygxctzmmqi.civpro.co.za",
    "http://192.168.1.1/admin/login.php",
    "https://www.sbi.co.in",
    "http://free-iphone-winner.tk/claim-now",
]

for url in test_urls:
    features = pd.DataFrame([extract_features(url)])[feature_names]
    prob = model.predict_proba(features)[0][1]
    verdict = "DANGEROUS" if prob > 0.5 else "SAFE"
    print(f"{verdict:10} {prob*100:5.1f}%   {url}")