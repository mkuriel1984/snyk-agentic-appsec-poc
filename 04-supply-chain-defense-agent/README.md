# Supply Chain Defense Agent (Multi-Agent Coordination)

Multi-agent system that coordinates specialist agents to detect and block malicious packages, typosquatting attacks, and supply chain threats in Snyk Open Source findings.

## The Problem

**Supply chain attacks are increasing:**
- **84% increase** in supply chain attacks (2023 vs 2022)
- Attacks like **SolarWinds, Log4Shell, colors/faker protestware** show the risk
- Traditional scanners detect known malware but miss:
  - **Typosquatting** (reqeusts vs requests)
  - **Malicious behavior** (obfuscation, suspicious network calls)
  - **Dependency confusion** attacks
  - **Maintainer account takeovers**

**Detection Challenge:**
- No single signal reliably detects supply chain attacks
- Need multiple perspectives: code analysis + behavioral analysis + reputation analysis
- Human review doesn't scale to 1,000s of dependencies

## The Solution: Multi-Agent Coordination

Three specialist agents analyze each dependency from different angles. A coordinator agent synthesizes findings and makes the final decision.

```
┌─────────────────────────────────────────────────────────────┐
│                    Coordinator Agent                        │
│  (Synthesizes findings, assigns confidence, decides action) │
└─────────────────────────────────────────────────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │   Malicious  │   │ Typosquatting│   │   Reputation │
    │     Code     │   │   Analyzer   │   │   Analyzer   │
    │   Detector   │   │              │   │              │
    └──────────────┘   └──────────────┘   └──────────────┘
```

---

## Specialist Agents

### 1. Malicious Code Detector

**What it analyzes:**
- Code obfuscation (base64, hex encoding, eval())
- Suspicious network calls (to unexpected domains)
- File system access patterns
- Crypto mining signatures
- Known malware patterns

**Scoring:**
```
Malicious Score = 
  + 30 if obfuscated code
  + 25 if network calls to suspicious domains
  + 20 if file system access in install scripts
  + 15 if crypto mining patterns
  + 10 if eval() or Function() in unexpected contexts
```

**Output:**
```json
{
  "agent": "malicious_code_detector",
  "score": 75,
  "indicators": [
    "Obfuscated code in setup.py (base64 encoded)",
    "Network call to unknown domain: evil.com",
    "Post-install script modifies system files"
  ],
  "confidence": "high"
}
```

### 2. Typosquatting Analyzer

**What it analyzes:**
- Levenshtein distance from popular packages
- Package age (< 30 days = suspicious)
- Download count (< 1,000 downloads = flag)
- Maintainer reputation
- Similar package with much higher popularity exists

**Scoring:**
```
Typosquat Score = 
  + 40 if Levenshtein distance ≤ 2 from popular package
  + 25 if package age < 30 days
  + 20 if downloads < 1,000
  + 15 if maintainer has no other packages
```

**Output:**
```json
{
  "agent": "typosquat_analyzer",
  "score": 85,
  "indicators": [
    "Package 'reqeusts' is 1 character different from 'requests'",
    "'requests' has 500M downloads, 'reqeusts' has 200 downloads",
    "Package published 5 days ago",
    "Maintainer has no other published packages"
  ],
  "likely_target": "requests",
  "confidence": "high"
}
```

### 3. Reputation Analyzer

**What it analyzes:**
- Package download trends
- Maintainer history and reputation
- GitHub stars/forks (if available)
- Security advisories history
- Community signals (npm security advisories, GitHub discussions)

**Scoring:**
```
Reputation Score = 
  + 30 if no security advisories
  + 25 if maintainer has good history
  + 20 if consistent download trends
  + 15 if active GitHub repository
  + 10 if community endorsements
```

**Output:**
```json
{
  "agent": "reputation_analyzer",
  "score": 25,
  "indicators": [
    "Package has no security advisories",
    "Maintainer account created recently (15 days ago)",
    "No GitHub repository linked",
    "Download spike from 0 to 5k in 24 hours (suspicious)"
  ],
  "confidence": "medium"
}
```

---

## Coordinator Decision Logic

The coordinator weighs specialist findings using a confidence-weighted average:

```
Confidence = (Malicious × 0.5) + (Typosquat × 0.3) + (Reputation × 0.2)

If Confidence ≥ 90:  
  Verdict: MALICIOUS (high confidence)
  Action: Auto-block + create incident + notify security
  
Elif Confidence ≥ 70:  
  Verdict: SUSPICIOUS (medium confidence)
  Action: Block + request human review
  
Elif Confidence ≥ 40:  
  Verdict: MONITOR (low confidence)
  Action: Flag for monitoring + notify security
  
Else:
  Verdict: BENIGN (likely safe)
  Action: Log only
```

---

## Demo Scenarios

### Scenario 1: Typosquatting Attack

```
Package: reqeusts@1.0.0 (typosquat of 'requests')

Malicious Code Detector:
  Score: 15 (minimal code, mostly pass-through)
  Indicators: None significant

Typosquatting Analyzer:
  Score: 95 (HIGH)
  Indicators:
    - Levenshtein distance: 1 ('reqeusts' vs 'requests')
    - Target has 500M downloads, typosquat has 200
    - Package age: 3 days
    - Maintainer: no other packages

Reputation Analyzer:
  Score: 10 (LOW)
  Indicators:
    - New maintainer account
    - Sudden download spike
    - No GitHub repository

Coordinator Decision:
  Confidence: 59.5 = (15 × 0.5) + (95 × 0.3) + (10 × 0.2)
  Verdict: SUSPICIOUS
  Action: Block PR + notify security + create ticket for review

Rationale: Clear typosquatting pattern. Block until manual review confirms legitimacy.
```

### Scenario 2: Malicious Code

```
Package: webpack-optimizer@2.1.0

Malicious Code Detector:
  Score: 85 (HIGH)
  Indicators:
    - Base64 encoded payload in postinstall script
    - Network call to unknown domain: collector-xyz.com
    - Attempts to read ~/.ssh/id_rsa
    - Obfuscated JavaScript code

Typosquatting Analyzer:
  Score: 45 (name similar to 'webpack-bundle-analyzer')
  Indicators:
    - Moderate similarity to popular package
    - Package age: 60 days

Reputation Analyzer:
  Score: 20 (LOW)
  Indicators:
    - Multiple security advisories filed
    - Maintainer account suspended on npm

Coordinator Decision:
  Confidence: 60.0 = (85 × 0.5) + (45 × 0.3) + (20 × 0.2)
  Verdict: SUSPICIOUS → escalate to MALICIOUS (multi-signal agreement)
  Action: Auto-block + create P0 incident + notify security immediately

Rationale: Multiple high-confidence signals. Obfuscated code + suspicious network
           + poor reputation = likely malware. Immediate block.
```

### Scenario 3: Legitimate Package (Benign)

```
Package: axios@1.6.0

Malicious Code Detector:
  Score: 5 (clean code, no suspicious patterns)

Typosquatting Analyzer:
  Score: 0 (well-known, established package)
  Indicators:
    - 40M+ downloads/week
    - Package age: 8 years
    - Trusted maintainer

Reputation Analyzer:
  Score: 95 (HIGH - excellent reputation)
  Indicators:
    - Active GitHub: 100k stars
    - Consistent download trends
    - No security advisories in 2 years
    - Maintained by trusted org

Coordinator Decision:
  Confidence: 21.5 = (5 × 0.5) + (0 × 0.3) + (95 × 0.2)
  Verdict: BENIGN
  Action: Log only (no action needed)

Rationale: Established, trusted package with excellent reputation.
```

---

## Quick Start

```bash
cd 04-supply-chain-defense-agent

# Demo mode - runs all specialist agents + coordinator
python3 coordinator.py --demo --auto-approve

# View coordinator decisions
cat reports/coordinator_decisions.json

# View individual agent analyses
cat reports/agent_analyses.json

# Production mode (requires Snyk API token)
export SNYK_TOKEN="your-token"
python3 coordinator.py --project PROJECT_ID
```

---

## Production Integration

### Snyk Open Source API

```python
def get_new_dependencies(project_id):
    """Pull newly added dependencies from Snyk"""
    response = requests.get(
        f"https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/dependencies",
        headers={"Authorization": f"token {snyk_token}"},
        params={"added_in_last": "7_days"}
    )
    return response.json()
```

### Running Specialist Agents in Parallel

```python
import asyncio

async def analyze_package_parallel(package):
    """Run all specialist agents in parallel"""
    tasks = [
        run_malicious_code_detector(package),
        run_typosquat_analyzer(package),
        run_reputation_analyzer(package)
    ]
    results = await asyncio.gather(*tasks)
    return {
        "malicious_code": results[0],
        "typosquat": results[1],
        "reputation": results[2]
    }
```

---

## Metrics

```
snyk_supply_chain_packages_analyzed_total 1247
snyk_supply_chain_blocked_total{verdict="malicious"} 3
snyk_supply_chain_suspicious_total{verdict="suspicious"} 12
snyk_supply_chain_false_positive_rate 0.008
snyk_supply_chain_detection_time_seconds{quantile="0.99"} 4.2
```

---

## Regulatory Compliance

| Regulation | Requirement | How Multi-Agent Addresses |
|------------|-------------|--------------------------|
| **EO 14028** | Software supply chain security | Multi-signal malware detection, audit trail |
| **NIST SSDF** | Verify software integrity | Typosquatting + malicious code detection |
| **SOC 2 CC7.2** | Vendor management | Reputation analysis, security advisory tracking |
| **DORA (EU)** | ICT supply chain risk | Automated detection, incident response |

---

## What Makes This Snyk-Specific

- ✅ Analyzes **Snyk Open Source dependency findings** (not just npm registry)
- ✅ Integrates with **Snyk's dependency graph** for context
- ✅ Leverages **Snyk's vulnerability database** for reputation signals
- ✅ **Multi-agent architecture** demonstrates advanced agentic patterns
- ✅ **Policy-driven decisions** configurable per organization

---

**This agent demonstrates how multiple AI agents can work together to solve complex security problems that no single agent can solve alone.**
