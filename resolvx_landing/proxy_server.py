#!/usr/bin/env python3
"""
Simple CORS proxy server for local development.
This server proxies requests to the CRM API and adds CORS headers.

Usage:
    python proxy_server.py

Then access the landing page at http://localhost:8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
import sys

# CRM Server URL
CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver'

class CORSProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
        self.send_header('Access-Control-Max-Age', '3600')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests and proxy to CRM API"""
        # Only proxy requests to /api/tickets
        if self.path.startswith('/api/tickets'):
            try:
                # Build the full URL
                target_url = f"{CRM_SERVER_URL}{self.path}"
                
                # Make request to CRM server
                req = Request(target_url)
                req.add_header('Accept', 'application/json')
                
                try:
                    with urlopen(req, timeout=30) as response:
                        data = response.read()
                        status_code = response.getcode()
                        
                        # Send response with CORS headers
                        self.send_response(status_code)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(data)
                        
                except URLError as e:
                    self.send_error(502, f"Bad Gateway: {str(e)}")
                    
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            # For other paths, serve files normally (if needed)
            self.send_error(404, "Not Found")
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        # Uncomment the next line if you want to see proxy requests
        # print(f"[PROXY] {format % args}")
        pass

def run_proxy_server(port=8001):
    """Run the CORS proxy server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSProxyHandler)
    print(f"🚀 CORS Proxy Server running on http://localhost:{port}")
    print(f"📡 Proxying requests to: {CRM_SERVER_URL}")
    print(f"💡 Update dashboard.js to use: http://localhost:{port}/api/tickets")
    print("\nPress Ctrl+C to stop the server\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down proxy server...")
        httpd.shutdown()

if __name__ == '__main__':
    port = 8001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    run_proxy_server(port)

