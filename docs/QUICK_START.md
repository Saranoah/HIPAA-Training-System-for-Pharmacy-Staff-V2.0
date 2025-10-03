# Quick Start Guide

Get up and running with the HIPAA Training System in 5 minutes.

## 🚀 Installation (3 Steps)

### Step 1: Download

**Option A - Git Clone**:
```bash
git clone https://github.com/yourusername/hipaa-training-system.git
cd hipaa-training-system
```

**Option B - Download ZIP**:
```bash
# Download from https://github.com/yourusername/hipaa-training-system/archive/main.zip
unzip hipaa-training-system-main.zip
cd hipaa-training-system-main
```

### Step 2: Setup

**Linux/Mac**:
```bash
chmod +x setup.sh
./setup.sh
```

**Windows**:
```batch
setup.bat
```

### Step 3: Run

```bash
python hipaa_ai_pharmacy_production.py
```

That's it! 🎉

## 📖 Basic Usage

### Main Menu
```
1. View HIPAA Lessons      ← Study material
2. Complete Checklist      ← Self-audit
3. Take Quiz              ← Test knowledge
4. Generate Report        ← See your score
5. View History           ← Check progress
6. System Info            ← Configuration
7. Exit                   ← Save and quit
```

### Typical Workflow

1. **First Time Users**:
   ```
   Start → View Lessons (1) → Take Quiz (3) → Generate Report (4)
   ```

2. **Regular Training**:
   ```
   Start → Complete Checklist (2) → Generate Report (4) → Exit (7)
   ```

3. **Quick Check**:
   ```
   Start → View History (5) → Exit (7)
   ```

## 🎯 Example Session

```bash
$ python hipaa_ai_pharmacy_production.py

=== HIPAA AI Learning & Self-Check System ===
• Pass Threshold: 80%
• Good Threshold: 60%
• Scenarios Available: 3
• Checklist Items: 10

Run system self-test? (y/n): n

MAIN MENU
1. View HIPAA Lessons
2. Complete Self-Audit Checklist
3. Take Scenario Quiz
4. Generate Compliance Report
5. View Progress History
6. System Information
7. Exit Program

Enter your choice (1-7): 3

--- HIPAA Scenario Quiz ---

Scenario 1: A pharmacy technician accidentally emails...
  A) Ignore and delete the email
  B) Notify the patient and supervisor immediately
  C) Report only if the patient complains

Your answer (A/B/C): B
✅ Correct!
Explanation: Immediate notification allows for proper breach documentation...

Quiz Score: 3/3 (100.0%)
🎉 Excellent! You're HIPAA ready!

Press Enter to continue...
```

## 📊 Understanding Your Scores

### Compliance Checklist
- **100%**: Perfect compliance ✅
- **80-99%**: Excellent, minor gaps
- **60-79%**: Good, needs improvement
- **<60%**: Requires immediate attention ⚠️

### Quiz Performance
- **80%+**: Passing grade 🎉
- **60-79%**: Good effort 📚
- **<60%**: Review lessons 📖

## 💾 Your Data

Progress is saved to `hipaa_progress.json`:

```json
{
  "last_updated": "2025-10-02T14:30:00",
  "compliance_score": "8/10",
  "percentage": 80.0,
  "checklist": { ... }
}
```

**Location**: Same directory as the program  
**Backup**: Copy this file before updates

## 🔧 Common Commands

```bash
# Run program
python hipaa_ai_pharmacy_production.py

# Run tests
python test_hipaa_training.py

# Quick test (exit immediately)
echo "7" | python hipaa_ai_pharmacy_production.py

# Check Python version
python --version

# View help
python hipaa_ai_pharmacy_production.py --help  # (if implemented)
```

## 📱 Keyboard Shortcuts

- **Ctrl+C**: Exit program (graceful shutdown)
- **Enter**: Continue after messages
- **1-7**: Menu navigation
- **A/B/C**: Quiz answers
- **yes/no**: Checklist responses

## ⚡ Pro Tips

1. **Complete lessons first**: Review material before taking quiz
2. **Be honest with checklist**: Accurate self-audit helps identify gaps
3. **Review explanations**: Learn from both correct and incorrect answers
4. **Track progress**: Check history regularly to monitor improvement
5. **Take breaks**: Don't rush through - understanding is key

## 🆘 Quick Troubleshooting

### "Python not found"
```bash
# Install Python 3.8+
# Mac: brew install python3
# Ubuntu: sudo apt install python3
# Windows: Download from python.org
```

### "Permission denied"
```bash
chmod +x hipaa_ai_pharmacy_production.py
# or
python3 hipaa_ai_pharmacy_production.py  # Try python3 instead of python
```

### "Tests failed"
```bash
# Check Python version
python --version  # Must be 3.8+

# Reinstall
rm -rf hipaa-training-system
git clone https://github.com/yourusername/hipaa-training-system.git
```

### "Progress not saving"
```bash
# Check permissions
ls -l hipaa_progress.json

# Ensure write access
touch hipaa_progress.json
```

## 📚 Next Steps

- **Read full documentation**: `cat README.md`
- **Review testing guide**: `cat TESTING.md`
- **Learn to contribute**: `cat CONTRIBUTING.md`
- **Deploy in production**: `cat DEPLOYMENT.md`

## 🎓 Learning Path

### Week 1: Foundation
- Day 1-2: View all lessons
- Day 3-4: Complete checklist
- Day 5: Take quiz, review explanations

### Week 2: Mastery
- Day 1-2: Retake quiz for 100%
- Day 3-4: Review any weak areas
- Day 5: Final assessment

### Week 3: Maintenance
- Weekly: Quick checklist review
- Monthly: Full quiz retake
- Quarterly: Complete refresh

## 📞 Support

- **Documentation**: Check README.md first
- **Issues**: GitHub Issues for bugs
- **Questions**: GitHub Discussions
- **Email**: your.email@example.com

## 📖 Quick Reference Card

```
┌──────────────────────────────────────────┐
│     HIPAA TRAINING QUICK REFERENCE       │
├──────────────────────────────────────────┤
│ SHORTCUTS:                               │
│   Ctrl+C → Exit                          │
│   1-7    → Menu options                  │
│   A/B/C  → Quiz answers                  │
└──────────────────────────────────────────┘
```

---

**Ready to start? Run**: `python hipaa_ai_pharmacy_production.py` 🚀

**Last Updated**: October 2, 2025 START:     python hipaa_ai_*.py          │
│ TEST:      python test_hipaa_*.py        │
│ EXIT:      Choose option 7               │
├──────────────────────────────────────────┤
│ SCORES:                                  │
│   80%+  → Passing ✅                     │
│   60-79% → Good   📚                     │
│   <60%  → Review  📖                     │
├──────────────────────────────────────────┤
│ FILES:                                   │
│   Progress: hipaa_progress.json          │
│   Logs:     hipaa_training_audit.log     │
│   Backup:   hipaa_progress.json.backup   │
├──────────────────────────────────────────┤
│
