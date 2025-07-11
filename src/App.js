import React, { useState } from 'react';
import './App.css';
import MatchTable from './components/MatchTable';
import PreviousResults from './components/PreviousResults';
import TodayPredictions from './components/TodayPredictions';

function App() {
  const [activeTab, setActiveTab] = useState('today');

  const renderContent = () => {
    switch(activeTab) {
      case 'today':
        return <TodayPredictions />;
      case 'upcoming':
        return <MatchTable />;
      case 'results':
        return <PreviousResults />;
      default:
        return <TodayPredictions />;
    }
  };

  return (
    <div className="App">
      <nav className="main-nav">
        <div className="nav-brand">
          <h1>🚀 Ultra Football Predictor</h1>
        </div>
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${activeTab === 'today' ? 'active' : ''}`}
            onClick={() => setActiveTab('today')}
          >
            🔥 Today
          </button>
          <button 
            className={`nav-tab ${activeTab === 'upcoming' ? 'active' : ''}`}
            onClick={() => setActiveTab('upcoming')}
          >
            📅 Upcoming
          </button>
          <button 
            className={`nav-tab ${activeTab === 'results' ? 'active' : ''}`}
            onClick={() => setActiveTab('results')}
          >
            📊 Results
          </button>
        </div>
      </nav>
      
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
