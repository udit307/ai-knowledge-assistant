Title: Database Backup SOP
Tags: infrastructure, database, backup
Type: procedure
----------------------------------------

# Database Backup SOP

Procedures to safeguard company data assets against loss or corruption.

SOP Details:
- Automated snapshots are taken every 4 hours and stored in AWS S3
- Full database logical backups are completed nightly at 02:00 UTC
- Retain daily backups for 30 days, monthly backups for 1 year
- Perform a simulated recovery test on the first Monday of every month
