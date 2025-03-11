import subprocess
import sys
import time
import os
import webbrowser
import threading

def run_api_server():
    """Run the Flask API server"""
    print("Starting API server...")
    env = os.environ.copy()
    env["FLASK_APP"] = "app/api.py"
    env["CONFIG_FILE"] = "config.yaml"
    
    api_process = subprocess.Popen(
        ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Wait for API server to start
    for line in api_process.stdout:
        print(f"API: {line.strip()}")
        if "Running on" in line:
            break
    
    return api_process

def run_web_interface():
    """Run the Streamlit web interface"""
    print("Starting web interface...")
    web_process = subprocess.Popen(
        ["python", "-m", "streamlit", "run", "web/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Wait for web interface to start
    for line in web_process.stdout:
        print(f"Web: {line.strip()}")
        if "You can now view your Streamlit app in your browser" in line:
            break
    
    return web_process

def open_browser():
    """Open the web browser to the Streamlit interface"""
    time.sleep(5)  # Give some time for servers to start
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    print("Financial Report Summarizer System")
    print("=================================")
    
    # Install required packages if needed
    print("Checking and installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start API server
    api_process = run_api_server()
    
    # Start web interface
    web_process = run_web_interface()
    
    # Open browser
    threading.Thread(target=open_browser).start()
    
    print("\nSystem is running!")
    print("API server: http://localhost:5000")
    print("Web interface: http://localhost:8501")
    print("\nPress Ctrl+C to stop the system")
    
    try:
        # Keep the script running
        api_process.wait()
    except KeyboardInterrupt:
        print("\nStopping the system...")
        api_process.terminate()
        web_process.terminate()
        print("System stopped.") 