// Complete J-League 2 predictions data for July 12, 2025
const allPredictions = [
    {
        homeTeam: "Mito Hollyhock",
        awayTeam: "Kataller Toyama",
        time: "18:00 JST",
        venue: "K's Denki Stadium",
        predictions: {
            matchResult: { value: "Home Win", confidence: 78.3 },
            handicap: { value: "Home Win", confidence: 78.3 },
            overUnder: { value: "Over 2.5", confidence: 54.3 },
            corner1st: { value: "Under 5", confidence: 87.2 },
            corner2nd: { value: "Over 5", confidence: 82.7 }
        },
        probabilities: { home: 78.3, draw: 21.1, away: 0.6 },
        valueAssessment: "high",
        avgConfidence: 76.1
    },
    {
        homeTeam: "Blaublitz Akita",
        awayTeam: "Roasso Kumamoto",
        time: "18:00 JST",
        venue: "Soyu Stadium",
        predictions: {
            matchResult: { value: "Away Win", confidence: 54.5 },
            handicap: { value: "Away Win", confidence: 54.5 },
            overUnder: { value: "Over 2.5", confidence: 60.0 },
            corner1st: { value: "Under 5", confidence: 61.1 },
            corner2nd: { value: "Over 5", confidence: 89.2 }
        },
        probabilities: { home: 27.5, draw: 18.0, away: 54.5 },
        valueAssessment: "good",
        avgConfidence: 63.9
    },
    {
        homeTeam: "Iwaki",
        awayTeam: "V-varen Nagasaki",
        time: "18:00 JST",
        venue: "Hawaiians Stadium Iwaki",
        predictions: {
            matchResult: { value: "Draw", confidence: 38.9 },
            handicap: { value: "Draw", confidence: 38.9 },
            overUnder: { value: "Over 2.5", confidence: 65.5 },
            corner1st: { value: "Over 5", confidence: 80.5 },
            corner2nd: { value: "Over 5", confidence: 95.7 }
        },
        probabilities: { home: 24.0, draw: 38.9, away: 37.2 },
        valueAssessment: "good",
        avgConfidence: 63.9
    },
    {
        homeTeam: "Imabari",
        awayTeam: "Ehime FC",
        time: "18:05 JST",
        venue: "Imabari Satoyama Stadium",
        predictions: {
            matchResult: { value: "Draw", confidence: 80.5 },
            handicap: { value: "Draw", confidence: 80.5 },
            overUnder: { value: "Under 2.5", confidence: 66.0 },
            corner1st: { value: "Under 5", confidence: 56.3 },
            corner2nd: { value: "Over 5", confidence: 81.5 }
        },
        probabilities: { home: 10.4, draw: 80.5, away: 9.2 },
        valueAssessment: "high",
        avgConfidence: 72.9
    },
    {
        homeTeam: "Ventforet Kofu",
        awayTeam: "Omiya Ardija",
        time: "18:30 JST",
        venue: "JIT Recycle Ink Stadium",
        predictions: {
            matchResult: { value: "Away Win", confidence: 59.7 },
            handicap: { value: "Away Win", confidence: 59.7 },
            overUnder: { value: "Under 2.5", confidence: 51.7 },
            corner1st: { value: "Under 5", confidence: 73.7 },
            corner2nd: { value: "Over 5", confidence: 57.0 }
        },
        probabilities: { home: 20.1, draw: 20.2, away: 59.7 },
        valueAssessment: "good",
        avgConfidence: 60.4
    },
    {
        homeTeam: "Sagan Tosu",
        awayTeam: "Oita Trinita",
        time: "19:00 JST",
        venue: "Ekimae Real Estate Stadium",
        predictions: {
            matchResult: { value: "Draw", confidence: 47.1 },
            handicap: { value: "Draw", confidence: 47.1 },
            overUnder: { value: "Under 2.5", confidence: 71.1 },
            corner1st: { value: "Under 5", confidence: 60.9 },
            corner2nd: { value: "Over 5", confidence: 70.3 }
        },
        probabilities: { home: 35.3, draw: 47.1, away: 17.6 },
        valueAssessment: "low",
        avgConfidence: 59.3
    },
    {
        homeTeam: "Renofa Yamaguchi",
        awayTeam: "Tokushima Vortis",
        time: "19:00 JST",
        venue: "Ishin Me-Life Stadium",
        predictions: {
            matchResult: { value: "Away Win", confidence: 52.8 },
            handicap: { value: "Away Win", confidence: 52.8 },
            overUnder: { value: "Under 2.5", confidence: 89.5 },
            corner1st: { value: "Under 5", confidence: 79.3 },
            corner2nd: { value: "Over 5", confidence: 83.1 }
        },
        probabilities: { home: 10.6, draw: 36.6, away: 52.8 },
        valueAssessment: "high",
        avgConfidence: 71.5
    },
    {
        homeTeam: "Montedio Yamagata",
        awayTeam: "JEF United Chiba",
        time: "19:00 JST",
        venue: "ND Soft Stadium",
        predictions: {
            matchResult: { value: "Away Win", confidence: 68.0 },
            handicap: { value: "Away Win", confidence: 68.0 },
            overUnder: { value: "Over 2.5", confidence: 51.6 },
            corner1st: { value: "Under 5", confidence: 57.4 },
            corner2nd: { value: "Over 5", confidence: 67.9 }
        },
        probabilities: { home: 7.3, draw: 24.7, away: 68.0 },
        valueAssessment: "good",
        avgConfidence: 62.6
    },
    {
        homeTeam: "Fujieda MYFC",
        awayTeam: "Vegalta Sendai",
        time: "19:00 JST",
        venue: "Fujieda City General Sports Park",
        predictions: {
            matchResult: { value: "Away Win", confidence: 87.1 },
            handicap: { value: "Away Win", confidence: 87.1 },
            overUnder: { value: "Under 2.5", confidence: 59.5 },
            corner1st: { value: "Over 5", confidence: 60.2 },
            corner2nd: { value: "Over 5", confidence: 85.2 }
        },
        probabilities: { home: 9.4, draw: 3.5, away: 87.1 },
        valueAssessment: "high",
        avgConfidence: 75.8
    },
    {
        homeTeam: "Jubilo Iwata",
        awayTeam: "Consadole Sapporo",
        time: "19:30 JST",
        venue: "Yamaha Stadium",
        predictions: {
            matchResult: { value: "Home Win", confidence: 76.4 },
            handicap: { value: "Home Win", confidence: 76.4 },
            overUnder: { value: "Over 2.5", confidence: 54.5 },
            corner1st: { value: "Under 5", confidence: 76.9 },
            corner2nd: { value: "Over 5", confidence: 80.3 }
        },
        probabilities: { home: 76.4, draw: 11.7, away: 11.9 },
        valueAssessment: "high",
        avgConfidence: 72.9
    }
];

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = allPredictions;
}
