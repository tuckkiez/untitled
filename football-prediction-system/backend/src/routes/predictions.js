const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Get predictions for a match
router.get('/match/:matchId', async (req, res) => {
  try {
    const { matchId } = req.params;
    
    const predictions = await prisma.prediction.findMany({
      where: { matchId: parseInt(matchId) },
      include: {
        match: {
          include: { league: true }
        },
        results: true
      }
    });
    
    res.json({
      success: true,
      data: predictions
    });
  } catch (error) {
    console.error('Error fetching match predictions:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch match predictions'
    });
  }
});

// Get predictions by league
router.get('/league/:leagueId', async (req, res) => {
  try {
    const { leagueId } = req.params;
    const { category, limit = 50 } = req.query;
    
    const where = {
      match: { leagueId }
    };
    
    if (category) {
      where.category = category;
    }
    
    const predictions = await prisma.prediction.findMany({
      where,
      include: {
        match: {
          include: { league: true }
        },
        results: true
      },
      orderBy: {
        createdAt: 'desc'
      },
      take: parseInt(limit)
    });
    
    res.json({
      success: true,
      data: predictions
    });
  } catch (error) {
    console.error('Error fetching league predictions:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch league predictions'
    });
  }
});

module.exports = router;
