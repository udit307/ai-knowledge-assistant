from pathlib import Path
import random

# Create output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Sample topics
# documents = [
#     {
#         "filename": "flocard_overview.md",
#         "content": """
# # FloCard Overview

# FloCard is a digital business card platform that allows professionals
# to share contact information instantly using QR codes and NFC technology.

# Key Features:
# - Digital profiles
# - QR sharing
# - Team management
# - Analytics dashboard
# """
#     },

#     {
#         "filename": "employee_onboarding.md",
#         "content": """
# # Employee Onboarding SOP

# All new employees must complete onboarding within 5 days.

# Steps:
# 1. Create company email
# 2. Join Slack workspace
# 3. Setup development environment
# 4. Read security policies
# 5. Attend orientation meeting
# """
#     },

#     {
#         "filename": "api_guidelines.md",
#         "content": """
# # API Development Guidelines

# All APIs should follow REST standards.

# Best Practices:
# - Use proper HTTP methods
# - Validate request payloads
# - Return JSON responses
# - Include status codes
# - Write API documentation
# """
#     },

#     {
#         "filename": "security_policy.md",
#         "content": """
# # Security Policy

# Employees must never share passwords.

# Security Rules:
# - Use MFA authentication
# - Rotate passwords every 90 days
# - Report phishing emails
# - Lock systems when away
# """
#     }
# ]

documents = [
    {
        "filename": "flocard_overview.md",
        "title": "FloCard Overview",
        "tags": ["product", "flocard"],
        "type": "overview",
        "content": """
# FloCard Overview

FloCard is a digital business card platform that allows professionals
to share contact information instantly using QR codes and NFC technology.

Key Features:
- Digital profiles
- QR sharing
- Team management
- Analytics dashboard
"""
    },

    {
        "filename": "employee_onboarding.md",
        "title": "Employee Onboarding SOP",
        "tags": ["hr", "onboarding"],
        "type": "sop",
        "content": """
# Employee Onboarding SOP

All new employees must complete onboarding within 5 days.

Steps:
1. Create company email
2. Join Slack workspace
3. Setup development environment
4. Read security policies
5. Attend orientation meeting
"""
    }
]

# Generate files
for doc in documents:
    file_path = output_dir / doc["filename"]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(doc["content"])

print("Synthetic documents generated successfully!")