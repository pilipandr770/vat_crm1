#!/usr/bin/env python3
"""Entry point for running the Flask application."""

import sys
import os

# Add the parent directory to the Python path so we can import the backend package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
