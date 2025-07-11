const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');

// Get all matches for admin dropdown
router.get('/matches', adminController.getAllMatches);

// Get match details by ID
router.get('/matches/:matchId', adminController.getMatchDetails);

// Update single prediction result
router.post('/results/update', adminController.updatePredictionResult);

// Bulk update prediction results
router.post('/results/bulk-update', adminController.bulkUpdateResults);

// Get accuracy statistics
router.get('/stats/accuracy', adminController.getAccuracyStats);

// Move completed matches (maintenance)
router.post('/maintenance/move-completed', adminController.moveCompletedMatches);

// Get prediction categories (for dropdown)
router.get('/categories', (req, res) => {
  res.json({
    success: true,
    data: [
      { value: 'MATCH_RESULT', label: 'Match Result' },
      { value: 'HANDICAP', label: 'Handicap' },
      { value: 'OVER_UNDER', label: 'Over/Under' },
      { value: 'CORNERS', label: 'Corners' }
    ]
  });
});

// Get leagues (for dropdown)
router.get('/leagues', async (req, res) => {
  try {
    const { PrismaClient } = require('@prisma/client');
    const prisma = new PrismaClient();
    
    const leagues = await prisma.league.findMany({
      where: { isActive: true },
      select: {
        id: true,
        name: true,
        country: true
      },
      orderBy: { name: 'asc' }
    });
    
    res.json({
      success: true,
      data: leagues.map(league => ({
        value: league.id,
        label: `${league.name} (${league.country})`
      }))
    });
  } catch (error) {
    console.error('Error fetching leagues:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch leagues'
    });
  }
});

// Get match statuses (for dropdown)
router.get('/statuses', (req, res) => {
  res.json({
    success: true,
    data: [
      { value: 'UPCOMING', label: 'Upcoming' },
      { value: 'LIVE', label: 'Live' },
      { value: 'FINISHED', label: 'Finished' },
      { value: 'POSTPONED', label: 'Postponed' },
      { value: 'CANCELLED', label: 'Cancelled' }
    ]
  });
});

module.exports = router;
