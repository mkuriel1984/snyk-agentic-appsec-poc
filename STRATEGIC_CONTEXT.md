# Strategic Context: Agentic AppSec at Snyk

## Vision Alignment

This POC demonstrates how Snyk can evolve from a **detection platform** to an **autonomous defense platform** — enabling customers to move from "finding vulnerabilities" to "auto-remediating vulnerabilities with human oversight."

## The Strategic Opportunity

### Market Context

The AppSec market is at an inflection point:
- **Detection is commoditized** — Every vendor finds vulnerabilities. Differentiation comes from what happens next.
- **Security teams are overwhelmed** — 10,000+ findings per enterprise, <5% remediated within SLA
- **AI is shifting from detection to action** — GPT-5.5-Cyber class models enable reasoning about security context, not just pattern matching
- **Regulatory pressure is increasing** — DORA, NYDFS Part 500, EU AI Act require demonstrable automated controls with audit trails

### Snyk's Positioning

Snyk has unique advantages for agentic security:
1. **Developer workflow integration** — Already embedded in IDE, CI/CD, SCM where remediation happens
2. **Comprehensive context** — Vulnerability + reachability + code + dependencies in one platform
3. **Trusted brand** — Developers already trust Snyk's findings; they'll trust Snyk's agents
4. **Ecosystem position** — Integrates with Jira, Slack, GitHub, GitLab — agents can orchestrate end-to-end

### The Gap

Current state: Snyk tells developers **what is wrong**.  
Desired state: Snyk agents **fix what is wrong** with developer approval.

This POC bridges that gap.

## How This Connects to Snyk's Product Strategy

### 1. Snyk Issues (Phase 1 Accelerant)

The **Issues** product provides unified prioritization across vulnerability, license, code quality, and secrets findings. Agentic triage agents amplify this by:
- **Scoring** — ML-powered composite risk scores (exploitability × reachability × asset criticality × business impact)
- **Routing** — Auto-assigning issues to the right teams with context
- **Tracking** — Monitoring remediation progress and escalating overdue items

**Integration point:** Agents consume Issues API, enrich with additional context (threat intel, asset metadata), and write back actions/decisions.

### 2. Snyk Code (Developer Experience Focus)

Snyk Code scans show secrets, code quality issues, and security flaws. Agents make these findings actionable:
- **Secrets Agent** — Auto-vaults secrets, creates PR with remediation code, notifies security
- **Code Quality Agent** (future) — Auto-applies safe refactorings, suggests patterns
- **IaC Misconfig Agent** (future) — Auto-fixes common Terraform/CloudFormation mistakes

**Integration point:** Agents act on Snyk Code findings, generate PRs with fixes, developer reviews and merges.

### 3. Snyk Open Source + Container (Scale Challenge)

Customers have 10,000+ dependency vulnerabilities. Manual triage doesn't scale. Agents solve this:
- **Triage Agent** — Auto-prioritizes based on exploit availability, reachability, asset context
- **Remediation Agent** (future) — Auto-generates PRs with version upgrades, backports, patches
- **Dependency Health Agent** (future) — Monitors for malicious packages, abandoned projects, supply chain risks

**Integration point:** Agents consume Snyk's vulnerability data + reachability analysis, apply ML scoring, execute remediation workflows.

### 4. Snyk Evo (Orchestration Layer)

**Evo is the natural home for agentic workflows.** It already orchestrates across Snyk products and external tools (Jira, Slack, GitHub). Agents extend Evo's capabilities:
- **Policy-driven workflows** — "When critical vulnerability in production, auto-create P1 incident + notify on-call + block deployments"
- **Cross-product intelligence** — "If vulnerability has no reachability analysis, deprioritize; if reachable in prod asset with secrets exposed, escalate"
- **Human-in-the-loop approvals** — Evo UI shows agent recommendations, security team approves/rejects, feedback trains models

**Strategic thesis:** Evo evolves from workflow automation tool to **agent orchestration platform**.

### 5. Snyk Asset Management (Asset Context Layer)

Snyk Asset Management provides asset criticality data (production vs dev, customer-facing vs internal, compliance scope). Agents need this context:
- **Asset criticality** — Vulnerability in PCI-scoped production asset → Critical priority
- **Business impact** — Issue in revenue-critical service → Escalate to exec team
- **Team mapping** — Auto-route findings to owning teams based on Snyk Asset Management's service catalog

**Integration point:** Agents query Snyk Asset Management API for asset metadata, incorporate into risk scoring and routing decisions.

## Agentic AppSec Roadmap (9 Milestones)

This POC demonstrates **Milestones 1-3**. Full roadmap:

### Phase 1: Foundation (0-6 months)
**Milestone 1: Intelligent Triage**  
✅ Demonstrated in this POC — Vulnerability Triage Agent

**Milestone 2: Secrets Auto-Remediation**  
✅ Demonstrated in this POC — Secrets Remediation Agent

**Milestone 3: Policy-Driven Compliance**  
✅ Demonstrated in this POC — License Risk Agent

### Phase 2: Multi-Agent Coordination (6-12 months)
**Milestone 4: Supply Chain Defense**  
✅ Demonstrated in this POC — Multi-agent coordinator for malicious package detection

**Milestone 5: Cross-Product Risk Scoring**  
Unified risk model across Open Source, Code, Container, IaC findings. Agent synthesizes signals from all products.

**Milestone 6: Auto-Remediation with Verification**  
Agent generates fix PR, runs tests, verifies vulnerability is resolved, auto-merges if safe.

### Phase 3: Full Autonomy (12-18 months)
**Milestone 7: Self-Healing Pipelines**  
Agent detects vulnerability in deployed app, generates fix, tests in staging, deploys to production with rollback capability.

**Milestone 8: Threat Intel Fusion**  
Agent monitors threat feeds (CISA KEV, exploit-db, dark web), correlates with Snyk findings, auto-escalates active exploitation.

**Milestone 9: Compliance-as-Code**  
Agent maintains audit artifacts, generates compliance reports (SOC 2, PCI-DSS evidence), alerts on control gaps.

## Competitive Differentiation

### vs. Traditional SAST/DAST Vendors (Checkmarx, Veracode, Fortify)
- **They detect flaws. We auto-remediate with developer approval.**
- **They generate reports. Our agents create PRs with fixes.**
- **They require security experts to triage. Our agents do it autonomously.**

### vs. Cloud Security Vendors (Wiz, Orca, Lacework)
- **They focus on cloud misconfigurations. We cover the full SDLC (code, dependencies, containers, IaC).**
- **They notify security teams. Our agents act on developer workflows (GitHub, Jira, IDE).**

### vs. AI-Native Startups
- **They start from scratch. We have 10+ years of vulnerability data, reachability analysis, and customer trust.**
- **They lack distribution. We're already in 1,000+ enterprises' CI/CD pipelines.**
- **They treat AI as a product feature. We're architecting AI as the orchestration layer (Evo as agent platform).**

## Why Now?

Three converging trends make 2026-2027 the right window:

### 1. GPT-5.5-Cyber Class Models
- **Reasoning capability** — Models can understand security context (CVSS vs EPSS, reachability, asset criticality)
- **Code generation** — Fix quality is production-ready, not just PoC demos
- **Reliability** — Structured outputs (JSON mode) enable deterministic agent workflows

### 2. Developer Toolchain Consolidation
- **Platform plays winning** — GitHub/GitLab absorbing CI/CD, issue tracking, security scanning
- **Snyk already integrated** — Native GitHub/GitLab apps give us access to act, not just notify

### 3. Regulatory Pressure (DORA, EU AI Act, NYDFS)
- **Automation is expected** — "We manually review findings" no longer acceptable for regulated industries
- **Audit trails required** — Compliance teams need machine-readable evidence of controls
- **Human oversight mandated** — Fits perfectly with tiered autonomy architecture

## Customer Value Proposition

### For Security Teams
- **10x productivity** — Agents triage 90% of findings, humans focus on the critical 10%
- **Faster remediation** — Auto-generated PRs reduce mean-time-to-fix from weeks to hours
- **Audit readiness** — Immutable logs + policy versioning = compliance artifacts on demand

### For Developers
- **Less noise** — Only see high-priority, actionable findings with clear fix guidance
- **Faster shipping** — Agents handle security toil (vault secrets, upgrade dependencies, fix licenses)
- **Better defaults** — Agents suggest secure patterns based on org's best practices

### For Executives
- **Risk visibility** — Real-time dashboards show auto-remediated vs overdue vs accepted risk
- **Cost reduction** — Security headcount scales sublinearly with application portfolio growth
- **Competitive advantage** — Ship faster without sacrificing security posture

## Success Metrics

### Phase 1 (Triage + Secrets)
- **90% of vulnerabilities auto-triaged** within 5 minutes of discovery
- **50% of secrets auto-vaulted** with zero developer friction
- **<5% false positive rate** on agent decisions (human override)

### Phase 2 (Multi-Agent + Remediation)
- **70% of critical vulnerabilities auto-remediated** with fix PRs
- **10x reduction in mean-time-to-fix** for reachable vulnerabilities
- **100% audit trail completeness** for regulated customers

### Phase 3 (Full Autonomy)
- **Self-healing for 80% of vulnerabilities** (detect → fix → verify → deploy)
- **Zero-touch compliance** — Auto-generated SOC 2, PCI-DSS evidence artifacts
- **Proactive defense** — Agents respond to threat intel faster than human SOC teams

## Go-to-Market Motion

### Tier 1: Enterprise Security Teams (Early Adopters)
**Target:** FSI, healthcare, regulated industries with dedicated AppSec teams  
**Pitch:** "Automate 90% of vulnerability triage and achieve audit-ready compliance"  
**Pricing:** Add-on to Snyk Enterprise ($50k-$200k/year per 100 apps)

### Tier 2: Platform Engineering Teams (Efficiency Play)
**Target:** Tech companies with high developer:security ratios (>100:1)  
**Pitch:** "Your security team can manage 10x more apps without more headcount"  
**Pricing:** Bundled with Snyk Asset Management ($100k-$500k/year)

### Tier 3: Developers (Friction Reduction)
**Target:** Startups, scale-ups prioritizing shipping velocity  
**Pitch:** "Stop context-switching for security alerts — agents handle the toil"  
**Pricing:** Freemium tier with basic agents (secrets, license), upsell to advanced (triage, remediation)

## Risks & Mitigations

### Risk 1: Agents make mistakes (false positives, wrong fixes)
**Mitigation:**
- Tiered autonomy — High-risk actions require human approval
- Gradual rollout — Start with read-only recommendations, earn autonomy through accuracy
- Override feedback loop — Train models on human corrections

### Risk 2: Customers fear loss of control
**Mitigation:**
- Policy-first design — Customers configure thresholds, approval workflows
- Explainable decisions — Every agent action includes rationale visible in audit log
- Kill switch — Customers can disable agents per-team or per-project

### Risk 3: Regulatory scrutiny (EU AI Act "high-risk" classification)
**Mitigation:**
- Human-in-the-loop by design — Critical actions always require approval
- Audit trail completeness — Regulatory-grade evidence from day 1
- Alignment with GDPR Article 22 — "Meaningful human oversight" built into architecture

### Risk 4: Developer adoption friction
**Mitigation:**
- Solve pain, don't create work — Agents reduce developer toil, not add process
- Progressive enhancement — Works alongside existing workflows (Jira, GitHub, Slack)
- Show, don't tell — Pilot with 5 teams, prove ROI, scale org-wide

## Next Steps for Productization

### Q3 2026: Technical Proof Points
- [ ] Deploy POC to 5 Snyk design partner customers
- [ ] Measure: triage throughput, auto-action rate, false positive rate, developer satisfaction
- [ ] Iterate on policy models based on real-world feedback

### Q4 2026: Snyk Issues + Evo Integration
- [ ] Integrate agents with Snyk Issues API for unified prioritization
- [ ] Build Evo workflow designer for agent orchestration
- [ ] Pilot with 20 customers (10 FSI, 10 tech companies)

### Q1 2027: GA Launch
- [ ] Full product launch at Snyk Summit 2027
- [ ] Launch tiers: Enterprise Add-On, Asset Management Bundle, Developer Freemium
- [ ] Target: $10M ARR from agentic workflows by EOY 2027

### Q2-Q4 2027: Expand Agent Portfolio
- [ ] Auto-remediation agent (generates fix PRs)
- [ ] Threat intel fusion agent (correlates CVEs with active exploits)
- [ ] Compliance agent (auto-generates audit artifacts)

---

**This POC is the foundation. The strategic opportunity is transforming Snyk from "find vulnerabilities" to "fix vulnerabilities autonomously with human oversight."**

**The window is now. GPT-5.5-Cyber enables the reasoning. DORA mandates the automation. Snyk has the distribution and trust.**

**Let's build the future of autonomous AppSec.**
