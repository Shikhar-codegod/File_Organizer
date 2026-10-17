"""
File Organizer - Web UI & Engine
Launches the modern, sleek HTML/Flask interface by default.
"""

import sys
import os

if __name__ == '__main__':
    # Launch the sleek web UI with HTML frontend
    from app import app, open_browser, threading
    
    threading.Thread(target=open_browser, daemon=True).start()
    print("==================================================")
    print(" 🚀 File Organizer Web UI is running!")
    print(" 🌐 Opening browser at: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=False)