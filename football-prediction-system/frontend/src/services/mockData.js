// Mock data for testing UI without backend
export const mockLeagues = [
  { id: 'PL', name: 'Premier League', country: 'England' },
  { id: 'PD', name: 'La Liga', country: 'Spain' },
  { id: 'BL1', name: 'Bundesliga', country: 'Germany' },
  { id: 'SA', name: 'Serie A', country: 'Italy' },
  { id: 'FL1', name: 'Ligue 1', country: 'France' }
];

export const mockLeagueStats = {
  PL: {
    totalMatches: 380,
    completedMatches: 156,
    upcomingMatches: 224,
    accuracy: {
      overall: 72.5,
      homeWin: 78.3,
      draw: 45.2,
      awayWin: 68.8,
      handicap: 74.2,
      overUnder: 61.9,
      corners: 67.4
    },
    recentForm: [
      { date: '2024-07-10', correct: 8, total: 10, accuracy: 80 },
      { date: '2024-07-09', correct: 6, total: 8, accuracy: 75 },
      { date: '2024-07-08', correct: 7, total: 12, accuracy: 58.3 },
      { date: '2024-07-07', correct: 9, total: 10, accuracy: 90 },
      { date: '2024-07-06', correct: 5, total: 8, accuracy: 62.5 }
    ]
  },
  PD: {
    totalMatches: 380,
    completedMatches: 142,
    upcomingMatches: 238,
    accuracy: {
      overall: 69.2,
      homeWin: 73.8,
      draw: 42.1,
      awayWin: 66.4,
      handicap: 71.7,
      overUnder: 58.3,
      corners: 63.8
    }
  },
  BL1: {
    totalMatches: 306,
    completedMatches: 128,
    upcomingMatches: 178,
    accuracy: {
      overall: 75.1,
      homeWin: 79.2,
      draw: 48.6,
      awayWin: 71.9,
      handicap: 76.8,
      overUnder: 64.4,
      corners: 69.7
    }
  },
  SA: {
    totalMatches: 380,
    completedMatches: 134,
    upcomingMatches: 246,
    accuracy: {
      overall: 68.8,
      homeWin: 74.5,
      draw: 44.3,
      awayWin: 67.2,
      handicap: 72.9,
      overUnder: 59.8,
      corners: 65.2
    }
  },
  FL1: {
    totalMatches: 380,
    completedMatches: 148,
    upcomingMatches: 232,
    accuracy: {
      overall: 66.7,
      homeWin: 71.9,
      draw: 41.8,
      awayWin: 64.1,
      handicap: 69.3,
      overUnder: 56.9,
      corners: 61.6
    }
  }
};

export const mockUpcomingMatches = {
  PL: [
    {
      id: 1,
      homeTeam: 'Arsenal',
      awayTeam: 'Chelsea',
      matchDate: '2024-07-12',
      matchTime: '16:30',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 82.4  // สูงมาก - เขียว
        },
        {
          category: 'HANDICAP',
          prediction: 'Arsenal -0.5',
          confidence: 76.8  // สูง - เขียว
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 68.4  // ดี - น้ำเงิน
        },
        {
          category: 'CORNERS',
          prediction: 'Over 10.5',
          confidence: 62.9  // ปานกลาง - เหลือง
        }
      ]
    },
    {
      id: 2,
      homeTeam: 'Manchester City',
      awayTeam: 'Liverpool',
      matchDate: '2024-07-13',
      matchTime: '14:00',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Draw',
          confidence: 58.9  // ปานกลาง - เหลือง
        },
        {
          category: 'HANDICAP',
          prediction: 'Draw',
          confidence: 65.3  // ดี - น้ำเงิน
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 3.5',
          confidence: 79.1  // สูง - เขียว
        },
        {
          category: 'CORNERS',
          prediction: 'Over 12.5',
          confidence: 72.7  // ดี - น้ำเงิน
        }
      ]
    },
    {
      id: 3,
      homeTeam: 'Tottenham',
      awayTeam: 'Manchester United',
      matchDate: '2024-07-14',
      matchTime: '17:00',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Away Win',
          confidence: 47.4  // ต่ำ - ส้ม
        },
        {
          category: 'HANDICAP',
          prediction: 'Man United -0.25',
          confidence: 52.9  // ปานกลาง - เหลือง
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 64.7  // ดี - น้ำเงิน
        },
        {
          category: 'CORNERS',
          prediction: 'Under 9.5',
          confidence: 41.2  // ต่ำมาก - แดง
        }
      ]
    },
    {
      id: 4,
      homeTeam: 'Brighton',
      awayTeam: 'West Ham',
      matchDate: '2024-07-15',
      matchTime: '15:00',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 87.2  // สูงมาก - เขียว
        },
        {
          category: 'HANDICAP',
          prediction: 'Brighton -1.0',
          confidence: 83.5  // สูงมาก - เขียว
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 71.8  // ดี - น้ำเงิน
        },
        {
          category: 'CORNERS',
          prediction: 'Over 11.5',
          confidence: 66.3  // ดี - น้ำเงิน
        }
      ]
    },
    {
      id: 5,
      homeTeam: 'Crystal Palace',
      awayTeam: 'Fulham',
      matchDate: '2024-07-16',
      matchTime: '20:00',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Draw',
          confidence: 45.2  // ต่ำ - แดง
        },
        {
          category: 'HANDICAP',
          prediction: 'Draw',
          confidence: 48.9  // ต่ำ - แดง
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Under 2.5',
          confidence: 51.8  // ผ่านเกณฑ์ - เขียวอ่อน
        },
        {
          category: 'CORNERS',
          prediction: 'Under 9.5',
          confidence: 42.1  // ต่ำมาก - แดง
        }
      ]
    }
  ],
  PD: [
    {
      id: 5,
      homeTeam: 'Real Madrid',
      awayTeam: 'Barcelona',
      matchDate: '2024-07-12',
      matchTime: '21:00',
      homeScore: null,
      awayScore: null,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 78.8  // สูง - เขียว
        },
        {
          category: 'HANDICAP',
          prediction: 'Real Madrid -0.5',
          confidence: 74.4  // ดี - น้ำเงิน
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 81.2  // สูงมาก - เขียว
        },
        {
          category: 'CORNERS',
          prediction: 'Over 11.5',
          confidence: 69.8  // ดี - น้ำเงิน
        }
      ]
    }
  ]
};

export const mockPreviousMatches = {
  PL: [
    {
      id: 101,
      homeTeam: 'Brighton',
      awayTeam: 'Newcastle',
      matchDate: '2024-07-08',
      matchTime: '15:00',
      homeScore: 2,
      awayScore: 1,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 75.3  // สูง - เขียว
        },
        {
          category: 'HANDICAP',
          prediction: 'Brighton -0.25',
          confidence: 68.7  // ดี - เขียว
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 58.9  // ปานกลาง - เขียว
        },
        {
          category: 'CORNERS',
          prediction: 'Over 10.5',
          confidence: 42.4  // ต่ำ - แดง
        }
      ],
      results: [
        {
          category: 'MATCH_RESULT',
          isCorrect: true
        },
        {
          category: 'HANDICAP',
          isCorrect: true
        },
        {
          category: 'OVER_UNDER',
          isCorrect: true
        },
        {
          category: 'CORNERS',
          isCorrect: false
        }
      ]
    },
    {
      id: 102,
      homeTeam: 'West Ham',
      awayTeam: 'Everton',
      matchDate: '2024-07-07',
      matchTime: '17:30',
      homeScore: 1,
      awayScore: 1,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 48.7  // ต่ำ - แดง
        },
        {
          category: 'HANDICAP',
          prediction: 'West Ham -0.5',
          confidence: 44.2  // ต่ำ - แดง
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Under 2.5',
          confidence: 62.8  // ดี - เขียว
        },
        {
          category: 'CORNERS',
          prediction: 'Over 9.5',
          confidence: 59.3  // ปานกลาง - เขียว
        }
      ],
      results: [
        {
          category: 'MATCH_RESULT',
          isCorrect: false
        },
        {
          category: 'HANDICAP',
          isCorrect: false
        },
        {
          category: 'OVER_UNDER',
          isCorrect: true
        },
        {
          category: 'CORNERS',
          isCorrect: true
        }
      ]
    },
    {
      id: 103,
      homeTeam: 'Arsenal',
      awayTeam: 'Tottenham',
      matchDate: '2024-07-06',
      matchTime: '16:30',
      homeScore: 3,
      awayScore: 0,
      predictions: [
        {
          category: 'MATCH_RESULT',
          prediction: 'Home Win',
          confidence: 85.4  // สูงมาก - เขียวเข้ม
        },
        {
          category: 'HANDICAP',
          prediction: 'Arsenal -1.0',
          confidence: 79.2  // สูง - เขียว
        },
        {
          category: 'OVER_UNDER',
          prediction: 'Over 2.5',
          confidence: 71.8  // ดี - เขียว
        },
        {
          category: 'CORNERS',
          prediction: 'Over 11.5',
          confidence: 46.3  // ต่ำ - แดง
        }
      ],
      results: [
        {
          category: 'MATCH_RESULT',
          isCorrect: true
        },
        {
          category: 'HANDICAP',
          isCorrect: true
        },
        {
          category: 'OVER_UNDER',
          isCorrect: true
        },
        {
          category: 'CORNERS',
          isCorrect: false
        }
      ]
    }
  ]
};

// Mock API functions
export const mockAPI = {
  getAllLeagues: () => Promise.resolve({ data: mockLeagues }),
  
  getLeagueData: (leagueId) => Promise.resolve({ 
    data: mockLeagueStats[leagueId] || mockLeagueStats.PL 
  }),
  
  getUpcomingMatches: ({ leagueId }) => Promise.resolve({ 
    data: mockUpcomingMatches[leagueId] || mockUpcomingMatches.PL 
  }),
  
  getPreviousMatches: ({ leagueId }) => Promise.resolve({ 
    data: mockPreviousMatches[leagueId] || mockPreviousMatches.PL 
  }),
  
  getLeagueStats: (leagueId) => Promise.resolve({ 
    data: mockLeagueStats[leagueId] || mockLeagueStats.PL 
  })
};
