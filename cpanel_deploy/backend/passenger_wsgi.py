import sys
import os

# Add your project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app

# This is the WSGI application
application = app