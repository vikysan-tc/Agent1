/**
 * Configuration file for Landing Page and Dashboard
 * 
 * Update these values based on your environment:
 * - Development: Use local proxy
 * - Production: Use direct CRM API (requires CORS on server)
 */

// Environment detection
const IS_PRODUCTION = window.location.hostname !== 'localhost' && 
                      window.location.hostname !== '127.0.0.1' &&
                      !window.location.hostname.startsWith('192.168.');

// CRM Server Configuration
const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';

// Proxy Configuration (for local development)
const USE_LOCAL_PROXY = !IS_PRODUCTION; // Automatically false in production
const LOCAL_PROXY_URL = 'http://localhost:8001';

// API Endpoints
const TICKETS_API_URL = USE_LOCAL_PROXY 
    ? `${LOCAL_PROXY_URL}/api/tickets`
    : `${CRM_SERVER_URL}/api/tickets`;

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        IS_PRODUCTION,
        CRM_SERVER_URL,
        USE_LOCAL_PROXY,
        LOCAL_PROXY_URL,
        TICKETS_API_URL
    };
}

