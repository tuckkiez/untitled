const cron = require('node-cron');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

class SchedulerService {
  constructor() {
    this.tasks = [];
  }

  startScheduledTasks() {
    console.log('⏰ Starting scheduled tasks...');

    // Task 1: Update match statuses every hour
    const updateMatchStatusTask = cron.schedule('0 * * * *', async () => {
      console.log('🔄 Running match status update...');
      await this.updateMatchStatuses();
    }, {
      scheduled: false
    });

    // Task 2: Clean old data daily at 2 AM
    const cleanupTask = cron.schedule('0 2 * * *', async () => {
      console.log('🧹 Running daily cleanup...');
      await this.cleanupOldData();
    }, {
      scheduled: false
    });

    // Task 3: Update league statistics every 6 hours
    const updateStatsTask = cron.schedule('0 */6 * * *', async () => {
      console.log('📊 Updating league statistics...');
      await this.updateLeagueStatistics();
    }, {
      scheduled: false
    });

    // Start tasks only if enabled in environment
    if (process.env.ENABLE_SCHEDULED_TASKS === 'true') {
      updateMatchStatusTask.start();
      cleanupTask.start();
      updateStatsTask.start();

      this.tasks.push(updateMatchStatusTask, cleanupTask, updateStatsTask);
      console.log('✅ Scheduled tasks started');
    } else {
      console.log('⏸️ Scheduled tasks disabled (set ENABLE_SCHEDULED_TASKS=true to enable)');
    }
  }

  async updateMatchStatuses() {
    try {
      const now = new Date();
      
      // Update matches that should be LIVE (within match time window)
      const matchesToLive = await prisma.match.updateMany({
        where: {
          status: 'UPCOMING',
          matchDate: {
            lte: now
          }
        },
        data: {
          status: 'LIVE'
        }
      });

      // Update matches that should be FINISHED (2 hours after match time)
      const twoHoursAgo = new Date(now.getTime() - 2 * 60 * 60 * 1000);
      const matchesToFinish = await prisma.match.updateMany({
        where: {
          status: 'LIVE',
          matchDate: {
            lte: twoHoursAgo
          }
        },
        data: {
          status: 'FINISHED'
        }
      });

      console.log(`📊 Updated ${matchesToLive.count} matches to LIVE, ${matchesToFinish.count} to FINISHED`);
    } catch (error) {
      console.error('❌ Error updating match statuses:', error);
    }
  }

  async cleanupOldData() {
    try {
      // Delete matches older than 6 months
      const sixMonthsAgo = new Date();
      sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

      const deletedMatches = await prisma.match.deleteMany({
        where: {
          matchDate: {
            lt: sixMonthsAgo
          },
          status: 'FINISHED'
        }
      });

      // Delete old league stats (keep last 3 months)
      const threeMonthsAgo = new Date();
      threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);

      const deletedStats = await prisma.leagueStats.deleteMany({
        where: {
          createdAt: {
            lt: threeMonthsAgo
          }
        }
      });

      console.log(`🧹 Cleaned up ${deletedMatches.count} old matches, ${deletedStats.count} old stats`);
    } catch (error) {
      console.error('❌ Error during cleanup:', error);
    }
  }

  async updateLeagueStatistics() {
    try {
      const leagues = await prisma.league.findMany({
        where: { isActive: true }
      });

      for (const league of leagues) {
        await this.calculateLeagueStats(league.id);
      }

      console.log(`📊 Updated statistics for ${leagues.length} leagues`);
    } catch (error) {
      console.error('❌ Error updating league statistics:', error);
    }
  }

  async calculateLeagueStats(leagueId) {
    try {
      // Get all results for this league in the last month
      const oneMonthAgo = new Date();
      oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);

      const results = await prisma.result.findMany({
        where: {
          match: { leagueId },
          createdAt: { gte: oneMonthAgo }
        }
      });

      if (results.length === 0) return;

      // Calculate stats by category
      const stats = {
        MATCH_RESULT: { correct: 0, total: 0 },
        HANDICAP: { correct: 0, total: 0 },
        OVER_UNDER: { correct: 0, total: 0 },
        CORNERS: { correct: 0, total: 0 }
      };

      results.forEach(result => {
        if (stats[result.category]) {
          stats[result.category].total++;
          if (result.isCorrect) stats[result.category].correct++;
        }
      });

      // Update or create league stats
      const currentSeason = new Date().getFullYear().toString();
      
      await prisma.leagueStats.upsert({
        where: {
          leagueId_season_periodStart: {
            leagueId,
            season: currentSeason,
            periodStart: oneMonthAgo
          }
        },
        update: {
          matchResultAcc: stats.MATCH_RESULT.total > 0 
            ? (stats.MATCH_RESULT.correct / stats.MATCH_RESULT.total * 100) 
            : 0,
          handicapAcc: stats.HANDICAP.total > 0 
            ? (stats.HANDICAP.correct / stats.HANDICAP.total * 100) 
            : 0,
          overUnderAcc: stats.OVER_UNDER.total > 0 
            ? (stats.OVER_UNDER.correct / stats.OVER_UNDER.total * 100) 
            : 0,
          cornersAcc: stats.CORNERS.total > 0 
            ? (stats.CORNERS.correct / stats.CORNERS.total * 100) 
            : 0,
          totalPredictions: results.length,
          correctPredictions: results.filter(r => r.isCorrect).length,
          updatedAt: new Date()
        },
        create: {
          leagueId,
          season: currentSeason,
          matchResultAcc: stats.MATCH_RESULT.total > 0 
            ? (stats.MATCH_RESULT.correct / stats.MATCH_RESULT.total * 100) 
            : 0,
          handicapAcc: stats.HANDICAP.total > 0 
            ? (stats.HANDICAP.correct / stats.HANDICAP.total * 100) 
            : 0,
          overUnderAcc: stats.OVER_UNDER.total > 0 
            ? (stats.OVER_UNDER.correct / stats.OVER_UNDER.total * 100) 
            : 0,
          cornersAcc: stats.CORNERS.total > 0 
            ? (stats.CORNERS.correct / stats.CORNERS.total * 100) 
            : 0,
          totalPredictions: results.length,
          correctPredictions: results.filter(r => r.isCorrect).length,
          periodStart: oneMonthAgo,
          periodEnd: new Date()
        }
      });
    } catch (error) {
      console.error(`❌ Error calculating stats for league ${leagueId}:`, error);
    }
  }

  stopAllTasks() {
    console.log('⏹️ Stopping all scheduled tasks...');
    this.tasks.forEach(task => {
      if (task) {
        task.stop();
      }
    });
    this.tasks = [];
    console.log('✅ All scheduled tasks stopped');
  }

  // Manual trigger methods for testing
  async triggerMatchStatusUpdate() {
    console.log('🔄 Manually triggering match status update...');
    await this.updateMatchStatuses();
  }

  async triggerCleanup() {
    console.log('🧹 Manually triggering cleanup...');
    await this.cleanupOldData();
  }

  async triggerStatsUpdate() {
    console.log('📊 Manually triggering stats update...');
    await this.updateLeagueStatistics();
  }
}

// Export singleton instance
const schedulerService = new SchedulerService();

module.exports = {
  startScheduledTasks: () => schedulerService.startScheduledTasks(),
  stopAllTasks: () => schedulerService.stopAllTasks(),
  triggerMatchStatusUpdate: () => schedulerService.triggerMatchStatusUpdate(),
  triggerCleanup: () => schedulerService.triggerCleanup(),
  triggerStatsUpdate: () => schedulerService.triggerStatsUpdate()
};
