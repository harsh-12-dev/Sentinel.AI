from urllib.parse import urlparse
import ipaddress


SUSPICIOUS_SUBDOMAINS = [
    "login",
    "verify",
    "secure",
    "account",
    "update",
    "signin",
    "payment",
]


def analyze_domain(url: str) -> dict:
    parsed_url = urlparse(url)

    hostname = parsed_url.hostname or ""

    result = {
        "domain": hostname,
        "is_ip": False,
        "subdomain_count": 0,
        "domain_length": len(hostname),
        "signals": []
    }

    # 1. IP address detection
    try:
        ipaddress.ip_address(hostname)

        result["is_ip"] = True

        result["signals"].append(
            "Host is an IP address instead of a domain."
        )

        return result

    except ValueError:
        pass

    # 2. Split domain
    parts = hostname.split(".")

    # 3. Subdomain count
    if len(parts) > 2:
        result["subdomain_count"] = len(parts) - 2

    # 4. Excessive subdomains
    if result["subdomain_count"] >= 3:
        result["signals"].append(
            "Domain contains multiple subdomains."
        )

    # 5. Suspicious subdomain keywords
    suspicious_subdomains = [
        part.lower()
        for part in parts[:-2]
        if part.lower() in SUSPICIOUS_SUBDOMAINS
    ]

    if suspicious_subdomains:
        result["signals"].append(
            "Suspicious subdomain detected: "
            + ", ".join(suspicious_subdomains)
        )

    # 6. Long domain
    if len(hostname) > 50:
        result["signals"].append(
            "Domain name is unusually long."
        )

    # 7. Excessive hyphens
    if hostname.count("-") >= 3:
        result["signals"].append(
            "Domain contains an unusually high number of hyphens."
        )

    return result


if __name__ == "__main__":
    test_url = "https://secure.login.verify.example.com"

    result = analyze_domain(test_url)

    print(result)