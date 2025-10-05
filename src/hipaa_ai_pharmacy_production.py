# hipaa_ai_pharmacy_production.py
"""
PRODUCTION-READY HIPAA AI Learning & Self-Check System for Pharmacy Staff
Enhanced with type hints, constants, robust error handling, and testing structure.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# -----------------------------
# CONSTANTS (Improvement #1)
# -----------------------------
PASS_THRESHOLD: int = 80
GOOD_THRESHOLD: int = 60
PROGRESS_FILE: str = "hipaa_progress.json"
MAX_QUIZ_ATTEMPTS: int = 3

# -----------------------------
# Enhanced lessons data structure
# -----------------------------
lessons: Dict[str, Dict[str, Any]] = {
    "Privacy Rule": {
        "content": "HIPAA Privacy Rule protects patient information and requires minimum necessary use.",
        "key_points": ["Patient authorization", "Minimum necessary", "Patient rights"]
    },
    "Security Rule": {
        "content": "HIPAA Security Rule requires administrative, physical, and technical safeguards for ePHI.",
        "key_points": ["Encryption", "Access controls", "Audit trails"]
    },
    "Breach Notification": {
        "content": "HIPAA requires notifying affected patients and HHS within 60 days if PHI is breached.",
        "key_points": ["60-day timeline", "Patient notification", "HHS reporting"]
    }
}

# -----------------------------
# Self-audit checklist
# -----------------------------
checklist: Dict[str, bool] = {
    "Completed Privacy Rule training": False,
    "Reviewed Security Rule requirements": False,
    "Understands breach notification timeline": False,
    "Can identify unauthorized access": False,
    "Knows minimum necessary standard": False,
    "Encrypted ePHI at rest": False,
    "Encrypted ePHI in transit": False,
    "Audit logs enabled": False,
    "Staff HIPAA training completed": False,
    "Business Associate Agreements signed": False
}

# -----------------------------
# Multiple scenarios (enhanced)
# -----------------------------
scenarios: List[Dict[str, Any]] = [
    {
        "question": "A pharmacy technician accidentally emails a patient prescription to the wrong email address. What should they do?",
        "options": [
            "A) Ignore and delete the email",
            "B) Notify the patient and supervisor immediately", 
            "C) Report only if the patient complains"
        ],
        "answer": "B",
        "explanation": "Immediate notification allows for proper breach documentation and mitigation."
    },
    {
        "question": "You notice a coworker looking at patient records without a work-related purpose. What action should you take?",
        "options": [
            "A) Ignore it - it's not your business",
            "B) Report to privacy officer immediately",
            "C) Confront them privately first"
        ],
        "answer": "B",
        "explanation": "Unauthorized access must be reported to maintain compliance and patient trust."
    },
    {
        "question": "A patient asks for their entire medical record. Under minimum necessary standard, you should:",
        "options": [
            "A) Provide everything without question",
            "B) Provide only what's needed for their current request",
            "C) Refuse the request entirely"
        ],
        "answer": "B",
        "explanation": "Minimum necessary means providing only the information needed for the specific purpose."
    }
]

# -----------------------------
# SCORING & CALCULATION FUNCTIONS (Improvement #4)
# -----------------------------

def calculate_score(responses: Dict[str, bool]) -> float:
    """Calculate percentage score from checklist responses."""
    completed = sum(responses.values())
    total = len(responses)
    return (completed / total) * 100 if total > 0 else 0.0

def calculate_quiz_score(correct_answers: int, total_questions: int) -> float:
    """Calculate quiz score percentage."""
    return (correct_answers / total_questions) * 100 if total_questions > 0 else 0.0

def get_performance_feedback(percentage: float) -> str:
    """Generate performance feedback based on score thresholds."""
    if percentage >= PASS_THRESHOLD:
        return "🎉 Excellent! You're HIPAA ready!"
    elif percentage >= GOOD_THRESHOLD:
        return "📚 Good effort! Review the lessons and try again."
    else:
        return "📖 Keep studying! Focus on the key concepts."

# -----------------------------
# CORE APPLICATION FUNCTIONS
# -----------------------------

def enhanced_show_lessons() -> None:
    """Show all HIPAA lessons with key points."""
    print("\n--- HIPAA Lessons ---")
    for topic, data in lessons.items():
        print(f"\n{topic}:")
        print(f"Content: {data['content']}")
        print("Key Points:")
        for point in data['key_points']:
            print(f"  • {point}")
    print("\n[End of Lessons]")

def quiz_checklist() -> None:
    """Interactive checklist completion with input validation."""
    print("\n--- Self-Audit Checklist ---")
    print("Answer 'yes' or 'no' for each item:\n")
    
    for item in checklist:
        attempts = 0
        while attempts < MAX_QUIZ_ATTEMPTS:
            response = input(f"{item}? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                checklist[item] = True
                break
            elif response in ['no', 'n']:
                checklist[item] = False
                break
            else:
                attempts += 1
                remaining_attempts = MAX_QUIZ_ATTEMPTS - attempts
                if remaining_attempts > 0:
                    print(f"Please enter 'yes' or 'no'. {remaining_attempts} attempts remaining.")
                else:
                    print("Maximum attempts reached. Moving to next item.")
                    checklist[item] = False  # Default to non-compliant
                    break
    
    print("\n✅ Checklist completed!")

def take_quiz() -> None:
    """Scenario-based quiz with enhanced error handling and scoring."""
    print("\n--- HIPAA Scenario Quiz ---")
    score = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario['question']}")
        for option in scenario['options']:
            print(f"  {option}")
        
        attempts = 0
        while attempts < MAX_QUIZ_ATTEMPTS:
            answer = input("\nYour answer (A/B/C): ").strip().upper()
            if answer in ['A', 'B', 'C']:
                break
            else:
                attempts += 1
                remaining_attempts = MAX_QUIZ_ATTEMPTS - attempts
                if remaining_attempts > 0:
                    print(f"Please enter A, B, or C. {remaining_attempts} attempts remaining.")
                else:
                    print("Maximum attempts reached. Moving to next question.")
                    answer = ""  # Empty answer for incorrect
                    break
        
        if answer == scenario['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {scenario['answer']}")
        
        print(f"Explanation: {scenario['explanation']}\n")
        print("-" * 50)
    
    percentage = calculate_quiz_score(score, len(scenarios))
    print(f"\nQuiz Score: {score}/{len(scenarios)} ({percentage:.1f}%)")
    print(get_performance_feedback(percentage))

def save_checklist_progress() -> bool:
    """Save progress to JSON file with comprehensive error handling."""
    try:
        progress = {
            "last_updated": datetime.now().isoformat(),
            "checklist": checklist,
            "compliance_score": f"{sum(checklist.values())}/{len(checklist)}",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "percentage": calculate_score(checklist)
        }
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
        return True
    except IOError as e:
        print(f"❌ File I/O Error saving progress: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error saving progress: {e}")
        return False

def enhanced_generate_report() -> None:
    """Generate compliance report with enhanced metrics."""
    print("\n--- HIPAA Self-Check Report ---")
    
    completed = sum(checklist.values())
    total = len(checklist)
    percentage = calculate_score(checklist)
    
    print(f"Overall Compliance: {completed}/{total} ({percentage:.1f}%)")
    print("\nChecklist Items:")
    
    for item, status in checklist.items():
        print(f"  {'✅' if status else '❌'} {item}")
    
    print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Save progress
    if save_checklist_progress():
        print("💾 Progress saved to hipaa_progress.json")
    
    # Recommendations based on constants
    if percentage == 100:
        print("\n🎉 Perfect compliance! Maintain these standards.")
    elif percentage >= PASS_THRESHOLD:
        print(f"\n📈 Excellent! You've passed the {PASS_THRESHOLD}% threshold.")
    elif percentage >= GOOD_THRESHOLD:
        print(f"\n📈 Good progress! Focus on reaching {PASS_THRESHOLD}% compliance.")
    else:
        print(f"\n⚠️  Needs attention! Prioritize HIPAA training to reach {GOOD_THRESHOLD}%.")

def view_scenario_history() -> None:
    """View previous progress with enhanced exception handling (Improvement #3)."""
    try:
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)
        
        print("\n--- Previous Progress ---")
        print(f"Last audit: {progress.get('timestamp', 'Unknown')}")
        print(f"Previous score: {progress.get('compliance_score', '0/0')}")
        
        percentage = progress.get('percentage', 0)
        print(f"Compliance Percentage: {percentage:.1f}%")
        print(get_performance_feedback(percentage))
        
        print("\nPrevious Checklist Status:")
        for item, status in progress.get('checklist', {}).items():
            print(f"  {'✅' if status else '❌'} {item}")
            
    except FileNotFoundError:
        print("\n📝 No previous progress found. Complete a checklist first!")
    except json.JSONDecodeError:
        print("\n❌ Progress file corrupted. Starting fresh.")
        # Optionally, reset the file or create backup
    except PermissionError:
        print("\n❌ Cannot read progress file. Check file permissions.")
    except Exception as e:
        print(f"\n❌ Unexpected error loading progress: {e}")

# -----------------------------
# TESTING SUPPORT FUNCTIONS (Improvement #4)
# -----------------------------

def run_self_test() -> bool:
    """Run basic self-tests to verify system functionality."""
    print("\n--- System Self-Test ---")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Calculate score function
    total_tests += 1
    test_responses = {"item1": True, "item2": False, "item3": True}
    score = calculate_score(test_responses)
    expected_score = (2/3) * 100
    if abs(score - expected_score) < 0.01:
        print("✅ calculate_score() test passed")
        tests_passed += 1
    else:
        print(f"❌ calculate_score() test failed: got {score}, expected {expected_score}")
    
    # Test 2: Quiz score calculation
    total_tests += 1
    quiz_score = calculate_quiz_score(3, 5)
    expected_quiz_score = 60.0
    if quiz_score == expected_quiz_score:
        print("✅ calculate_quiz_score() test passed")
        tests_passed += 1
    else:
        print(f"❌ calculate_quiz_score() test failed: got {quiz_score}, expected {expected_quiz_score}")
    
    # Test 3: Performance feedback
    total_tests += 1
    feedback = get_performance_feedback(85)
    if "Excellent" in feedback:
        print("✅ get_performance_feedback() test passed")
        tests_passed += 1
    else:
        print(f"❌ get_performance_feedback() test failed")
    
    print(f"\nSelf-test Results: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests

# -----------------------------
# MAIN PROGRAM FLOW
# -----------------------------

def display_welcome() -> None:
    """Display welcome message and system information."""
    print("=" * 60)
    print("=== HIPAA AI Learning & Self-Check System ===")
    print("=" * 60)
    print(f"• Pass Threshold: {PASS_THRESHOLD}%")
    print(f"• Good Threshold: {GOOD_THRESHOLD}%")
    print(f"• Scenarios Available: {len(scenarios)}")
    print(f"• Checklist Items: {len(checklist)}")
    print("Designed for Pharmacy Staff Compliance Training")
    print("=" * 60)

def main() -> None:
    """Main application loop with enhanced menu options."""
    display_welcome()
    
    # Optional: Run self-test on startup
    if input("Run system self-test? (y/n): ").lower() == 'y':
        if not run_self_test():
            print("⚠️  System tests failed. Some features may not work correctly.")
        input("\nPress Enter to continue...")
    
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. View HIPAA Lessons")
        print("2. Complete Self-Audit Checklist") 
        print("3. Take Scenario Quiz")
        print("4. Generate Compliance Report")
        print("5. View Progress History")
        print("6. System Information")
        print("7. Exit Program")
        print("-" * 50)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            enhanced_show_lessons()
        elif choice == "2":
            quiz_checklist()
        elif choice == "3":
            take_quiz()
        elif choice == "4":
            enhanced_generate_report()
        elif choice == "5":
            view_scenario_history()
        elif choice == "6":
            display_welcome()
        elif choice == "7":
            print("\nThank you for using the HIPAA Training System!")
            print("Stay compliant and protect patient privacy! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")
        
        input("\nPress Enter to continue...")

# -----------------------------
# PROGRAM EXECUTION
# -----------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("Please contact system administrator.")
