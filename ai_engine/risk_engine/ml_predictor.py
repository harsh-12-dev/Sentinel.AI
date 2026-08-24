from pathlib import Path

import joblib
import pandas as pd

# ml/ folder me jo feature extractor banaya tha, wahi reuse karenge
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ml"))

from feature_extractor import extract_features  # noqa: E402

MODEL_PATH = ROOT / "ml" / "models" / "url_model.pkl"
FEATURES_PATH = ROOT / "ml" / "models" / "feature_names.pkl"

_model = None
_feature_names = None


def _load_model():
    """Model ko sirf ek baar load karta hai (lazy loading)."""
    global _model, _feature_names

    if _model is None:
        if not MODEL_PATH.exists():
            return None, None
        _model = joblib.load(MODEL_PATH)
        _feature_names = joblib.load(FEATURES_PATH)

    return _model, _feature_names


def predict_risk(url: str) -> float | None:
    """URL ke dangerous hone ki probability (0-1). Model na ho to None."""
    model, feature_names = _load_model()

    if model is None:
        return None

    try:
        features = pd.DataFrame([extract_features(url)])[feature_names]
        return float(model.predict_proba(features)[0][1])
    except Exception:
        return None