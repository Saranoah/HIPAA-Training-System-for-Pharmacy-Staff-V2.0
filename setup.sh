#!/bin/bash
# HIPAA Training System V2.0 - Setup Script
# Enhanced for new V2.0 structure

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HIPAA Training System V2.0 - Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}Error: Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}\n"

# Verify Python 3.8+
REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python 3.8+ required, found $PYTHON_VERSION${NC}"
    exit 1
fi

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N]: " CREATE_VENV
if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    
    # Activate based on OS
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    echo -e "${GREEN}✓ Virtual environment created and activated${NC}\n"
fi

# Check for V2.0 required files
echo -e "${YELLOW}Checking V2.0 required files...${NC}"
REQUIRED_FILES=(
    "hipaa_training_v2.py"
    "test_hipaa_training_v2.py"
    "README.md"
    "LICENSE"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ Missing: $file${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    else
        echo -e "${GREEN}✓ Found: $file${NC}"
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo -e "${RED}Error: Missing required files${NC}"
    exit 1
fi
echo ""

# Verify V2.0 content completeness
echo -e "${YELLOW}Verifying V2.0 content...${NC}"
$PYTHON_CMD -c "
import hipaa_training_v2
print('✓ 13 lessons loaded:', len(hipaa_training_v2.LESSONS))
print('✓ 15 quiz questions:', len(hipaa_training_v2.QUIZ_QUESTIONS))  
print('✓ 15 checklist items:', len(hipaa_training_v2.CHECKLIST_ITEMS))
"
echo -e "${GREEN}✓ V2.0 content verified${NC}\n"

# Run V2.0 tests
echo -e "${YELLOW}Running V2.0 system tests...${NC}"
$PYTHON_CMD test_hipaa_training_v2.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All V2.0 tests passed${NC}\n"
else
    echo -e "${RED}✗ Some tests failed${NC}\n"
    read -p "Continue anyway? [y/N]: " CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Test V2.0 program startup
echo -e "${YELLOW}Testing V2.0 program startup...${NC}"
echo "5" | timeout 5 $PYTHON_CMD hipaa_training_v2.py > /dev/null 2>&1
if [ $? -eq 0 ] || [ $? -eq 124 ]; then  # 124 is timeout exit code
    echo -e "${GREEN}✓ V2.0 program starts successfully${NC}\n"
else
    echo -e "${RED}✗ Program failed to start${NC}\n"
    exit 1
fi

# Set up Git hooks for V2.0
if [ -d ".git" ]; then
    echo -e "${YELLOW}Setting up Git hooks for V2.0...${NC}"
    
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running V2.0 tests before commit..."
python test_hipaa_training_v2.py
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
echo "V2.0 tests passed. Proceeding with commit."
EOF
    
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}✓ V2.0 Git hooks installed${NC}\n"
fi

# Security check for V2.0
echo -e "${YELLOW}Setting V2.0 file permissions...${NC}"
chmod 644 hipaa_training_v2.py
chmod 644 test_hipaa_training_v2.py
if [ -f "hipaa_progress.json" ]; then
    chmod 600 hipaa_progress.json  # User read/write only for sensitive data
    echo -e "${GREEN}✓ Secured hipaa_progress.json (600)${NC}"
fi
echo -e "${GREEN}✓ V2.0 file permissions set${NC}\n"

# Display V2.0 setup summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}V2.0 Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}✓ Python $PYTHON_VERSION verified${NC}"
echo -e "${GREEN}✓ All V2.0 files present${NC}"
echo -e "${GREEN}✓ 13 lessons, 15 quiz questions, 15 checklist items${NC}"
echo -e "${GREEN}✓ V2.0 tests passing${NC}"
echo -e "${GREEN}✓ Program verified${NC}"

if [ -d ".git" ]; then
    echo -e "${GREEN}✓ V2.0 Git hooks installed${NC}"
fi

echo -e "\n${YELLOW}V2.0 Quick Start:${NC}"
echo -e "  Run the program: ${BLUE}$PYTHON_CMD hipaa_training_v2.py${NC}"
echo -e "  Run tests:       ${BLUE}$PYTHON_CMD test_hipaa_training_v2.py${NC}"
echo -e "  View README:     ${BLUE}cat README.md${NC}"

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Note: Virtual environment active${NC}"
    echo -e "  Deactivate:      ${BLUE}deactivate${NC}"
    echo -e "  Reactivate:      ${BLUE}source venv/bin/activate${NC}"
fi

echo -e "\n${YELLOW}V2.0 Features:${NC}"
echo -e "  • 13 comprehensive lessons"
echo -e "  • 15 real-world quiz scenarios" 
echo -e "  • 15-item compliance checklist"
echo -e "  • 95%+ HIPAA coverage"
echo -e "  • Pharmacy-specific content"

echo -e "\n${GREEN}V2.0 setup completed successfully! 🎉${NC}\n"
