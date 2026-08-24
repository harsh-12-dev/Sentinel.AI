import re
from urllib.parse import urlparse

# Scam URLs me aksar dikhne wale shabd
SUSPICIOUS_WORDS = [
    "login", "signin", "verify", "secure", "account", "update",
    "banking", "confirm", "password", "credential", "otp",
    "free", "bonus", "prize", "winner", "click",
]

SHORTENERS = [
    "bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly",
    "is.gd", "buff.ly", "cutt.ly", "rb.gy",
]


def extract_features(url: str) -> dict:
    """URL se numeric features nikalta hai."""

    url = str(url).strip()

    # HTTPS ka flag pehle nikal lo, phir scheme hata do
    has_https_flag = 1 if url.lower().startswith("https://") else 0

    # Training data me scheme nahi hai, real URLs me hai —
    # dono ko ek jaisa banane ke liye scheme hata dete hain
    url_clean = re.sub(r"^https?://", "", url, flags=re.IGNORECASE)

    parsed = urlparse("http://" + url_clean)
    domain = parsed.netloc
    path = parsed.path

    features = {}

    # --- Length wale features (scheme ke bina) ---
    features["url_length"] = len(url_clean)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)

    # --- Character counts ---
    features["num_dots"] = url_clean.count(".")
    features["num_hyphens"] = url_clean.count("-")
    features["num_slashes"] = url_clean.count("/")
    features["num_digits"] = sum(c.isdigit() for c in url_clean)
    features["num_special"] = sum(c in "@?%=&_~" for c in url_clean)

    # --- Boolean checks (0 ya 1) ---
    features["has_https"] = has_https_flag
    features["has_at_symbol"] = 1 if "@" in url_clean else 0
    features["has_ip"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+", domain) else 0
    features["has_port"] = 1 if ":" in domain else 0

    # --- Domain structure ---
    features["num_subdomains"] = max(0, domain.count(".") - 1)

    # --- Suspicious patterns ---
    url_lower = url_clean.lower()
    features["num_suspicious_words"] = sum(
        1 for word in SUSPICIOUS_WORDS if word in url_lower
    )
    features["is_shortened"] = 1 if any(s in url_lower for s in SHORTENERS) else 0

    # --- Ratios ---
    features["digit_ratio"] = (
        features["num_digits"] / len(url_clean) if url_clean else 0
    )

    return features


# Quick test
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "www.google.com",
        "http://paytm-secure-login.xyz/verify?account=123",
        "http://192.168.1.1/admin",
        "signin.eby.de.zukruygxctzmmqi.civpro.co.za",
    ]

    for u in test_urls:
        print(f"\n{u}")
        for key, value in extract_features(u).items():
            print(f"  {key}: {value}")