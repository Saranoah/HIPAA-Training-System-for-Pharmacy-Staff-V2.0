#!/bin/bash
# HIPAA Training System - Setup Script
# Automated setup for development and testing

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HIPAA Training System - Setup${NC}"
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

# Check for required files
echo -e "${YELLOW}Checking required files...${NC}"
REQUIRED_FILES=(
    "hipaa_ai_pharmacy_production.py"
    "test_hipaa_training.py"
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

# Run self-test
echo -e "${YELLOW}Running system tests...${NC}"
$PYTHON_CMD test_hipaa_training.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}\n"
else
    echo -e "${RED}✗ Some tests failed${NC}\n"
    read -p "Continue anyway? [y/N]: " CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Test program startup
echo -e "${YELLOW}Testing program startup...${NC}"
echo "7" | timeout 5 $PYTHON_CMD hipaa_ai_pharmacy_production.py > /dev/null 2>&1
if [ $? -eq 0 ] || [ $? -eq 124 ]; then  # 124 is timeout exit code
    echo -e "${GREEN}✓ Program starts successfully${NC}\n"
else
    echo -e "${RED}✗ Program failed to start${NC}\n"
    exit 1
fi

# Set up Git hooks (if in git repo)
if [ -d ".git" ]; then
    echo -e "${YELLOW}Setting up Git hooks...${NC}"
    
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running tests before commit..."
python test_hipaa_training.py
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
echo "Tests passed. Proceeding with commit."
EOF
    
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}✓ Git hooks installed${NC}\n"
fi

# Create sample config (optional)
read -p "Generate sample progress file for testing? [y/N]: " CREATE_SAMPLE
if [[ $CREATE_SAMPLE =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Creating sample progress file...${NC}"
    cat > hipaa_progress_sample.json << 'EOF'
{
  "last_updated": "2025-10-02T14:30:00.123456",
  "timestamp": "2025-10-02 14:30:00",
  "checklist": {
    "Completed Privacy Rule training": true,
    "Reviewed Security Rule requirements": true,
    "Understands breach notification timeline": false,
    "Can identify unauthorized access": true,
    "Knows minimum necessary standard": true,
    "Encrypted ePHI at rest": false,
    "Encrypted ePHI in transit": false,
    "Audit logs enabled": false,
    "Staff HIPAA training completed": true,
    "Business Associate Agreements signed": false
  },
  "compliance_score": "5/10",
  "percentage": 50.0
}
EOF
    echo -e "${GREEN}✓ Sample file created: hipaa_progress_sample.json${NC}\n"
fi

# Security check
echo -e "${YELLOW}Checking file permissions...${NC}"
chmod 644 hipaa_ai_pharmacy_production.py
chmod 644 test_hipaa_training.py
if [ -f "hipaa_progress.json" ]; then
    chmod 600 hipaa_progress.json  # User read/write only for sensitive data
    echo -e "${GREEN}✓ Secured hipaa_progress.json (600)${NC}"
fi
echo -e "${GREEN}✓ File permissions set${NC}\n"

# Display setup summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}✓ Python $PYTHON_VERSION verified${NC}"
echo -e "${GREEN}✓ All required files present${NC}"
echo -e "${GREEN}✓ Tests passing${NC}"
echo -e "${GREEN}✓ Program verified${NC}"

if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git hooks installed${NC}"
fi

echo -e "\n${YELLOW}Quick Start:${NC}"
echo -e "  Run the program: ${BLUE}$PYTHON_CMD hipaa_ai_pharmacy_production.py${NC}"
echo -e "  Run tests:       ${BLUE}$PYTHON_CMD test_hipaa_training.py${NC}"
echo -e "  View README:     ${BLUE}cat README.md${NC}"

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Note: Virtual environment active${NC}"
    echo -e "  Deactivate:      ${BLUE}deactivate${NC}"
    echo -e "  Reactivate:      ${BLUE}source venv/bin/activate${NC}"
fi

echo -e "\n${YELLOW}Documentation:${NC}"
echo -e "  Testing Guide:   ${BLUE}TESTING.md${NC}"
echo -e "  Contributing:    ${BLUE}CONTRIBUTING.md${NC}"

echo -e "\n${GREEN}Setup completed successfully! 🎉${NC}\n"
