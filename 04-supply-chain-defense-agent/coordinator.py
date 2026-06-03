#!/usr/bin/env python3
"""
Supply Chain Defense Coordinator
Multi-agent system coordinating specialist agents to detect malicious packages

Usage:
    python3 coordinator.py --demo                # Run with demo packages
    python3 coordinator.py --project PROJECT_ID  # Production mode
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Import specialist agents
sys.path.append(str(Path(__file__).parent))
from agents import malicious_code_detector, typosquat_analyzer, reputation_analyzer

# ============================================================================
# 1. DETECT — Get new/suspicious packages
# ============================================================================

def detect_suspicious_packages(demo_mode=True, project_id=None):
    """Load suspicious packages from Snyk or demo data"""
    if demo_mode:
        scenarios_path = Path(__file__).parent / "scenarios" / "suspicious_packages.json"
        with open(scenarios_path) as f:
            packages = json.load(f)
        print(f"📥 Loaded {len(packages)} packages for analysis (demo mode)")
        return packages
    else:
        raise NotImplementedError("Production Snyk API integration requires SNYK_TOKEN")


# ============================================================================
# 2. COORDINATE — Run specialist agents in parallel
# ============================================================================

def coordinate_analysis(package):
    """Coordinate all specialist agents to analyze package"""
    print(f"\n🔍 Analyzing: {package['name']}@{package['version']}")

    # Run specialist agents
    malicious_result = malicious_code_detector.analyze(package)
    typosquat_result = typosquat_analyzer.analyze(package)
    reputation_result = reputation_analyzer.analyze(package)

    # Display individual findings
    print(f"   Malicious Code Score: {malicious_result['score']}/100 ({malicious_result['confidence']})")
    print(f"   Typosquat Score: {typosquat_result['score']}/100 ({typosquat_result['confidence']})")
    print(f"   Reputation Score: {reputation_result['score']}/100 ({reputation_result['confidence']})")

    return {
        "malicious_code": malicious_result,
        "typosquat": typosquat_result,
        "reputation": reputation_result
    }


# ============================================================================
# 3. SYNTHESIZE — Combine findings with weighted confidence
# ============================================================================

def synthesize_verdict(package, analyses):
    """Synthesize findings from all specialist agents"""
    # Confidence-weighted scoring
    confidence_score = (
        analyses["malicious_code"]["score"] * 0.5 +
        analyses["typosquat"]["score"] * 0.3 +
        analyses["reputation"]["score"] * 0.2
    )

    # Determine verdict
    if confidence_score >= 90:
        verdict = "MALICIOUS"
        actions = ["auto_block", "create_incident", "notify_security_immediate"]
    elif confidence_score >= 70:
        verdict = "SUSPICIOUS"
        actions = ["block_pending_review", "notify_security", "create_ticket"]
    elif confidence_score >= 40:
        verdict = "MONITOR"
        actions = ["flag_for_monitoring", "notify_security"]
    else:
        verdict = "BENIGN"
        actions = ["log_only"]

    # Generate combined rationale
    rationale = generate_rationale(package, analyses, verdict, confidence_score)

    return {
        "verdict": verdict,
        "confidence_score": round(confidence_score, 2),
        "actions": actions,
        "rationale": rationale
    }


def generate_rationale(package, analyses, verdict, confidence_score):
    """Generate human-readable rationale combining all signals"""
    signals = []

    # Collect high-confidence signals
    if analyses["malicious_code"]["score"] >= 50:
        signals.extend(analyses["malicious_code"]["indicators"])

    if analyses["typosquat"]["score"] >= 50:
        signals.extend(analyses["typosquat"]["indicators"])

    if analyses["reputation"]["score"] <= 30:  # Low reputation is bad
        signals.extend(analyses["reputation"]["indicators"])

    if not signals:
        return f"{verdict}: No significant risk indicators detected. Confidence: {confidence_score:.1f}"

    signals_text = "\n  • ".join(signals[:5])  # Top 5 signals
    return f"{verdict} (Confidence: {confidence_score:.1f})\n  • {signals_text}"


# ============================================================================
# 4. EXECUTE — Take coordinated action
# ============================================================================

def execute_actions(package, verdict_data, dry_run=False):
    """Execute coordinated actions based on verdict"""
    executed = []

    for action in verdict_data["actions"]:
        if dry_run:
            status = "DRY RUN"
        else:
            status = "EXECUTED"

        result = simulate_action(action, package, verdict_data)

        executed.append({
            "action": action,
            "status": status,
            "result": result
        })

        print(f"   ✓ {action}: {result}")

    return executed


def simulate_action(action, package, verdict_data):
    """Simulate action execution"""
    pkg = f"{package['name']}@{package['version']}"

    actions_simulation = {
        "auto_block": f"Blocked {pkg} via GitHub/GitLab status check",
        "block_pending_review": f"Blocked {pkg} pending manual security review",
        "create_incident": f"Created P0 incident SEC-{hash(pkg) % 10000:04d}",
        "create_ticket": f"Created security review ticket SEC-{hash(pkg) % 10000:04d}",
        "notify_security_immediate": f"Paged security on-call via PagerDuty",
        "notify_security": f"Posted to #security-alerts on Slack",
        "flag_for_monitoring": f"Added to security monitoring watchlist",
        "log_only": f"Logged to audit trail for compliance"
    }

    return actions_simulation.get(action, f"Executed: {action}")


# ============================================================================
# 5. LOG — Audit trail
# ============================================================================

def log_analysis(package, analyses, verdict_data, executed_actions, audit_path):
    """Write coordinated decision to audit log"""
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "coordinator": "supply-chain-defense",
        "package": {
            "name": package["name"],
            "version": package["version"],
            "registry": package.get("registry", "npm")
        },
        "specialist_analyses": analyses,
        "verdict": verdict_data,
        "executed_actions": executed_actions
    }

    with open(audit_path, 'a') as f:
        f.write(json.dumps(audit_entry) + '\n')


# ============================================================================
# 6. REPORT — Generate coordination report
# ============================================================================

def generate_report(results, reports_dir):
    """Generate multi-agent coordination report"""
    report_path = reports_dir / "coordinator_decisions.json"

    with open(report_path, 'w') as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_packages": len(results),
            "verdicts": {
                "malicious": sum(1 for r in results if r["verdict_data"]["verdict"] == "MALICIOUS"),
                "suspicious": sum(1 for r in results if r["verdict_data"]["verdict"] == "SUSPICIOUS"),
                "monitor": sum(1 for r in results if r["verdict_data"]["verdict"] == "MONITOR"),
                "benign": sum(1 for r in results if r["verdict_data"]["verdict"] == "BENIGN")
            },
            "analyses": results
        }, f, indent=2)

    print(f"\n📊 Coordination report: {report_path}")


# ============================================================================
# Main orchestration
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Supply Chain Defense Coordinator")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--project", help="Snyk project ID (production mode)")
    parser.add_argument("--dry-run", action="store_true", help="Show decisions without executing")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve all actions")
    args = parser.parse_args()

    if not args.demo and not args.project:
        print("❌ Error: Specify --demo or --project PROJECT_ID")
        sys.exit(1)

    # Setup paths
    base_path = Path(__file__).parent
    audit_path = base_path / "audit" / "coordinator_log.jsonl"
    reports_dir = base_path / "reports"
    audit_path.parent.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    print("🛡️ Supply Chain Defense Coordinator Starting...")
    print("=" * 60)

    # 1. DETECT
    packages = detect_suspicious_packages(demo_mode=args.demo, project_id=args.project)

    # Process each package through multi-agent pipeline
    results = []

    for package in packages:
        # 2. COORDINATE specialist agents
        analyses = coordinate_analysis(package)

        # 3. SYNTHESIZE findings
        verdict_data = synthesize_verdict(package, analyses)
        print(f"   Verdict: {verdict_data['verdict']} (Confidence: {verdict_data['confidence_score']})")

        # 4. EXECUTE coordinated actions
        executed_actions = execute_actions(package, verdict_data, dry_run=args.dry_run)

        # 5. LOG
        log_analysis(package, analyses, verdict_data, executed_actions, audit_path)

        results.append({
            "package": package,
            "analyses": analyses,
            "verdict_data": verdict_data,
            "executed_actions": executed_actions
        })

    # 6. REPORT
    generate_report(results, reports_dir)

    print("\n" + "=" * 60)
    print(f"✅ Multi-agent analysis complete! Processed {len(packages)} packages")
    print(f"📝 Audit log: {audit_path}")


if __name__ == "__main__":
    main()
