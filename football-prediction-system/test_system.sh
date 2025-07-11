#!/bin/bash

echo "🧪 Testing Football Prediction System"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test backend health
echo -e "\n${YELLOW}1. Testing Backend Health...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:3001/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${RED}❌ Backend is not running${NC}"
    echo "Please start backend: cd backend && npm run dev"
    exit 1
fi

# Test admin matches endpoint
echo -e "\n${YELLOW}2. Testing Admin Matches API...${NC}"
MATCHES_RESPONSE=$(curl -s http://localhost:3001/api/admin/matches 2>/dev/null)
if echo "$MATCHES_RESPONSE" | grep -q '"success":true'; then
    MATCH_COUNT=$(echo "$MATCHES_RESPONSE" | grep -o '"total":[0-9]*' | cut -d':' -f2)
    echo -e "${GREEN}✅ Admin API working - Found $MATCH_COUNT matches${NC}"
else
    echo -e "${RED}❌ Admin API not working${NC}"
fi

# Test leagues endpoint
echo -e "\n${YELLOW}3. Testing Leagues API...${NC}"
LEAGUES_RESPONSE=$(curl -s http://localhost:3001/api/leagues 2>/dev/null)
if echo "$LEAGUES_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ Leagues API working${NC}"
else
    echo -e "${RED}❌ Leagues API not working${NC}"
fi

# Test categories endpoint
echo -e "\n${YELLOW}4. Testing Categories API...${NC}"
CATEGORIES_RESPONSE=$(curl -s http://localhost:3001/api/admin/categories 2>/dev/null)
if echo "$CATEGORIES_RESPONSE" | grep -q 'MATCH_RESULT'; then
    echo -e "${GREEN}✅ Categories API working${NC}"
else
    echo -e "${RED}❌ Categories API not working${NC}"
fi

# Test database
echo -e "\n${YELLOW}5. Testing Database...${NC}"
if [ -f "backend/football_predictions.db" ]; then
    echo -e "${GREEN}✅ Database file exists${NC}"
else
    echo -e "${RED}❌ Database file not found${NC}"
fi

echo -e "\n${GREEN}🎉 System Test Complete!${NC}"
echo -e "\n${YELLOW}📋 Next Steps:${NC}"
echo "1. Backend is running on: http://localhost:3001"
echo "2. Start frontend: cd frontend && npm start"
echo "3. Open: http://localhost:3000"
echo "4. Click ⚙️ button for Admin Panel"
