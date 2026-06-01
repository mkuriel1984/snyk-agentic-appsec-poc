# Snyk Agentic AppSec POC

Proof of concept demonstrating autonomous security agent patterns applied to Snyk's Application Security platform. Built to showcase how **Detect → Decide → Act → Log** architecture enables intelligent, scalable, and compliant security automation.

## Overview

This POC demonstrates four autonomous agents that operate on Snyk security findings, each showcasing different aspects of agentic security architecture:

1. **Vulnerability Triage Agent** — Intelligent prioritization based on exploitability, reachability, and business context
2. **Secrets Remediation Agent** — Automated detection and vaulting with developer-friendly workflows
3. **License Risk Agent** — Policy-driven license compliance with tiered autonomy
4. **Supply Chain Defense Agent** — Multi-agent coordination for malicious package detection

## Why This Matters for Snyk

### The Challenge

Snyk customers face an overwhelming volume of security findings:
- **10,000+ vulnerabilities** in a typical enterprise application portfolio
- **50-200 secrets** exposed per repository on average
- **License violations** requiring legal review and remediation
- **Malicious packages** disguised as legitimate dependencies

Security teams cannot manually triage this volume. Developers are overwhelmed by noise and miss critical issues. Traditional tooling produces findings but doesn't guide action.

### The Agentic Solution

Autonomous agents bridge the gap between detection and remediation by:
- **Intelligent triage** — ML-powered scoring that considers exploit availability, reachability analysis, asset criticality, and business impact
- **Tiered autonomy** — Auto-executing safe actions (notify, tag, create ticket) while requiring human approval for disruptive ones (block PR, disable package)
- **Developer experience** — Surfacing only actionable, contextualized findings with clear remediation paths
- **Compliance by design** — Immutable audit trails, policy-based decisioning, and regulatory mapping built in

## Architecture Principles

All agents in this POC follow the same architectural pattern:

```
┌────────────────────────────────────────────────────────┐
│  DETECT → DECIDE → ACT → LOG                           │
└────────────────────────────────────────────────────────┘

1. DETECT    — Pull findings from Snyk API / webhooks
2. DECIDE    — Apply ML scoring + policy rules to determine action
3. ACT       — Execute with tiered autonomy (auto where safe, approval where needed)
4. LOG       — Immutable audit trail for compliance and learning
```

### Key Design Decisions

**Tiered Autonomy** — Actions are categorized by reversibility and blast radius:
- **Tier 1 (Auto)** — Create Jira ticket, add PR comment, tag issue, notify Slack → no approval needed
- **Tier 2 (Approval)** — Block PR merge, disable CI pipeline, revoke API key → human approval required
- **Tier 3 (Advisory)** — High-impact decisions like emergency patches → agent recommends, human decides

**Policy Separation** — Decision logic lives independently from execution:
- `policy/` — Scoring models, threshold rules, action mappings (versioned, auditable)
- `agents/` — Core agent logic (detect, decide, act, log)
- `adapters/` — Swappable integrations (Snyk API, Jira, Slack, GitHub)

**Swappable Adapters** — All external integrations are clean interfaces:
- Production: Real Snyk API, Jira, Slack webhooks, GitHub Actions
- POC: Simulated responses for demo purposes
- Testing: Mock adapters for CI/CD validation

**Audit-First Design** — Every decision generates:
- **Audit log** (immutable, JSONL) — timestamp, agent, finding, decision, rationale, outcome
- **Metrics** (Prometheus format) — triage rate, auto-action rate, approval latency, false positive rate
- **Learning feedback** — When humans override, capture for model tuning

## Strategic Alignment with Snyk

This POC directly supports Snyk's strategic priorities:

### 1. **Developer-First Security**
Agents reduce noise by surfacing only high-priority, actionable findings with clear remediation guidance. Developers spend less time triaging and more time shipping secure code.

### 2. **Scale Through Automation**
Autonomous triage and remediation enable security teams to manage 10x more applications without proportional headcount growth.

### 3. **AI-Native Platform**
Demonstrates how Snyk can differentiate by embedding intelligence into every stage of the security workflow — not just detection, but decisioning and action.

### 4. **Compliance by Design**
Built-in audit trails, policy versioning, and regulatory mapping (PCI-DSS, SOC 2, GDPR, DORA) make customers audit-ready by default.

### 5. **Ecosystem Integration**
Clean adapter architecture shows how Snyk agents orchestrate across the entire DevSecOps toolchain (Jira, Slack, GitHub, CI/CD, Snyk Asset Management).

## Projects

### [01 — Vulnerability Triage Agent](./01-vulnerability-triage-agent/)

Automatically prioritizes Snyk Open Source and Container vulnerabilities using a composite risk score:
- **Exploitability** — EPSS score, exploit maturity, active exploitation indicators
- **Reachability** — Snyk Reachability Analysis results
- **Asset criticality** — Production vs dev, customer-facing vs internal, PCI/PHI data handling
- **Business impact** — Revenue-critical services weighted higher

**Demo scenarios:**
- Critical CVSS 9.8 vulnerability with no exploit → Medium priority
- Medium CVSS 6.2 with active exploitation + reachable + production asset → Critical priority

### [02 — Secrets Remediation Agent](./02-secrets-remediation-agent/)

Detects secrets in Snyk Code scans and automatically:
1. Vaults the secret value in AWS Secrets Manager / HashiCorp Vault
2. Replaces code references with `{{secret://...}}` URIs
3. Creates PR with remediation + vault integration code
4. Notifies security team with discovery context

**Demo scenarios:**
- AWS key hardcoded in config file → auto-vaulted + PR created with boto3 resolver code
- Slack webhook in logs → vaulted + PR comment guides developer to env vars

### [03 — License Risk Agent](./03-license-risk-agent/)

Policy-driven license compliance enforcement:
- **Critical licenses** (GPL, AGPL on proprietary code) → Auto-block PR + notify legal
- **High-risk licenses** (LGPL, MPL with copyleft concerns) → Request approval from legal
- **Medium licenses** (Apache with patent clauses) → Notify + create compliance ticket
- **Low/approved licenses** (MIT, BSD, ISC) → Log only

**Demo scenarios:**
- GPL dependency added to commercial SaaS product → PR blocked, legal notified, Jira created
- Apache 2.0 dependency → Auto-approved with attribution reminder

### [04 — Supply Chain Defense Agent](./04-supply-chain-defense-agent/)

Multi-agent coordination for malicious package detection. Three specialist agents analyze findings:
1. **Malicious Code Detector** — Static analysis for obfuscation, suspicious network calls, crypto miners
2. **Typosquatting Analyzer** — Levenshtein distance from popular packages, recent registration, low download count
3. **Behavior Anomaly Detector** — Post-install scripts, unusual file system access, privilege escalation

A **Coordinator Agent** synthesizes findings, assigns confidence scores, and decides action:
- **High confidence malicious** → Auto-block + notify security + create incident
- **Medium confidence suspicious** → Request approval + flag for manual review
- **Low confidence / benign** → Log + monitor

**Demo scenarios:**
- Package `reqeusts` (typosquat of `requests`) with 3 downloads → Blocked
- Legitimate `webpack` with post-install script → Approved (common pattern)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mkuriel1984/snyk-agentic-appsec-poc.git
cd snyk-agentic-appsec-poc

# Run all agents in sequence (demo mode)
./run_demo.sh

# Or run individual agents
cd 01-vulnerability-triage-agent
python3 agent.py --demo
open reports/triage_report.html

cd ../02-secrets-remediation-agent
python3 agent.py --demo
cat audit/actions.jsonl

cd ../03-license-risk-agent
python3 agent.py --demo

cd ../04-supply-chain-defense-agent
python3 coordinator.py --demo
```

## Production Considerations

### Snyk API Integration
Replace simulated findings in `adapters/snyk_api.py` with real API calls:
```python
import snyk

client = snyk.SnykClient(token=os.environ["SNYK_TOKEN"])
projects = client.organizations.get("org-id").projects.all()
issues = project.issues.all()
```

### Webhook-Driven Architecture
For real-time response, deploy agents as webhook listeners:
- Snyk webhook triggers agent on new finding
- Agent processes in <5 seconds
- Action taken before developer context-switches

### ML Model Training
The POC uses heuristic scoring. In production:
- Train on historical triage decisions (supervised learning)
- Fine-tune LLM on Snyk's vulnerability corpus
- Active learning from human overrides

### Security & IAM
- Agents run with least-privilege service accounts
- Vault access via short-lived tokens with audit logging
- Policy changes require PR approval + SOC sign-off

## Regulatory Alignment

All agents include compliance artifacts:

| Regulation | Requirement | How Agents Address |
|---|---|---|
| **PCI-DSS** | Req 6.2 — Protect against known vulnerabilities | Vulnerability Triage Agent prioritizes and tracks remediation |
| **PCI-DSS** | Req 3.5 — Cryptographic key management | Secrets Agent vaults keys with lifecycle tracking |
| **GDPR** | Article 30 — Record of processing activities | Immutable audit logs with rationale and timestamp |
| **DORA (EU)** | ICT risk management, incident response | Automated detection + response with <15 min time-to-action |
| **NYDFS Part 500** | Cybersecurity policy, incident notification | Policy-driven decisioning with documented overrides |
| **SOC 2** | Change management, access controls | All actions logged, high-risk actions require approval |
| **SR 11-7** | Model risk management | ML scoring models versioned, tested, and monitored |

## Metrics & Observability

Each agent exposes metrics for monitoring:
```
snyk_agent_findings_processed_total{agent="vuln_triage", severity="critical"}
snyk_agent_auto_actions_total{agent="secrets", action="vault"}
snyk_agent_approval_latency_seconds{agent="license"}
snyk_agent_false_positive_rate{agent="supply_chain"}
```

Dashboards show:
- **Triage throughput** — Findings processed per hour
- **Autonomy rate** — % auto-executed vs approval-required
- **Time to remediation** — Detection to fix deployment
- **Override rate** — Human disagreements with agent decisions (learning signal)

## User Experience

Want to see how people actually interact with this system?

- **[USER_EXPERIENCE.md](USER_EXPERIENCE.md)** — Complete walkthroughs for Security Engineer, Developer, and Security Manager personas
- **[UI_MOCKUPS.md](UI_MOCKUPS.md)** — Visual mockups of Slack alerts, Jira tickets, GitHub PR comments, and dashboards

**TL;DR:** Security teams triage 10,000+ vulnerabilities in minutes instead of weeks. Developers get actionable guidance with clear remediation steps. Managers get one-click compliance reports.

## Extending the POC

### Add New Agents
1. Create `05-new-agent/` directory
2. Implement `detect()`, `decide()`, `act()`, `log()` functions
3. Add policy rules in `policy/new_agent_policy.yaml`
4. Create adapter in `adapters/new_integration.py`

### Integrate with Snyk Issues
Connect to Snyk's **Issues** product for unified prioritization:
- Pull vulnerability, license, and code quality findings
- Apply cross-product risk scoring (vulnerability + reachability + license risk)
- Generate unified remediation plan
- Track fix verification across all issue types

### LLM Integration
Replace heuristic decisioning with Claude API for natural language reasoning:
```python
import anthropic

def ai_decide(finding, context):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4",
        messages=[{
            "role": "user",
            "content": f"""You are a security triage agent. Analyze this finding:

Finding: {finding}
Context: {context}

Provide:
1. Risk score (0-100)
2. Recommended action (ignore, notify, block)
3. Rationale for developers
4. Regulatory implications

Respond as JSON."""
        }]
    )
    return parse_response(response.content[0].text)
```

## Repository Structure

```
snyk-agentic-appsec-poc/
├── README.md                              # This file
├── ARCHITECTURE.md                        # Deep dive on design decisions
├── STRATEGIC_CONTEXT.md                   # How this aligns with Snyk's vision
├── run_demo.sh                            # Run all agents in demo mode
├── common/                                # Shared utilities
│   ├── audit.py                          # Audit logging interface
│   ├── policy.py                         # Policy engine
│   └── scoring.py                        # Risk scoring models
├── adapters/                             # External integrations
│   ├── snyk_api.py                       # Snyk API client (simulated)
│   ├── jira.py                           # Jira integration
│   ├── slack.py                          # Slack notifications
│   └── github.py                         # GitHub PR automation
├── 01-vulnerability-triage-agent/
│   ├── README.md
│   ├── agent.py                          # Main agent logic
│   ├── policy/vuln_triage_policy.yaml
│   ├── scenarios/                        # Demo scenarios
│   └── reports/                          # Output
├── 02-secrets-remediation-agent/
│   ├── README.md
│   ├── agent.py
│   ├── vault_adapter.py                  # Vault integration
│   ├── policy/secrets_policy.yaml
│   └── scenarios/
├── 03-license-risk-agent/
│   ├── README.md
│   ├── agent.py
│   ├── policy/license_policy.yaml
│   └── scenarios/
└── 04-supply-chain-defense-agent/
    ├── README.md
    ├── coordinator.py                     # Multi-agent coordinator
    ├── agents/
    │   ├── malicious_code_detector.py
    │   ├── typosquat_analyzer.py
    │   └── behavior_anomaly_detector.py
    ├── policy/supply_chain_policy.yaml
    └── scenarios/
```

## License

MIT — Use freely, attribution appreciated, no warranty.

## About

Built by Maor Kuriel as a proof of concept demonstrating how agentic security patterns can transform Snyk's Application Security platform from detection-focused to action-oriented.

**Contact:** maor.kuriel@snyk.io  
**GitHub:** [@mkuriel1984](https://github.com/mkuriel1984)

---

*This POC is inspired by architectural patterns from the agentic security community but implements original use cases specifically designed for Snyk's platform and strategic direction.*
