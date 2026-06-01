# Architecture Deep Dive

## Design Philosophy

This POC is built on five architectural principles that make agentic security work in production:

### 1. Detect → Decide → Act → Log (The Canonical Loop)

Every agent follows this pattern:

```python
def agent_loop():
    # 1. DETECT — Pull findings from data sources
    findings = detect_vulnerabilities(snyk_api)
    
    # 2. ENRICH — Add context (EPSS, threat intel, asset metadata)
    enriched = [enrich_finding(f, context_sources) for f in findings]
    
    # 3. SCORE — Calculate risk using composite model
    scored = [calculate_risk_score(f) for f in enriched]
    
    # 4. DECIDE — Map score to priority and determine actions
    decisions = [decide_actions(f, policy) for f in scored]
    
    # 5. ACT — Execute with tiered autonomy
    results = [execute_actions(d, approval_system) for d in decisions]
    
    # 6. LOG — Write immutable audit trail
    [log_decision(r, audit_store) for r in results]
```

This loop is:
- **Observable** — Every step produces artifacts for debugging
- **Testable** — Each function is pure and can be unit tested
- **Auditable** — Decisions are logged with full rationale
- **Interruptible** — Human oversight can pause at any step

### 2. Tiered Autonomy (Speed Where Safe, Oversight Where Needed)

Actions are classified by reversibility and blast radius:

| Tier | Criteria | Examples | Auto-Execute? |
|---|---|---|---|
| **Tier 1 (Safe)** | Reversible, non-disruptive, informational | Create Jira, add PR comment, notify Slack | ✅ Yes |
| **Tier 2 (Caution)** | Disruptive but recoverable | Block PR merge, disable package, revoke API key | ⚠️ Approval required |
| **Tier 3 (Critical)** | High-impact, code changes, production deployments | Auto-deploy fix, emergency patch | ❌ Advisory only |

```python
def execute_actions(decision, approval_system):
    for action in decision['actions']:
        if action.tier == 1:
            # Auto-execute safe actions
            result = execute(action)
        elif action.tier == 2:
            # Request approval via Slack/UI
            if approval_system.request_approval(action):
                result = execute(action)
            else:
                result = "SKIPPED (user rejected)"
        else:  # Tier 3
            # Advisory only — agent recommends, human decides
            result = "RECOMMENDED (awaiting human decision)"
        
        log(action, result)
```

### 3. Policy-Based Decisioning (Logic Separated from Execution)

Decision logic lives in versioned policy files, not hardcoded in agent code:

**Policy File (`policy/vuln_triage_policy.yaml`):**
```yaml
priority_buckets:
  critical:
    score_min: 90
    score_max: 100
    sla_hours: 24
    actions:
      - type: escalate_oncall
        tier: 2
        auto_approve: true  # For P0 only
      - type: block_deployments
        tier: 2
        auto_approve: false
      - type: create_jira
        project: SEC
        issue_type: Incident
        priority: P0
        tier: 1
        auto_approve: true

risk_scoring:
  weights:
    exploitability: 0.40
    reachability: 0.30
    asset_criticality: 0.20
    business_impact: 0.10
  
  exploitability:
    epss_multiplier: 40
    exploit_maturity:
      functional: 30
      poc: 20
      high: 15
      none: 0
    cisa_kev_bonus: 30
```

**Agent Code:**
```python
def decide_actions(finding, policy):
    score = calculate_score(finding, policy['risk_scoring'])
    
    # Find matching priority bucket
    for bucket_name, bucket_config in policy['priority_buckets'].items():
        if bucket_config['score_min'] <= score <= bucket_config['score_max']:
            return {
                'priority': bucket_name,
                'sla_hours': bucket_config['sla_hours'],
                'actions': bucket_config['actions']
            }
```

**Benefits:**
- **Version control** — Policy changes tracked in git with PR review
- **A/B testing** — Run two policies in parallel, measure outcomes
- **Compliance mapping** — Document why thresholds were chosen
- **Non-technical editing** — Security teams can tune without touching code

### 4. Swappable Adapters (Demo Today, Production Tomorrow)

All external integrations are clean interfaces:

```python
# Interface
class VulnerabilitySource:
    def fetch_vulnerabilities(self, filters) -> List[Vulnerability]:
        raise NotImplementedError

# Demo implementation
class DemoVulnerabilitySource(VulnerabilitySource):
    def fetch_vulnerabilities(self, filters):
        with open('scenarios/demo_vulnerabilities.json') as f:
            return json.load(f)

# Production implementation
class SnykAPISource(VulnerabilitySource):
    def __init__(self, api_token, org_id):
        self.client = SnykClient(api_token)
        self.org_id = org_id
    
    def fetch_vulnerabilities(self, filters):
        projects = self.client.organizations.get(self.org_id).projects.all()
        vulnerabilities = []
        for project in projects:
            vulnerabilities.extend(project.issues.all())
        return [self._convert_to_standard_format(v) for v in vulnerabilities]
```

Same pattern for:
- **Asset metadata** — Demo JSON file → Snyk Asset Management API
- **Threat intel** — Demo EPSS scores → FIRST.org API + CISA KEV
- **Ticketing** — Demo console output → Jira REST API
- **Notifications** — Demo logs → Slack webhooks
- **Approvals** — Demo terminal input → Slack interactive buttons / web UI

### 5. Audit-First Design (Compliance by Construction)

Every decision generates three audit artifacts:

**1. Immutable Decision Log (`audit/triage_decisions.jsonl`)**
```jsonl
{"timestamp": "2026-06-01T15:45:23Z", "agent": "vuln-triage", "vulnerability": {"cve": "CVE-2024-5678", "package": "express@4.16.0"}, "scores": {"composite": 94.72, "exploitability": 96.8, "reachability": 100, "asset_criticality": 100, "business_impact": 60}, "decision": {"priority": "P0-Critical", "sla_hours": 24, "rationale": "Immediate attention required: actively exploited in the wild (CISA KEV), vulnerable code is reachable, exposed on public API surface, production environment, PCI-scoped asset, customer-facing service"}, "executed_actions": [{"action": "escalate_oncall", "status": "EXECUTED", "timestamp": "2026-06-01T15:45:24Z"}]}
```

**2. Action Metrics (Prometheus format)**
```
snyk_triage_vulnerabilities_processed_total{priority="P0"} 3
snyk_triage_auto_actions_total{action="create_jira"} 847
snyk_triage_approval_latency_seconds{quantile="0.99"} 120
snyk_triage_false_positive_rate 0.047
```

**3. Human-Readable Report (`reports/triage_report.html`)**
- Visual dashboard with priority distribution
- Detailed rationale for each decision
- Links to Snyk findings, Jira tickets, PRs

**Regulatory Mapping:**

| Audit Artifact | Regulations Addressed |
|---|---|
| Immutable decision log | GDPR Art 30 (record of processing), SOC 2 (change control), DORA (incident response) |
| Action metrics | SR 11-7 (model monitoring), NYDFS Part 500 (cybersecurity event tracking) |
| Policy version control | PCI-DSS Req 12.1 (security policy), SOC 2 (policy enforcement) |
| Human approval records | EU AI Act (human oversight), GDPR Art 22 (automated decisions) |

## Composite Risk Scoring Model

The vulnerability triage agent uses a weighted composite score:

```
Risk Score = (Exploitability × 40%) + (Reachability × 30%) + (Asset Criticality × 20%) + (Business Impact × 10%)
```

### Why These Weights?

**Exploitability (40%)** — Highest weight because:
- A vulnerability with no exploit has low real-world risk regardless of CVSS
- EPSS (Exploit Prediction Scoring System) outperforms CVSS for prioritization
- CISA KEV list represents confirmed active exploitation

**Reachability (30%)** — Second highest because:
- Unreachable vulnerabilities (dead code, transitive dependencies) have lower urgency
- Snyk's Reachability Analysis provides ground truth on exploitability
- Public API surface exposure multiplies risk

**Asset Criticality (20%)** — Third because:
- Production environments require faster response than dev/staging
- Compliance scope (PCI, PHI) mandates specific controls
- Customer-facing services have higher blast radius

**Business Impact (10%)** — Lowest weight because:
- Service tier and SLA are context for severity, not risk itself
- Used as tie-breaker when technical risk is equal
- Helps prioritize limited security resources

### Example Scenarios

**Scenario A: High CVSS, Low Real Risk**
```
CVE-2024-1234 in lodash@4.17.19
CVSS: 9.8 (Critical)
→ Exploitability: 0.04 (EPSS: 0.001, no exploit, not on CISA KEV)
→ Reachability: 15 (not reachable, transitive dependency)
→ Asset Criticality: 5 (dev environment)
→ Business Impact: 20 (tier 3 service)
= Composite Score: 7.52 → P4 Informational

Rationale: Despite critical CVSS, extremely low exploitation probability + 
not reachable + dev environment = can safely defer to monthly review.
```

**Scenario B: Medium CVSS, High Real Risk**
```
CVE-2024-5678 in express@4.16.0
CVSS: 6.5 (Medium)
→ Exploitability: 96.8 (EPSS: 0.92, functional exploit, CISA KEV)
→ Reachability: 100 (reachable, direct dependency, public API)
→ Asset Criticality: 100 (production, PCI-scoped, customer-facing)
→ Business Impact: 60 (tier 1, 500k users, 99.99% SLA)
= Composite Score: 94.72 → P0 Critical

Rationale: Active exploitation in the wild + reachable in auth 
middleware + production PCI asset = immediate remediation required.
```

## Multi-Agent Coordination (Supply Chain Defense Example)

The Supply Chain Defense agent demonstrates how specialist agents coordinate:

```
┌─────────────────────────────────────────────────────────────┐
│                    Coordinator Agent                        │
│  (Synthesizes findings, assigns confidence, decides action) │
└─────────────────────────────────────────────────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │   Malicious  │   │ Typosquatting│   │   Behavior   │
    │     Code     │   │   Analyzer   │   │   Anomaly    │
    │   Detector   │   │              │   │   Detector   │
    └──────────────┘   └──────────────┘   └──────────────┘
```

Each specialist agent analyzes one dimension:

**1. Malicious Code Detector**
- Static analysis for obfuscation, suspicious patterns
- Network calls to unexpected domains
- Crypto mining, keylogging signatures
- Output: `malicious_score` (0-100), list of indicators

**2. Typosquatting Analyzer**
- Levenshtein distance from popular packages
- Package age, download count, maintainer history
- Name patterns (reqeusts vs requests, colurs vs colors)
- Output: `typosquat_score` (0-100), suspected target package

**3. Behavior Anomaly Detector**
- Post-install script analysis
- File system access patterns
- Privilege escalation attempts
- Network behavior (DNS queries, HTTP requests)
- Output: `anomaly_score` (0-100), list of anomalies

**Coordinator Decision Logic:**
```python
def coordinate(findings):
    # Weight specialist findings
    confidence = (
        findings['malicious_code']['score'] * 0.5 +
        findings['typosquat']['score'] * 0.3 +
        findings['anomaly']['score'] * 0.2
    )
    
    # Determine action based on confidence
    if confidence >= 90:
        # High confidence malicious
        return {
            'verdict': 'BLOCK',
            'actions': ['block_package', 'create_incident', 'notify_security'],
            'auto_approve': True
        }
    elif confidence >= 70:
        # Medium confidence suspicious
        return {
            'verdict': 'SUSPICIOUS',
            'actions': ['flag_for_review', 'notify_security'],
            'auto_approve': False  # Requires human review
        }
    else:
        # Low confidence / likely benign
        return {
            'verdict': 'MONITOR',
            'actions': ['log_only', 'add_to_watchlist'],
            'auto_approve': True
        }
```

## Production Considerations

### Scaling to 10,000+ Vulnerabilities

**Problem:** Enterprise organizations have 10,000+ vulnerabilities across hundreds of projects.

**Solution:**
1. **Stream processing** — Use Snyk webhooks instead of polling
2. **Parallel execution** — Process findings concurrently with `asyncio`
3. **Incremental updates** — Only re-score when context changes (new exploit, asset reclassification)
4. **Caching** — Cache EPSS scores, threat intel lookups for 24 hours

```python
import asyncio

async def process_vulnerabilities_parallel(vulnerabilities):
    tasks = [process_vulnerability(v) for v in vulnerabilities]
    return await asyncio.gather(*tasks)

async def process_vulnerability(vuln):
    # Fetch context in parallel
    epss_task = fetch_epss_score(vuln['cve'])
    asset_task = fetch_asset_metadata(vuln['asset_id'])
    threat_task = fetch_threat_intel(vuln['cve'])
    
    epss, asset, threat = await asyncio.gather(epss_task, asset_task, threat_task)
    
    # Score and decide
    score = calculate_risk_score(vuln, epss, asset, threat)
    decision = decide_actions(score)
    
    # Execute actions (with approval if needed)
    result = await execute_actions(decision)
    
    # Log
    log_decision(vuln, score, decision, result)
    
    return result
```

### Learning from Human Overrides

**Problem:** Agents will make mistakes. How do we improve over time?

**Solution:** Capture override rationale and retrain models.

```python
def handle_human_override(original_decision, human_decision, rationale):
    # Log override for analysis
    log_override({
        'timestamp': datetime.now(),
        'vulnerability': original_decision['vulnerability'],
        'agent_priority': original_decision['priority'],
        'human_priority': human_decision['priority'],
        'agent_score': original_decision['score'],
        'rationale': rationale  # Why human disagreed
    })
    
    # If override is systematic, update policy
    if is_systematic_error(original_decision, human_decision):
        suggest_policy_update(original_decision, human_decision, rationale)
    
    # Feed back into ML model training (if using ML scoring)
    if use_ml_scoring:
        training_queue.add({
            'features': extract_features(original_decision['vulnerability']),
            'label': human_decision['priority'],
            'weight': 2.0  # Human feedback gets higher weight
        })
```

### Security & IAM

**Problem:** Agents need access to sensitive APIs (Snyk, Jira, Slack) and can take disruptive actions.

**Solution:**
1. **Least privilege** — Agent service account has minimal required permissions
2. **Time-bounded tokens** — Credentials rotate every 24 hours
3. **Audit logging** — Every API call logged with agent identity
4. **Rate limiting** — Prevent runaway agents from spamming systems
5. **Kill switch** — Emergency disable via environment variable or API call

```python
class AgentExecutor:
    def __init__(self, identity, credentials_manager):
        self.identity = identity
        self.credentials = credentials_manager.get_short_lived_token(identity)
        self.rate_limiter = RateLimiter(max_requests=100, window=60)
        self.audit_logger = AuditLogger()
    
    def execute_action(self, action):
        # Check kill switch
        if os.environ.get('AGENT_DISABLED'):
            raise AgentDisabledException("Agent has been disabled via kill switch")
        
        # Rate limit
        if not self.rate_limiter.allow():
            raise RateLimitException("Agent exceeded rate limit")
        
        # Audit log
        self.audit_logger.log({
            'agent_identity': self.identity,
            'action': action,
            'timestamp': datetime.now()
        })
        
        # Execute with short-lived credentials
        result = action.execute(self.credentials)
        
        # Rotate credentials if needed
        if self.credentials.expires_soon():
            self.credentials = self.credentials_manager.rotate(self.identity)
        
        return result
```

## Next Steps for Production

1. **Phase 1 (MVP, 3 months)**
   - Deploy Vulnerability Triage Agent to 5 pilot customers
   - Integrate with Snyk Issues API, real EPSS/CISA KEV data
   - Build Slack approval workflow UI
   - Measure: triage throughput, auto-action rate, false positive rate

2. **Phase 2 (Scale, 6 months)**
   - Add Secrets Remediation Agent (auto-vaulting + PR generation)
   - Add License Risk Agent (policy-driven compliance)
   - Build learning feedback loop from human overrides
   - Integrate with Evo for workflow orchestration

3. **Phase 3 (Full Autonomy, 12 months)**
   - Multi-agent coordination (Supply Chain Defense)
   - Auto-remediation with verification (generate fix PR, run tests, auto-merge)
   - Compliance-as-code (auto-generate SOC 2, PCI-DSS evidence)
   - Threat intel fusion (correlate CVEs with active exploits)

---

**This is not a research project. This is production-ready architecture, ready to scale.**
