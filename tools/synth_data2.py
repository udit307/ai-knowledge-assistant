from pathlib import Path

# Create output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Document collection including original and 5 new topics with metadata
documents = [
    {
        "filename": "flocard_overview.md",
        "title": "FloCard Overview",
        "tags": ["product", "overview", "nfc"],
        "type": "documentation",
        "content": """# FloCard Overview

FloCard is a digital business card platform that allows professionals to share contact information instantly using QR codes and NFC technology.

Key Features:
- Digital profiles
- QR sharing
- Team management
- Analytics dashboard"""
    },
    {
        "filename": "employee_onboarding.md",
        "title": "Employee Onboarding SOP",
        "tags": ["hr", "onboarding", "sop"],
        "type": "procedure",
        "content": """# Employee Onboarding SOP

All new employees must complete onboarding within 5 days.

Steps:
1. Create company email
2. Join Slack workspace
3. Setup development environment
4. Read security policies
5. Attend orientation meeting"""
    },
    {
        "filename": "api_guidelines.md",
        "title": "API Development Guidelines",
        "tags": ["engineering", "api", "rest"],
        "type": "guideline",
        "content": """# API Development Guidelines

All APIs should follow REST standards.

Best Practices:
- Use proper HTTP methods
- Validate request payloads
- Return JSON responses
- Include status codes
- Write API documentation"""
    },
    {
        "filename": "security_policy.md",
        "title": "Security Policy",
        "tags": ["security", "compliance", "policy"],
        "type": "policy",
        "content": """# Security Policy

Employees must never share passwords.

Security Rules:
- Use MFA authentication
- Rotate passwords every 90 days
- Report phishing emails
- Lock systems when away"""
    },
    {
        "filename": "leave_policy.md",
        "title": "Company Leave Policy",
        "tags": ["hr", "benefits", "policy"],
        "type": "policy",
        "content": """# Company Leave Policy

Our leave policy ensures employees get adequate rest and personal time.

Guidelines:
- 20 days of paid annual leave per calendar year
- Up to 10 days of sick leave with medical certificate
- Maternity leave (26 weeks) and Paternity leave (4 weeks)
- All leave requests must be submitted via the HR portal 2 weeks in advance"""
    },
    {
        "filename": "coding_standards.md",
        "title": "Engineering Coding Standards",
        "tags": ["engineering", "quality", "clean-code"],
        "type": "guideline",
        "content": """# Engineering Coding Standards

Maintained code quality ensures system scalability and seamless collaboration.

Standards:
- Follow language-specific style guides (e.g., PEP 8 for Python)
- Keep functions small and focused on a single responsibility
- Write meaningful unit tests covering at least 80% of new code
- Ensure every PR goes through at least one peer review before merging"""
    },
    {
        "filename": "deployment_process.md",
        "title": "CI/CD Deployment Process",
        "tags": ["devops", "cicd", "deployment"],
        "type": "procedure",
        "content": """# CI/CD Deployment Process

Standard operating procedure for moving code from staging to production.

Steps:
1. Trigger automated testing pipeline on the release branch
2. Verify all checks pass and manual QA sign-off is granted
3. Initiate blue-green deployment via the orchestration platform
4. Monitor system metrics and error logs for 15 minutes post-release
5. Execute rollback strategy immediately if anomalies are detected"""
    },
    {
        "filename": "database_backup_sop.md",
        "title": "Database Backup SOP",
        "tags": ["infrastructure", "database", "backup"],
        "type": "procedure",
        "content": """# Database Backup SOP

Procedures to safeguard company data assets against loss or corruption.

SOP Details:
- Automated snapshots are taken every 4 hours and stored in AWS S3
- Full database logical backups are completed nightly at 02:00 UTC
- Retain daily backups for 30 days, monthly backups for 1 year
- Perform a simulated recovery test on the first Monday of every month"""
    },
    {
        "filename": "customer_support_workflow.md",
        "title": "Customer Support Workflow",
        "tags": ["support", "operations", "helpdesk"],
        "type": "procedure",
        "content": """# Customer Support Workflow

Standard operational workflow for resolving client queries efficiently.

Workflow:
- Tier 1: Initial triage and basic troubleshooting within 2 hours
- Tier 2: Escalation to technical support specialists if unresolved
- Tier 3: Critical bugs assigned directly to the engineering triage team
- Always follow up with the customer to confirm satisfaction before closing a ticket"""
    }
]

# Generate files with metadata embedded at the top
for doc in documents:
    file_path = output_dir / doc["filename"]

    with open(file_path, "w", encoding="utf-8") as f:
        # Prepend front-matter style metadata before the content
        metadata_header = (
            f"Title: {doc['title']}\n"
            f"Tags: {', '.join(doc['tags'])}\n"
            f"Type: {doc['type']}\n"
            f"{'-' * 40}\n\n"
        )
        f.write(metadata_header + doc["content"].strip() + "\n")

print(f"Synthetic documents generated successfully! Check '{output_dir}/'")