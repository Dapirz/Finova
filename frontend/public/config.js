// Configuration for API endpoints
// Use backend URL from environment or default to /api for local
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8001/api'
    : 'https://budget-master-389.preview.emergentagent.com/api';