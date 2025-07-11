const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Constants for categories and statuses
const PREDICTION_CATEGORIES = {
  MATCH_RESULT: 'MATCH_RESULT',
  HANDICAP: 'HANDICAP',
  OVER_UNDER: 'OVER_UNDER',
  CORNERS: 'CORNERS'
};

const MATCH_STATUSES = {
  UPCOMING: 'UPCOMING',
  LIVE: 'LIVE',
  FINISHED: 'FINISHED',
  POSTPONED: 'POSTPONED',
  CANCELLED: 'CANCELLED'
};

class AdminController {
  // Get all matches for admin dropdown
  async getAllMatches(req, res) {
    try {
      const { status, league } = req.query;
      
      const where = {};
      if (status) where.status = status;
      if (league) where.leagueId = league;
      
      const matches = await prisma.match.findMany({
        where,
        include: {
          league: true,
          predictions: true,
          results: true
        },
        orderBy: [
          { matchDate: 'desc' },
          { matchTime: 'desc' }
        ]
      });
      
      // Format for dropdown
      const formattedMatches = matches.map(match => ({
        id: match.id,
        label: `#${match.id} - ${match.homeTeam} vs ${match.awayTeam}`,
        homeTeam: match.homeTeam,
        awayTeam: match.awayTeam,
        date: match.matchDate,
        time: match.matchTime,
        league: match.league.name,
        status: match.status,
        hasResults: match.results.length > 0
      }));
      
      res.json({
        success: true,
        data: formattedMatches,
        total: formattedMatches.length
      });
    } catch (error) {
      console.error('Error fetching matches:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch matches'
      });
    }
  }
  
  // Get match details by ID
  async getMatchDetails(req, res) {
    try {
      const { matchId } = req.params;
      
      const match = await prisma.match.findUnique({
        where: { id: parseInt(matchId) },
        include: {
          league: true,
          predictions: true,
          results: true
        }
      });
      
      if (!match) {
        return res.status(404).json({
          success: false,
          error: 'Match not found'
        });
      }
      
      // Format predictions with results
      const predictionsWithResults = match.predictions.map(prediction => {
        const result = match.results.find(r => r.category === prediction.category);
        return {
          ...prediction,
          result: result ? {
            isCorrect: result.isCorrect,
            actualOutcome: result.actualOutcome,
            updatedBy: result.updatedBy,
            updatedAt: result.updatedAt
          } : null
        };
      });
      
      res.json({
        success: true,
        data: {
          ...match,
          predictions: predictionsWithResults
        }
      });
    } catch (error) {
      console.error('Error fetching match details:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch match details'
      });
    }
  }
  
  // Update prediction result
  async updatePredictionResult(req, res) {
    try {
      const { matchId, category, isCorrect, actualOutcome, updatedBy } = req.body;
      
      // Validation
      if (!matchId || !category || typeof isCorrect !== 'boolean') {
        return res.status(400).json({
          success: false,
          error: 'Missing required fields: matchId, category, isCorrect'
        });
      }
      
      // Validate category
      if (!Object.values(PREDICTION_CATEGORIES).includes(category)) {
        return res.status(400).json({
          success: false,
          error: 'Invalid category'
        });
      }
      
      // Find the prediction
      const prediction = await prisma.prediction.findFirst({
        where: {
          matchId: parseInt(matchId),
          category: category
        }
      });
      
      if (!prediction) {
        return res.status(404).json({
          success: false,
          error: 'Prediction not found'
        });
      }
      
      // Check if result already exists
      const existingResult = await prisma.result.findFirst({
        where: {
          matchId: parseInt(matchId),
          category: category
        }
      });
      
      let result;
      if (existingResult) {
        // Update existing result
        result = await prisma.result.update({
          where: { id: existingResult.id },
          data: {
            isCorrect,
            actualOutcome: actualOutcome || '',
            updatedBy: updatedBy || 'admin',
            updatedAt: new Date()
          }
        });
      } else {
        // Create new result
        result = await prisma.result.create({
          data: {
            matchId: parseInt(matchId),
            predictionId: prediction.id,
            category: category,
            isCorrect,
            actualOutcome: actualOutcome || '',
            updatedBy: updatedBy || 'admin'
          }
        });
      }
      
      // Update league statistics
      const match = await prisma.match.findUnique({
        where: { id: parseInt(matchId) }
      });
      
      if (match) {
        await this.updateLeagueStats(match.leagueId);
      }
      
      res.json({
        success: true,
        message: 'Prediction result updated successfully',
        data: result
      });
    } catch (error) {
      console.error('Error updating prediction result:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to update prediction result'
      });
    }
  }
  
  // Bulk update results
  async bulkUpdateResults(req, res) {
    try {
      const { updates, updatedBy } = req.body;
      
      if (!Array.isArray(updates) || updates.length === 0) {
        return res.status(400).json({
          success: false,
          error: 'Updates array is required'
        });
      }
      
      const results = [];
      const errors = [];
      
      for (const update of updates) {
        try {
          const { matchId, category, isCorrect, actualOutcome } = update;
          
          // Find prediction
          const prediction = await prisma.prediction.findFirst({
            where: {
              matchId: parseInt(matchId),
              category: category
            }
          });
          
          if (!prediction) {
            errors.push(`Prediction not found for match ${matchId}, category ${category}`);
            continue;
          }
          
          // Check if result exists
          const existingResult = await prisma.result.findFirst({
            where: {
              matchId: parseInt(matchId),
              category: category
            }
          });
          
          let result;
          if (existingResult) {
            result = await prisma.result.update({
              where: { id: existingResult.id },
              data: {
                isCorrect,
                actualOutcome: actualOutcome || '',
                updatedBy: updatedBy || 'admin',
                updatedAt: new Date()
              }
            });
          } else {
            result = await prisma.result.create({
              data: {
                matchId: parseInt(matchId),
                predictionId: prediction.id,
                category: category,
                isCorrect,
                actualOutcome: actualOutcome || '',
                updatedBy: updatedBy || 'admin'
              }
            });
          }
          
          results.push(result);
        } catch (error) {
          errors.push(`Error updating match ${update.matchId}: ${error.message}`);
        }
      }
      
      res.json({
        success: true,
        message: `Updated ${results.length} results`,
        data: {
          updated: results.length,
          errors: errors
        }
      });
    } catch (error) {
      console.error('Error bulk updating results:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to bulk update results'
      });
    }
  }
  
  // Get accuracy statistics
  async getAccuracyStats(req, res) {
    try {
      const { leagueId, period } = req.query;
      
      // Calculate date range
      let startDate = new Date();
      switch (period) {
        case 'week':
          startDate.setDate(startDate.getDate() - 7);
          break;
        case 'month':
          startDate.setMonth(startDate.getMonth() - 1);
          break;
        case 'season':
          startDate.setMonth(startDate.getMonth() - 6);
          break;
        default:
          startDate.setDate(startDate.getDate() - 30);
      }
      
      const where = {
        createdAt: { gte: startDate }
      };
      
      if (leagueId) {
        where.match = { leagueId };
      }
      
      // Get all results in period
      const results = await prisma.result.findMany({
        where,
        include: {
          match: {
            include: { league: true }
          }
        }
      });
      
      // Calculate statistics
      const stats = {
        overall: { correct: 0, total: 0, accuracy: 0 },
        byCategory: {},
        byLeague: {}
      };
      
      results.forEach(result => {
        // Overall stats
        stats.overall.total++;
        if (result.isCorrect) stats.overall.correct++;
        
        // By category
        if (!stats.byCategory[result.category]) {
          stats.byCategory[result.category] = { correct: 0, total: 0, accuracy: 0 };
        }
        stats.byCategory[result.category].total++;
        if (result.isCorrect) stats.byCategory[result.category].correct++;
        
        // By league
        const leagueName = result.match.league.name;
        if (!stats.byLeague[leagueName]) {
          stats.byLeague[leagueName] = { correct: 0, total: 0, accuracy: 0 };
        }
        stats.byLeague[leagueName].total++;
        if (result.isCorrect) stats.byLeague[leagueName].correct++;
      });
      
      // Calculate accuracy percentages
      stats.overall.accuracy = stats.overall.total > 0 
        ? (stats.overall.correct / stats.overall.total * 100).toFixed(1)
        : 0;
      
      Object.keys(stats.byCategory).forEach(category => {
        const cat = stats.byCategory[category];
        cat.accuracy = cat.total > 0 ? (cat.correct / cat.total * 100).toFixed(1) : 0;
      });
      
      Object.keys(stats.byLeague).forEach(league => {
        const lg = stats.byLeague[league];
        lg.accuracy = lg.total > 0 ? (lg.correct / lg.total * 100).toFixed(1) : 0;
      });
      
      res.json({
        success: true,
        data: stats,
        period: period || 'month',
        dateRange: {
          start: startDate,
          end: new Date()
        }
      });
    } catch (error) {
      console.error('Error fetching accuracy stats:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch accuracy statistics'
      });
    }
  }
  
  // Move completed matches to previous
  async moveCompletedMatches(req, res) {
    try {
      const { weekOffset = 1 } = req.body;
      
      // Find matches that are completed and older than specified weeks
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - (weekOffset * 7));
      
      const completedMatches = await prisma.match.findMany({
        where: {
          status: MATCH_STATUSES.FINISHED,
          matchDate: { lt: cutoffDate }
        }
      });
      
      // This is handled by the frontend display logic
      // We don't actually move data, just mark it appropriately
      
      res.json({
        success: true,
        message: `Found ${completedMatches.length} completed matches older than ${weekOffset} week(s)`,
        data: {
          matchesFound: completedMatches.length,
          cutoffDate: cutoffDate
        }
      });
    } catch (error) {
      console.error('Error moving completed matches:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to move completed matches'
      });
    }
  }
  
  // Helper method to update league statistics
  async updateLeagueStats(leagueId) {
    if (!leagueId) return;
    
    try {
      // Get all results for this league
      const results = await prisma.result.findMany({
        where: {
          match: { leagueId }
        }
      });
      
      // Calculate stats by category
      const stats = {
        [PREDICTION_CATEGORIES.MATCH_RESULT]: { correct: 0, total: 0 },
        [PREDICTION_CATEGORIES.HANDICAP]: { correct: 0, total: 0 },
        [PREDICTION_CATEGORIES.OVER_UNDER]: { correct: 0, total: 0 },
        [PREDICTION_CATEGORIES.CORNERS]: { correct: 0, total: 0 }
      };
      
      results.forEach(result => {
        if (stats[result.category]) {
          stats[result.category].total++;
          if (result.isCorrect) stats[result.category].correct++;
        }
      });
      
      // Update or create league stats
      const currentSeason = new Date().getFullYear().toString();
      const periodStart = new Date();
      periodStart.setMonth(periodStart.getMonth() - 1);
      
      // Check if stats exist
      const existingStats = await prisma.leagueStats.findFirst({
        where: {
          leagueId,
          season: currentSeason,
          periodStart: { gte: periodStart }
        }
      });
      
      const statsData = {
        matchResultAcc: stats[PREDICTION_CATEGORIES.MATCH_RESULT].total > 0 
          ? (stats[PREDICTION_CATEGORIES.MATCH_RESULT].correct / stats[PREDICTION_CATEGORIES.MATCH_RESULT].total * 100) 
          : 0,
        handicapAcc: stats[PREDICTION_CATEGORIES.HANDICAP].total > 0 
          ? (stats[PREDICTION_CATEGORIES.HANDICAP].correct / stats[PREDICTION_CATEGORIES.HANDICAP].total * 100) 
          : 0,
        overUnderAcc: stats[PREDICTION_CATEGORIES.OVER_UNDER].total > 0 
          ? (stats[PREDICTION_CATEGORIES.OVER_UNDER].correct / stats[PREDICTION_CATEGORIES.OVER_UNDER].total * 100) 
          : 0,
        cornersAcc: stats[PREDICTION_CATEGORIES.CORNERS].total > 0 
          ? (stats[PREDICTION_CATEGORIES.CORNERS].correct / stats[PREDICTION_CATEGORIES.CORNERS].total * 100) 
          : 0,
        totalPredictions: results.length,
        correctPredictions: results.filter(r => r.isCorrect).length,
        updatedAt: new Date()
      };
      
      if (existingStats) {
        await prisma.leagueStats.update({
          where: { id: existingStats.id },
          data: statsData
        });
      } else {
        await prisma.leagueStats.create({
          data: {
            leagueId,
            season: currentSeason,
            periodStart,
            periodEnd: new Date(),
            ...statsData
          }
        });
      }
    } catch (error) {
      console.error('Error updating league stats:', error);
    }
  }
}

module.exports = new AdminController();
