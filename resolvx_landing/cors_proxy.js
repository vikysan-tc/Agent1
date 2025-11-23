/**
 * CORS Proxy Solution for Local Development
 * 
 * This file provides alternative solutions to handle CORS issues:
 * 
 * Option 1: Use a CORS proxy service (easiest, no setup required)
 * Option 2: Use the local Python proxy server (proxy_server.py)
 * Option 3: Browser extension (Chrome/Firefox)
 */

// Option 1: CORS Proxy Service (No setup required)
// Uncomment and use this if you want a quick solution
const USE_CORS_PROXY = false; // Set to true to use a public CORS proxy
const CORS_PROXY_URL = 'https://cors-anywhere.herokuapp.com/'; // Public CORS proxy

// Option 2: Local Proxy Server (Recommended for development)
// Run: python proxy_server.py
// Then set USE_LOCAL_PROXY to true
const USE_LOCAL_PROXY = true; // Set to true if running local proxy
const LOCAL_PROXY_URL = 'http://localhost:8001'; // Local proxy server URL

// Original CRM Server URL
const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';

/**
 * Get the API URL based on proxy settings
 */
function getApiUrl(endpoint = '/api/tickets') {
    if (USE_LOCAL_PROXY) {
        return `${LOCAL_PROXY_URL}${endpoint}`;
    } else if (USE_CORS_PROXY) {
        return `${CORS_PROXY_URL}${CRM_SERVER_URL}${endpoint}`;
    } else {
        return `${CRM_SERVER_URL}${endpoint}`;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getApiUrl };
}

