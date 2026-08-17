from ai_engine.url_analysis.url_analyzer import analyze_url
from ai_engine.domain_intelligence.domain_analyzer import analyze_domain


def calculate_risk(url: str) -> dict:
    """
    Central risk engine for Sentinel AI.

    URL Analyzer and Domain Analyzer identify signals.
    This layer calculates the final risk score.
    """

    url_result = analyze_url(url)
    domain_result = analyze_domain(url)

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

        elif "hyphens" in reason:
            score += 10

        reasons.append(reason)

    # -----------------------------
    # Domain-level signals
    # -----------------------------

    if domain_result["is_ip"]:

        # IP risk is already handled
        # by URL analysis.
        pass

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

    # -----------------------------
    # Limit score
    # -----------------------------

    score = min(score, 100)

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
        "domain": domain_result["domain"]
    }


if __name__ == "__main__":

    test_url = "http://192.168.1.10/login/verify"

    result = calculate_risk(test_url)

    print(result)