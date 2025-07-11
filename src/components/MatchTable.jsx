import React, { useState, useEffect } from 'react';
import './MatchTable.css';

const MatchTable = () => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // จำลองข้อมูลการทำนายที่จะมาถึง
    const upcomingMatches = [
      {
        id: 1,
        homeTeam: 'Arsenal',
        awayTeam: 'Chelsea',
        league: 'Premier League',
        date: '2025-07-12',
        time: '16:30',
        matchResult: { prediction: 'Arsenal Win', confidence: 68 },
        handicap: { prediction: 'Arsenal -0.5', confidence: 65 },
        overUnder: { prediction: 'Over 2.5', confidence: 72 },
        corners: { prediction: 'Over 10.5', confidence: 75 }
      },
      {
        id: 2,
        homeTeam: 'Manchester City',
        awayTeam: 'Liverpool',
        league: 'Premier League',
        date: '2025-07-13',
        time: '14:00',
        matchResult: { prediction: 'Draw', confidence: 55 },
        handicap: { prediction: 'Liverpool +0.5', confidence: 58 },
        overUnder: { prediction: 'Over 3.5', confidence: 80 },
        corners: { prediction: 'Over 11.5', confidence: 85 }
      },
      {
        id: 3,
        homeTeam: 'Real Madrid',
        awayTeam: 'Barcelona',
        league: 'La Liga',
        date: '2025-07-14',
        time: '20:00',
        matchResult: { prediction: 'Real Madrid Win', confidence: 70 },
        handicap: { prediction: 'Real Madrid -1', confidence: 67 },
        overUnder: { prediction: 'Over 2.5', confidence: 78 },
        corners: { prediction: 'Over 9.5', confidence: 73 }
      }
    ];

    setTimeout(() => {
      setMatches(upcomingMatches);
      setLoading(false);
    }, 1000);
  }, []);

  const getConfidenceColor = (confidence) => {
    if (confidence >= 70) return '#22c55e';
    if (confidence >= 60) return '#eab308';
    return '#ef4444';
  };

  if (loading) {
    return (
      <div className="match-table-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading upcoming predictions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="match-table-container">
      <div className="header-section">
        <h1 className="page-title">
          <span className="title-icon">📅</span>
          Upcoming Predictions
        </h1>
        <p className="subtitle">AI-powered predictions for upcoming matches</p>
      </div>

      <div className="matches-grid">
        {matches.map((match) => (
          <div key={match.id} className="match-card">
            <div className="match-header">
              <div className="match-info">
                <h3 className="match-title">
                  {match.homeTeam} vs {match.awayTeam}
                </h3>
                <div className="match-details">
                  <span className="league">{match.league}</span>
                  <span className="datetime">📅 {match.date} 🕐 {match.time}</span>
                </div>
              </div>
            </div>

            <div className="predictions-grid">
              <div className="prediction-card">
                <h4>Match Result</h4>
                <div className="prediction-value">{match.matchResult.prediction}</div>
                <div 
                  className="confidence-bar"
                  style={{ backgroundColor: getConfidenceColor(match.matchResult.confidence) }}
                >
                  {match.matchResult.confidence}%
                </div>
              </div>

              <div className="prediction-card">
                <h4>Handicap</h4>
                <div className="prediction-value">{match.handicap.prediction}</div>
                <div 
                  className="confidence-bar"
                  style={{ backgroundColor: getConfidenceColor(match.handicap.confidence) }}
                >
                  {match.handicap.confidence}%
                </div>
              </div>

              <div className="prediction-card">
                <h4>Over/Under</h4>
                <div className="prediction-value">{match.overUnder.prediction}</div>
                <div 
                  className="confidence-bar"
                  style={{ backgroundColor: getConfidenceColor(match.overUnder.confidence) }}
                >
                  {match.overUnder.confidence}%
                </div>
              </div>

              <div className="prediction-card">
                <h4>Corners</h4>
                <div className="prediction-value">{match.corners.prediction}</div>
                <div 
                  className="confidence-bar"
                  style={{ backgroundColor: getConfidenceColor(match.corners.confidence) }}
                >
                  {match.corners.confidence}%
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MatchTable;
