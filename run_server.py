import subprocess
import sys
import os
from webapp_server import start_server

def run_in_background():
    """Run the server in background without showing console window"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "background":
        # This runs the actual server
        start_server(8000)
    else:
        # This starts the background process
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        
        # Start as background process (no window)
        subprocess.Popen([
            python_exe, script_path, "background"
        ], creationflags=subprocess.CREATE_NO_WINDOW)
        
        print("Webapp server started in background")
        print("Access at: http://localhost:8000")
        print("To stop: Use Task Manager or restart computer")

if __name__ == "__main__":
    run_in_background()