"""
Launch Server - Serves the web interface for the automation system
"""

import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

class LaunchHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/goal_interface.html'
        return super().do_GET()

def start_launch_server():
    """Start the launch server"""
    port = 8080
    server = HTTPServer(('localhost', port), LaunchHandler)
    
    print("🌐 Starting Launch Server...")
    print("=" * 50)
    print(f"🚀 Launch Page: http://localhost:{port}")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    print("💡 Click the 'Launch Automation' button to start!")
    print("=" * 50)
    
    # Open browser automatically
    threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Launch server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_launch_server()
