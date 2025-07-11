#!/bin/bash

# 🚀 Quick Deploy Script for Football Predictor
# Usage: ./quick_deploy.sh "Your commit message"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Football Predictor Quick Deploy${NC}"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo -e "${RED}❌ Error: Not in project directory!${NC}"
    echo -e "${YELLOW}💡 Run: cd /Users/80090/Desktop/Project/untitle${NC}"
    exit 1
fi

# Get commit message
if [ -z "$1" ]; then
    COMMIT_MSG="🚀 Quick update $(date '+%Y-%m-%d %H:%M')"
else
    COMMIT_MSG="$1"
fi

echo -e "${BLUE}📝 Commit message: ${NC}$COMMIT_MSG"

# Check git status
echo -e "\n${BLUE}📊 Checking git status...${NC}"
git status --short

# Add all files
echo -e "\n${BLUE}📦 Adding files...${NC}"
git add .

# Commit
echo -e "\n${BLUE}💾 Committing changes...${NC}"
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Commit successful!${NC}"
else
    echo -e "${YELLOW}⚠️  Nothing to commit or commit failed${NC}"
fi

# Push to main
echo -e "\n${BLUE}🚀 Pushing to GitHub...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Push successful!${NC}"
    echo -e "\n${GREEN}🌐 Website will be updated at:${NC}"
    echo -e "${BLUE}   https://tuckkiez.github.io/untitled/${NC}"
    echo -e "\n${GREEN}📊 Check deployment status:${NC}"
    echo -e "${BLUE}   https://github.com/tuckkiez/untitled/actions${NC}"
else
    echo -e "${RED}❌ Push failed!${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 Deployment complete!${NC}"
