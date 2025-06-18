import sys
import os

# Add Tutex/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import Base, engine
from backend.models import User

# Create all tables
Base.metadata.create_all(bind=engine)