# Secrets Remediation Agent (Snyk Code Integration)

Autonomous agent that detects secrets in Snyk Code scan results and automatically vaults them, creates fix PRs, and notifies security teams — all with full audit trail and developer-friendly workflows.

## The Problem

**Snyk Code finds secrets, but what happens next?**
- Security teams get alerts but can't act on all of them
- Developers don't know how to safely vault secrets
- Secrets sit exposed in repos for days/weeks
- No automated workflow from detection to remediation

**Industry Data:**
- 50-200 secrets per repository on average
- 73% of secrets are still valid 90 days after discovery (GitGuardian 2024)
- Mean time to remediation: 27 days (manual process)

## The Solution: Auto-Vaulting with Fix PRs

This agent automates the entire remediation workflow:

1. **Detect** — Pull secrets findings from Snyk Code API
2. **Classify** — Determine secret type and exposure level
3. **Vault** — Store secret in AWS Secrets Manager / HashiCorp Vault
4. **Replace** — Generate PR replacing hardcoded secret with vault reference
5. **Notify** — Alert security team with context and tracking
6. **Log** — Immutable audit trail for compliance

**Time to remediation:** <1 hour (vs 27 days manual)

---

## How It Works

### 1. Detect Secrets from Snyk Code

```python
# Pull secrets findings from Snyk Code API
secrets = snyk_code_api.get_secrets_findings(project_id)

# Example finding:
{
  "id": "snyk-code-123456",
  "type": "aws_access_key",
  "severity": "critical",
  "file_path": "src/config/aws.py",
  "line_number": 42,
  "matched_text": "AKIAIOSFODNN7EXAMPLE",
  "is_valid": true,
  "exposure": "committed"
}
```

### 2. Classify by Severity & Exposure

| Secret Type | Severity | Exposure | Action |
|-------------|----------|----------|--------|
| AWS Access Key | Critical | Committed to repo | Auto-vault + PR + revoke old key |
| GitHub PAT | Critical | Committed to repo | Auto-vault + PR + notify security |
| Stripe API Key (live) | Critical | Committed to repo | Auto-vault + PR + escalate to finance |
| Stripe API Key (test) | High | Committed to repo | Auto-vault + PR |
| Database password | High | Env vars only | Create vault PR (no old value exposed) |
| Generic API key | Medium | Env vars only | PR with guidance |

### 3. Vault the Secret

```python
# Store in AWS Secrets Manager
secret_arn = vault.store_secret(
    name=f"snyk-remediated/{project}/{secret_type}/{hash}",
    value=secret_value,
    tags={
        "source": "snyk-code",
        "project": project_id,
        "remediated_by": "agent",
        "severity": "critical"
    }
)

# Returns: arn:aws:secretsmanager:us-east-1:123456789:secret:snyk-remediated/...
```

### 4. Generate Fix PR

The agent creates a PR that:
- Removes hardcoded secret from code
- Replaces with vault reference: `os.environ.get("AWS_ACCESS_KEY")`
- Adds code to fetch from vault at runtime
- Includes instructions for team to deploy

**Example PR for AWS Key:**

```python
# Before (Snyk Code finding):
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# After (Agent-generated fix):
import os
import boto3

# Secrets managed by security team via AWS Secrets Manager
# Deployed via: kubectl create secret aws-credentials --from-literal=...
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    raise ValueError("AWS credentials not configured. See README.md for setup.")
```

**PR Description (Auto-generated):**
```markdown
## 🔐 Security: Auto-Remediation of AWS Credentials

**Detected by:** Snyk Code (Finding ID: snyk-code-123456)  
**Remediated by:** Secrets Remediation Agent  
**Vault Location:** `aws-secretsmanager://snyk-remediated/payment-api/aws_access_key/a3f9d2`

### What Changed
- Removed hardcoded AWS credentials from `src/config/aws.py`
- Replaced with environment variables loaded from AWS Secrets Manager
- Old credentials have been **revoked** and are no longer valid
- New credentials are deployed via Kubernetes secrets

### How to Deploy

1. **Local Development:**
   ```bash
   export AWS_ACCESS_KEY="your-dev-key"
   export AWS_SECRET_KEY="your-dev-secret"
   ```

2. **Staging/Production:**
   Already deployed via Kubernetes. No action needed.

3. **Verification:**
   ```bash
   python -c "import src.config.aws; print('✓ AWS credentials loaded')"
   ```

### Security Actions Taken
✅ Secret vaulted in AWS Secrets Manager  
✅ Old AWS key revoked (no longer functional)  
✅ Security team notified  
✅ Audit log updated  

**Merge this PR to complete remediation.**

/cc @security-team
```

### 5. Notify Security Team

**Slack notification:**
```
🔐 Secret Auto-Remediated

Type: AWS Access Key (Critical)
Project: payment-api-prod
File: src/config/aws.py

Actions Taken:
✅ Secret vaulted in AWS Secrets Manager
✅ Old key revoked
✅ Fix PR created: #1234
✅ Audit log updated

Vault Location: aws-secretsmanager://snyk-remediated/...

[View PR] [View Snyk Finding] [View Vault]
```

### 6. Audit Trail

```jsonl
{
  "timestamp": "2026-06-01T15:32:45Z",
  "agent": "secrets-remediation-agent",
  "finding": {
    "snyk_id": "snyk-code-123456",
    "type": "aws_access_key",
    "severity": "critical",
    "file": "src/config/aws.py",
    "line": 42
  },
  "actions": {
    "vaulted": "arn:aws:secretsmanager:us-east-1:...",
    "revoked_old_key": true,
    "pr_created": "https://github.com/company/payment-api/pull/1234",
    "security_notified": true
  },
  "decision_rationale": "Critical AWS key in committed code. Auto-vault + revoke + PR.",
  "approvals": [],
  "status": "completed"
}
```

---

## Supported Secret Types

### Cloud Credentials
- AWS Access Keys & Secret Keys
- GCP Service Account Keys
- Azure Storage Keys
- DigitalOcean API Tokens

### SaaS/API Tokens
- GitHub Personal Access Tokens
- GitLab Access Tokens
- Slack API Tokens / Webhooks
- Stripe API Keys (live & test)
- SendGrid API Keys
- Twilio Auth Tokens

### Database Credentials
- PostgreSQL passwords
- MySQL passwords
- MongoDB connection strings
- Redis passwords

### Cryptographic Keys
- RSA private keys
- SSH private keys
- JWT secrets
- Encryption keys

### Custom Secrets
- Internal API keys
- Service-to-service tokens
- Customer-specific credentials

---

## Demo Scenarios

### Scenario 1: AWS Key in Production Code

```
Finding: AWS Access Key hardcoded in payment API
Severity: Critical
Exposure: Committed to git (public repo)

Agent Actions:
1. Vault secret in AWS Secrets Manager
2. Revoke old AWS key via AWS API
3. Create PR with environment variable approach
4. Notify security + on-call
5. Block deployments until PR merged

Time to Remediation: 15 minutes (vs 27 days manual)
```

### Scenario 2: GitHub PAT in CI Configuration

```
Finding: GitHub Personal Access Token in .github/workflows/deploy.yml
Severity: Critical  
Exposure: Committed to git

Agent Actions:
1. Vault token in AWS Secrets Manager
2. Create PR using GitHub Actions secrets
3. Notify security team
4. Guide developer to rotate token

PR Changes:
- Remove: GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
+ Add: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Scenario 3: Stripe Test Key (Low Risk)

```
Finding: Stripe test API key in test fixtures
Severity: Low
Exposure: Test file only

Agent Actions:
1. Create PR with .env.example pattern
2. Notify team (no escalation)
3. Log for compliance

No vault needed (test key, low risk)
```

---

## Quick Start

```bash
cd 02-secrets-remediation-agent

# Demo mode with sample Snyk Code findings
python3 agent.py --demo --auto-approve

# View generated PR templates
cat reports/pr_template_*.md

# View audit log
cat audit/remediation_log.jsonl

# Production mode (requires Snyk API token)
export SNYK_TOKEN="your-token"
export VAULT_ADDR="https://vault.company.com"
python3 agent.py --project PROJECT_ID
```

---

## Production Integration

### Snyk Code API

```python
import requests

def get_secrets_findings(project_id):
    response = requests.get(
        f"https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/issues",
        headers={
            "Authorization": f"token {snyk_token}",
            "Content-Type": "application/vnd.api+json"
        },
        params={"type": "secret", "severity": "critical,high"}
    )
    return response.json()
```

### AWS Secrets Manager Integration

```python
import boto3

secretsmanager = boto3.client('secretsmanager')

def vault_secret(name, value, tags):
    response = secretsmanager.create_secret(
        Name=name,
        SecretString=value,
        Tags=[{"Key": k, "Value": v} for k, v in tags.items()]
    )
    return response['ARN']

def revoke_aws_key(access_key_id):
    iam = boto3.client('iam')
    # Find user for this access key
    response = iam.get_access_key_last_used(AccessKeyId=access_key_id)
    user_name = response['UserName']
    # Delete the access key
    iam.delete_access_key(UserName=user_name, AccessKeyId=access_key_id)
```

### GitHub PR Creation

```python
from github import Github

def create_fix_pr(repo_name, branch, files_changed, description):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # Create branch
    main = repo.get_branch("main")
    repo.create_git_ref(f"refs/heads/{branch}", main.commit.sha)
    
    # Update files
    for file_path, new_content in files_changed.items():
        repo.update_file(
            path=file_path,
            message=f"Security: Remove hardcoded secret from {file_path}",
            content=new_content,
            branch=branch,
            sha=repo.get_contents(file_path, ref="main").sha
        )
    
    # Create PR
    pr = repo.create_pull(
        title="🔐 Security: Auto-remediate secrets found by Snyk Code",
        body=description,
        head=branch,
        base="main"
    )
    
    # Add labels
    pr.add_to_labels("security", "automated", "snyk")
    
    return pr.html_url
```

---

## Metrics

The agent exposes metrics for monitoring:

```
snyk_secrets_detected_total{severity="critical"} 12
snyk_secrets_vaulted_total{vault="aws_secretsmanager"} 12
snyk_secrets_prs_created_total 12
snyk_secrets_keys_revoked_total 8
snyk_secrets_remediation_time_seconds{quantile="0.99"} 420
snyk_secrets_false_positive_rate 0.02
```

---

## Regulatory Compliance

| Regulation | Requirement | How Agent Addresses |
|------------|-------------|-------------------|
| **PCI-DSS Req 3.5** | Cryptographic key management | Secrets vaulted with lifecycle tracking |
| **SOC 2 CC6.1** | Logical access controls | Secrets rotated, old credentials revoked |
| **GDPR Article 32** | Security of processing | Secrets discovery + remediation automated |
| **NYDFS Part 500** | Access controls | Audit trail of every secret remediation |

---

## Architecture

**Tiered Autonomy:**
- **Tier 1 (Auto):** Vault secret, create PR, notify team
- **Tier 2 (Approval):** Revoke old credentials (for critical secrets only)
- **Tier 3 (Advisory):** Guide for complex secrets (DB connections, service accounts)

**Swappable Vault Adapters:**
- AWS Secrets Manager (default)
- HashiCorp Vault
- Azure Key Vault
- GCP Secret Manager

**Integration Points:**
- Snyk Code API (secrets detection)
- GitHub/GitLab/Bitbucket (PR creation)
- Slack (notifications)
- Jira (ticket tracking)
- Vault (secret storage)

---

## What Makes This Snyk-Specific

Unlike generic secret scanners, this agent:
- ✅ **Pulls from Snyk Code findings** (not log files or custom regex)
- ✅ **Integrates with Snyk Asset Management** (prioritize by asset criticality)
- ✅ **Leverages Snyk's secret type classification** (AWS, GitHub, Stripe, etc.)
- ✅ **Creates developer-friendly PRs** (not just "rotate your secrets")
- ✅ **Tracks remediation in Snyk Issues** (unified view across all security findings)

---

**This agent transforms Snyk Code from "we found secrets" to "we fixed secrets" — fully automated with human oversight.**
