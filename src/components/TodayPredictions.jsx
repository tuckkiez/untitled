import React, { useState, useEffect } from 'react';
import './TodayPredictions.css';

const TodayPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // จำลองข้อมูลการทำนายวันนี้
    const todayMatches = [
      {
        id: 1,
        homeTeam: 'Aldosivi',
        awayTeam: 'Central Córdoba',
        league: 'Argentina Primera Division',
        time: '01:30',
        matchResult: {
          prediction: 'Central Córdoba Win',
          confidence: 75,
          odds: '2.10'
        },
        handicap: {
          prediction: 'Central Córdoba -0.5',
          confidence: 68,
          odds: '1.85'
        },
        overUnder: {
          prediction: 'Under 2.5',
          confidence: 65,
          odds: '1.75'
        },
        corners: {
          prediction: 'Under 10.5',
          confidence: 70,
          odds: '1.80'
        }
      }
    ];

    setTimeout(() => {
      setPredictions(todayMatches);
      setLoading(false);
    }, 1000);
  }, []);

  const getConfidenceColor = (confidence) => {
    if (confidence >= 70) return '#22c55e'; // เขียว - มั่นใจสูง
    if (confidence >= 60) return '#eab308'; // เหลือง - มั่นใจปานกลาง
    return '#ef4444'; // แดง - มั่นใจต่ำ
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 70) return 'High';
    if (confidence >= 60) return 'Medium';
    return 'Low';
  };

  if (loading) {
    return (
      <div className="today-predictions-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading today's predictions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="today-predictions-container">
      <div className="header-section">
        <h1 className="page-title">
          <span className="title-icon">🔥</span>
          Today's Predictions
        </h1>
        <p className="subtitle">Live predictions for today's matches</p>
      </div>

      <div className="predictions-grid">
        {predictions.map((match) => (
          <div key={match.id} className="match-card">
            {/* Match Header */}
            <div className="match-header">
              <div className="match-info">
                <h3 className="match-title">
                  {match.homeTeam} vs {match.awayTeam}
                </h3>
                <div className="match-details">
                  <span className="league">{match.league}</span>
                  <span className="time">🕐 {match.time}</span>
                </div>
              </div>
            </div>

            {/* Predictions Grid */}
            <div className="predictions-section">
              {/* Match Result */}
              <div className="prediction-item">
                <div className="prediction-header">
                  <h4>Match Result</h4>
                  <span 
                    className="confidence-badge"
                    style={{ backgroundColor: getConfidenceColor(match.matchResult.confidence) }}
                  >
                    {getConfidenceText(match.matchResult.confidence)}
                  </span>
                </div>
                <div className="prediction-content">
                  <div className="prediction-value">{match.matchResult.prediction}</div>
                  <div className="prediction-stats">
                    <span className="confidence">{match.matchResult.confidence}%</span>
                    <span className="odds">@{match.matchResult.odds}</span>
                  </div>
                </div>
              </div>

              {/* Handicap */}
              <div className="prediction-item">
                <div className="prediction-header">
                  <h4>Handicap</h4>
                  <span 
                    className="confidence-badge"
                    style={{ backgroundColor: getConfidenceColor(match.handicap.confidence) }}
                  >
                    {getConfidenceText(match.handicap.confidence)}
                  </span>
                </div>
                <div className="prediction-content">
                  <div className="prediction-value">{match.handicap.prediction}</div>
                  <div className="prediction-stats">
                    <span className="confidence">{match.handicap.confidence}%</span>
                    <span className="odds">@{match.handicap.odds}</span>
                  </div>
                </div>
              </div>

              {/* Over/Under */}
              <div className="prediction-item">
                <div className="prediction-header">
                  <h4>Over/Under</h4>
                  <span 
                    className="confidence-badge"
                    style={{ backgroundColor: getConfidenceColor(match.overUnder.confidence) }}
                  >
                    {getConfidenceText(match.overUnder.confidence)}
                  </span>
                </div>
                <div className="prediction-content">
                  <div className="prediction-value">{match.overUnder.prediction}</div>
                  <div className="prediction-stats">
                    <span className="confidence">{match.overUnder.confidence}%</span>
                    <span className="odds">@{match.overUnder.odds}</span>
                  </div>
                </div>
              </div>

              {/* Corners */}
              <div className="prediction-item">
                <div className="prediction-header">
                  <h4>Corners</h4>
                  <span 
                    className="confidence-badge"
                    style={{ backgroundColor: getConfidenceColor(match.corners.confidence) }}
                  >
                    {getConfidenceText(match.corners.confidence)}
                  </span>
                </div>
                <div className="prediction-content">
                  <div className="prediction-value">{match.corners.prediction}</div>
                  <div className="prediction-stats">
                    <span className="confidence">{match.corners.confidence}%</span>
                    <span className="odds">@{match.corners.odds}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="action-buttons">
              <button className="btn-primary">View Analysis</button>
              <button className="btn-secondary">Live Updates</button>
            </div>
          </div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="summary-section">
        <h3>Today's Summary</h3>
        <div className="summary-stats">
          <div className="stat-item">
            <span className="stat-number">1</span>
            <span className="stat-label">Matches</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">4</span>
            <span className="stat-label">Predictions</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">69.5%</span>
            <span className="stat-label">Avg Confidence</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TodayPredictions;
