# UI Mockups: Visual Interface Design

This document shows what users actually see when interacting with the agentic security system.

---

## 1. Slack Alert (Critical Vulnerability)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 Security Agent BOT  APP  8:32 AM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🚨 *P0 Critical Vulnerability Detected*                         │
│                                                                 │
│ *CVE-2024-5678: Authentication Bypass in express@4.16.0*       │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                 │
│ *Risk Score:* 94.72/100                                         │
│ *Priority:* 🔴 P0 Critical                                      │
│ *Asset:* payment-api-prod (PCI-scoped, production)             │
│ *Status:* 🔴 Actively Exploited (CISA KEV)                     │
│                                                                 │
│ *Why This Matters:*                                             │
│ • Active exploitation confirmed in the wild                     │
│ • Vulnerable code is reachable in authentication middleware     │
│ • Production asset handling payment card data                   │
│ • 500,000 customers impacted                                    │
│                                                                 │
│ *Actions Taken by Agent:*                                       │
│ ✅ Paged on-call engineer (Jessica)                             │
│ ✅ Created Jira ticket SEC-4A7B29 (P0)                          │
│ ✅ Blocked deployments for payment-api-prod                     │
│ ⏳ Awaiting approval to block PR merges                         │
│                                                                 │
│ *Remediation:* Upgrade to express@4.18.2 or apply patch        │
│                                                                 │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐    │
│ │ View in Snyk │ │ View Jira    │ │ ⚠️ Approve Block PR │    │
│ └──────────────┘ └──────────────┘ └──────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Slack Approval Request (Interactive)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 Security Agent BOT  APP  8:35 AM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ⚠️ *Approval Required*                                          │
│                                                                 │
│ *Action:* Block PR merges for payment-api-prod                  │
│ *Reason:* P0 Critical vulnerability (CVE-2024-5678)             │
│ *Impact:* Developers cannot merge PRs until vuln is fixed       │
│ *Requested by:* vulnerability-triage-agent                      │
│ *Risk Level:* 🟠 Medium (disruptive to development)             │
│                                                                 │
│ *Rationale:*                                                    │
│ Actively exploited vulnerability in production PCI asset.       │
│ Blocking merges prevents introducing new features while         │
│ critical security issue remains unpatched.                      │
│                                                                 │
│ ┌────────────────────┐ ┌─────────┐ ┌──────────────────┐        │
│ │ ✅ Approve & Execute│ │ ❌ Reject│ │ ⏸️ Defer 1 Hour  │        │
│ └────────────────────┘ └─────────┘ └──────────────────┘        │
│                                                                 │
│ _sarah@company.com can approve this action_                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**After approval:**
```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 Security Agent BOT  APP  8:40 AM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ✅ *Action Approved & Executed*                                 │
│                                                                 │
│ *Action:* Block PR merges for payment-api-prod                  │
│ *Approved by:* sarah@company.com                                │
│ *Approved at:* 8:40 AM                                          │
│                                                                 │
│ *Results:*                                                      │
│ ✅ GitHub branch protection rule added                          │
│ ✅ 3 open PRs marked with security block                        │
│ ✅ Payments team notified                                       │
│ ✅ Audit log updated                                            │
│                                                                 │
│ This action will auto-revert when CVE-2024-5678 is fixed.      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Jira Ticket (Auto-Generated)

```
┌──────────────────────────────────────────────────────────────────┐
│ SEC-4A7B29                                     🔴 P0 — In Progress │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ [P0] CVE-2024-5678: Authentication Bypass in express             │
│                                                                  │
│ Type: 🐛 Bug (Security Incident)                                 │
│ Priority: ⚫ P0 — Highest                                         │
│ Assignee: @jessica                                               │
│ Reporter: 🤖 security-agent (automated)                          │
│ Labels: security, p0, pci-scoped, auto-triaged, payments-team   │
│ Sprint: Security Sprint 2026-W23                                 │
│ SLA: ⏰ Fix within 24h (by June 2, 8:32 AM)                      │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ DESCRIPTION                                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ## 🔍 VULNERABILITY DETAILS                                      │
│                                                                  │
│ | Field | Value |                                                │
│ |-------|-------|                                                │
│ | Package | express@4.16.0 (direct dependency) |                │
│ | CVE | CVE-2024-5678 |                                          │
│ | CVSS | 6.5 (Medium) — _Agent scored as P0 Critical_ |          │
│ | Asset | payment-api-prod (Production, PCI-scoped) |            │
│ | Team | payments-team |                                         │
│                                                                  │
│ ## 📊 RISK ASSESSMENT (Automated)                                │
│                                                                  │
│ **Composite Risk Score: 94.72 / 100**                            │
│                                                                  │
│ ```                                                              │
│ Exploitability:     96.8  ████████████████████░ (40% weight)    │
│ Reachability:      100.0  ████████████████████  (30% weight)    │
│ Asset Criticality: 100.0  ████████████████████  (20% weight)    │
│ Business Impact:    60.0  ███████████░░░░░░░░░  (10% weight)    │
│ ```                                                              │
│                                                                  │
│ ## ⚠️ WHY THIS MATTERS                                           │
│                                                                  │
│ This vulnerability is being **actively exploited in the wild**   │
│ (confirmed by CISA KEV list). The vulnerable code is reachable   │
│ in your authentication middleware, meaning attackers can bypass  │
│ login and access customer payment data.                          │
│                                                                  │
│ **This is a PCI compliance violation.**                          │
│                                                                  │
│ ## 🔧 REMEDIATION                                                │
│                                                                  │
│ ### Step 1: Upgrade Package                                     │
│ ```bash                                                          │
│ cd services/payment-api                                          │
│ npm install express@4.18.2                                       │
│ ```                                                              │
│                                                                  │
│ ### Step 2: Test Locally                                        │
│ ```bash                                                          │
│ npm test                                                         │
│ npm run integration-test                                         │
│ ```                                                              │
│                                                                  │
│ ### Step 3: Deploy to Staging                                   │
│ ```bash                                                          │
│ kubectl apply -f k8s/staging/                                    │
│ curl https://staging.payment-api.company.com/health              │
│ ```                                                              │
│                                                                  │
│ ### Step 4: Deploy to Production                                │
│ ```bash                                                          │
│ kubectl apply -f k8s/production/                                 │
│ ```                                                              │
│                                                                  │
│ **Estimated Time:** 2 hours                                      │
│ **SLA:** Fix within 24 hours (by June 2, 8:32 AM)               │
│                                                                  │
│ ## 🎯 ACTIONS TAKEN BY AGENT                                     │
│                                                                  │
│ ✅ Paged on-call engineer (Jessica) via PagerDuty                │
│ ✅ Blocked deployments for payment-api-prod                      │
│ ✅ Blocked PR merges (approved by sarah@company.com at 8:40 AM)  │
│ ✅ Notified #payments-team on Slack                              │
│ ✅ Posted to #security-alerts                                    │
│                                                                  │
│ ## 🔗 LINKS                                                      │
│                                                                  │
│ • [View in Snyk](https://app.snyk.io/vuln/SNYK-JS-EXPRESS-...)  │
│ • [GitHub Repo](https://github.com/company/payment-api)          │
│ • [PagerDuty Incident](https://company.pagerduty.com/...)        │
│ • [Audit Trail](https://security-agent.company.com/audit/...)    │
│                                                                  │
│ ---                                                              │
│ 🤖 _This ticket was automatically created and triaged by the     │
│ vulnerability-triage-agent. The agent will monitor this issue    │
│ and update the ticket when the vulnerability is resolved._       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. GitHub PR Comment (Auto-Generated)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🤖 security-agent commented 2 hours ago                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ## 🤖 Security Agent — Vulnerability Remediation                 │
│                                                                  │
│ This PR addresses: **CVE-2024-5678 (P0 Critical)**              │
│                                                                  │
│ ### Security Impact                                              │
│ ✅ Fixes actively exploited authentication bypass                │
│ ✅ Resolves PCI compliance violation                             │
│ ✅ Protects 500k customer payment records                        │
│                                                                  │
│ ### Verification Checklist                                       │
│ - [x] Unit tests pass                                            │
│ - [x] Integration tests pass                                     │
│ - [x] Staging deployment successful                              │
│ - [x] Smoke tests pass on staging                                │
│ - [ ] Security team approval                                     │
│                                                                  │
│ ### Once Merged                                                  │
│ The agent will automatically:                                    │
│ ✅ Remove deployment block from payment-api-prod                 │
│ ✅ Remove PR merge block                                         │
│ ✅ Transition Jira ticket SEC-4A7B29 to "Resolved"               │
│ ✅ Update compliance dashboard                                   │
│ ✅ Notify security team                                          │
│                                                                  │
│ Agent will monitor this PR and verify fix in production.         │
│                                                                  │
│ /cc @sarah @jessica                                              │
│                                                                  │
│ ---                                                              │
│ 📊 [View Risk Analysis] • 🔍 [View Snyk Finding] • 📋 [View Jira]│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Web Dashboard (Weekly Report)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ Security Posture Dashboard                          Week of May 26 - Jun 1│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 VULNERABILITIES TRIAGED THIS WEEK                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  Total: 347 vulnerabilities across 45 projects                             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                                                                 │       │
│  │  P0 Critical    ⚫⚫⚫⚫⚫⚫  6                                     │       │
│  │  P1 High        🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴  11                        │       │
│  │  P2 Medium      🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠🟠  47                  │       │
│  │  P3 Low         🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡  89                  │       │
│  │  P4 Info        ⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪  194                       │       │
│  │                                                                 │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│  📈 RESOLUTION STATUS                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │  Fixed           ████████████████████░░░░░░░░  68%             │       │
│  │  In Progress     ███████░░░░░░░░░░░░░░░░░░░░░  22%             │       │
│  │  Scheduled       ██░░░░░░░░░░░░░░░░░░░░░░░░░░   8%             │       │
│  │  Risk Accepted   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2%             │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│  ⏱️ MEAN TIME TO REMEDIATION                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  P0 Critical:   3.2 hours   (SLA: 24h)   ✅  █████████████████████░        │
│  P1 High:       2.1 days    (SLA: 7d)    ✅  █████████████████████░        │
│  P2 Medium:     12.4 days   (SLA: 30d)   ✅  ██████████░░░░░░░░░░░        │
│  P3 Low:        45.2 days   (SLA: 90d)   ✅  ██████████░░░░░░░░░░░        │
│                                                                             │
│  🤖 AGENT AUTOMATION METRICS                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  Auto-Triaged:        347 / 347   (100%) ✅                                │
│  Auto-Actions:        823 / 847   (97%)  ✅                                │
│  Human Approvals:     24  / 847   (3%)   ✅                                │
│  False Positives:     4   / 347   (1.2%) ✅                                │
│  Human Overrides:     7   / 347   (2.0%) ⚠️                                │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │ Agent Autonomy Rate:  97%  ██████████████████████████████░░      │      │
│  │                                                                  │      │
│  │ This means 97% of actions were auto-executed.                   │      │
│  │ Only 3% required human approval. Trending ↑                     │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ✅ COMPLIANCE STATUS                                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  PCI-DSS Req 6.2     ✅ Compliant    All vulns in PCI assets triaged      │
│  SOC 2 CC7.1         ✅ Compliant    Change control audit trail complete   │
│  DORA (EU)           ✅ Compliant    Incident response <15 min             │
│  NYDFS Part 500      ✅ Compliant    Cybersecurity events tracked          │
│                                                                             │
│  📋 Audit Trail: All 347 decisions logged with full rationale              │
│     Ready for audit review                                                 │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │ [📥 Export Audit Report] [📊 Download Compliance Evidence] │             │
│  └───────────────────────────────────────────────────────────┘             │
│                                                                             │
│  🏆 TOP TEAMS BY REMEDIATION SPEED                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  1. payments-team      2.1 hour avg MTTR   ⭐⭐⭐                           │
│  2. platform-team      4.7 hour avg MTTR   ⭐⭐                             │
│  3. frontend-team      8.3 hour avg MTTR   ⭐                               │
│                                                                             │
│  ⚠️ AREAS NEEDING ATTENTION                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                                             │
│  ⚠️ 7 human overrides this week (up from 3 last week)                      │
│     → Review override rationale and retrain model                          │
│                                                                             │
│  ⚠️ legacy-services has 12 P2 issues >30 days old                          │
│     → Schedule remediation sprint with legacy team                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │ [🔍 View Override Analysis] [📅 Schedule Sprint Meeting]  │             │
│  └───────────────────────────────────────────────────────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Email Digest (Daily Summary for Managers)

```
From: Security Agent <security-agent@company.com>
To: Lisa Chen <lisa@company.com>
Subject: Daily Security Digest — June 1, 2026
Date: June 1, 2026 6:00 PM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAILY SECURITY DIGEST
June 1, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

47 new vulnerabilities detected and triaged today
3 P0 Critical issues escalated and in progress
68% of P1 issues from this week already fixed
All SLAs met ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 P0 CRITICAL ISSUES (REQUIRE IMMEDIATE ATTENTION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CVE-2024-5678: Authentication Bypass in express
   Asset: payment-api-prod (PCI-scoped)
   Status: 🟡 In Progress (Fix PR created by Mike, under review)
   Time Remaining: 21 hours until SLA breach
   [View Jira SEC-4A7B29]

2. CVE-2024-4567: Buffer Overflow in nginx
   Asset: web-frontend-prod
   Status: 🟢 Resolved (Deployed 2 hours ago)
   Time to Fix: 4.2 hours
   [View Jira SEC-8F3A11]

3. CVE-2021-44228: Log4Shell in legacy Java service
   Asset: legacy-java-service-prod
   Status: 🔴 Blocked (Legacy team capacity constrained)
   Time Remaining: 18 hours until SLA breach
   Action Needed: Escalate to VP Engineering
   [View Jira SEC-9D2C45]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 TODAY'S METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Vulnerabilities Triaged:    47
Auto-Actions Executed:      112
Human Approvals Required:   3
Mean Time to Triage:        1.8 seconds
Mean Time to Remediation:   3.7 hours (P0/P1 only)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ WINS TODAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• payments-team fixed P0 nginx vulnerability in 4.2 hours ⭐
• Zero SLA breaches today
• Agent autonomy rate: 97% (3% required human approval)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ATTENTION NEEDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Log4Shell issue in legacy-services at risk of SLA breach
  → Recommend escalating to VP Engineering for emergency sprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[View Full Dashboard] [Export Audit Report] [Schedule Review]

This is an automated email from the Security Agent.
Reply to security-team@company.com with questions.
```

---

## Key UI/UX Principles Demonstrated

### 1. **Progressive Disclosure**
- Slack alerts show summary → Click for full detail in Jira/Dashboard
- Users see what they need at each level

### 2. **Contextual Actions**
- Every notification has relevant action buttons
- "View in Snyk", "Approve Action", "View Jira" are one-click

### 3. **Visual Hierarchy**
- Emojis and color coding (🔴 P0, 🟠 P2) for instant recognition
- Progress bars and charts for quick scanning

### 4. **Explain the Decision**
- Every priority includes rationale ("actively exploited + reachable + PCI")
- Users understand *why* the agent made this choice

### 5. **Close the Loop**
- Success messages when issues are resolved
- Users see the full lifecycle, not just the alert

### 6. **Audit Trail Transparency**
- "Approved by sarah@company.com at 8:40 AM"
- Every action is attributable and reviewable

---

## Implementation Notes

### Slack Integration
- Uses Slack Block Kit for rich formatting
- Interactive buttons via Slack's Interactivity API
- Real-time updates to existing messages (no spam)

### Jira Integration
- Uses Jira REST API for ticket creation
- Custom fields for risk scores and agent metadata
- Automatic transitions based on GitHub events

### GitHub Integration
- Uses GitHub Actions for deployment tracking
- GitHub Apps API for PR comments and status checks
- Webhook listeners for real-time events

### Web Dashboard
- React + Tailwind CSS for responsive design
- Real-time updates via WebSocket
- Chart.js for visualizations
- Export buttons generate PDF/CSV on-demand

These mockups show **exactly** what users experience, making the agentic security system tangible and actionable.
