# License Risk Agent (Snyk Open Source Integration)

Policy-driven license compliance agent that enforces license policies, blocks risky dependencies, and automates compliance workflows based on Snyk Open Source license findings.

## The Problem

**License violations are a legal and business risk:**
- GPL/AGPL dependencies in proprietary software → Legal risk
- Copyleft licenses without attribution → Compliance violation
- License changes in dependencies → Undetected policy violations
- Manual review doesn't scale → 100s of dependencies per project

**Industry Data:**
- 85% of codebases contain open source with license compliance risks (Synopsys 2024)
- Average legal review: 3-5 days per dependency
- Cost of license violation lawsuit: $500k-$2M+

## The Solution: Automated License Policy Enforcement

This agent enforces license policies automatically:

1. **Detect** — Pull license findings from Snyk Open Source API
2. **Classify** — Map licenses to policy categories (Approved / Review / Blocked)
3. **Decide** — Determine action based on policy + business context
4. **Act** — Block PRs, create compliance tickets, notify legal
5. **Log** — Immutable audit trail for compliance

---

## Policy-Based Decision Making

### License Categories

| Category | Licenses | Commercial Use | Copyleft | Action |
|----------|----------|----------------|----------|--------|
| **Approved** | MIT, BSD, Apache-2.0, ISC | ✅ Allowed | No | Auto-approve |
| **Permissive with Attribution** | Apache-2.0, BSD-3-Clause | ✅ Allowed | Weak | Create attribution ticket |
| **Weak Copyleft** | LGPL, MPL | ⚠️ Conditional | Weak | Request legal review |
| **Strong Copyleft** | GPL-2.0, GPL-3.0 | ⚠️ Conditional | Strong | Block if proprietary code |
| **Network Copyleft** | AGPL-3.0 | ❌ Not allowed | Very Strong | Auto-block + legal escalation |
| **Commercial/Proprietary** | Custom, proprietary | ❌ Not allowed | N/A | Block + negotiate |
| **Unknown/No License** | None, unlicensed | ❌ Not allowed | Unknown | Block + research |

### Decision Matrix

**For Commercial/Proprietary Software:**

| License | Direct Dependency | Transitive Dependency | Action |
|---------|-------------------|----------------------|--------|
| MIT, BSD, ISC | ✅ Approve | ✅ Approve | Log + optional attribution |
| Apache-2.0 | ✅ Approve | ✅ Approve | Create attribution ticket |
| LGPL | ⚠️ Review | ✅ Conditional | Request legal review |
| GPL | ❌ Block | ⚠️ Review | Block PR + legal escalation |
| AGPL | ❌ Block | ❌ Block | Block PR + notify legal immediately |

**For Open Source Software:**

| License | Direct Dependency | Transitive Dependency | Action |
|---------|-------------------|----------------------|--------|
| Any OSI-approved | ✅ Approve | ✅ Approve | Log only |
| GPL | ✅ Approve | ✅ Approve | Verify GPL compatibility |
| AGPL | ⚠️ Review | ⚠️ Review | Check if network service |
| Proprietary | ❌ Block | ❌ Block | Block + notify maintainers |

---

## Demo Scenarios

### Scenario 1: AGPL Dependency in Commercial SaaS

```
Finding: redis-py@4.5.0 with AGPL-3.0 license
Project: payment-api-prod (Commercial SaaS)
Dependency Type: Direct

Policy Violation: AGPL in proprietary network service

Agent Actions:
1. ❌ Block PR merge
2. 🚨 Escalate to legal team
3. 📋 Create Jira compliance ticket (P0)
4. 📧 Notify engineering leadership
5. 📝 Suggest alternatives: redis-py@3.5.3 (BSD) or valkey-py (BSD)

Rationale: AGPL requires source code disclosure for network services.
           Incompatible with proprietary SaaS business model.
```

### Scenario 2: GPL Dependency in Open Source Project

```
Finding: readline@8.2 with GPL-3.0 license
Project: cli-tool (Open Source, MIT licensed)
Dependency Type: Direct

Policy Check: GPL-3.0 incompatible with MIT (copyleft conflict)

Agent Actions:
1. ⚠️ Flag for review
2. 📋 Create compatibility check ticket
3. 📖 Provide guidance: "GPL requires downstream to also use GPL"
4. 🔄 Suggest relicense to GPL-3.0 or find alternative

Rationale: MIT + GPL combination requires explicit handling.
```

### Scenario 3: Apache-2.0 Dependency (Approved)

```
Finding: boto3@1.26.0 with Apache-2.0 license
Project: payment-api-prod (Commercial SaaS)
Dependency Type: Direct

Policy: Approved with attribution

Agent Actions:
1. ✅ Auto-approve (no PR block)
2. 📋 Create attribution ticket (P3 - due in 30 days)
3. 📝 Add to NOTICE file generation queue
4. 📊 Log for compliance reporting

Rationale: Apache-2.0 is approved for commercial use.
           Attribution required (automatic via NOTICE file).
```

### Scenario 4: Unknown License

```
Finding: internal-lib@1.0.0 with no license metadata
Project: web-frontend
Dependency Type: Direct

Policy Violation: No license = assume proprietary = blocked

Agent Actions:
1. ❌ Block PR merge
2. 📋 Create research ticket assigned to contributor
3. 📧 Notify team with guidance:
   - Check package README/LICENSE file
   - Contact maintainer for clarification
   - Find alternative if no license

Rationale: No license means "all rights reserved" legally.
           Cannot be used without explicit permission.
```

---

## Quick Start

```bash
cd 03-license-risk-agent

# Demo mode with sample license findings
python3 agent.py --demo --auto-approve

# View policy decisions
cat reports/license_decisions.txt

# View compliance tickets created
cat reports/compliance_tickets.json

# Production mode (requires Snyk API token)
export SNYK_TOKEN="your-token"
python3 agent.py --project PROJECT_ID
```

---

## Production Integration

### Snyk Open Source API

```python
import requests

def get_license_findings(project_id):
    response = requests.get(
        f"https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/issues",
        headers={"Authorization": f"token {snyk_token}"},
        params={"type": "license"}
    )
    
    licenses = []
    for issue in response.json().get("data", []):
        licenses.append({
            "package_name": issue["attributes"]["package_name"],
            "package_version": issue["attributes"]["package_version"],
            "license": issue["attributes"]["license"],
            "is_direct": issue["attributes"]["is_direct_dependency"],
            "severity": issue["attributes"]["severity"]
        })
    return licenses
```

### GitHub PR Block

```python
def block_pr_with_license_check(repo_name, pr_number, violations):
    from github import Github
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Add failing status check
    commit = pr.get_commits().reversed[0]
    commit.create_status(
        state="failure",
        context="License Compliance / Snyk Agent",
        description=f"{len(violations)} license violations found",
        target_url="https://security.company.com/licenses"
    )
    
    # Add PR comment
    comment = f"""## ⚖️ License Compliance Check Failed

{len(violations)} license policy violation(s) detected:

{chr(10).join([f"- **{v['package']}** ({v['license']}) - {v['reason']}" for v in violations])}

**Next Steps:**
1. Review the violations above
2. See https://wiki.company.com/license-policy for approved licenses
3. Contact legal@company.com if you need an exception

**This PR cannot be merged until violations are resolved.**

/cc @legal-team
"""
    pr.create_issue_comment(comment)
```

---

## Regulatory Compliance

| Regulation | Requirement | How Agent Addresses |
|------------|-------------|-------------------|
| **GPL/AGPL Compliance** | Source code disclosure for copyleft | Auto-detects, blocks violations, audit trail |
| **Corporate Policy** | License allowlist/blocklist | Policy-driven decisions, consistent enforcement |
| **SOC 2 CC8.1** | Software licensing compliance | Automated checks, audit logs, policy versioning |
| **GDPR Article 5(2)** | Accountability (if using GDPR-incompatible licenses) | Documented decisions, legal review triggers |

---

## Metrics

```
snyk_license_findings_total{severity="high"} 12
snyk_license_violations_total{category="strong_copyleft"} 3
snyk_license_prs_blocked_total 3
snyk_license_legal_escalations_total 2
snyk_license_attribution_tickets_created_total 47
snyk_license_policy_enforcement_rate 1.0
```

---

## What Makes This Snyk-Specific

- ✅ Pulls from **Snyk Open Source license findings** (not package.json scanning)
- ✅ Integrates with **Snyk Issues API** for unified view
- ✅ Leverages **Snyk's license database** (400k+ packages, 1,000+ licenses)
- ✅ **Policy-driven** decisions configurable per organization
- ✅ **Tiered autonomy**: Auto-approve safe licenses, block risky ones, escalate edge cases

---

**This agent transforms Snyk from "we found license issues" to "we enforce license policies automatically."**
