const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Get all leagues
router.get('/', async (req, res) => {
  try {
    const leagues = await prisma.league.findMany({
      where: { isActive: true },
      include: {
        _count: {
          select: {
            matches: true
          }
        },
        stats: {
          orderBy: { createdAt: 'desc' },
          take: 1
        }
      },
      orderBy: { name: 'asc' }
    });
    
    res.json({
      success: true,
      data: leagues
    });
  } catch (error) {
    console.error('Error fetching leagues:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch leagues'
    });
  }
});

// Get league statistics
router.get('/:leagueId/stats', async (req, res) => {
  try {
    const { leagueId } = req.params;
    
    const stats = await prisma.leagueStats.findMany({
      where: { leagueId },
      orderBy: { createdAt: 'desc' },
      take: 1
    });
    
    if (stats.length === 0) {
      return res.json({
        success: true,
        data: {
          matchResultAcc: 0,
          handicapAcc: 0,
          overUnderAcc: 0,
          cornersAcc: 0,
          totalPredictions: 0,
          correctPredictions: 0
        }
      });
    }
    
    res.json({
      success: true,
      data: stats[0]
    });
  } catch (error) {
    console.error('Error fetching league stats:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch league statistics'
    });
  }
});

// Get league data with matches and predictions
router.get('/:leagueId/data', async (req, res) => {
  try {
    const { leagueId } = req.params;
    
    // Get league info
    const league = await prisma.league.findUnique({
      where: { id: leagueId },
      include: {
        stats: {
          orderBy: { createdAt: 'desc' },
          take: 1
        }
      }
    });
    
    if (!league) {
      return res.status(404).json({
        success: false,
        error: 'League not found'
      });
    }
    
    // Get upcoming matches
    const upcomingMatches = await prisma.match.findMany({
      where: {
        leagueId,
        status: 'UPCOMING'
      },
      include: {
        predictions: true,
        results: true
      },
      orderBy: [
        { matchDate: 'asc' },
        { matchTime: 'asc' }
      ],
      take: 10
    });
    
    // Get previous matches (last 2 weeks)
    const twoWeeksAgo = new Date();
    twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);
    
    const previousMatches = await prisma.match.findMany({
      where: {
        leagueId,
        status: 'FINISHED',
        matchDate: { gte: twoWeeksAgo }
      },
      include: {
        predictions: true,
        results: true
      },
      orderBy: [
        { matchDate: 'desc' },
        { matchTime: 'desc' }
      ]
    });
    
    res.json({
      success: true,
      data: {
        league,
        upcomingMatches,
        previousMatches,
        stats: league.stats[0] || {
          matchResultAcc: 0,
          handicapAcc: 0,
          overUnderAcc: 0,
          cornersAcc: 0,
          totalPredictions: 0,
          correctPredictions: 0
        }
      }
    });
  } catch (error) {
    console.error('Error fetching league data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch league data'
    });
  }
});

module.exports = router;
