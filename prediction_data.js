// Football Prediction Data with Previous Results
const predictionData = {
    'premier-league': {
        name: 'Premier League',
        stats: {
            matchResult: 40,
            handicap: 35,
            overUnder: 50,
            corners: 67
        },
        // Previous matches (last 2 weeks)
        previousMatches: [
            {
                id: 101,
                homeTeam: 'Liverpool',
                awayTeam: 'Manchester United',
                date: '2024-01-01',
                time: '16:30',
                actualResult: { home: 2, away: 1 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 65, result: 'correct' },
                    handicap: { prediction: 'Liverpool -1.5', confidence: 45, result: 'incorrect' },
                    overUnder: { prediction: 'Over 2.5', confidence: 72, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 68, result: 'correct' }
                }
            },
            {
                id: 102,
                homeTeam: 'Chelsea',
                awayTeam: 'Tottenham',
                date: '2024-01-02',
                time: '14:00',
                actualResult: { home: 1, away: 1 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 52, result: 'incorrect' },
                    handicap: { prediction: 'Chelsea -1.5', confidence: 38, result: 'incorrect' },
                    overUnder: { prediction: 'Under 2.5', confidence: 58, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 71, result: 'incorrect' }
                }
            },
            {
                id: 103,
                homeTeam: 'Arsenal',
                awayTeam: 'Brighton',
                date: '2024-01-03',
                time: '17:30',
                actualResult: { home: 3, away: 0 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 78, result: 'correct' },
                    handicap: { prediction: 'Arsenal -1.5', confidence: 82, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 69, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 74, result: 'correct' }
                }
            },
            {
                id: 104,
                homeTeam: 'Manchester City',
                awayTeam: 'Everton',
                date: '2024-01-04',
                time: '20:00',
                actualResult: { home: 1, away: 2 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 85, result: 'incorrect' },
                    handicap: { prediction: 'Man City -1.5', confidence: 76, result: 'incorrect' },
                    overUnder: { prediction: 'Over 2.5', confidence: 73, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 79, result: 'incorrect' }
                }
            },
            {
                id: 105,
                homeTeam: 'Newcastle',
                awayTeam: 'West Ham',
                date: '2024-01-05',
                time: '19:45',
                actualResult: { home: 0, away: 0 },
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 42, result: 'correct' },
                    handicap: { prediction: 'West Ham +1.5', confidence: 67, result: 'correct' },
                    overUnder: { prediction: 'Under 2.5', confidence: 55, result: 'correct' },
                    corners: { prediction: 'Under 9.5', confidence: 61, result: 'correct' }
                }
            }
        ],
        // Upcoming matches
        matches: [
            {
                id: 1,
                homeTeam: 'Arsenal',
                awayTeam: 'Chelsea',
                date: '2024-01-15',
                time: '17:30',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 45, result: '' },
                    handicap: { prediction: 'Chelsea +1.5', confidence: 35, result: '' },
                    overUnder: { prediction: 'Under 2.5', confidence: 50, result: '' },
                    corners: { prediction: 'Over 9.5', confidence: 67, result: '' }
                }
            },
            {
                id: 2,
                homeTeam: 'Manchester City',
                awayTeam: 'Liverpool',
                date: '2024-01-16',
                time: '20:00',
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 42, result: 'correct' },
                    handicap: { prediction: 'Liverpool +1.5', confidence: 38, result: 'incorrect' },
                    overUnder: { prediction: 'Over 2.5', confidence: 55, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 72, result: 'correct' }
                }
            },
            {
                id: 3,
                homeTeam: 'Manchester United',
                awayTeam: 'Tottenham',
                date: '2024-01-17',
                time: '19:30',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 48, result: 'incorrect' },
                    handicap: { prediction: 'Man United -1.5', confidence: 32, result: 'incorrect' },
                    overUnder: { prediction: 'Under 2.5', confidence: 52, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 65, result: 'correct' }
                }
            }
        ]
    },
    'la-liga': {
        name: 'La Liga',
        stats: {
            matchResult: 25,
            handicap: 55,
            overUnder: 65,
            corners: 67
        },
        previousMatches: [
            {
                id: 201,
                homeTeam: 'Barcelona',
                awayTeam: 'Atletico Madrid',
                date: '2024-01-01',
                time: '21:00',
                actualResult: { home: 2, away: 1 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 68, result: 'correct' },
                    handicap: { prediction: 'Barcelona -1.5', confidence: 55, result: 'incorrect' },
                    overUnder: { prediction: 'Over 2.5', confidence: 71, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 73, result: 'correct' }
                }
            },
            {
                id: 202,
                homeTeam: 'Real Madrid',
                awayTeam: 'Sevilla',
                date: '2024-01-02',
                time: '19:30',
                actualResult: { home: 4, away: 0 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 82, result: 'correct' },
                    handicap: { prediction: 'Real Madrid -1.5', confidence: 78, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 75, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 69, result: 'correct' }
                }
            },
            {
                id: 203,
                homeTeam: 'Valencia',
                awayTeam: 'Real Sociedad',
                date: '2024-01-03',
                time: '18:00',
                actualResult: { home: 1, away: 3 },
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 35, result: 'incorrect' },
                    handicap: { prediction: 'Real Sociedad +1.5', confidence: 62, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 68, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 71, result: 'incorrect' }
                }
            }
        ],
        matches: [
            {
                id: 6,
                homeTeam: 'Real Madrid',
                awayTeam: 'Barcelona',
                date: '2024-01-20',
                time: '21:00',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 28, result: '' },
                    handicap: { prediction: 'Real Madrid -1.5', confidence: 58, result: '' },
                    overUnder: { prediction: 'Over 2.5', confidence: 68, result: '' },
                    corners: { prediction: 'Over 10.5', confidence: 71, result: '' }
                }
            }
        ]
    },
    'bundesliga': {
        name: 'Bundesliga',
        stats: {
            matchResult: 15,
            handicap: 35,
            overUnder: 75,
            corners: 67
        },
        previousMatches: [
            {
                id: 301,
                homeTeam: 'Bayern Munich',
                awayTeam: 'RB Leipzig',
                date: '2024-01-01',
                time: '18:30',
                actualResult: { home: 3, away: 2 },
                predictions: {
                    matchResult: { prediction: 'Away Win', confidence: 25, result: 'incorrect' },
                    handicap: { prediction: 'Leipzig +1.5', confidence: 45, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 82, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 78, result: 'correct' }
                }
            },
            {
                id: 302,
                homeTeam: 'Borussia Dortmund',
                awayTeam: 'Bayer Leverkusen',
                date: '2024-01-02',
                time: '15:30',
                actualResult: { home: 2, away: 4 },
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 18, result: 'incorrect' },
                    handicap: { prediction: 'Leverkusen +1.5', confidence: 38, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 85, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 74, result: 'correct' }
                }
            }
        ],
        matches: [
            {
                id: 11,
                homeTeam: 'Bayern Munich',
                awayTeam: 'Borussia Dortmund',
                date: '2024-01-25',
                time: '18:30',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 18, result: '' },
                    handicap: { prediction: 'Bayern -1.5', confidence: 38, result: '' },
                    overUnder: { prediction: 'Over 2.5', confidence: 78, result: '' },
                    corners: { prediction: 'Over 10.5', confidence: 73, result: '' }
                }
            }
        ]
    },
    'serie-a': {
        name: 'Serie A',
        stats: {
            matchResult: 25,
            handicap: 70,
            overUnder: 60,
            corners: 67
        },
        previousMatches: [
            {
                id: 401,
                homeTeam: 'Juventus',
                awayTeam: 'Inter Milan',
                date: '2024-01-01',
                time: '20:45',
                actualResult: { home: 1, away: 0 },
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 32, result: 'incorrect' },
                    handicap: { prediction: 'Juventus -1.5', confidence: 75, result: 'incorrect' },
                    overUnder: { prediction: 'Under 2.5', confidence: 68, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 71, result: 'incorrect' }
                }
            },
            {
                id: 402,
                homeTeam: 'AC Milan',
                awayTeam: 'Napoli',
                date: '2024-01-02',
                time: '18:00',
                actualResult: { home: 0, away: 2 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 28, result: 'incorrect' },
                    handicap: { prediction: 'Milan -1.5', confidence: 72, result: 'incorrect' },
                    overUnder: { prediction: 'Under 2.5', confidence: 65, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 69, result: 'correct' }
                }
            }
        ],
        matches: [
            {
                id: 16,
                homeTeam: 'Juventus',
                awayTeam: 'AC Milan',
                date: '2024-01-30',
                time: '20:45',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 28, result: '' },
                    handicap: { prediction: 'Juventus -1.5', confidence: 73, result: '' },
                    overUnder: { prediction: 'Under 2.5', confidence: 62, result: '' },
                    corners: { prediction: 'Over 9.5', confidence: 69, result: '' }
                }
            }
        ]
    },
    'ligue-1': {
        name: 'Ligue 1',
        stats: {
            matchResult: 60,
            handicap: 60,
            overUnder: 65,
            corners: 67
        },
        previousMatches: [
            {
                id: 501,
                homeTeam: 'Paris Saint-Germain',
                awayTeam: 'AS Monaco',
                date: '2024-01-01',
                time: '21:00',
                actualResult: { home: 3, away: 1 },
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 78, result: 'correct' },
                    handicap: { prediction: 'PSG -1.5', confidence: 72, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 71, result: 'correct' },
                    corners: { prediction: 'Over 10.5', confidence: 75, result: 'correct' }
                }
            },
            {
                id: 502,
                homeTeam: 'Lyon',
                awayTeam: 'Marseille',
                date: '2024-01-02',
                time: '19:00',
                actualResult: { home: 2, away: 2 },
                predictions: {
                    matchResult: { prediction: 'Draw', confidence: 58, result: 'correct' },
                    handicap: { prediction: 'Marseille +1.5', confidence: 65, result: 'correct' },
                    overUnder: { prediction: 'Over 2.5', confidence: 69, result: 'correct' },
                    corners: { prediction: 'Over 9.5', confidence: 67, result: 'incorrect' }
                }
            }
        ],
        matches: [
            {
                id: 21,
                homeTeam: 'Paris Saint-Germain',
                awayTeam: 'Olympique Marseille',
                date: '2024-02-04',
                time: '21:00',
                predictions: {
                    matchResult: { prediction: 'Home Win', confidence: 63, result: '' },
                    handicap: { prediction: 'PSG -1.5', confidence: 62, result: '' },
                    overUnder: { prediction: 'Over 2.5', confidence: 68, result: '' },
                    corners: { prediction: 'Over 10.5', confidence: 70, result: '' }
                }
            }
        ]
    }
};
