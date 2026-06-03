# Agentic AppSec POC — Meeting One-Pager

**Meeting with:** Sergey Gerasimenko  
**Date:** June 3, 2026  
**Project:** [github.com/mkuriel1984/snyk-agentic-appsec-poc](https://github.com/mkuriel1984/snyk-agentic-appsec-poc)

---

## 30-Second Pitch

**The Problem:** Snyk customers have 10,000+ security findings. Manual triage doesn't scale. Detection is commoditized.

**The Solution:** Autonomous agents that **auto-remediate 90% of findings** with human oversight on the critical 10%. Transforms Snyk from "find vulnerabilities" to "fix vulnerabilities autonomously."

**The Opportunity:** First-mover on AI-native remediation automation. $10M ARR potential by EOY 2027.

---

## What the POC Demonstrates

### 4 Autonomous Agents

1. **Vulnerability Triage Agent** → ML-powered risk scoring (exploitability × reachability × asset criticality)
2. **Secrets Remediation Agent** → Auto-vaults secrets + creates PR with remediation code
3. **License Risk Agent** → Policy-driven compliance (auto-blocks GPL, requests approval for LGPL)
4. **Supply Chain Defense Agent** → Multi-agent coordinator detects malicious packages (typosquatting, crypto miners)

### Architecture: **Detect → Decide → Act → Log**

**Tiered Autonomy:**
- Tier 1 (Auto): Create ticket, add PR comment → no approval
- Tier 2 (Approval): Block PR, revoke key → human approval required
- Tier 3 (Advisory): Emergency patches → agent recommends, human decides

**Audit-First:** Immutable logs, policy versioning, regulatory mapping (PCI-DSS, GDPR, DORA, SOC 2)

---

## Strategic Value to Snyk

### 1. Differentiation
**Detection is commoditized. Remediation automation is the moat.**

Snyk's unique advantage: 10+ years of vulnerability data + reachability analysis + customer trust

### 2. Product Strategy Alignment

| **Product** | **How Agents Amplify** |
|-------------|------------------------|
| **Snyk Issues** | ML-powered composite risk scoring, auto-routing, remediation tracking |
| **Snyk Evo** | **Natural home for agents** — evolve from workflow automation to agent orchestration platform |
| **Asset Management** | Agent risk scoring incorporates asset criticality (production, PCI-scoped, revenue-critical) |
| **Developer UX** | Reduce noise, reduce toil, auto-generate fix PRs |

### 3. Business Impact

**Customer ROI:**
- 10x productivity (security teams manage 10x more apps without 10x headcount)
- 90% auto-triage rate within 5 minutes
- Mean-time-to-fix: weeks → hours
- Audit-ready compliance (SOC 2, PCI-DSS, DORA artifacts on demand)

**Snyk Revenue:**
- **Expansion:** $50k-$200k/year add-on per 100 apps
- **Retention:** High switching cost once agents adopted
- **Enterprise unlock:** Compliance artifacts unlock FSI, healthcare, regulated industries

---

## Market Opportunity: Why Now?

### 3 Converging Trends

1. **GPT-5.5-Cyber class models** → Reasoning + code generation crossed production threshold
2. **Regulatory pressure** → DORA, NYDFS, PCI-DSS 4.0 mandate automation with audit trails
3. **Toolchain consolidation** → GitHub/GitLab platforms winning, Snyk already integrated

**The window:** 2026-2027 before competitors catch up

---

## Competitive Differentiation

| **vs. Traditional SAST/DAST** | **vs. Cloud Security** | **vs. AI Startups** |
|--------------------------------|------------------------|---------------------|
| They detect → We auto-remediate | They notify security → We act on developer workflows | They lack distribution → We're in 1,000+ CI/CD pipelines |
| They generate reports → We create PRs | They focus on cloud → We cover full SDLC | They start from scratch → We have 10 years of data + trust |

---

## Go-to-Market

### 3 Tiers

1. **Enterprise Security Teams** (FSI, healthcare) → "Auto-triage + audit-ready compliance" → $50k-$200k/year
2. **Platform Engineering** (tech companies, >100:1 dev:sec ratio) → "10x scale without 10x headcount" → $100k-$500k/year
3. **Developers** (startups, scale-ups) → "Reduce security toil" → Freemium → upsell

---

## Path to Production

| **Timeline** | **Milestone** |
|--------------|---------------|
| **Q3 2026** | Deploy to 5 design partners, measure metrics (triage rate, false positives, dev satisfaction) |
| **Q4 2026** | Snyk Issues + Evo integration, pilot with 20 customers (10 FSI, 10 tech) |
| **Q1 2027** | GA launch at Snyk Summit 2027 → **Target: $10M ARR by EOY 2027** |
| **Q2-Q4 2027** | Expand agent portfolio (auto-remediation, threat intel fusion, compliance) |

---

## Next Steps

**Today's Goal:** Align on strategic fit with your current work and explore integration opportunities.

**Questions to Discuss:**
1. Where do you see overlap with your business goals?
2. What's the right home for this work? (Issues? Evo? New product line?)
3. What would a Q3 pilot look like with design partner customers?

---

**Full details:** `EXECUTIVE_BRIEF.md` in the repo  
**GitHub:** [github.com/mkuriel1984/snyk-agentic-appsec-poc](https://github.com/mkuriel1984/snyk-agentic-appsec-poc)
