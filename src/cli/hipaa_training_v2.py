#!/usr/bin/env python3
"""
HIPAA Training System V2.0 for Pharmacy Staff
Complete CLI application with enhanced content
"""

import json
import os
import csv
from datetime import datetime
from typing import Dict, List, Tuple

from data import LESSONS, QUIZ_QUESTIONS, CHECKLIST_ITEMS

# Constants
PASS_THRESHOLD = 80
GOOD_THRESHOLD = 60
PROGRESS_FILE = "data/hipaa_progress.json"

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

def generate_certificate(name: str, score: float) -> Tuple[str, str]:
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
    filename = f"data/HIPAA_Certificate_{cert_id}.txt"
    os.makedirs("data", exist_ok=True)
    with open(filename, 'w') as f:
        f.write(cert)
    
    return cert, filename

def export_report_csv() -> None:
    """Export compliance report as CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"data/hipaa_compliance_report_{timestamp}.csv"
    
    try:
        os.makedirs("data", exist_ok=True)
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

def complete_checklist() -> None:
    """Interactive checklist completion"""
    print("\n" + "="*70)
    print("COMPLIANCE CHECKLIST (15 Items)")
    print("="*70)
    
    for item_data in CHECKLIST_ITEMS:
        text = item_data["text"]
        category = item_data["category"]
        
        response = ""
        while response not in ["y", "n", "yes", "no"]:
            response = input(f"\n[{category}] {text}? (yes/no): ").strip().lower()
        
        checklist[text] = response in ["y", "yes"]
    
    print("\nChecklist completed!")
    input("Press Enter to continue...")

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
    
    print("\nDetailed Checklist:")
    for item_data in CHECKLIST_ITEMS:
        text = item_data["text"]
        status = "✓" if checklist[text] else "✗"
        print(f"  [{status}] {text}")
    
    # Save progress
    try:
        os.makedirs("data", exist_ok=True)
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
    
    # Offer CSV export
    export = input("\nExport report to CSV? (yes/no): ").strip().lower()
    if export in ['y', 'yes']:
        export_report_csv()
    
    input("\nPress Enter to continue...")

def main() -> None:
    """Main application loop"""
    show_welcome()
    
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

# Initialize checklist
checklist: Dict[str, bool] = {item["text"]: False for item in CHECKLIST_ITEMS}

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\nError: {e}")
