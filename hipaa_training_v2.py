#!/usr/bin/env python3
"""
HIPAA Training System V2.0 for Pharmacy Staff
Complete CLI application with enhanced content
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
def show_welcome():
    """Display professional welcome screen"""
    print("\n" + "="*70)
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║         HIPAA TRAINING SYSTEM V2.0 - PROFESSIONAL EDITION       ║")
    print("║              Complete Training for Pharmacy Staff                ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("="*70)
    print("\n📚 13 Comprehensive Lessons | 🎯 15 Quiz Questions | ✅ 15-Item Checklist")
    print("\n95% HIPAA Coverage | Certification-Grade Training")
    print("\nDeveloped by: Saranoah")
    print("Support: [Your Email]")
    print("="*70)
    input("\nPress Enter to begin training...")
# Constants
PASS_THRESHOLD = 80
GOOD_THRESHOLD = 60
PROGRESS_FILE = "hipaa_progress.json"

# 13 Complete Lessons
LESSONS = {
    "Privacy Rule Basics": {
        "content": "The HIPAA Privacy Rule establishes national standards to protect individuals' medical records and other personal health information (PHI). It applies to health plans, healthcare clearinghouses, and healthcare providers. The rule requires appropriate safeguards to protect privacy and sets limits on uses and disclosures without patient authorization.",
        "key_points": [
            "Protects all individually identifiable health information",
            "Requires written patient authorization for most disclosures",
            "Patients have right to access their own health information",
            "Minimum necessary standard must be applied"
        ]
    },
    "Security Rule Requirements": {
        "content": "The HIPAA Security Rule protects electronic protected health information (ePHI) through administrative, physical, and technical safeguards. Administrative safeguards include security management processes and workforce training. Physical safeguards control facility access and workstation use. Technical safeguards involve access controls, audit controls, and transmission security.",
        "key_points": [
            "Applies specifically to electronic PHI (ePHI)",
            "Requires risk analysis and risk management",
            "Encryption strongly recommended for data at rest and in transit",
            "Regular security training required for all staff"
        ]
    },
    "Breach Notification Rule": {
        "content": "The Breach Notification Rule requires covered entities to notify affected individuals, HHS, and sometimes the media following a breach of unsecured PHI. Notifications must be provided without unreasonable delay, no later than 60 days after discovery. Breaches affecting 500+ individuals require immediate media notification and HHS reporting.",
        "key_points": [
            "60-day notification deadline from breach discovery",
            "Must notify patients, HHS, and media (for large breaches)",
            "Breach defined as unauthorized access, use, or disclosure",
            "Risk assessment required to determine if breach occurred"
        ]
    },
    "Patient Rights Under HIPAA": {
        "content": "Patients have seven key rights under HIPAA: right to access their health records, right to request corrections, right to receive accounting of disclosures, right to request restrictions, right to confidential communications, right to file complaints, and right to receive a Notice of Privacy Practices. Pharmacies must honor these rights and have procedures in place to facilitate them.",
        "key_points": [
            "Right to access records within 30 days of request",
            "Right to request amendments to incorrect information",
            "Right to know who accessed their information",
            "Right to file complaints without retaliation"
        ]
    },
    "Minimum Necessary Standard": {
        "content": "The minimum necessary standard requires that covered entities make reasonable efforts to limit PHI uses, disclosures, and requests to only the minimum necessary to accomplish the intended purpose. This does not apply to treatment purposes, disclosures to patients, or when required by law. Pharmacies must implement policies defining what constitutes minimum necessary for routine operations.",
        "key_points": [
            "Use only information needed for specific purpose",
            "Does not apply to treatment activities",
            "Implement role-based access controls",
            "Regular review of access privileges required"
        ]
    },
    "18 Identifiers of PHI": {
        "content": "HIPAA defines 18 specific identifiers that make health information individually identifiable: names, geographic subdivisions smaller than state, dates (except year), telephone/fax numbers, email addresses, SSN, medical record numbers, health plan numbers, account numbers, certificate/license numbers, vehicle identifiers, device identifiers, URLs, IP addresses, biometric identifiers, photos, and any other unique identifying characteristic.",
        "key_points": [
            "All 18 identifiers must be removed for de-identification",
            "Dates more specific than year are identifiers",
            "ZIP codes must be truncated to first 3 digits only",
            "Photos and biometric data are PHI"
        ]
    },
    "Authorized vs Unauthorized Disclosures": {
        "content": "Authorized disclosures require valid patient authorization except for specific exceptions: treatment, payment, healthcare operations, required by law, public health activities, abuse/neglect reporting, law enforcement purposes, and decedents. Unauthorized disclosures include gossiping about patients, leaving records visible to others, discussing cases in public areas, and accessing records without legitimate need.",
        "key_points": [
            "Treatment purposes don't require authorization",
            "Payment and operations have limited authorization exceptions",
            "Marketing and fundraising require explicit authorization",
            "Any disclosure not specifically permitted is prohibited"
        ]
    },
    "Business Associate Agreements": {
        "content": "Business associates are entities that perform functions involving PHI on behalf of covered entities. Examples include billing companies, IT vendors, shredding services, and cloud storage providers. Written Business Associate Agreements (BAAs) are required before sharing any PHI. BAAs must specify permitted uses, require appropriate safeguards, mandate breach reporting, and include termination provisions.",
        "key_points": [
            "Required before any PHI sharing with vendors",
            "Must be in writing and signed by both parties",
            "Vendor must agree to HIPAA compliance",
            "Covered entity remains liable for vendor breaches"
        ]
    },
    "Proper PHI Disposal": {
        "content": "PHI disposal must render information unreadable and indecipherable. Paper records require cross-cut shredding, pulping, burning, or pulverizing. Electronic media requires overwriting, degaussing, or physical destruction. Simply deleting files or throwing papers in trash is insufficient. Pharmacies must have documented disposal procedures and may use certified disposal services.",
        "key_points": [
            "Cross-cut shredders required for paper PHI",
            "Electronic media must be completely destroyed",
            "Maintain logs of disposal activities",
            "Vendor disposal requires Business Associate Agreement"
        ]
    },
    "Workforce Training Requirements": {
        "content": "All workforce members must receive HIPAA training upon hire and annually thereafter. Training must cover Privacy Rule, Security Rule, organizational policies, breach notification procedures, and sanctions for violations. Documentation of training must be maintained for six years. New policies require additional training. Pharmacies must track training completion and maintain records.",
        "key_points": [
            "Initial training required for all new employees",
            "Annual refresher training mandatory",
            "Training records retained for 6 years",
            "Additional training required for policy changes"
        ]
    },
    "Incident Response Procedures": {
        "content": "When a privacy or security incident occurs, immediate action is required: contain the incident, assess the scope, determine if breach occurred, conduct risk assessment, notify appropriate parties if breach is confirmed, document all actions, and implement corrective measures. Pharmacies need written incident response plans with designated response team members and clear escalation procedures.",
        "key_points": [
            "Immediate containment is first priority",
            "Risk assessment determines if breach occurred",
            "Document everything from discovery onwards",
            "Implement corrective actions to prevent recurrence"
        ]
    },
    "Physical Safeguards": {
        "content": "Physical safeguards protect the physical environment where ePHI is stored and accessed. Requirements include facility access controls (locks, badges, visitor logs), workstation security (privacy screens, auto-logout), device controls (encryption, tracking), and secure disposal methods. Computer screens must face away from public areas. Mobile devices need encryption and remote wipe capabilities.",
        "key_points": [
            "Lock medication rooms and computer areas",
            "Position screens away from public view",
            "Encrypt all mobile devices and laptops",
            "Implement auto-logout after inactivity"
        ]
    },
    "Penalties and Enforcement": {
        "content": "HIPAA violations carry civil penalties from $100 to $50,000 per violation, with annual maximum of $1.5 million. Criminal penalties include fines up to $250,000 and imprisonment up to 10 years for violations committed with intent to sell PHI. OCR (Office for Civil Rights) conducts compliance reviews and investigates complaints. Recent enforcement actions show increasing penalties, with several multi-million dollar settlements.",
        "key_points": [
            "Civil fines range from $100 to $50,000 per violation",
            "Criminal penalties include imprisonment",
            "OCR actively investigates complaints",
            "Willful neglect violations carry steepest penalties"
        ]
    }
}

# 15 Quiz Questions (Complete scenarios)
QUIZ_QUESTIONS = [
    {
        "question": "A pharmacy technician accidentally emails a patient's prescription details to the wrong email address. What is the FIRST action they should take?",
        "options": [
            "A) Delete the sent email and hope the recipient doesn't open it",
            "B) Immediately notify their supervisor and the Privacy Officer",
            "C) Wait to see if the patient complains before taking action",
            "D) Send a follow-up email asking the recipient to delete it"
        ],
        "answer": "B",
        "explanation": "Immediate notification to supervisor and Privacy Officer is required. This allows for proper breach assessment, timely patient notification if needed, and documentation. Waiting or attempting to handle it alone delays required breach response procedures."
    },
    {
        "question": "You notice a coworker accessing patient records of celebrities without any work-related reason. What should you do?",
        "options": [
            "A) Ignore it - it's not your responsibility",
            "B) Confront the coworker privately first",
            "C) Report immediately to the Privacy Officer or compliance hotline",
            "D) Only report if they access records multiple times"
        ],
        "answer": "C",
        "explanation": "Unauthorized access to PHI must be reported immediately regardless of who is involved. Snooping in medical records is a serious HIPAA violation that can result in termination and criminal penalties. Early reporting protects patients and the organization."
    },
    {
        "question": "A patient requests copies of their complete prescription history for the past 5 years. Under HIPAA, you must provide this within:",
        "options": [
            "A) 24 hours of the request",
            "B) 30 days, with possible 30-day extension",
            "C) 60 days with no exceptions",
            "D) Whatever timeframe is convenient for the pharmacy"
        ],
        "answer": "B",
        "explanation": "HIPAA requires provision of requested records within 30 days of the request. One 30-day extension is permitted if needed, but the patient must be notified of the delay. Reasonable copying fees may be charged."
    },
    {
        "question": "A pharmaceutical sales representative asks to see which patients are taking a specific medication. Should you provide this information?",
        "options": [
            "A) Yes, if they work for the manufacturer of that medication",
            "B) Yes, but only after removing patient names",
            "C) No, unless each patient has signed an authorization",
            "D) Yes, this falls under healthcare operations"
        ],
        "answer": "C",
        "explanation": "Sharing patient lists with sales representatives requires individual patient authorization. This is considered marketing under HIPAA, not healthcare operations. Even de-identified lists of patients taking specific medications could allow re-identification when combined with prescriber information."
    },
    {
        "question": "When disposing of outdated prescription labels and patient counseling sheets, you should:",
        "options": [
            "A) Tear them in half and place in regular trash",
            "B) Use a cross-cut shredder or secure disposal bin",
            "C) Burn them in an incinerator",
            "D) Both B and C are acceptable"
        ],
        "answer": "D",
        "explanation": "PHI must be rendered unreadable and indecipherable before disposal. Cross-cut shredding or incineration both meet this standard. Simply tearing documents or using strip shredders is insufficient. Pharmacies should have documented disposal procedures."
    },
    {
        "question": "A police officer requests prescription records for a suspect in a criminal investigation. You should:",
        "options": [
            "A) Provide immediately - law enforcement requests are always authorized",
            "B) Require a warrant, court order, subpoena, or administrative request",
            "C) Refuse - HIPAA never permits disclosure to police",
            "D) Only provide if the patient is present and consents"
        ],
        "answer": "B",
        "explanation": "Law enforcement requests require proper legal process (warrant, court order, subpoena, or valid administrative request). You cannot simply hand over records to police without proper documentation. Document what was requested and provided, and notify your supervisor."
    },
    {
        "question": "Which of the following is NOT considered Protected Health Information (PHI)?",
        "options": [
            "A) Patient's date of birth",
            "B) Patient's full 5-digit ZIP code",
            "C) Patient's first 3 digits of ZIP code only",
            "D) Patient's phone number"
        ],
        "answer": "C",
        "explanation": "ZIP codes truncated to first 3 digits only (for populations over 20,000) are not PHI identifiers. However, full 5-digit ZIP codes, dates of birth, and phone numbers are all PHI identifiers. This is important for de-identification processes."
    },
    {
        "question": "Your pharmacy uses a cloud-based prescription management system. Before using this service, you must:",
        "options": [
            "A) Obtain patient consent from every patient",
            "B) Execute a Business Associate Agreement with the vendor",
            "C) Only use it for non-sensitive prescriptions",
            "D) Ensure the vendor is located in the United States"
        ],
        "answer": "B",
        "explanation": "Any vendor that stores, processes, or transmits PHI on your behalf is a business associate requiring a signed BAA. This applies to cloud services, billing companies, IT support, and many others. The BAA must be in place before any PHI is shared."
    },
    {
        "question": "A patient's family member calls asking about the patient's current medications. You should:",
        "options": [
            "A) Provide the information - family members have a right to know",
            "B) Verify the caller's identity and relationship before disclosing anything",
            "C) Only disclose if the patient has authorized this person in writing",
            "D) Refuse to confirm the patient is even a customer"
        ],
        "answer": "C",
        "explanation": "Disclosure to family members requires patient authorization unless it's an emergency or the patient is incapacitated and disclosure is in their best interest. Simply verifying identity is insufficient. Maintain a list of authorized representatives for each patient who has granted permission."
    },
    {
        "question": "Which situation requires a breach notification to be sent to patients?",
        "options": [
            "A) A pharmacy employee accidentally views their neighbor's prescription",
            "B) Unencrypted backup tapes containing 1,000 patient records are stolen from a vehicle",
            "C) A fax is sent to a wrong number but retrieved within 5 minutes",
            "D) Paper prescription is found on the floor but no one accessed it"
        ],
        "answer": "B",
        "explanation": "Theft of unencrypted media containing PHI is a presumed breach requiring notification. Option A is an impermissible access needing investigation. Options C and D may not require notification if risk assessment shows low probability of compromise and retrieval/containment was immediate."
    },
    {
        "question": "The 'minimum necessary' standard means you should:",
        "options": [
            "A) Never access any patient information",
            "B) Only access the specific PHI needed for your current task",
            "C) Always access complete patient records for context",
            "D) Minimum necessary doesn't apply to pharmacy staff"
        ],
        "answer": "B",
        "explanation": "Minimum necessary requires limiting access, use, and disclosure to only what's needed for the specific purpose. For example, if verifying insurance, you don't need to view the patient's complete medical history. Implement role-based access controls to enforce this."
    },
    {
        "question": "How long must you retain HIPAA training documentation?",
        "options": [
            "A) 1 year from completion",
            "B) 3 years from completion",
            "C) 6 years from creation or last effective date",
            "D) Indefinitely"
        ],
        "answer": "C",
        "explanation": "HIPAA requires retention of training records for 6 years from date of creation or when last in effect, whichever is later. This applies to all policies, procedures, and documentation required by the Privacy and Security Rules."
    },
    {
        "question": "A patient posts a negative review on social media mentioning their prescription. Can you respond with details about their care?",
        "options": [
            "A) Yes - they posted publicly so you can respond publicly",
            "B) Yes - but only to correct factual errors",
            "C) No - responding would be an unauthorized disclosure of PHI",
            "D) Yes - social media is not covered by HIPAA"
        ],
        "answer": "C",
        "explanation": "You cannot disclose PHI on social media even if the patient posted about their own care. Responding with details confirms they are a patient and reveals PHI. Respond generically without confirming their patient status, and direct them to private channels."
    },
    {
        "question": "Encryption is:",
        "options": [
            "A) Required by HIPAA for all ePHI in all circumstances",
            "B) Addressable under the Security Rule (strongly recommended)",
            "C) Only required for transmissions, not stored data",
            "D) Optional if you have good physical security"
        ],
        "answer": "B",
        "explanation": "Encryption is an 'addressable' specification under the Security Rule, meaning it's strongly recommended but not absolutely required. However, if you don't implement encryption, you must document why alternative measures provide equivalent protection. Most experts recommend encryption for all ePHI."
    },
    {
        "question": "You discover that your pharmacy has been transmitting ePHI via unencrypted email for years. This is:",
        "options": [
            "A) Acceptable if marked 'confidential' in subject line",
            "B) A violation requiring immediate self-reporting to OCR",
            "C) Only a problem if someone complains",
            "D) Acceptable for internal emails only"
        ],
        "answer": "B",
        "explanation": "Transmitting ePHI via unencrypted email violates the Security Rule's transmission security requirements. This systematic violation constitutes willful neglect if not corrected promptly. Self-reporting, immediate cessation, and corrective action plan are required. OCR takes systemic violations seriously."
    }
]

# 15-Item Checklist
CHECKLIST_ITEMS = [
    {"text": "Completed Privacy Rule training", "category": "Training"},
    {"text": "Reviewed Security Rule requirements", "category": "Training"},
    {"text": "Understands breach notification timeline (60 days)", "category": "Knowledge"},
    {"text": "Can identify and report unauthorized access", "category": "Knowledge"},
    {"text": "Knows and applies minimum necessary standard", "category": "Knowledge"},
    {"text": "Can identify all 18 types of Protected Health Information", "category": "Knowledge"},
    {"text": "Understands all patient rights under HIPAA", "category": "Knowledge"},
    {"text": "ePHI encrypted at rest (hard drives, servers)", "category": "Technical"},
    {"text": "ePHI encrypted in transit (secure transmissions)", "category": "Technical"},
    {"text": "Audit logs enabled and monitored regularly", "category": "Technical"},
    {"text": "Cross-cut shredders used for all PHI disposal", "category": "Technical"},
    {"text": "Unique login credentials for every staff member", "category": "Technical"},
    {"text": "All staff HIPAA training completed annually", "category": "Compliance"},
    {"text": "Business Associate Agreements signed with vendors", "category": "Compliance"},
    {"text": "Notice of Privacy Practices provided to all patients", "category": "Compliance"}
]

# Initialize checklist
checklist: Dict[str, bool] = {item["text"]: False for item in CHECKLIST_ITEMS}

# Scoring functions
def calculate_score(responses: Dict[str, bool]) -> float:
    """Calculate percentage score from checklist responses"""
    completed = sum(responses.values())
    total = len(responses)
    return (completed / total) * 100 if total > 0 else 0.0

def get_performance_feedback(percentage: float) -> str:
    """Generate performance feedback based on score"""
    if percentage >= PASS_THRESHOLD:
        return "Excellent! You're HIPAA compliant!"
    elif percentage >= GOOD_THRESHOLD:
        return "Good progress! Review areas needing improvement."
    else:
        return "Critical gaps identified. Immediate action required."

# Main functions
def show_lessons() -> None:
    """Display all HIPAA lessons"""
    print("\n" + "="*70)
    print("HIPAA LESSONS (13 Complete Topics)")
    print("="*70)
    
    for i, (topic, data) in enumerate(LESSONS.items(), 1):
        print(f"\n[{i}/13] {topic}")
        print("-" * 70)
        print(data["content"])
        print("\nKey Points:")
        for point in data["key_points"]:
            print(f"  • {point}")
    
    print("\n" + "="*70)
    input("Press Enter to continue...")

def take_quiz() -> None:
    """Administer the complete quiz"""
    print("\n" + "="*70)
    print("HIPAA KNOWLEDGE QUIZ (15 Questions)")
    print("="*70)
    
    score = 0
    for i, q in enumerate(QUIZ_QUESTIONS, 1):
        print(f"\nQuestion {i}/15:")
        print(q["question"])
        print()
        for option in q["options"]:
            print(option)
        
        answer = ""
        while answer not in ["A", "B", "C", "D"]:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
        
        if answer == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {q['answer']}")
        
        print(f"\nExplanation: {q['explanation']}")
        print("-" * 70)
    
    percentage = (score / len(QUIZ_QUESTIONS)) * 100
    print(f"\nFinal Score: {score}/{len(QUIZ_QUESTIONS)} ({percentage:.1f}%)")
    print(get_performance_feedback(percentage))
    # Generate certificate if passed
    if percentage >= PASS_THRESHOLD:
        print("\n🎉 Congratulations! You passed!")
        name = input("\nEnter your name for certificate: ").strip()
        if name:
            cert, filename = generate_certificate(name, percentage)
            print(cert)
            print(f"\nCertificate saved to: {filename}")
    input("\nPress Enter to continue...")

def main() -> None:
    """Main application loop"""
    show_welcome()  # Add this line
    
    while True:
    
    for item_data in CHECKLIST_ITEMS:
        text = item_data["text"]
        category = item_data["category"]
        
        response = ""
        while response not in ["y", "n", "yes", "no"]:
            response = input(f"\n[{category}] {text}? (yes/no): ").strip().lower()
        
        checklist[text] = response in ["y", "yes"]
    
    print("\nChecklist completed!")
    input("Press Enter to continue...")
# Offer CSV export
    export = input("\nExport report to CSV? (yes/no): ").strip().lower()
    if export in ['y', 'yes']:
        export_report_csv()
def generate_report() -> None:
    """Generate compliance report"""
    print("\n" + "="*70)
    print("COMPLIANCE REPORT")
    print("="*70)
    
    completed = sum(checklist.values())
    total = len(checklist)
    percentage = calculate_score(checklist)
    
    print(f"\nOverall Compliance: {completed}/{total} ({percentage:.1f}%)")
    print(f"Status: {get_performance_feedback(percentage)}")
    
    # Category breakdown
    categories = {}
    for item_data in CHECKLIST_ITEMS:
        cat = item_data["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "completed": 0}
        categories[cat]["total"] += 1
        if checklist[item_data["text"]]:
            categories[cat]["completed"] += 1
    
    print("\nBy Category:")
    for cat, stats in categories.items():
        cat_pct = (stats["completed"] / stats["total"]) * 100
        print(f"  {cat}: {stats['completed']}/{stats['total']} ({cat_pct:.0f}%)")
    def export_report_csv() -> None:
    """Export compliance report as CSV"""
    import csv
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"hipaa_compliance_report_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Item', 'Status', 'Compliant'])
            
            for item_data in CHECKLIST_ITEMS:
                text = item_data["text"]
                category = item_data["category"]
                status = 'YES' if checklist[text] else 'NO'
                compliant = '✓' if checklist[text] else '✗'
                writer.writerow([category, text, status, compliant])
        
        print(f"\n✓ Report exported to: {filename}")
        return filename
    except Exception as e:
        print(f"\n✗ Error exporting report: {e}")
        return None
    print("\nDetailed Checklist:")
    for item_data in CHECKLIST_ITEMS:
        text = item_data["text"]
        status = "✓" if checklist[text] else "✗"
        print(f"  [{status}] {text}")
    def generate_certificate(name: str, score: float) -> str:
    """Generate text certificate"""
    cert_id = datetime.now().strftime('%Y%m%d%H%M%S')
    cert = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    CERTIFICATE OF COMPLETION                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  This certifies that                                             ║
║                                                                   ║
║  {name:^63}  ║
║                                                                   ║
║  has successfully completed the HIPAA Training System V2.0       ║
║  for Pharmacy Staff with a score of {score:.1f}%                    ║
║                                                                   ║
║  Date: {datetime.now().strftime('%B %d, %Y'):^54}  ║
║  Certificate ID: {cert_id:^46}  ║
║                                                                   ║
║  Valid for 12 months from issue date                             ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    """
    
    # Save to file
    filename = f"HIPAA_Certificate_{cert_id}.txt"
    with open(filename, 'w') as f:
        f.write(cert)
    
    return cert, filename
    # Save progress
    try:
        progress = {
            "timestamp": datetime.now().isoformat(),
            "checklist": checklist,
            "compliance_score": f"{completed}/{total}",
            "percentage": percentage
        }
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
        print(f"\nProgress saved to {PROGRESS_FILE}")
    except Exception as e:
        print(f"\nWarning: Could not save progress: {e}")
    
    input("\nPress Enter to continue...")

def main() -> None:
    """Main application loop"""
    print("="*70)
    print("HIPAA TRAINING SYSTEM V2.0")
    print("Complete Training for Pharmacy Staff")
    print("="*70)
    
    while True:
        print("\nMAIN MENU")
        print("1. View All Lessons (13 topics)")
        print("2. Take Knowledge Quiz (15 questions)")
        print("3. Complete Compliance Checklist (15 items)")
        print("4. Generate Compliance Report")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            show_lessons()
        elif choice == "2":
            take_quiz()
        elif choice == "3":
            complete_checklist()
        elif choice == "4":
            generate_report()
        elif choice == "5":
            print("\nThank you for completing HIPAA training!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\nError: {e}")
