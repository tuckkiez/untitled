#!/bin/bash

echo "🏆 Football Prediction System Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js found: $(node --version)${NC}"

# Setup Backend
echo -e "\n${BLUE}🔧 Setting up Backend...${NC}"
cd backend

# Install dependencies
echo "📦 Installing backend dependencies..."
npm install

# Setup environment
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️ Please edit backend/.env with your API keys${NC}"
fi

# Setup database
echo "🗄️ Setting up database..."
npx prisma generate
npx prisma migrate dev --name init

echo -e "${GREEN}✅ Backend setup complete!${NC}"

# Setup Frontend
echo -e "\n${BLUE}🎨 Setting up Frontend...${NC}"
cd ../frontend

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Setup environment
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
fi

echo -e "${GREEN}✅ Frontend setup complete!${NC}"

# Back to root
cd ..

echo -e "\n${GREEN}🎉 Setup Complete!${NC}"
echo -e "\n${BLUE}📋 Next Steps:${NC}"
echo "1. Edit backend/.env with your API keys:"
echo "   - FOOTBALL_DATA_API_KEY=052fd4885cf943ad859c89cef542e2e5"
echo "   - API_SPORTS_KEY=9936a2866ebc7271a809ff2ab164b032"
echo ""
echo "2. Start the backend:"
echo "   cd backend && npm run dev"
echo ""
echo "3. Start the frontend (in new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}💡 Admin Panel: Click the ⚙️ button in the bottom-right corner${NC}"
echo -e "${GREEN}🚀 Happy predicting!${NC}"
