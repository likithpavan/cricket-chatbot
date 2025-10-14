"""
Setup script to load your JSON data into database
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import CricketDatabase
import json

def setup():
    print("🏏 Setting up Cricket Database...")
    
    # Initialize database
    db = CricketDatabase()
    
    # Path to your JSON file (relative to backend directory)
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "cricket_data.json")
    
    # Check if file exists
    if not os.path.exists(json_path):
        print(f"❌ JSON file not found at {json_path}")
        print("Please place your JSON file in the data folder")
        return
    
    # Load data
    print(f"📂 Loading data from {json_path}")
    db.load_json_data(json_path)
    
    # Test query
    result = db.execute_query("SELECT COUNT(*) as count FROM players")
    player_count = result.iloc[0]['count'] if not result.empty else 0
    
    print(f"✅ Database setup complete!")
    print(f"📊 Loaded {player_count} players")
    
    # Show sample data
    players = db.execute_query("SELECT * FROM players LIMIT 5")
    if not players.empty:
        print("\n📋 Sample Players:")
        for _, player in players.iterrows():
            print(f"  - {player['full_name']}")

if __name__ == "__main__":
    setup()
