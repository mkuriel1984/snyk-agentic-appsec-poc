# User Experience: End-to-End Walkthrough

## User Personas

### 1. **Sarah (Security Engineer)**
- Manages AppSec for 200+ microservices
- Drowning in 10,000+ Snyk findings
- Needs to prioritize what actually matters

### 2. **Mike (Backend Developer)**
- Ships features weekly
- Gets pinged about security issues mid-sprint
- Wants clear, actionable guidance

### 3. **Lisa (Security Manager)**
- Reports to CISO on security posture
- Needs audit trails for compliance (SOC 2, PCI-DSS)
- Budget for 3 security engineers, supporting 50 dev teams

---

## Scenario 1: Morning Triage (Sarah's Experience)

### 8:30 AM — Agent Detects New Vulnerabilities

**What happens automatically:**
1. Snyk scan completes overnight, finds 47 new vulnerabilities across 12 projects
2. Triage agent runs automatically (webhook-triggered or scheduled)
3. Agent enriches each vulnerability:
   - Fetches EPSS scores from FIRST.org
   - Checks CISA KEV list for active exploitation
   - Pulls asset metadata from Snyk Asset Management
   - Queries Snyk Reachability Analysis results
4. Scores all 47 vulnerabilities using composite model
5. Makes decisions and executes actions

**Time elapsed:** 90 seconds

### 8:32 AM — Sarah Gets a Slack Notification

Sarah sees this in `#security-alerts`:

```
🚨 P0 Critical Vulnerability Detected

CVE-2024-5678: Authentication Bypass in express@4.16.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Risk Score: 94.72/100
Priority: P0 Critical
Asset: payment-api-prod (PCI-scoped, production)
Status: 🔴 Actively Exploited (CISA KEV)

Why This Matters:
• Active exploitation confirmed in the wild
• Vulnerable code is reachable in authentication middleware
• Production asset handling payment card data
• 500,000 customers impacted

Actions Taken by Agent:
✅ Paged on-call engineer (Jessica)
✅ Created Jira ticket SEC-4A7B29 (P0)
✅ Blocked deployments for payment-api-prod
⏳ Awaiting approval to block PR merges

Remediation: Upgrade to express@4.18.2 or apply patch

[View in Snyk] [View Jira Ticket] [Approve Block PR]
```

**Sarah's reaction:** "Finally! I see *why* this matters, not just another CVSS score."

### 8:35 AM — Sarah Reviews the Full Triage Report

Sarah clicks through to the HTML report dashboard:

**Summary View:**
```
Vulnerability Triage Report — June 1, 2026 8:32 AM

Total Vulnerabilities: 47
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P0 Critical        ⚫⚫⚫ 3
P1 High            🔴🔴🔴🔴🔴🔴🔴 7  
P2 Medium          🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠 12
P3 Low             🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡 10
P4 Informational   ⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪ 15

Auto-Actions Executed: 42
Awaiting Approval: 1
Average Triage Time: 1.9 seconds per vulnerability
```

**Detailed View (P0 findings):**

Sarah sees three P0 Critical vulnerabilities with full context:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 P0 CRITICAL

CVE-2024-5678: Authentication Bypass in express@4.16.0

Package: express@4.16.0 (direct dependency)
Asset: payment-api-prod (Production, PCI-scoped)
Team: payments-team

Risk Breakdown:
┌─────────────────────────────────────────────────┐
│ Composite Score:    94.72 / 100                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Exploitability:     96.8  (40% weight)          │
│ Reachability:       100.0 (30% weight)          │
│ Asset Criticality:  100.0 (20% weight)          │
│ Business Impact:    60.0  (10% weight)          │
└─────────────────────────────────────────────────┘

Triage Rationale:
Immediate attention required: actively exploited in the wild 
(CISA KEV), vulnerable code is reachable, exposed on public API 
surface, production environment, PCI-scoped asset, customer-facing 
service, tier 1 service serving 500,000 customers

Actions Taken:
✅ Paged on-call engineer via PagerDuty (8:32 AM)
✅ Created Jira SEC-4A7B29 (P0 Incident)
✅ Blocked deployments for payment-api-prod
✅ Posted to #security-alerts
⏳ Awaiting approval: Block PR merges

Remediation:
npm install express@4.18.2

Estimated Fix Time: 2 hours (upgrade + testing)
SLA: Fix within 24 hours

[View in Snyk] [View Jira] [View Code] [Approve Actions]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8:40 AM — Sarah Approves High-Risk Action

Sarah clicks **[Approve Actions]** for blocking PR merges.

**Approval Interface (Slack Interactive Message):**
```
⚠️ Approval Required

Action: Block PR merges for payment-api-prod
Reason: P0 Critical vulnerability (CVE-2024-5678)
Impact: Developers cannot merge PRs until vulnerability is fixed
Requested by: vulnerability-triage-agent
Risk: Medium (disruptive to development workflow)

[✅ Approve & Execute] [❌ Reject] [⏸️ Defer 1 Hour]

Rationale: Actively exploited vulnerability in production PCI asset. 
Blocking merges prevents introducing new features while critical 
security issue remains unpatched.
```

Sarah clicks **[✅ Approve & Execute]**.

**Result:**
- GitHub branch protection rule added to payment-api-prod repo
- All open PRs get status check: ❌ Blocked by security (CVE-2024-5678)
- Payment team gets Slack notification with context
- Audit log records: approved by sarah@company.com at 8:40 AM

### 8:45 AM — Sarah's Work is Done

**What Sarah accomplished in 15 minutes:**
- ✅ Triaged 47 vulnerabilities (automated)
- ✅ Identified 3 P0 critical issues
- ✅ Auto-escalated to on-call engineers
- ✅ Created 22 Jira tickets with full context
- ✅ Approved 1 high-risk action (block PRs)
- ✅ Communicated with 6 dev teams via Slack

**Without agents:** This would take 4-6 hours of manual work.

---

## Scenario 2: Developer Gets Notified (Mike's Experience)

### 9:15 AM — Mike Sees a Slack Message

Mike is mid-code review when he sees this in `#payments-team`:

```
🔧 Security Action Required — Your Team

CVE-2024-5678 in payment-api-prod requires immediate attention

Priority: P0 Critical (fix within 24 hours)
Risk Score: 94.72/100

Why this matters for your service:
• Actively exploited vulnerability in express auth middleware
• Your production payment API is exposed
• 500k customers at risk
• PCI compliance violation if not fixed immediately

What you need to do:
1. Upgrade express: npm install express@4.18.2
2. Run tests: npm test
3. Deploy to staging first
4. Merge PR and deploy to prod

Jira ticket created: SEC-4A7B29
Assigned to: @jessica (on-call)

Note: PR merges are blocked until this is fixed.

[View Jira] [View Snyk Finding] [Need Help?]
```

**Mike's reaction:** "Okay, I understand *why* this is critical and *exactly* what to do."

### 9:20 AM — Mike Checks Jira

Mike clicks through to Jira ticket SEC-4A7B29:

```
[P0] CVE-2024-5678: Authentication Bypass in express

Status: 🔴 In Progress
Assignee: Jessica Chen (on-call)
Labels: security, p0, pci-scoped, auto-triaged
Sprint: Security Sprint 2026-W23

Description:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VULNERABILITY DETAILS
Package: express@4.16.0 (direct dependency)
CVE: CVE-2024-5678
CVSS: 6.5 (Medium) — But agent scored as P0 Critical
Asset: payment-api-prod (Production, PCI-scoped)

RISK ASSESSMENT (Automated)
Composite Risk Score: 94.72/100
• Exploitability: 96.8 (CISA KEV — actively exploited)
• Reachability: 100.0 (used in auth middleware)
• Asset Criticality: 100.0 (prod PCI asset)
• Business Impact: 60.0 (500k customers)

WHY THIS MATTERS
This vulnerability is being actively exploited in the wild. 
The vulnerable code is reachable in your authentication 
middleware, meaning attackers can bypass login and access 
customer payment data. This is a PCI compliance violation.

REMEDIATION
1. Upgrade to express@4.18.2:
   cd services/payment-api
   npm install express@4.18.2

2. Test locally:
   npm test
   npm run integration-test

3. Deploy to staging:
   kubectl apply -f k8s/staging/

4. Smoke test staging:
   curl https://staging.payment-api.company.com/health

5. Deploy to production:
   kubectl apply -f k8s/production/

ESTIMATED TIME: 2 hours
SLA: Fix within 24 hours (by June 2, 8:32 AM)

ACTIONS TAKEN BY AGENT:
✅ Paged on-call engineer (Jessica)
✅ Blocked deployments for payment-api-prod
✅ Blocked PR merges (approved by Sarah)
✅ Notified #payments-team

Links:
• Snyk Finding: https://app.snyk.io/vuln/SNYK-JS-EXPRESS-5678901
• GitHub Repo: https://github.com/company/payment-api
• PagerDuty Incident: https://company.pagerduty.com/incidents/P4K2L9
```

**Mike's reaction:** "This is the most useful security ticket I've ever seen. I know exactly what to do."

### 9:30 AM — Mike Creates a Fix PR

Mike upgrades the package and creates a PR:

**GitHub PR: "Security: Upgrade express to 4.18.2 (CVE-2024-5678)"**

The PR gets an automatic comment from the agent:

```
🤖 Security Agent — Vulnerability Remediation

This PR addresses: CVE-2024-5678 (P0 Critical)

Security Impact:
✅ Fixes actively exploited authentication bypass
✅ Resolves PCI compliance violation
✅ Protects 500k customer payment records

Verification Checklist:
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Staging deployment successful
- [ ] Smoke tests pass on staging
- [ ] Security team approval

Once merged:
✅ Deployment block will be automatically removed
✅ PR merge block will be automatically removed
✅ Jira ticket SEC-4A7B29 will auto-transition to "Resolved"
✅ Compliance dashboard will update

Agent will monitor this PR and notify security team when deployed.

/cc @sarah @jessica
```

**Mike's reaction:** "The agent is tracking this end-to-end. Nice."

### 11:45 AM — Mike Merges the PR

After testing on staging, Mike merges the PR.

**What happens automatically:**
1. Agent detects PR merge via GitHub webhook
2. Agent waits for production deployment (monitors Kubernetes events)
3. Agent re-scans payment-api-prod with Snyk
4. Agent confirms CVE-2024-5678 is resolved
5. Agent removes deployment block
6. Agent removes PR merge block
7. Agent transitions Jira ticket to "Resolved"
8. Agent posts success message to #payments-team

**Slack notification in #payments-team:**
```
✅ Vulnerability Resolved

CVE-2024-5678 in payment-api-prod has been fixed!

Timeline:
• 8:32 AM — Vulnerability detected and triaged
• 9:15 AM — Team notified
• 9:30 AM — Fix PR created by @mike
• 11:45 AM — PR merged and deployed

Time to Resolution: 3 hours 13 minutes (well within 24h SLA)

Actions Completed:
✅ Vulnerability patched (express@4.18.2)
✅ Production deployment verified
✅ Snyk re-scan confirms fix
✅ Deployment block removed
✅ PR merge block removed
✅ Jira ticket resolved
✅ Compliance dashboard updated

Great work, team! 🎉

[View Audit Trail] [View Updated Risk Report]
```

---

## Scenario 3: Weekly Security Review (Lisa's Experience)

### Friday 2:00 PM — Lisa Reviews the Week

Lisa (Security Manager) opens the weekly security dashboard.

### Security Posture Dashboard

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECURITY POSTURE DASHBOARD
Week of May 26 - June 1, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VULNERABILITIES TRIAGED THIS WEEK
Total: 347 vulnerabilities across 45 projects

┌─────────────────────────────────────────────┐
│ P0 Critical    ⚫⚫⚫⚫⚫⚫ 6                  │
│ P1 High        🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 11     │
│ P2 Medium      🟠 × 47                      │
│ P3 Low         🟡 × 89                      │
│ P4 Info        ⚪ × 194                     │
└─────────────────────────────────────────────┘

RESOLUTION STATUS
┌─────────────────────────────────────────────┐
│ Fixed           ██████████████░░░░░░ 68%    │
│ In Progress     ████░░░░░░░░░░░░░░░░ 22%    │
│ Scheduled       ██░░░░░░░░░░░░░░░░░░  8%    │
│ Risk Accepted   ░░░░░░░░░░░░░░░░░░░░  2%    │
└─────────────────────────────────────────────┘

MEAN TIME TO REMEDIATION
┌─────────────────────────────────────────────┐
│ P0 Critical:  3.2 hours  (SLA: 24h) ✅      │
│ P1 High:      2.1 days   (SLA: 7d) ✅       │
│ P2 Medium:    12.4 days  (SLA: 30d) ✅      │
│ P3 Low:       45.2 days  (SLA: 90d) ✅      │
└─────────────────────────────────────────────┘

AGENT AUTOMATION METRICS
┌─────────────────────────────────────────────┐
│ Auto-Triaged:        347 / 347  (100%) ✅   │
│ Auto-Actions:        823 / 847  (97%)  ✅   │
│ Human Approvals:     24  / 847  (3%)   ✅   │
│ False Positives:     4   / 347  (1.2%) ✅   │
│ Human Overrides:     7   / 347  (2.0%) ⚠️   │
└─────────────────────────────────────────────┘

COMPLIANCE STATUS
┌─────────────────────────────────────────────┐
│ PCI-DSS Req 6.2    ✅ Compliant             │
│ SOC 2 CC7.1        ✅ Compliant             │
│ DORA (EU)          ✅ Compliant             │
│ NYDFS Part 500     ✅ Compliant             │
└─────────────────────────────────────────────┘

AUDIT TRAIL COMPLETENESS
All 347 triage decisions logged with full rationale ✅
Ready for audit review

TOP TEAMS BY REMEDIATION SPEED
1. payments-team    — 2.1 hour avg MTTR ⭐⭐⭐
2. platform-team    — 4.7 hour avg MTTR ⭐⭐
3. frontend-team    — 8.3 hour avg MTTR ⭐

AREAS NEEDING ATTENTION
⚠️ 7 human overrides this week (up from 3 last week)
   → Review override rationale and retrain model
⚠️ legacy-services has 12 P2 issues >30 days old
   → Schedule remediation sprint with legacy team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Export Audit Report] [Download Compliance Evidence] 
[View Override Analysis] [Schedule Sprint]
```

### Lisa Reviews Override Analysis

Lisa clicks **[View Override Analysis]** to understand why humans disagreed with the agent:

```
HUMAN OVERRIDE ANALYSIS
7 overrides this week

Override #1: CVE-2024-9999 in lodash@4.17.21
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent Decision: P3 Low (Score: 35.2)
Human Decision: P4 Info (Downgraded by sarah@company.com)
Rationale: "Package is used in test fixtures only, not production code"

Learning: Update reachability detection to distinguish test vs prod code

Override #2: CVE-2024-8888 in nginx@1.21.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent Decision: P1 High (Score: 78.4)
Human Decision: P2 Medium (Downgraded by sarah@company.com)
Rationale: "Web frontend sits behind Cloudflare WAF with rule blocking this attack"

Learning: Incorporate WAF/CDN protection layer into asset metadata

Override #3: Malicious package 'ua-parser-js@0.7.29'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent Decision: P2 Medium (Score: 65.0)
Human Decision: P0 Critical (Upgraded by jessica@company.com)
Rationale: "This package is used in auth flow for session tracking. Supply chain attack in auth = critical"

Learning: Increase weight for supply chain issues in authentication/authorization paths

[Retrain Model with Overrides] [Update Policy]
```

**Lisa's reaction:** "The agent is learning from our corrections. This is getting smarter over time."

### Lisa Exports Compliance Evidence

Lisa clicks **[Download Compliance Evidence]** and gets a ZIP file:

```
compliance-evidence-2026-06-01.zip
├── audit-trail.jsonl              (347 triage decisions with full rationale)
├── remediation-timeline.csv       (timestamp for each fix)
├── sla-compliance-report.pdf      (visual report with charts)
├── policy-version-history.json    (all policy changes this period)
├── human-oversight-log.jsonl      (all approval requests and outcomes)
└── compliance-mapping.xlsx        (findings mapped to PCI-DSS, SOC 2, DORA)
```

Lisa uploads this to the compliance portal for the SOC 2 audit next week.

**Lisa's reaction:** "We're audit-ready in one click. This would normally take 3 days to compile manually."

---

## User Journey Map

### Traditional Workflow (Without Agents)
```
┌──────────────────────────────────────────────────────────────┐
│ Day 1: Manual Triage                                         │
├──────────────────────────────────────────────────────────────┤
│ 9:00 AM   Security engineer reviews Snyk dashboard          │
│ 9:30 AM   Manually checks EPSS scores (copy-paste CVEs)     │
│ 10:00 AM  Cross-references CISA KEV list                     │
│ 10:30 AM  Looks up asset criticality in wiki/spreadsheet    │
│ 11:00 AM  Calculates priority mentally                       │
│ 11:30 AM  Creates Jira ticket manually                       │
│ 12:00 PM  Pings dev team on Slack                            │
│           ... repeat for next vulnerability ...              │
│ 5:00 PM   Triaged 15 out of 347 vulnerabilities            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Day 2-4: More Triage + Chase Dev Teams                      │
├──────────────────────────────────────────────────────────────┤
│           Continue manual triage (332 remaining)             │
│           Follow up with dev teams who haven't responded     │
│           Update Jira tickets                                │
│           Explain to developers why each issue matters       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Week 2: Remediation Tracking                                 │
├──────────────────────────────────────────────────────────────┤
│           Manually check which PRs were merged               │
│           Re-scan in Snyk to verify fixes                    │
│           Update Jira tickets                                │
│           Compile metrics for weekly report                  │
│           Build compliance evidence for auditors             │
└──────────────────────────────────────────────────────────────┘

Total Time: 40-60 hours per week per security engineer
```

### Agentic Workflow (With Agents)
```
┌──────────────────────────────────────────────────────────────┐
│ 8:32 AM: Automatic Triage (90 seconds)                      │
├──────────────────────────────────────────────────────────────┤
│ ✅ Agent triages all 347 vulnerabilities                     │
│ ✅ Agent enriches with EPSS, CISA KEV, asset metadata       │
│ ✅ Agent scores using composite risk model                   │
│ ✅ Agent creates 64 Jira tickets with full context          │
│ ✅ Agent notifies 12 dev teams on Slack                      │
│ ✅ Agent escalates 6 P0 issues to on-call                    │
│ ✅ Agent blocks deployments for critical assets              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 8:35-8:45 AM: Human Oversight (10 minutes)                  │
├──────────────────────────────────────────────────────────────┤
│ 👤 Security engineer reviews P0/P1 findings                  │
│ 👤 Approves 3 high-risk actions (PR blocks, deploy blocks)  │
│ 👤 Overrides 2 decisions (agent learns)                      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Hours-Days Later: Automatic Verification                     │
├──────────────────────────────────────────────────────────────┤
│ ✅ Agent monitors GitHub PRs for fixes                       │
│ ✅ Agent verifies deployments                                │
│ ✅ Agent re-scans to confirm vulnerabilities resolved        │
│ ✅ Agent updates Jira tickets                                │
│ ✅ Agent removes blocks automatically                        │
│ ✅ Agent notifies teams of completion                        │
│ ✅ Agent maintains audit trail                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Friday: One-Click Reporting                                  │
├──────────────────────────────────────────────────────────────┤
│ 👤 Security manager opens dashboard                          │
│ 👤 Reviews metrics (2 minutes)                               │
│ 👤 Exports compliance evidence (1 click)                     │
│ 👤 Done                                                       │
└──────────────────────────────────────────────────────────────┘

Total Time: 30-60 minutes per week per security engineer
```

**Productivity Gain: 95% reduction in manual work**

---

## Integration Touchpoints

### Where Users Interact with the Agent

#### 1. **Slack** (Primary Communication Channel)
- Receive critical alerts with context
- Approve high-risk actions via interactive buttons
- Get notifications when issues are resolved
- Weekly digest of security posture

#### 2. **Jira** (Work Tracking)
- Auto-created tickets with full context
- Rich descriptions with remediation steps
- Automatic status transitions
- Links to Snyk, GitHub, and audit logs

#### 3. **GitHub** (Code & PRs)
- PR comments with security impact analysis
- Status checks for blocked PRs
- Automatic PR updates when vulnerabilities are fixed
- Integration with branch protection rules

#### 4. **Snyk Dashboard** (Source of Truth)
- View original vulnerability findings
- See reachability analysis results
- Access detailed CVE information
- Link back from agent-created artifacts

#### 5. **Web Dashboard** (Reporting & Analytics)
- Weekly security posture reports
- Compliance evidence exports
- Override analysis and model training
- Team performance metrics

#### 6. **Email** (Backup Communication)
- Daily digest for P0/P1 issues
- Weekly summary for managers
- Compliance reports for auditors

---

## Key Experience Principles

### 1. **Context, Not Just Alerts**
❌ Bad: "CVE-2024-5678 detected"  
✅ Good: "Authentication bypass actively exploited in your PCI production asset serving 500k customers"

### 2. **Actionable Guidance**
❌ Bad: "Vulnerability found"  
✅ Good: "Run `npm install express@4.18.2` to fix (2 hour effort)"

### 3. **Explain the Decision**
❌ Bad: "Priority: P0"  
✅ Good: "P0 because: actively exploited + reachable + production + PCI-scoped"

### 4. **Close the Loop**
❌ Bad: *silence after fix*  
✅ Good: "✅ Verified fixed, blocks removed, ticket closed, compliance updated"

### 5. **Learn from Humans**
❌ Bad: Agent ignores overrides  
✅ Good: Agent captures rationale, retrains, improves over time

---

## Summary: The Agent as a Team Member

Users interact with the agent like a **highly efficient junior security engineer**:

- **Sarah (Security Engineer)** delegates triage to the agent, only reviews P0/P1
- **Mike (Developer)** receives clear, actionable security guidance without noise
- **Lisa (Security Manager)** gets executive visibility and audit-ready compliance

The agent handles the **toil** (enrichment, scoring, ticket creation, notification, tracking).  
Humans handle the **judgment** (approving high-risk actions, handling edge cases, policy tuning).

**The experience is:** "Security that accelerates development instead of blocking it."
