#!/usr/bin/env python3
"""
Start the web interface for the AI automation system
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def start_web_interface():
    """Start the web interface server"""
    port = 8081  # Use port 8081 to avoid conflicts
    
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    # Create a custom handler that serves the goal interface
    class WebInterfaceHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.getcwd(), **kwargs)
        
        def do_GET(self):
            if self.path == '/':
                self.path = '/goal_interface.html'
            return super().do_GET()
    
    try:
        with socketserver.TCPServer(("", port), WebInterfaceHandler) as httpd:
            print(f"🌐 Web Interface Server starting...")
            print(f"📱 Open your browser and go to: http://localhost:{port}")
            print(f"🤖 AI Automation Interface is ready!")
            print(f"📝 You can now submit any goal and see the AI automation in action!")
            print(f"⏹️  Press Ctrl+C to stop the server")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{port}')
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Web Interface Server stopped")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_web_interface_on_port(port + 1)
        else:
            print(f"❌ Error starting server: {e}")

def start_web_interface_on_port(port):
    """Start web interface on a specific port"""
    class WebInterfaceHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.getcwd(), **kwargs)
        
        def do_GET(self):
            if self.path == '/':
                self.path = '/goal_interface.html'
            return super().do_GET()
    
    try:
        with socketserver.TCPServer(("", port), WebInterfaceHandler) as httpd:
            print(f"🌐 Web Interface Server starting on port {port}...")
            print(f"📱 Open your browser and go to: http://localhost:{port}")
            print(f"🤖 AI Automation Interface is ready!")
            print(f"📝 You can now submit any goal and see the AI automation in action!")
            print(f"⏹️  Press Ctrl+C to stop the server")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{port}')
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Web Interface Server stopped")
    except Exception as e:
        print(f"❌ Error starting server on port {port}: {e}")

if __name__ == "__main__":
    start_web_interface()
