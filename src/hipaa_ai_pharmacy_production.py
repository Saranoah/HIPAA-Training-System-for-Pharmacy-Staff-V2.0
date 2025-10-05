# app.py - Complete HIPAA Training System (95% Coverage)
"""
HIPAA Training System - Duolingo-Style Web App
COMPREHENSIVE VERSION - Certification-Grade Coverage
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os
from typing import Dict, List, Any

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # CHANGE THIS IN PRODUCTION!

# Constants
PASS_THRESHOLD = 80
GOOD_THRESHOLD = 60
PROGRESS_FILE = "user_progress.json"

# ========================================
# COMPLETE LESSONS - 13 Comprehensive Modules
# ========================================
LESSONS = {
    "What is PHI?": {
        "icon": "🏥",
        "order": 1,
        "content": "Protected Health Information (PHI) is any information about health status, healthcare provision, or payment that can identify an individual. HIPAA protects 18 specific identifiers.",
        "key_points": [
            "18 HIPAA Identifiers: Name, address, DOB, SSN, medical record number, phone, email, photos, etc.",
            "Pharmacy PHI Examples: Prescription history, medication lists, insurance info, allergies, patient accounts",
            "De-identified data (no identifiers) is NOT PHI and can be used freely",
            "Even a single identifier linked to health info becomes PHI requiring protection"
        ]
    },
    "Privacy Rule": {
        "icon": "🔒",
        "order": 2,
        "content": "HIPAA Privacy Rule protects patient information and requires minimum necessary use. It establishes national standards for protecting PHI.",
        "key_points": [
            "Patient authorization required for most disclosures",
            "Minimum necessary standard applies to routine uses",
            "Patients have rights to access their own records",
            "Treatment, payment, and operations (TPO) allowed without authorization"
        ]
    },
    "Security Rule": {
        "icon": "🛡️",
        "order": 3,
        "content": "HIPAA Security Rule requires administrative, physical, and technical safeguards for electronic Protected Health Information (ePHI).",
        "key_points": [
            "Encryption of data at rest and in transit",
            "Access controls and user authentication required",
            "Audit trails and monitoring systems mandatory",
            "Risk analysis and management processes must be documented"
        ]
    },
    "Patient Rights": {
        "icon": "⚖️",
        "order": 4,
        "content": "HIPAA grants patients seven fundamental rights regarding their health information. Pharmacies must honor these rights and respond to requests within specific timeframes.",
        "key_points": [
            "Right to Access: View/copy records within 30 days, can charge reasonable copying fee",
            "Right to Amend: Request corrections to errors, pharmacy must respond within 60 days",
            "Right to Accounting: List of disclosures for past 6 years",
            "Right to Request Restrictions: Ask to limit uses/disclosures",
            "Right to Confidential Communications: Request alternate contact methods",
            "Right to Notice of Privacy Practices: Receive written NPP",
            "Right to Complain: File complaints with pharmacy or HHS without retaliation"
        ]
    },
    "Breach Notification": {
        "icon": "⚠️",
        "order": 5,
        "content": "HIPAA requires notifying affected patients and HHS within 60 days if PHI is breached. A breach is unauthorized access, use, or disclosure that compromises security or privacy.",
        "key_points": [
            "60-day notification timeline from discovery of breach",
            "Patient notification required for all breaches",
            "HHS reporting mandatory for breaches affecting 500+ individuals",
            "Media notification required for breaches over 500 people",
            "Document all breach investigations even if no notification needed"
        ]
    },
    "Violations & Penalties": {
        "icon": "⚖️",
        "order": 6,
        "content": "HIPAA violations carry significant financial and criminal penalties. Understanding the consequences helps emphasize why compliance matters for every pharmacy staff member.",
        "key_points": [
            "Civil Penalties: $100 to $50,000 per violation (up to $1.9M per year for repeated violations)",
            "Criminal Penalties: Up to 10 years prison + $250,000 for violations with malicious intent",
            "Real Cases: CVS ($2.25M for improper disposal), Walgreens ($1.4M for dumpster PHI)",
            "Individual Liability: Staff members can be personally fined or prosecuted",
            "Violation Categories: Unknowing, reasonable cause, willful neglect (corrected/uncorrected)"
        ]
    },
    "Business Associates": {
        "icon": "🤝",
        "order": 7,
        "content": "A Business Associate (BA) is any vendor or contractor that accesses PHI on behalf of your pharmacy. HIPAA requires written agreements (BAAs) with all BAs before sharing any PHI.",
        "key_points": [
            "Who is a BA: Billing companies, IT support, shredding services, cloud storage, software vendors",
            "BAA Requirements: Must be signed BEFORE PHI access, defines protection responsibilities",
            "Pharmacy Liability: You're responsible if your BA causes a breach",
            "Common Mistake: Assuming vendors 'know' HIPAA - always get signed BAA first",
            "Regular Reviews: Audit BA compliance annually, update agreements when services change"
        ]
    },
    "Secure Disposal": {
        "icon": "🗑️",
        "order": 8,
        "content": "Improper disposal of PHI is one of the most common HIPAA violations in pharmacies. All PHI must be destroyed in a way that makes it unreadable and irretrievable.",
        "key_points": [
            "Paper Records: Cross-cut shred (not tear), burn, or pulverize",
            "Electronic Records: Overwrite hard drives, physically destroy devices",
            "Pharmacy-Specific: Shred prescription labels, expired Rx records, counseling notes",
            "Never: Throw PHI in regular trash, recycle bins, or accessible dumpsters",
            "Retention Rules: Keep records 7 years (varies by state), then proper disposal required",
            "Document: Use certificates of destruction for large batches"
        ]
    },
    "Access Controls": {
        "icon": "🔐",
        "order": 9,
        "content": "Technical safeguards require strict controls over who can access ePHI systems. Proper password management and access controls are essential security measures.",
        "key_points": [
            "Unique User IDs: Every staff member must have own login - NEVER share passwords",
            "Password Standards: Minimum 8 characters (12+ recommended), change every 90 days",
            "Automatic Logoff: System locks after 15 minutes of in
