# 🏗️ Football Prediction System - New Architecture

## 📁 Project Structure

```
football-prediction-system/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── Match.js
│   │   │   ├── Prediction.js
│   │   │   └── League.js
│   │   ├── routes/
│   │   │   ├── matches.js
│   │   │   ├── predictions.js
│   │   │   └── admin.js
│   │   ├── controllers/
│   │   │   ├── matchController.js
│   │   │   ├── predictionController.js
│   │   │   └── adminController.js
│   │   ├── services/
│   │   │   ├── apiService.js
│   │   │   ├── predictionService.js
│   │   │   └── dbService.js
│   │   ├── database/
│   │   │   ├── connection.js
│   │   │   └── migrations/
│   │   └── app.js
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   ├── MatchTable/
│   │   │   ├── AdminPanel/
│   │   │   └── common/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   └── Admin.jsx
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   └── public/
└── README.md
```

## 🛠️ Technology Stack

### Backend:
- **Node.js + Express.js**
- **SQLite/PostgreSQL** (Database)
- **Prisma** (ORM)
- **Node-cron** (Scheduled tasks)

### Frontend:
- **React 18**
- **Ant Design** (UI Library)
- **Axios** (API calls)
- **React Query** (Data fetching)
- **Tailwind CSS** (Styling)

## 🗄️ Database Schema

### Tables:
1. **leagues** - League information
2. **matches** - All matches (upcoming + previous)
3. **predictions** - Prediction data
4. **results** - Actual match results
5. **accuracy_stats** - Performance tracking

## 🔄 Data Flow:
1. **API Service** fetches match data
2. **Database** stores everything
3. **Frontend** displays last 2 weeks previous + upcoming
4. **Admin Panel** updates results
5. **Cron Job** moves completed matches to previous
