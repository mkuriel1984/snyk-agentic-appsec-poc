"""Specialist agents for supply chain defense"""

# Malicious Code Detector
def analyze_malicious_code(package):
    """Detect malicious code patterns"""
    score = 0
    indicators = []

    # Check for obfuscation
    if package.get("has_obfuscated_code"):
        score += 30
        indicators.append("Obfuscated code detected (base64/hex encoding)")

    # Check for suspicious network calls
    if package.get("suspicious_network_calls"):
        score += 25
        indicators.append(f"Network calls to suspicious domains: {package.get('suspicious_network_calls')}")

    # Check for file system access
    if package.get("file_system_access"):
        score += 20
        indicators.append("File system access in install scripts")

    # Check for crypto mining
    if package.get("crypto_mining_patterns"):
        score += 15
        indicators.append("Crypto mining signatures detected")

    # Check for eval usage
    if package.get("uses_eval"):
        score += 10
        indicators.append("Uses eval() or Function() in suspicious contexts")

    confidence = "high" if score >= 50 else "medium" if score >= 25 else "low"

    return {
        "agent": "malicious_code_detector",
        "score": min(score, 100),
        "indicators": indicators,
        "confidence": confidence
    }

# Typosquatting Analyzer
def analyze_typosquat(package):
    """Detect typosquatting attacks"""
    score = 0
    indicators = []

    # Check Levenshtein distance
    if package.get("levenshtein_distance"):
        dist = package["levenshtein_distance"]
        if dist <= 2:
            score += 40
            indicators.append(f"Package name '{package['name']}' is {dist} character(s) different from popular package '{package.get('similar_to')}'")

    # Check package age
    age_days = package.get("age_days", 365)
    if age_days < 30:
        score += 25
        indicators.append(f"Package published only {age_days} days ago")

    # Check download count
    downloads = package.get("download_count", 1000000)
    if downloads < 1000:
        score += 20
        indicators.append(f"Only {downloads} downloads (suspicious for new package)")

    # Check maintainer reputation
    if package.get("new_maintainer"):
        score += 15
        indicators.append("Maintainer has no other published packages")

    confidence = "high" if score >= 60 else "medium" if score >= 30 else "low"

    return {
        "agent": "typosquat_analyzer",
        "score": min(score, 100),
        "indicators": indicators,
        "likely_target": package.get("similar_to"),
        "confidence": confidence
    }

# Reputation Analyzer
def analyze_reputation(package):
    """Analyze package and maintainer reputation"""
    score = 30  # Start with baseline
    indicators = []

    # Security advisories
    if package.get("security_advisories", 0) == 0:
        score += 30
        indicators.append("No security advisories filed")
    else:
        score -= 20
        indicators.append(f"{package['security_advisories']} security advisories on record")

    # Maintainer history
    if package.get("maintainer_good_history"):
        score += 25
        indicators.append("Maintainer has good track record")
    else:
        score -= 15
        indicators.append("Maintainer account created recently")

    # Download trends
    if package.get("download_spike"):
        score -= 20
        indicators.append("Suspicious download spike (0 to 5k in 24 hours)")
    elif package.get("consistent_downloads"):
        score += 20
        indicators.append("Consistent, organic download growth")

    # GitHub presence
    if package.get("github_stars", 0) > 100:
        score += 15
        indicators.append(f"Active GitHub: {package['github_stars']} stars")
    else:
        score -= 10
        indicators.append("No GitHub repository linked")

    confidence = "high" if score >= 60 else "medium" if score >= 30 else "low"

    return {
        "agent": "reputation_analyzer",
        "score": max(0, min(score, 100)),
        "indicators": indicators,
        "confidence": confidence
    }

# Module-level exports for imports
class malicious_code_detector:
    @staticmethod
    def analyze(package):
        return analyze_malicious_code(package)

class typosquat_analyzer:
    @staticmethod
    def analyze(package):
        return analyze_typosquat(package)

class reputation_analyzer:
    @staticmethod
    def analyze(package):
        return analyze_reputation(package)
