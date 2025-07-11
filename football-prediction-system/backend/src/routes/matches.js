const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Get upcoming matches
router.get('/upcoming', async (req, res) => {
  try {
    const { leagueId, limit = 10 } = req.query;
    
    const where = {
      status: 'UPCOMING',
      matchDate: { gte: new Date() }
    };
    
    if (leagueId) {
      where.leagueId = leagueId;
    }
    
    const matches = await prisma.match.findMany({
      where,
      include: {
        league: true,
        predictions: true,
        results: true
      },
      orderBy: [
        { matchDate: 'asc' },
        { matchTime: 'asc' }
      ],
      take: parseInt(limit)
    });
    
    res.json({
      success: true,
      data: matches
    });
  } catch (error) {
    console.error('Error fetching upcoming matches:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch upcoming matches'
    });
  }
});

// Get previous matches (last 2 weeks)
router.get('/previous', async (req, res) => {
  try {
    const { leagueId, weeks = 2 } = req.query;
    
    const twoWeeksAgo = new Date();
    twoWeeksAgo.setDate(twoWeeksAgo.getDate() - (parseInt(weeks) * 7));
    
    const where = {
      status: 'FINISHED',
      matchDate: { 
        gte: twoWeeksAgo,
        lte: new Date()
      }
    };
    
    if (leagueId) {
      where.leagueId = leagueId;
    }
    
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
    
    res.json({
      success: true,
      data: matches
    });
  } catch (error) {
    console.error('Error fetching previous matches:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch previous matches'
    });
  }
});

// Get matches by league
router.get('/league/:leagueId', async (req, res) => {
  try {
    const { leagueId } = req.params;
    const { status, limit = 20 } = req.query;
    
    const where = { leagueId };
    if (status) {
      where.status = status;
    }
    
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
      ],
      take: parseInt(limit)
    });
    
    res.json({
      success: true,
      data: matches
    });
  } catch (error) {
    console.error('Error fetching league matches:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch league matches'
    });
  }
});

// Get match by ID
router.get('/:matchId', async (req, res) => {
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
    
    res.json({
      success: true,
      data: match
    });
  } catch (error) {
    console.error('Error fetching match:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch match'
    });
  }
});

module.exports = router;
