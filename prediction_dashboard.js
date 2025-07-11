// Football Prediction Dashboard JavaScript - With Previous Results
let currentLeague = 'premier-league';

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    showLeague('premier-league');
});

// Show specific league data
function showLeague(leagueId) {
    currentLeague = leagueId;
    
    // Update active tab
    document.querySelectorAll('.league-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Find and activate the clicked tab
    const clickedTab = Array.from(document.querySelectorAll('.league-tab')).find(tab => 
        tab.onclick.toString().includes(leagueId)
    );
    if (clickedTab) {
        clickedTab.classList.add('active');
    }
    
    // Update league title
    const leagueData = predictionData[leagueId];
    document.getElementById('league-title').textContent = `${leagueData.name} Predictions`;
    
    // Update league statistics
    updateLeagueStats(leagueData.stats);
    
    // Update upcoming predictions table
    updatePredictionsTable(leagueData.matches);
    
    // Update previous results table
    updatePreviousResultsTable(leagueData.previousMatches || []);
}

// Update league statistics cards
function updateLeagueStats(stats) {
    const statCards = document.querySelectorAll('.stat-card');
    const statValues = [stats.matchResult, stats.handicap, stats.overUnder, stats.corners];
    
    statCards.forEach((card, index) => {
        const valueElement = card.querySelector('.value');
        valueElement.textContent = `${statValues[index]}%`;
        
        // Add color based on accuracy for dark mode
        valueElement.className = 'value';
        if (statValues[index] >= 70) {
            valueElement.style.color = '#4caf50'; // Green
        } else if (statValues[index] >= 60) {
            valueElement.style.color = '#64b5f6'; // Blue
        } else if (statValues[index] >= 50) {
            valueElement.style.color = '#ff9800'; // Orange
        } else {
            valueElement.style.color = '#f44336'; // Red
        }
    });
}

// Update upcoming predictions table
function updatePredictionsTable(matches) {
    const tableContent = document.getElementById('table-content');
    
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Upcoming Match</th>
                    <th>Match Result</th>
                    <th>Handicap</th>
                    <th>Over/Under</th>
                    <th>Corners</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    matches.forEach(match => {
        tableHTML += `
            <tr>
                <td class="match-info">
                    <div class="teams">
                        ${match.homeTeam} vs ${match.awayTeam}
                        <span class="match-id">#${match.id}</span>
                    </div>
                    <div class="match-time">${formatDate(match.date)} ${match.time}</div>
                </td>
                <td>${createPredictionCell(match.predictions.matchResult)}</td>
                <td>${createPredictionCell(match.predictions.handicap)}</td>
                <td>${createPredictionCell(match.predictions.overUnder)}</td>
                <td>${createPredictionCell(match.predictions.corners)}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    tableContent.innerHTML = tableHTML;
}

// Update previous results table
function updatePreviousResultsTable(previousMatches) {
    const previousContent = document.getElementById('previous-results-content');
    
    if (!previousMatches || previousMatches.length === 0) {
        previousContent.innerHTML = `
            <div class="no-data">
                <i class="fas fa-info-circle"></i>
                <p>No previous results available for this league</p>
            </div>
        `;
        return;
    }
    
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Previous Match</th>
                    <th>Score</th>
                    <th>Match Result</th>
                    <th>Handicap</th>
                    <th>Over/Under</th>
                    <th>Corners</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    previousMatches.forEach(match => {
        const score = `${match.actualResult.home}-${match.actualResult.away}`;
        
        tableHTML += `
            <tr>
                <td class="match-info">
                    <div class="teams">
                        ${match.homeTeam} vs ${match.awayTeam}
                        <span class="match-id">#${match.id}</span>
                    </div>
                    <div class="match-time">${formatDate(match.date)} ${match.time}</div>
                </td>
                <td class="score-cell">
                    <div class="score">${score}</div>
                </td>
                <td>${createResultCell(match.predictions.matchResult)}</td>
                <td>${createResultCell(match.predictions.handicap)}</td>
                <td>${createResultCell(match.predictions.overUnder)}</td>
                <td>${createResultCell(match.predictions.corners)}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    previousContent.innerHTML = tableHTML;
}

// Create prediction cell for upcoming matches
function createPredictionCell(prediction) {
    const confidenceClass = getConfidenceClass(prediction.confidence);
    const resultIcon = getResultIcon(prediction.result);
    
    return `
        <div class="prediction-cell ${confidenceClass}">
            ${resultIcon}
            <div>${prediction.prediction}</div>
            <div class="accuracy-badge">${prediction.confidence}%</div>
        </div>
    `;
}

// Create result cell for previous matches
function createResultCell(prediction) {
    const confidenceClass = getConfidenceClass(prediction.confidence);
    const resultIcon = getEnhancedResultIcon(prediction.result);
    
    return `
        <div class="result-cell ${confidenceClass}">
            <div class="result-icon-container">
                ${resultIcon}
            </div>
            <div class="prediction-text">${prediction.prediction}</div>
            <div class="accuracy-badge">${prediction.confidence}%</div>
        </div>
    `;
}

// Enhanced result icons with better styling
function getEnhancedResultIcon(result) {
    switch(result) {
        case 'correct':
            return `
                <div class="result-icon correct-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
            `;
        case 'incorrect':
            return `
                <div class="result-icon incorrect-icon">
                    <i class="fas fa-times-circle"></i>
                </div>
            `;
        default:
            return `
                <div class="result-icon pending-icon">
                    <i class="fas fa-clock"></i>
                </div>
            `;
    }
}

// Get CSS class based on confidence level
function getConfidenceClass(confidence) {
    if (confidence < 50) return 'confidence-below-50';
    if (confidence < 55) return 'confidence-50';
    if (confidence < 60) return 'confidence-55';
    if (confidence < 65) return 'confidence-60';
    if (confidence < 70) return 'confidence-65';
    if (confidence < 75) return 'confidence-70';
    if (confidence < 80) return 'confidence-75';
    if (confidence < 85) return 'confidence-80';
    if (confidence < 90) return 'confidence-85';
    if (confidence < 95) return 'confidence-90';
    return 'confidence-95';
}

// Get result icon (smaller for upcoming matches)
function getResultIcon(result) {
    switch(result) {
        case 'correct':
            return '<i class="fas fa-check-circle" style="color: #4caf50; position: absolute; top: 0.25rem; right: 0.25rem; font-size: 0.8rem;" title="Correct Prediction"></i>';
        case 'incorrect':
            return '<i class="fas fa-times-circle" style="color: #f44336; position: absolute; top: 0.25rem; right: 0.25rem; font-size: 0.8rem;" title="Incorrect Prediction"></i>';
        case 'pending':
        default:
            return ''; // No icon for pending results
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
}

// Calculate accuracy for previous matches
function calculatePreviousAccuracy(previousMatches) {
    if (!previousMatches || previousMatches.length === 0) return null;
    
    const categories = ['matchResult', 'handicap', 'overUnder', 'corners'];
    const accuracies = {};
    
    categories.forEach(category => {
        const predictions = previousMatches.map(m => m.predictions[category]);
        const correct = predictions.filter(p => p.result === 'correct').length;
        const total = predictions.length;
        
        accuracies[category] = {
            correct: correct,
            total: total,
            percentage: total > 0 ? Math.round((correct / total) * 100) : 0
        };
    });
    
    return accuracies;
}

// Admin functions for updating results
function updateMatchResult(matchId, category, isCorrect) {
    // Find the match across all leagues (both upcoming and previous)
    for (let leagueId in predictionData) {
        const league = predictionData[leagueId];
        
        // Check upcoming matches
        let match = league.matches.find(m => m.id === matchId);
        let isUpcoming = true;
        
        // Check previous matches if not found in upcoming
        if (!match && league.previousMatches) {
            match = league.previousMatches.find(m => m.id === matchId);
            isUpcoming = false;
        }
        
        if (match && match.predictions[category]) {
            match.predictions[category].result = isCorrect ? 'correct' : 'incorrect';
            
            // Refresh display if this league is currently shown
            if (leagueId === currentLeague) {
                if (isUpcoming) {
                    updatePredictionsTable(league.matches);
                } else {
                    updatePreviousResultsTable(league.previousMatches);
                }
            }
            
            // Update league statistics
            updateLeagueAccuracy(leagueId);
            
            console.log(`Updated match ${matchId} (${match.homeTeam} vs ${match.awayTeam}), category ${category}: ${isCorrect ? 'correct' : 'incorrect'}`);
            return true;
        }
    }
    
    console.log(`Match ${matchId} not found`);
    return false;
}

// Update league accuracy statistics
function updateLeagueAccuracy(leagueId) {
    const league = predictionData[leagueId];
    const categories = ['matchResult', 'handicap', 'overUnder', 'corners'];
    
    categories.forEach(category => {
        let allPredictions = [];
        
        // Collect predictions from both upcoming and previous matches
        if (league.matches) {
            allPredictions = allPredictions.concat(
                league.matches.map(m => m.predictions[category])
            );
        }
        
        if (league.previousMatches) {
            allPredictions = allPredictions.concat(
                league.previousMatches.map(m => m.predictions[category])
            );
        }
        
        const validPredictions = allPredictions.filter(p => p.result !== 'pending' && p.result !== '');
        
        if (validPredictions.length > 0) {
            const correct = validPredictions.filter(p => p.result === 'correct').length;
            const accuracy = Math.round((correct / validPredictions.length) * 100);
            
            // Update the category mapping
            const categoryMap = {
                'matchResult': 'matchResult',
                'handicap': 'handicap',
                'overUnder': 'overUnder',
                'corners': 'corners'
            };
            
            league.stats[categoryMap[category]] = accuracy;
        }
    });
    
    // Refresh stats display if this league is currently shown
    if (leagueId === currentLeague) {
        updateLeagueStats(league.stats);
    }
}

// Get match details by ID (helper function for admin)
function getMatchById(matchId) {
    for (let leagueId in predictionData) {
        const league = predictionData[leagueId];
        
        // Check upcoming matches
        let match = league.matches.find(m => m.id === matchId);
        if (match) {
            return {
                league: league.name,
                leagueId: leagueId,
                match: match,
                type: 'upcoming'
            };
        }
        
        // Check previous matches
        if (league.previousMatches) {
            match = league.previousMatches.find(m => m.id === matchId);
            if (match) {
                return {
                    league: league.name,
                    leagueId: leagueId,
                    match: match,
                    type: 'previous'
                };
            }
        }
    }
    
    return null;
}

// Get overall statistics including previous matches
function getOverallStats() {
    let totalMatches = 0;
    let totalCorrect = 0;
    let categoryStats = {
        matchResult: { correct: 0, total: 0 },
        handicap: { correct: 0, total: 0 },
        overUnder: { correct: 0, total: 0 },
        corners: { correct: 0, total: 0 }
    };
    
    for (let leagueId in predictionData) {
        const league = predictionData[leagueId];
        
        // Process upcoming matches
        if (league.matches) {
            league.matches.forEach(match => {
                Object.keys(match.predictions).forEach(category => {
                    const prediction = match.predictions[category];
                    
                    if (prediction.result !== 'pending' && prediction.result !== '') {
                        categoryStats[category].total++;
                        totalMatches++;
                        
                        if (prediction.result === 'correct') {
                            categoryStats[category].correct++;
                            totalCorrect++;
                        }
                    }
                });
            });
        }
        
        // Process previous matches
        if (league.previousMatches) {
            league.previousMatches.forEach(match => {
                Object.keys(match.predictions).forEach(category => {
                    const prediction = match.predictions[category];
                    
                    if (prediction.result !== 'pending' && prediction.result !== '') {
                        categoryStats[category].total++;
                        totalMatches++;
                        
                        if (prediction.result === 'correct') {
                            categoryStats[category].correct++;
                            totalCorrect++;
                        }
                    }
                });
            });
        }
    }
    
    const overallAccuracy = totalMatches > 0 ? (totalCorrect / totalMatches * 100).toFixed(1) : 0;
    
    return {
        overallAccuracy: overallAccuracy,
        totalMatches: totalMatches,
        categoryAccuracies: {
            matchResult: categoryStats.matchResult.total > 0 ? 
                (categoryStats.matchResult.correct / categoryStats.matchResult.total * 100).toFixed(1) : 0,
            handicap: categoryStats.handicap.total > 0 ? 
                (categoryStats.handicap.correct / categoryStats.handicap.total * 100).toFixed(1) : 0,
            overUnder: categoryStats.overUnder.total > 0 ? 
                (categoryStats.overUnder.correct / categoryStats.overUnder.total * 100).toFixed(1) : 0,
            corners: categoryStats.corners.total > 0 ? 
                (categoryStats.corners.correct / categoryStats.corners.total * 100).toFixed(1) : 0
        }
    };
}

// Bulk update function for admin
function bulkUpdateResults(updates) {
    updates.forEach(update => {
        updateMatchResult(update.matchId, update.category, update.isCorrect);
    });
    
    console.log(`Bulk updated ${updates.length} results`);
}

// Export data for analysis
function exportPredictionData() {
    const dataStr = JSON.stringify(predictionData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'prediction_data_export.json';
    link.click();
}

// Search functionality
function searchMatches(query) {
    const results = [];
    
    for (let leagueId in predictionData) {
        const league = predictionData[leagueId];
        let matches = [];
        
        // Search upcoming matches
        if (league.matches) {
            matches = matches.concat(
                league.matches.filter(match => 
                    match.homeTeam.toLowerCase().includes(query.toLowerCase()) ||
                    match.awayTeam.toLowerCase().includes(query.toLowerCase()) ||
                    match.id.toString().includes(query)
                ).map(match => ({...match, type: 'upcoming'}))
            );
        }
        
        // Search previous matches
        if (league.previousMatches) {
            matches = matches.concat(
                league.previousMatches.filter(match => 
                    match.homeTeam.toLowerCase().includes(query.toLowerCase()) ||
                    match.awayTeam.toLowerCase().includes(query.toLowerCase()) ||
                    match.id.toString().includes(query)
                ).map(match => ({...match, type: 'previous'}))
            );
        }
        
        if (matches.length > 0) {
            results.push({
                league: league.name,
                leagueId: leagueId,
                matches: matches
            });
        }
    }
    
    return results;
}

// Console helper functions for admin
console.log('🏆 Football Prediction Dashboard Loaded (With Previous Results)');
console.log('📊 Available admin functions:');
console.log('- updateMatchResult(matchId, category, isCorrect)');
console.log('- bulkUpdateResults([{matchId, category, isCorrect}, ...])');
console.log('- exportPredictionData()');
console.log('- searchMatches(query)');
console.log('- getMatchById(matchId)');
console.log('- getOverallStats()');

// Example usage in console:
// updateMatchResult(101, 'matchResult', true);
// getMatchById(101);
// searchMatches('Arsenal');
