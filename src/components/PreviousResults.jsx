import React, { useState, useEffect } from 'react';
import './PreviousResults.css';

const PreviousResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({});

  useEffect(() => {
    // จำลองข้อมูลผลการทำนายที่ผ่านมา
    const previousResults = [
      {
        id: 1,
        homeTeam: 'Aldosivi',
        awayTeam: 'Central Córdoba',
        league: 'Argentina Primera Division',
        date: '2025-07-11',
        actualResult: '0-2',
        predictions: {
          matchResult: { prediction: 'Central Córdoba Win', confidence: 75, correct: true },
          handicap: { prediction: 'Central Córdoba -0.5', confidence: 68, correct: true },
          overUnder: { prediction: 'Under 2.5', confidence: 65, correct: true },
          corners: { prediction: 'Under 10.5', confidence: 70, correct: false }
        },
        actualCorners: 11,
        accuracy: 75
      },
      {
        id: 2,
        homeTeam: 'Manchester United',
        awayTeam: 'Tottenham',
        league: 'Premier League',
        date: '2025-07-10',
        actualResult: '2-1',
        predictions: {
          matchResult: { prediction: 'Manchester United Win', confidence: 72, correct: true },
          handicap: { prediction: 'Manchester United -0.5', confidence: 69, correct: true },
          overUnder: { prediction: 'Over 2.5', confidence: 78, correct: true },
          corners: { prediction: 'Over 9.5', confidence: 73, correct: true }
        },
        actualCorners: 12,
        accuracy: 100
      },
      {
        id: 3,
        homeTeam: 'Bayern Munich',
        awayTeam: 'Borussia Dortmund',
        league: 'Bundesliga',
        date: '2025-07-09',
        actualResult: '1-1',
        predictions: {
          matchResult: { prediction: 'Bayern Munich Win', confidence: 68, correct: false },
          handicap: { prediction: 'Bayern Munich -1', confidence: 65, correct: false },
          overUnder: { prediction: 'Over 2.5', confidence: 75, correct: false },
          corners: { prediction: 'Over 10.5', confidence: 80, correct: true }
        },
        actualCorners: 13,
        accuracy: 25
      }
    ];

    // คำนวณสถิติ
    const totalPredictions = previousResults.length * 4;
    const correctPredictions = previousResults.reduce((acc, match) => {
      return acc + Object.values(match.predictions).filter(p => p.correct).length;
    }, 0);

    const calculatedStats = {
      totalMatches: previousResults.length,
      totalPredictions,
      correctPredictions,
      accuracy: Math.round((correctPredictions / totalPredictions) * 100),
      matchResultAccuracy: Math.round((previousResults.filter(m => m.predictions.matchResult.correct).length / previousResults.length) * 100),
      handicapAccuracy: Math.round((previousResults.filter(m => m.predictions.handicap.correct).length / previousResults.length) * 100),
      overUnderAccuracy: Math.round((previousResults.filter(m => m.predictions.overUnder.correct).length / previousResults.length) * 100),
      cornersAccuracy: Math.round((previousResults.filter(m => m.predictions.corners.correct).length / previousResults.length) * 100)
    };

    setTimeout(() => {
      setResults(previousResults);
      setStats(calculatedStats);
      setLoading(false);
    }, 1000);
  }, []);

  const getResultColor = (correct) => {
    return correct ? '#22c55e' : '#ef4444';
  };

  const getAccuracyColor = (accuracy) => {
    if (accuracy >= 75) return '#22c55e';
    if (accuracy >= 50) return '#eab308';
    return '#ef4444';
  };

  if (loading) {
    return (
      <div className="results-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading previous results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-container">
      <div className="header-section">
        <h1 className="page-title">
          <span className="title-icon">📊</span>
          Previous Results
        </h1>
        <p className="subtitle">Track record of our AI predictions</p>
      </div>

      {/* Statistics Summary */}
      <div className="stats-section">
        <h3>Performance Summary</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number" style={{ color: getAccuracyColor(stats.accuracy) }}>
              {stats.accuracy}%
            </div>
            <div className="stat-label">Overall Accuracy</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.totalMatches}</div>
            <div className="stat-label">Matches Analyzed</div>
          </div>
          <div className="stat-card">
            <div className="stat-number" style={{ color: getAccuracyColor(stats.matchResultAccuracy) }}>
              {stats.matchResultAccuracy}%
            </div>
            <div className="stat-label">Match Results</div>
          </div>
          <div className="stat-card">
            <div className="stat-number" style={{ color: getAccuracyColor(stats.cornersAccuracy) }}>
              {stats.cornersAccuracy}%
            </div>
            <div className="stat-label">Corners</div>
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="results-grid">
        {results.map((match) => (
          <div key={match.id} className="result-card">
            <div className="match-header">
              <div className="match-info">
                <h3 className="match-title">
                  {match.homeTeam} vs {match.awayTeam}
                </h3>
                <div className="match-details">
                  <span className="league">{match.league}</span>
                  <span className="date">📅 {match.date}</span>
                  <span className="score">⚽ {match.actualResult}</span>
                </div>
              </div>
              <div 
                className="accuracy-badge"
                style={{ backgroundColor: getAccuracyColor(match.accuracy) }}
              >
                {match.accuracy}%
              </div>
            </div>

            <div className="predictions-results">
              <div className="prediction-result">
                <h4>Match Result</h4>
                <div className="prediction-info">
                  <span className="prediction">{match.predictions.matchResult.prediction}</span>
                  <span 
                    className="result-indicator"
                    style={{ color: getResultColor(match.predictions.matchResult.correct) }}
                  >
                    {match.predictions.matchResult.correct ? '✅' : '❌'}
                  </span>
                </div>
              </div>

              <div className="prediction-result">
                <h4>Handicap</h4>
                <div className="prediction-info">
                  <span className="prediction">{match.predictions.handicap.prediction}</span>
                  <span 
                    className="result-indicator"
                    style={{ color: getResultColor(match.predictions.handicap.correct) }}
                  >
                    {match.predictions.handicap.correct ? '✅' : '❌'}
                  </span>
                </div>
              </div>

              <div className="prediction-result">
                <h4>Over/Under</h4>
                <div className="prediction-info">
                  <span className="prediction">{match.predictions.overUnder.prediction}</span>
                  <span 
                    className="result-indicator"
                    style={{ color: getResultColor(match.predictions.overUnder.correct) }}
                  >
                    {match.predictions.overUnder.correct ? '✅' : '❌'}
                  </span>
                </div>
              </div>

              <div className="prediction-result">
                <h4>Corners</h4>
                <div className="prediction-info">
                  <span className="prediction">{match.predictions.corners.prediction}</span>
                  <span className="actual-corners">({match.actualCorners} actual)</span>
                  <span 
                    className="result-indicator"
                    style={{ color: getResultColor(match.predictions.corners.correct) }}
                  >
                    {match.predictions.corners.correct ? '✅' : '❌'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PreviousResults;
