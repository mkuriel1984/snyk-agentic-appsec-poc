#!/usr/bin/env python3
"""
Secrets Remediation Agent - Snyk Code Integration
Auto-vaults secrets and creates fix PRs

Usage:
    python3 agent.py --demo                    # Run with demo Snyk Code findings
    python3 agent.py --project PROJECT_ID      # Production mode
    python3 agent.py --demo --dry-run          # Show what it would do
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
import hashlib

# ============================================================================
# 1. DETECT — Pull secrets findings from Snyk Code
# ============================================================================

def detect_secrets(demo_mode=True, project_id=None):
    """Pull secrets findings from Snyk Code API or demo data"""
    if demo_mode:
        scenarios_path = Path(__file__).parent / "scenarios" / "snyk_code_secrets.json"
        with open(scenarios_path) as f:
            findings = json.load(f)
        print(f"📥 Loaded {len(findings)} secret findings from Snyk Code (demo mode)")
        return findings
    else:
        # Production: Call real Snyk Code API
        # import requests
        # response = requests.get(
        #     f"https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/issues",
        #     headers={"Authorization": f"token {os.environ['SNYK_TOKEN']}"},
        #     params={"type": "secret", "severity": "critical,high"}
        # )
        # return parse_snyk_response(response.json())
        raise NotImplementedError("Production Snyk API integration requires SNYK_TOKEN")


# ============================================================================
# 2. CLASSIFY — Determine secret type and exposure level
# ============================================================================

def classify_secret(finding):
    """Classify secret by type and determine remediation strategy"""
    secret_type = finding["secret_type"]
    severity = finding["severity"]
    exposure = finding["exposure"]

    # Determine tier of autonomy
    if severity == "critical" and exposure == "committed":
        tier = "auto_vault_and_revoke"
        requires_approval = True  # For revocation only
    elif severity in ["critical", "high"]:
        tier = "auto_vault"
        requires_approval = False
    else:
        tier = "create_pr_only"
        requires_approval = False

    # Determine remediation strategy
    if secret_type == "aws_access_key":
        strategy = {
            "vault": True,
            "revoke_old": severity == "critical",
            "pr_template": "aws_credentials",
            "vault_name": f"snyk/{finding['project']}/aws_access_key/{hash_id(finding['id'])}"
        }
    elif secret_type == "github_pat":
        strategy = {
            "vault": True,
            "revoke_old": False,  # User must manually rotate GitHub PAT
            "pr_template": "github_actions_secret",
            "vault_name": f"snyk/{finding['project']}/github_pat/{hash_id(finding['id'])}"
        }
    elif secret_type == "stripe_api_key":
        is_live = "sk_live" in finding["matched_text"]
        strategy = {
            "vault": True,
            "revoke_old": is_live,
            "pr_template": "stripe_api_key",
            "vault_name": f"snyk/{finding['project']}/stripe_key/{hash_id(finding['id'])}"
        }
    else:
        strategy = {
            "vault": True,
            "revoke_old": False,
            "pr_template": "generic_secret",
            "vault_name": f"snyk/{finding['project']}/{secret_type}/{hash_id(finding['id'])}"
        }

    return {
        "tier": tier,
        "requires_approval": requires_approval,
        "strategy": strategy
    }


def hash_id(text):
    """Generate short hash for IDs"""
    return hashlib.sha256(text.encode()).hexdigest()[:8]


# ============================================================================
# 3. VAULT — Store secret in AWS Secrets Manager (simulated)
# ============================================================================

def vault_secret(secret_name, secret_value, metadata):
    """Store secret in vault (simulated in demo mode)"""
    # In production:
    # import boto3
    # secretsmanager = boto3.client('secretsmanager')
    # response = secretsmanager.create_secret(
    #     Name=secret_name,
    #     SecretString=secret_value,
    #     Tags=[{"Key": k, "Value": str(v)} for k, v in metadata.items()]
    # )
    # return response['ARN']

    # Demo simulation
    vault_arn = f"arn:aws:secretsmanager:us-east-1:123456789:secret:{secret_name}-AbCdEf"
    print(f"   ✓ Vaulted: {secret_name}")
    print(f"     ARN: {vault_arn}")
    return vault_arn


def revoke_old_credential(secret_type, access_key_id):
    """Revoke old credential (simulated in demo mode)"""
    # In production:
    # import boto3
    # if secret_type == "aws_access_key":
    #     iam = boto3.client('iam')
    #     # Get user for access key
    #     response = iam.get_access_key_last_used(AccessKeyId=access_key_id)
    #     user_name = response['UserName']
    #     # Delete access key
    #     iam.delete_access_key(UserName=user_name, AccessKeyId=access_key_id)

    # Demo simulation
    print(f"   ✓ Revoked old {secret_type}: {access_key_id}")


# ============================================================================
# 4. GENERATE FIX PR — Create PR with vault integration code
# ============================================================================

def generate_pr_template(finding, classification, vault_arn):
    """Generate PR description and code changes"""
    secret_type = finding["secret_type"]
    file_path = finding["file_path"]

    pr_templates = {
        "aws_credentials": f"""## 🔐 Security: Auto-Remediation of AWS Credentials

**Detected by:** Snyk Code (Finding ID: {finding['id']})
**Remediated by:** Secrets Remediation Agent
**Vault Location:** `{vault_arn}`

### What Changed
- Removed hardcoded AWS credentials from `{file_path}`
- Replaced with environment variables loaded from AWS Secrets Manager
- Old credentials have been **revoked** and are no longer valid

### How to Deploy

1. **Local Development:**
   ```bash
   export AWS_ACCESS_KEY="your-dev-key"
   export AWS_SECRET_KEY="your-dev-secret"
   ```

2. **Staging/Production:**
   Credentials deployed via Kubernetes secrets.

3. **Verification:**
   ```bash
   python -c "import {file_path.replace('/','.').replace('.py','')}; print('✓ AWS credentials loaded')"
   ```

### Code Changes

```python
# Before (hardcoded):
AWS_ACCESS_KEY = "{finding['matched_text']}"

# After (environment variable):
import os
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
if not AWS_ACCESS_KEY:
    raise ValueError("AWS_ACCESS_KEY not configured")
```

### Security Actions Taken
✅ Secret vaulted in AWS Secrets Manager
✅ Old AWS key revoked
✅ Security team notified
✅ Audit log updated

**Merge this PR to complete remediation.**

/cc @security-team
""",
        "github_actions_secret": f"""## 🔐 Security: Auto-Remediation of GitHub Personal Access Token

**Detected by:** Snyk Code (Finding ID: {finding['id']})
**Vault Location:** `{vault_arn}`

### What Changed
- Removed hardcoded GitHub PAT from `{file_path}`
- Replaced with GitHub Actions secret reference

### How to Deploy

1. Add GitHub Actions secret:
   ```bash
   gh secret set GITHUB_TOKEN --body "ghp_your_new_token_here"
   ```

2. The workflow will automatically use the secret

### Code Changes

```yaml
# Before:
- name: Deploy
  env:
    GITHUB_TOKEN: {finding['matched_text']}

# After:
- name: Deploy
  env:
    GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
```

**Important:** Rotate your GitHub PAT at https://github.com/settings/tokens

/cc @security-team
""",
        "generic_secret": f"""## 🔐 Security: Auto-Remediation of {secret_type}

**Detected by:** Snyk Code (Finding ID: {finding['id']})
**Vault Location:** `{vault_arn}`

### What Changed
- Removed hardcoded {secret_type} from `{file_path}`
- Replaced with environment variable pattern

### Security Actions Taken
✅ Secret vaulted
✅ Security team notified

/cc @security-team
"""
    }

    template_key = classification["strategy"]["pr_template"]
    return pr_templates.get(template_key, pr_templates["generic_secret"])


def create_pr(repo_name, finding, pr_description, dry_run=False):
    """Create GitHub PR with fixes (simulated in demo mode)"""
    if dry_run:
        print(f"   [DRY RUN] Would create PR in {repo_name}")
        return f"https://github.com/{repo_name}/pull/DRAFT"

    # In production:
    # from github import Github
    # g = Github(github_token)
    # repo = g.get_repo(repo_name)
    # branch = f"snyk-secrets-fix-{finding['id'][:8]}"
    # # Create branch, update files, create PR...
    # pr = repo.create_pull(...)
    # return pr.html_url

    # Demo simulation
    pr_url = f"https://github.com/{repo_name}/pull/{hash_id(finding['id'])[:4]}"
    print(f"   ✓ Created PR: {pr_url}")
    return pr_url


# ============================================================================
# 5. NOTIFY — Alert security team
# ============================================================================

def notify_security_team(finding, vault_arn, pr_url):
    """Send Slack notification to security team (simulated)"""
    # In production:
    # import slack_sdk
    # client = slack_sdk.WebClient(token=slack_token)
    # client.chat_postMessage(channel="#security-alerts", blocks=[...])

    # Demo simulation
    message = f"""
🔐 Secret Auto-Remediated

Type: {finding['secret_type']} ({finding['severity'].title()})
Project: {finding['project']}
File: {finding['file_path']}

Actions Taken:
✅ Secret vaulted: {vault_arn}
✅ Fix PR created: {pr_url}
✅ Audit log updated

[View Snyk Finding] [View Vault]
"""
    print(f"   ✓ Notified #security-alerts")
    return message


# ============================================================================
# 6. LOG — Write immutable audit trail
# ============================================================================

def log_remediation(finding, classification, vault_arn, pr_url, audit_path):
    """Write decision to audit log"""
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": "secrets-remediation-agent",
        "finding": {
            "snyk_id": finding["id"],
            "secret_type": finding["secret_type"],
            "severity": finding["severity"],
            "file": finding["file_path"],
            "line": finding["line_number"],
            "exposure": finding["exposure"]
        },
        "classification": classification,
        "actions": {
            "vaulted": vault_arn,
            "revoked_old": classification["strategy"]["revoke_old"],
            "pr_created": pr_url,
            "security_notified": True
        },
        "status": "completed"
    }

    with open(audit_path, 'a') as f:
        f.write(json.dumps(audit_entry) + '\n')


# ============================================================================
# 7. GENERATE REPORTS
# ============================================================================

def generate_pr_files(findings_with_results, reports_dir):
    """Generate PR template files for review"""
    for i, result in enumerate(findings_with_results):
        finding = result["finding"]
        pr_description = result["pr_description"]

        pr_file = reports_dir / f"pr_template_{i+1}_{finding['secret_type']}.md"
        with open(pr_file, 'w') as f:
            f.write(pr_description)

    print(f"\n📊 Generated {len(findings_with_results)} PR templates in {reports_dir}/")


# ============================================================================
# Main orchestration
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Secrets Remediation Agent")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--project", help="Snyk project ID (production mode)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve all actions")
    args = parser.parse_args()

    if not args.demo and not args.project:
        print("❌ Error: Specify --demo or --project PROJECT_ID")
        sys.exit(1)

    # Setup paths
    base_path = Path(__file__).parent
    audit_path = base_path / "audit" / "remediation_log.jsonl"
    reports_dir = base_path / "reports"
    audit_path.parent.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    print("🔐 Secrets Remediation Agent Starting...")
    print("=" * 60)

    # 1. DETECT
    findings = detect_secrets(demo_mode=args.demo, project_id=args.project)

    # Process each finding
    results = []

    for finding in findings:
        print(f"\n📌 Processing: {finding['secret_type']} in {finding['file_path']}")

        # 2. CLASSIFY
        classification = classify_secret(finding)
        print(f"   Classification: {classification['tier']}")

        # 3. VAULT
        vault_arn = vault_secret(
            secret_name=classification["strategy"]["vault_name"],
            secret_value=finding.get("matched_text", "[REDACTED]"),
            metadata={
                "source": "snyk-code",
                "project": finding["project"],
                "severity": finding["severity"]
            }
        )

        # Revoke old credential if needed
        if classification["strategy"]["revoke_old"]:
            if args.auto_approve or input("   ⚠️  Revoke old credential? [y/N]: ").lower() == 'y':
                revoke_old_credential(finding["secret_type"], finding.get("matched_text", ""))
            else:
                print("   ⊘ Revocation skipped (user rejected)")

        # 4. GENERATE PR
        pr_description = generate_pr_template(finding, classification, vault_arn)
        pr_url = create_pr(
            repo_name=f"{finding['org']}/{finding['project']}",
            finding=finding,
            pr_description=pr_description,
            dry_run=args.dry_run
        )

        # 5. NOTIFY
        notify_security_team(finding, vault_arn, pr_url)

        # 6. LOG
        log_remediation(finding, classification, vault_arn, pr_url, audit_path)

        results.append({
            "finding": finding,
            "classification": classification,
            "vault_arn": vault_arn,
            "pr_url": pr_url,
            "pr_description": pr_description
        })

    # 7. GENERATE REPORTS
    generate_pr_files(results, reports_dir)

    print("\n" + "=" * 60)
    print(f"✅ Remediation complete! Processed {len(findings)} secrets")
    print(f"📊 PR templates: {reports_dir}/")
    print(f"📝 Audit log: {audit_path}")


if __name__ == "__main__":
    main()
