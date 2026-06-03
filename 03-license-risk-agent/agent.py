#!/usr/bin/env python3
"""
License Risk Agent - Snyk Open Source Integration
Policy-driven license compliance enforcement

Usage:
    python3 agent.py --demo                    # Run with demo license findings
    python3 agent.py --project PROJECT_ID      # Production mode
    python3 agent.py --demo --dry-run          # Show decisions without executing
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
import hashlib

# ============================================================================
# License Policy Configuration
# ============================================================================

LICENSE_POLICY = {
    "commercial_software": {
        "approved": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Apache-2.0", "Unlicense"],
        "permissive_with_attribution": ["Apache-2.0", "BSD-3-Clause"],
        "weak_copyleft": ["LGPL-2.1", "LGPL-3.0", "MPL-2.0"],
        "strong_copyleft": ["GPL-2.0", "GPL-3.0"],
        "network_copyleft": ["AGPL-3.0"],
        "blocked": ["AGPL-3.0", "GPL-2.0", "GPL-3.0", "SSPL", "Custom", "Proprietary"]
    },
    "open_source_software": {
        "approved": ["MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Apache-2.0", "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0"],
        "review_needed": ["AGPL-3.0"],
        "blocked": ["Proprietary", "Custom"]
    }
}

# ============================================================================
# 1. DETECT — Pull license findings from Snyk Open Source
# ============================================================================

def detect_license_issues(demo_mode=True, project_id=None):
    """Pull license findings from Snyk Open Source API or demo data"""
    if demo_mode:
        scenarios_path = Path(__file__).parent / "scenarios" / "snyk_license_findings.json"
        with open(scenarios_path) as f:
            findings = json.load(f)
        print(f"📥 Loaded {len(findings)} license findings from Snyk Open Source (demo mode)")
        return findings
    else:
        # Production: Call real Snyk API
        raise NotImplementedError("Production Snyk API integration requires SNYK_TOKEN")


# ============================================================================
# 2. CLASSIFY — Determine license risk based on policy
# ============================================================================

def classify_license(finding, project_type="commercial"):
    """Classify license finding based on organizational policy"""
    license_name = finding["license"]
    is_direct = finding["is_direct_dependency"]

    policy = LICENSE_POLICY.get(f"{project_type}_software", LICENSE_POLICY["commercial_software"])

    # Determine risk category
    if license_name in policy.get("blocked", []):
        risk_category = "BLOCKED"
        severity = "critical"
    elif license_name in policy.get("strong_copyleft", []):
        if is_direct:
            risk_category = "HIGH_RISK"
            severity = "high"
        else:
            risk_category = "REVIEW_NEEDED"
            severity = "medium"
    elif license_name in policy.get("weak_copyleft", []):
        risk_category = "REVIEW_NEEDED"
        severity = "medium"
    elif license_name in policy.get("permissive_with_attribution", []):
        risk_category = "APPROVED_WITH_ATTRIBUTION"
        severity = "low"
    elif license_name in policy.get("approved", []):
        risk_category = "APPROVED"
        severity = "info"
    elif license_name in ["Unknown", "NONE", ""]:
        risk_category = "BLOCKED"
        severity = "critical"
    else:
        risk_category = "REVIEW_NEEDED"
        severity = "medium"

    # Generate rationale
    rationale = generate_rationale(finding, risk_category, is_direct)

    return {
        "risk_category": risk_category,
        "severity": severity,
        "rationale": rationale,
        "requires_approval": risk_category in ["BLOCKED", "HIGH_RISK"]
    }


def generate_rationale(finding, risk_category, is_direct):
    """Generate human-readable rationale for license decision"""
    license_name = finding["license"]
    package = f"{finding['package_name']}@{finding['package_version']}"
    dependency_type = "direct dependency" if is_direct else "transitive dependency"

    rationales = {
        "BLOCKED": f"{license_name} license is blocked by policy. {package} ({dependency_type}) cannot be used in commercial software. Strong copyleft or proprietary license incompatible with our business model.",
        "HIGH_RISK": f"{license_name} license ({dependency_type}) requires source code disclosure. May be incompatible with proprietary code. Legal review required before use.",
        "REVIEW_NEEDED": f"{license_name} license has weak copyleft obligations. Review needed to ensure compliance with license terms, especially for {dependency_type}.",
        "APPROVED_WITH_ATTRIBUTION": f"{license_name} license approved but requires attribution. Add {package} to NOTICE file and ensure proper attribution in product.",
        "APPROVED": f"{license_name} license fully approved for use. No restrictions beyond basic attribution (if any)."
    }

    return rationales.get(risk_category, f"{license_name} license requires review.")


# ============================================================================
# 3. DECIDE — Determine actions based on classification
# ============================================================================

def decide_actions(finding, classification):
    """Decide what actions to take based on license classification"""
    risk_category = classification["risk_category"]
    severity = classification["severity"]

    actions_map = {
        "BLOCKED": [
            "block_pr_merge",
            "escalate_to_legal",
            "create_jira_compliance_p0",
            "notify_engineering_leadership",
            "suggest_alternatives"
        ],
        "HIGH_RISK": [
            "block_pr_merge",
            "request_legal_review",
            "create_jira_compliance_p1",
            "notify_team"
        ],
        "REVIEW_NEEDED": [
            "create_jira_compliance_p2",
            "request_review",
            "notify_team"
        ],
        "APPROVED_WITH_ATTRIBUTION": [
            "create_attribution_ticket",
            "add_to_notice_file",
            "log_for_compliance"
        ],
        "APPROVED": [
            "log_for_compliance"
        ]
    }

    return {
        "actions": actions_map.get(risk_category, ["log_for_compliance"]),
        "sla_days": get_sla_days(severity)
    }


def get_sla_days(severity):
    """Get SLA days based on severity"""
    sla_map = {
        "critical": 1,
        "high": 7,
        "medium": 30,
        "low": 90,
        "info": None
    }
    return sla_map.get(severity)


# ============================================================================
# 4. ACT — Execute actions
# ============================================================================

def execute_actions(finding, classification, decision, dry_run=False):
    """Execute policy enforcement actions"""
    executed = []

    for action in decision["actions"]:
        if dry_run:
            status = "DRY RUN"
        else:
            status = "EXECUTED"

        result = simulate_action(action, finding, classification, decision)

        executed.append({
            "action": action,
            "status": status,
            "result": result
        })

        print(f"   ✓ {action}: {result}")

    return executed


def simulate_action(action, finding, classification, decision):
    """Simulate action execution"""
    package = f"{finding['package_name']}@{finding['package_version']}"

    actions_simulation = {
        "block_pr_merge": f"Blocked PR via GitHub status check (License: {finding['license']})",
        "escalate_to_legal": f"Escalated to legal@company.com: {finding['license']} violation",
        "request_legal_review": f"Legal review requested for {package}",
        "create_jira_compliance_p0": f"Created Jira LICENSE-{hash_id(finding['id'])} (P0)",
        "create_jira_compliance_p1": f"Created Jira LICENSE-{hash_id(finding['id'])} (P1)",
        "create_jira_compliance_p2": f"Created Jira LICENSE-{hash_id(finding['id'])} (P2)",
        "notify_engineering_leadership": f"Notified engineering leadership on Slack",
        "notify_team": f"Notified team on Slack: #{finding.get('team', 'engineering')}",
        "suggest_alternatives": f"Suggested alternatives: {get_alternatives(finding['package_name'])}",
        "create_attribution_ticket": f"Created attribution ticket for NOTICE file (P3)",
        "add_to_notice_file": f"Queued for NOTICE file generation",
        "request_review": f"Requested review from compliance team",
        "log_for_compliance": f"Logged for compliance reporting"
    }

    return actions_simulation.get(action, f"Executed: {action}")


def get_alternatives(package_name):
    """Suggest alternative packages with compatible licenses"""
    # Simplified - in production would query package registries
    alternatives_db = {
        "redis-py": "valkey-py (BSD), redis-py@3.5.3 (BSD)",
        "readline": "prompt-toolkit (BSD)",
        "mysql-connector": "pymysql (MIT), mysql-connector-python-rf (MIT)"
    }
    return alternatives_db.get(package_name, "Contact legal for alternatives")


def hash_id(text):
    """Generate short hash for IDs"""
    return hashlib.sha256(text.encode()).hexdigest()[:6].upper()


# ============================================================================
# 5. LOG — Write immutable audit trail
# ============================================================================

def log_decision(finding, classification, decision, executed_actions, audit_path):
    """Write license decision to audit log"""
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": "license-risk-agent",
        "finding": {
            "package": f"{finding['package_name']}@{finding['package_version']}",
            "license": finding["license"],
            "is_direct": finding["is_direct_dependency"],
            "project": finding["project"]
        },
        "classification": classification,
        "decision": decision,
        "executed_actions": executed_actions
    }

    with open(audit_path, 'a') as f:
        f.write(json.dumps(audit_entry) + '\n')


# ============================================================================
# 6. GENERATE REPORTS
# ============================================================================

def generate_compliance_report(results, reports_dir):
    """Generate compliance report"""
    report_path = reports_dir / "license_decisions.txt"

    with open(report_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("LICENSE COMPLIANCE REPORT\n")
        f.write("=" * 70 + "\n\n")

        # Summary
        blocked = sum(1 for r in results if r["classification"]["risk_category"] == "BLOCKED")
        high_risk = sum(1 for r in results if r["classification"]["risk_category"] == "HIGH_RISK")
        review = sum(1 for r in results if r["classification"]["risk_category"] == "REVIEW_NEEDED")
        approved = sum(1 for r in results if r["classification"]["risk_category"] in ["APPROVED", "APPROVED_WITH_ATTRIBUTION"])

        f.write(f"Total Findings: {len(results)}\n")
        f.write(f"  ❌ Blocked: {blocked}\n")
        f.write(f"  ⚠️  High Risk: {high_risk}\n")
        f.write(f"  📋 Review Needed: {review}\n")
        f.write(f"  ✅ Approved: {approved}\n\n")

        # Detailed findings
        for result in results:
            finding = result["finding"]
            classification = result["classification"]
            decision = result["decision"]

            f.write("-" * 70 + "\n")
            f.write(f"Package: {finding['package_name']}@{finding['package_version']}\n")
            f.write(f"License: {finding['license']}\n")
            f.write(f"Risk: {classification['risk_category']} ({classification['severity']})\n")
            f.write(f"Type: {'Direct' if finding['is_direct_dependency'] else 'Transitive'}\n")
            f.write(f"\nRationale:\n{classification['rationale']}\n")
            f.write(f"\nActions: {', '.join(decision['actions'])}\n")
            if decision['sla_days']:
                f.write(f"SLA: Resolve within {decision['sla_days']} days\n")
            f.write("\n")

    print(f"\n📊 Compliance report generated: {report_path}")


# ============================================================================
# Main orchestration
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="License Risk Agent")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--project", help="Snyk project ID (production mode)")
    parser.add_argument("--project-type", default="commercial", choices=["commercial", "open_source"], help="Project type for policy")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve all actions")
    args = parser.parse_args()

    if not args.demo and not args.project:
        print("❌ Error: Specify --demo or --project PROJECT_ID")
        sys.exit(1)

    # Setup paths
    base_path = Path(__file__).parent
    audit_path = base_path / "audit" / "license_decisions.jsonl"
    reports_dir = base_path / "reports"
    audit_path.parent.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    print("⚖️  License Risk Agent Starting...")
    print(f"Policy Mode: {args.project_type.title()} Software")
    print("=" * 60)

    # 1. DETECT
    findings = detect_license_issues(demo_mode=args.demo, project_id=args.project)

    # Process each finding
    results = []

    for finding in findings:
        print(f"\n📌 Processing: {finding['package_name']}@{finding['package_version']}")
        print(f"   License: {finding['license']} ({'Direct' if finding['is_direct_dependency'] else 'Transitive'})")

        # 2. CLASSIFY
        classification = classify_license(finding, project_type=args.project_type)
        print(f"   Risk: {classification['risk_category']} ({classification['severity']})")

        # 3. DECIDE
        decision = decide_actions(finding, classification)

        # 4. ACT
        executed_actions = execute_actions(finding, classification, decision, dry_run=args.dry_run)

        # 5. LOG
        log_decision(finding, classification, decision, executed_actions, audit_path)

        results.append({
            "finding": finding,
            "classification": classification,
            "decision": decision,
            "executed_actions": executed_actions
        })

    # 6. GENERATE REPORTS
    generate_compliance_report(results, reports_dir)

    print("\n" + "=" * 60)
    print(f"✅ License compliance check complete! Processed {len(findings)} packages")
    print(f"📊 Report: {reports_dir}/license_decisions.txt")
    print(f"📝 Audit log: {audit_path}")


if __name__ == "__main__":
    main()
