from urllib.parse import urlparse
import ipaddress
import re


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "account",
    "secure",
    "update",
    "password",
    "bank",
    "wallet",
    "payment",
    "confirm",
]


SUSPICIOUS_TLDS = [
    ".tk",
    ".ml",
    ".ga",
    ".cf",
    ".gq",
]


def analyze_url(url: str) -> dict:
    parsed_url = urlparse(url)

    score = 0
    reasons = []

    hostname = parsed_url.hostname or ""
    path = parsed_url.path.lower()

    # 1. HTTPS check
    if parsed_url.scheme != "https":
        score += 15
        reasons.append("URL does not use HTTPS.")

    # 2. IP address check
    try:
        ipaddress.ip_address(hostname)

        score += 30
        reasons.append(
            "URL uses an IP address instead of a domain name."
        )

    except ValueError:
        pass

    # 3. URL length
    if len(url) > 100:
        score += 10
        reasons.append("URL is unusually long.")

    # 4. Suspicious keywords
    matched_keywords = [
        keyword
        for keyword in SUSPICIOUS_KEYWORDS
        if keyword in path
    ]

    if matched_keywords:
        score += min(len(matched_keywords) * 10, 30)

        reasons.append(
            f"Suspicious keywords detected: "
            f"{', '.join(matched_keywords)}."
        )

    # 5. Excessive subdomains
    if hostname.count(".") >= 4:
        score += 15

        reasons.append(
            "URL contains an unusually high number of subdomains."
        )

    # 6. Suspicious TLD
    if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 20

        reasons.append(
            "Domain uses a potentially suspicious top-level domain."
        )

    # 7. @ symbol obfuscation
    if "@" in url:
        score += 25

        reasons.append(
            "URL contains '@', which can be used for URL obfuscation."
        )

    # 8. URL encoding
    encoded_parts = re.findall(r"%[0-9a-fA-F]{2}", url)

    if len(encoded_parts) >= 3:
        score += 10

        reasons.append(
            "URL contains multiple encoded characters."
        )

    # 9. Excessive hyphens
    if hostname.count("-") >= 3:
        score += 10

        reasons.append(
            "Domain contains an unusually high number of hyphens."
        )

    # Keep score within 0-100
    score = min(score, 100)

    # Risk classification
    if score >= 60:
        risk_level = "HIGH"

    elif score >= 30:
        risk_level = "SUSPICIOUS"

    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "risk_score": score,
        "reasons": reasons,
    }


if __name__ == "__main__":
    test_url = "http://192.168.1.10/login/verify"

    result = analyze_url(test_url)

    print(result)