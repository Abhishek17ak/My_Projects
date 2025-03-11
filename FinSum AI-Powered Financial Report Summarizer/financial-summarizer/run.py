#!/usr/bin/env python3
"""
Financial Report Summarizer - Main Runner Script
This script provides a simple way to run the Financial Report Summarizer system.
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from time import sleep

def main():
    """Main entry point for the runner script."""
    parser = argparse.ArgumentParser(description="Run the Financial Report Summarizer system")
    parser.add_argument("--mode", choices=["api", "web", "simple", "all"], default="simple",
                        help="Which component to run (api, web, simple, or all)")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open the browser automatically")
    args = parser.parse_args()

    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Check if required packages are installed
    try:
        import streamlit
        import flask
        import nltk
        import networkx
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Run the selected component
    if args.mode == "api":
        run_api()
    elif args.mode == "web":
        run_web(not args.no_browser)
    elif args.mode == "simple":
        run_simple(not args.no_browser)
    elif args.mode == "all":
        run_all(not args.no_browser)

def run_api():
    """Run the API server."""
    print("Starting API server...")
    env = os.environ.copy()
    env["FLASK_APP"] = "app/api.py"
    env["CONFIG_FILE"] = "config.yaml"
    
    subprocess.Popen(
        [sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"],
        env=env
    )
    print("API server running at http://localhost:5000")

def run_web(open_browser=True):
    """Run the web interface."""
    print("Starting web interface...")
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "web/app.py"]
    )
    
    if open_browser:
        sleep(2)  # Give Streamlit time to start
        webbrowser.open("http://localhost:8501")
    
    print("Web interface running at http://localhost:8501")
    return process

def run_simple(open_browser=True):
    """Run the simplified summarizer."""
    print("Starting simplified summarizer...")
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "simple_summarizer.py"]
    )
    
    if open_browser:
        sleep(2)  # Give Streamlit time to start
        webbrowser.open("http://localhost:8501")
    
    print("Simplified summarizer running at http://localhost:8501")
    return process

def run_all(open_browser=True):
    """Run both the API server and web interface."""
    run_api()
    sleep(2)  # Give the API time to start
    return run_web(open_browser)

if __name__ == "__main__":
    try:
        main()
        print("\nPress Ctrl+C to stop the system")
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the system...")
        sys.exit(0) 