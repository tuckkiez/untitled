import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('admin_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Admin API endpoints
export const adminAPI = {
  // Get all matches for dropdown
  getAllMatches: (params = {}) => 
    api.get('/admin/matches', { params }),
  
  // Get match details by ID
  getMatchDetails: (matchId) => 
    api.get(`/admin/matches/${matchId}`),
  
  // Update prediction result
  updatePredictionResult: (data) => 
    api.post('/admin/results/update', data),
  
  // Bulk update results
  bulkUpdateResults: (data) => 
    api.post('/admin/results/bulk-update', data),
  
  // Get accuracy statistics
  getAccuracyStats: (params = {}) => 
    api.get('/admin/stats/accuracy', { params }),
  
  // Get categories for dropdown
  getCategories: () => 
    api.get('/admin/categories'),
  
  // Get leagues for dropdown
  getLeagues: () => 
    api.get('/admin/leagues'),
  
  // Get match statuses for dropdown
  getStatuses: () => 
    api.get('/admin/statuses'),
  
  // Move completed matches
  moveCompletedMatches: (data) => 
    api.post('/admin/maintenance/move-completed', data),
};

// Matches API endpoints
export const matchesAPI = {
  // Get upcoming matches
  getUpcomingMatches: (params = {}) => 
    api.get('/matches/upcoming', { params }),
  
  // Get previous matches (last 2 weeks)
  getPreviousMatches: (params = {}) => 
    api.get('/matches/previous', { params }),
  
  // Get matches by league
  getMatchesByLeague: (leagueId, params = {}) => 
    api.get(`/matches/league/${leagueId}`, { params }),
};

// Predictions API endpoints
export const predictionsAPI = {
  // Get predictions for a match
  getMatchPredictions: (matchId) => 
    api.get(`/predictions/match/${matchId}`),
  
  // Get predictions by league
  getPredictionsByLeague: (leagueId, params = {}) => 
    api.get(`/predictions/league/${leagueId}`, { params }),
};

// Leagues API endpoints
export const leaguesAPI = {
  // Get all leagues
  getAllLeagues: () => 
    api.get('/leagues'),
  
  // Get league statistics
  getLeagueStats: (leagueId) => 
    api.get(`/leagues/${leagueId}/stats`),
  
  // Get league matches with predictions
  getLeagueData: (leagueId) => 
    api.get(`/leagues/${leagueId}/data`),
};

// Export default api instance
export default api;
