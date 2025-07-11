const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Create leagues
  const leagues = [
    { id: 'PL', name: 'Premier League', country: 'England', season: '2024' },
    { id: 'PD', name: 'La Liga', country: 'Spain', season: '2024' },
    { id: 'BL1', name: 'Bundesliga', country: 'Germany', season: '2024' },
    { id: 'SA', name: 'Serie A', country: 'Italy', season: '2024' },
    { id: 'FL1', name: 'Ligue 1', country: 'France', season: '2024' }
  ];

  for (const league of leagues) {
    await prisma.league.upsert({
      where: { id: league.id },
      update: {},
      create: league
    });
  }

  console.log('✅ Leagues created');

  // Create sample matches
  const sampleMatches = [
    // Premier League - Upcoming
    {
      leagueId: 'PL',
      homeTeam: 'Arsenal',
      awayTeam: 'Chelsea',
      matchDate: new Date('2024-01-15'),
      matchTime: '17:30',
      status: 'UPCOMING'
    },
    {
      leagueId: 'PL',
      homeTeam: 'Manchester City',
      awayTeam: 'Liverpool',
      matchDate: new Date('2024-01-16'),
      matchTime: '20:00',
      status: 'UPCOMING'
    },
    {
      leagueId: 'PL',
      homeTeam: 'Manchester United',
      awayTeam: 'Tottenham',
      matchDate: new Date('2024-01-17'),
      matchTime: '19:30',
      status: 'UPCOMING'
    },
    
    // Premier League - Previous (Finished)
    {
      leagueId: 'PL',
      homeTeam: 'Liverpool',
      awayTeam: 'Manchester United',
      matchDate: new Date('2024-01-01'),
      matchTime: '16:30',
      status: 'FINISHED',
      homeScore: 2,
      awayScore: 1
    },
    {
      leagueId: 'PL',
      homeTeam: 'Chelsea',
      awayTeam: 'Tottenham',
      matchDate: new Date('2024-01-02'),
      matchTime: '14:00',
      status: 'FINISHED',
      homeScore: 1,
      awayScore: 1
    },
    
    // La Liga
    {
      leagueId: 'PD',
      homeTeam: 'Real Madrid',
      awayTeam: 'Barcelona',
      matchDate: new Date('2024-01-20'),
      matchTime: '21:00',
      status: 'UPCOMING'
    },
    {
      leagueId: 'PD',
      homeTeam: 'Barcelona',
      awayTeam: 'Atletico Madrid',
      matchDate: new Date('2024-01-01'),
      matchTime: '21:00',
      status: 'FINISHED',
      homeScore: 2,
      awayScore: 1
    },
    
    // Bundesliga
    {
      leagueId: 'BL1',
      homeTeam: 'Bayern Munich',
      awayTeam: 'Borussia Dortmund',
      matchDate: new Date('2024-01-25'),
      matchTime: '18:30',
      status: 'UPCOMING'
    },
    {
      leagueId: 'BL1',
      homeTeam: 'Bayern Munich',
      awayTeam: 'RB Leipzig',
      matchDate: new Date('2024-01-01'),
      matchTime: '18:30',
      status: 'FINISHED',
      homeScore: 3,
      awayScore: 2
    },
    
    // Serie A
    {
      leagueId: 'SA',
      homeTeam: 'Juventus',
      awayTeam: 'AC Milan',
      matchDate: new Date('2024-01-30'),
      matchTime: '20:45',
      status: 'UPCOMING'
    },
    {
      leagueId: 'SA',
      homeTeam: 'Juventus',
      awayTeam: 'Inter Milan',
      matchDate: new Date('2024-01-01'),
      matchTime: '20:45',
      status: 'FINISHED',
      homeScore: 1,
      awayScore: 0
    },
    
    // Ligue 1
    {
      leagueId: 'FL1',
      homeTeam: 'Paris Saint-Germain',
      awayTeam: 'Olympique Marseille',
      matchDate: new Date('2024-02-04'),
      matchTime: '21:00',
      status: 'UPCOMING'
    },
    {
      leagueId: 'FL1',
      homeTeam: 'Paris Saint-Germain',
      awayTeam: 'AS Monaco',
      matchDate: new Date('2024-01-01'),
      matchTime: '21:00',
      status: 'FINISHED',
      homeScore: 3,
      awayScore: 1
    }
  ];

  const createdMatches = [];
  for (const match of sampleMatches) {
    const createdMatch = await prisma.match.create({
      data: match
    });
    createdMatches.push(createdMatch);
  }

  console.log('✅ Sample matches created');

  // Create predictions for all matches
  const categories = ['MATCH_RESULT', 'HANDICAP', 'OVER_UNDER', 'CORNERS'];
  const predictions = [
    // Match predictions with different confidence levels
    { prediction: 'Home Win', confidence: 65 },
    { prediction: 'Draw', confidence: 42 },
    { prediction: 'Away Win', confidence: 58 },
    { prediction: 'Home -1.5', confidence: 73 },
    { prediction: 'Away +1.5', confidence: 67 },
    { prediction: 'Over 2.5', confidence: 72 },
    { prediction: 'Under 2.5', confidence: 55 },
    { prediction: 'Over 9.5', confidence: 68 },
    { prediction: 'Under 9.5', confidence: 61 }
  ];

  for (const match of createdMatches) {
    for (const category of categories) {
      let predictionText, confidence;
      
      switch (category) {
        case 'MATCH_RESULT':
          if (Math.random() > 0.6) {
            predictionText = 'Home Win';
            confidence = 45 + Math.random() * 30;
          } else if (Math.random() > 0.5) {
            predictionText = 'Away Win';
            confidence = 40 + Math.random() * 35;
          } else {
            predictionText = 'Draw';
            confidence = 35 + Math.random() * 25;
          }
          break;
        case 'HANDICAP':
          if (Math.random() > 0.5) {
            predictionText = `${match.homeTeam} -1.5`;
            confidence = 50 + Math.random() * 30;
          } else {
            predictionText = `${match.awayTeam} +1.5`;
            confidence = 55 + Math.random() * 25;
          }
          break;
        case 'OVER_UNDER':
          if (Math.random() > 0.4) {
            predictionText = 'Over 2.5';
            confidence = 60 + Math.random() * 20;
          } else {
            predictionText = 'Under 2.5';
            confidence = 50 + Math.random() * 25;
          }
          break;
        case 'CORNERS':
          if (Math.random() > 0.3) {
            predictionText = 'Over 9.5';
            confidence = 65 + Math.random() * 15;
          } else {
            predictionText = 'Under 9.5';
            confidence = 55 + Math.random() * 20;
          }
          break;
      }

      await prisma.prediction.create({
        data: {
          matchId: match.id,
          category,
          prediction: predictionText,
          confidence: Math.round(confidence),
          modelVersion: 'v1.0'
        }
      });
    }
  }

  console.log('✅ Predictions created');

  // Create some results for finished matches
  const finishedMatches = createdMatches.filter(m => m.status === 'FINISHED');
  
  for (const match of finishedMatches) {
    const matchPredictions = await prisma.prediction.findMany({
      where: { matchId: match.id }
    });

    for (const prediction of matchPredictions) {
      let isCorrect = false;
      let actualOutcome = '';

      // Simulate results based on actual scores
      switch (prediction.category) {
        case 'MATCH_RESULT':
          if (match.homeScore > match.awayScore) {
            actualOutcome = 'Home Win';
            isCorrect = prediction.prediction === 'Home Win';
          } else if (match.homeScore < match.awayScore) {
            actualOutcome = 'Away Win';
            isCorrect = prediction.prediction === 'Away Win';
          } else {
            actualOutcome = 'Draw';
            isCorrect = prediction.prediction === 'Draw';
          }
          break;
        case 'HANDICAP':
          const handicapResult = (match.homeScore - 1.5) > match.awayScore;
          actualOutcome = handicapResult ? `${match.homeTeam} -1.5` : `${match.awayTeam} +1.5`;
          isCorrect = prediction.prediction.includes(handicapResult ? match.homeTeam : match.awayTeam);
          break;
        case 'OVER_UNDER':
          const totalGoals = match.homeScore + match.awayScore;
          actualOutcome = totalGoals > 2.5 ? 'Over 2.5' : 'Under 2.5';
          isCorrect = prediction.prediction === actualOutcome;
          break;
        case 'CORNERS':
          // Simulate corners (random for demo)
          const totalCorners = Math.floor(Math.random() * 15) + 5;
          actualOutcome = totalCorners > 9.5 ? 'Over 9.5' : 'Under 9.5';
          isCorrect = prediction.prediction === actualOutcome;
          break;
      }

      await prisma.result.create({
        data: {
          matchId: match.id,
          predictionId: prediction.id,
          category: prediction.category,
          isCorrect,
          actualOutcome,
          updatedBy: 'system'
        }
      });
    }
  }

  console.log('✅ Results created for finished matches');

  // Create initial league stats
  for (const league of leagues) {
    await prisma.leagueStats.create({
      data: {
        leagueId: league.id,
        season: league.season,
        matchResultAcc: 40 + Math.random() * 30,
        handicapAcc: 50 + Math.random() * 30,
        overUnderAcc: 45 + Math.random() * 25,
        cornersAcc: 60 + Math.random() * 20,
        totalPredictions: 20,
        correctPredictions: 8 + Math.floor(Math.random() * 8),
        periodStart: new Date('2024-01-01'),
        periodEnd: new Date()
      }
    });
  }

  console.log('✅ League stats created');
  console.log('🎉 Database seeded successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Error seeding database:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
