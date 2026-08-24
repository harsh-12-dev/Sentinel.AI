from ai_engine.url_analysis.url_analyzer import analyze_url
from ai_engine.domain_intelligence.domain_analyzer import analyze_domain
from ai_engine.risk_engine.ml_predictor import predict_risk


KNOWN_BRANDS = [
    "paytm", "phonepe", "gpay", "googlepay", "sbi", "hdfc",
    "icici", "axis", "kotak", "upi", "aadhaar", "irctc",
    "amazon", "flipkart", "netflix", "whatsapp", "instagram",
]

OFFICIAL_DOMAINS = [
    "paytm.com", "phonepe.com", "sbi.co.in", "onlinesbi.sbi",
    "hdfcbank.com", "icicibank.com", "axisbank.com", "kotak.com",
    "amazon.in", "amazon.com", "flipkart.com", "irctc.co.in",
    "netflix.com", "whatsapp.com", "instagram.com",
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly",
    "is.gd", "buff.ly", "cutt.ly", "rb.gy", "shorturl.at",
]

# Model ka weight kam rakha hai — dataset ki limitations ki wajah se
ML_WEIGHT = 0.35
ML_REPORT_THRESHOLD = 0.85


def calculate_risk(url: str) -> dict:
    """
    Central risk engine for Sentinel AI.

    Rules deterministic signals dete hain, ML model general
    probability deta hai. Final score dono me se zyada wala.
    """

    url = str(url).strip()

    # Bina scheme wali URL me urlparse hostname nahi nikal pata,
    # isliye analysis ke liye scheme laga dete hain
    url_for_analysis = url if "://" in url else "http://" + url

    url_result = analyze_url(url_for_analysis)
    domain_result = analyze_domain(url_for_analysis)

    score = 0
    reasons = []

    # -----------------------------
    # URL-level signals
    # -----------------------------

    for reason in url_result["reasons"]:

        if "HTTPS" in reason:
            score += 15

        elif "IP address" in reason:
            score += 30

        elif "unusually long" in reason:
            score += 10

        elif "Suspicious keywords" in reason:
            score += 10

        elif "'@'" in reason:
            score += 20

        elif "encoded characters" in reason:
            score += 10

        elif "top-level domain" in reason:
            score += 25

        elif "subdomains" in reason:
            score += 15

        elif "hyphens" in reason:
            score += 10

        reasons.append(reason)

    # -----------------------------
    # Domain-level signals
    # -----------------------------

    for signal in domain_result["signals"]:

        if "multiple subdomains" in signal:
            score += 15

        elif "Suspicious subdomain" in signal:
            score += 15

        elif "unusually long" in signal:
            score += 10

        elif "hyphens" in signal:
            score += 10

        reasons.append(signal)

    domain_lower = domain_result["domain"].lower()

    # -----------------------------
    # Brand impersonation check
    # -----------------------------

    for brand in KNOWN_BRANDS:
        if brand in domain_lower:
            is_official = any(
                domain_lower == official or domain_lower.endswith("." + official)
                for official in OFFICIAL_DOMAINS
            )
            if not is_official:
                score += 40
                reasons.append(
                    f"Domain impersonates a known brand ('{brand}') "
                    f"but is not an official domain."
                )
            break

    # -----------------------------
    # URL shortener check
    # -----------------------------

    if any(shortener in domain_lower for shortener in URL_SHORTENERS):
        score += 25
        reasons.append(
            "URL uses a link shortener, which hides the real destination."
        )

    # -----------------------------
    # ML model signal
    # -----------------------------

    rule_score = min(score, 100)
    ml_probability = predict_risk(url)

    if ml_probability is not None:
        ml_score = ml_probability * 100
        score = max(rule_score, ml_score * ML_WEIGHT)

        if ml_probability >= ML_REPORT_THRESHOLD:
            reasons.append(
                f"ML model flags this URL as suspicious "
                f"({ml_probability * 100:.0f}% confidence)"
            )
    else:
        score = rule_score

    score = int(min(score, 100))

    # -----------------------------
    # Risk classification
    # -----------------------------

    if score >= 60:
        risk_level = "HIGH"

    elif score >= 30:
        risk_level = "SUSPICIOUS"

    else:
        risk_level = "LOW"

    return {
        "url": url,
        "risk_level": risk_level,
        "risk_score": score,
        "reasons": reasons,
        "domain": domain_result["domain"],
    }


if __name__ == "__main__":

    test_urls = [
        "https://www.google.com",
        "https://www.sbi.co.in",
        "https://github.com/user/repo",
        "http://192.168.1.10/login/verify",
        "http://paytm-secure-login.xyz/verify?account=123",
        "signin.eby.de.zukruygxctzmmqi.civpro.co.za",
        "http://free-iphone-winner.tk/claim-now",
        "http://bit.ly/3xY2z",
    ]

    for u in test_urls:
        result = calculate_risk(u)
        print(f"\n{result['risk_level']:12} {result['risk_score']:3}  {u}")
        for r in result["reasons"]:
            print(f"    - {r}")