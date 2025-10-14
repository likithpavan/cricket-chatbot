"""
Cricket Database Manager for JSON Data
Handles your specific JSON structure
"""
import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CricketDatabase:
    def __init__(self, db_path: str = "cricket_stats.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """Create tables for players, batting, bowling, and matches"""
        cursor = self.conn.cursor()
        
        # Players table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            full_name TEXT,
            batting_style TEXT,
            bowling_style TEXT,
            team TEXT,
            profile_pic TEXT
        )''')
        
        # Batting performances
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS batting_performances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id TEXT,
            player_id INTEGER,
            player_name TEXT,
            runs_scored INTEGER,
            balls_faced INTEGER,
            fours INTEGER,
            sixes INTEGER,
            strike_rate REAL,
            is_out INTEGER,
            how_out TEXT,
            FOREIGN KEY (player_id) REFERENCES players (player_id)
        )''')
        
        # Bowling performances
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bowling_performances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id TEXT,
            player_id INTEGER,
            player_name TEXT,
            overs TEXT,
            balls INTEGER,
            runs_conceded INTEGER,
            wickets INTEGER,
            maidens INTEGER,
            dot_balls INTEGER,
            wides INTEGER,
            no_balls INTEGER,
            economy REAL,
            FOREIGN KEY (player_id) REFERENCES players (player_id)
        )''')
        
        # Match summary
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,
            team_name TEXT,
            total_runs INTEGER,
            total_overs TEXT,
            total_wickets INTEGER,
            run_rate REAL,
            match_date TEXT
        )''')
        
        self.conn.commit()
    
    def load_json_data(self, json_path: str):
        """Load your specific JSON format into database"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for match_data in data:
                self.process_match_data(match_data)
        else:
            self.process_match_data(data)
        
        logger.info(f"Data loaded successfully from {json_path}")
    
    def process_match_data(self, match_data: Dict):
        """Process a single match data object"""
        cursor = self.conn.cursor()
        
        # Process batting data
        if 'latestBatting' in match_data:
            batting = match_data['latestBatting']
            for key, batsman in batting.items():
                if isinstance(batsman, dict) and 'playerID' in batsman:
                    # Insert player
                    cursor.execute('''
                    INSERT OR IGNORE INTO players (player_id, first_name, last_name, full_name, batting_style)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        batsman['playerID'],
                        batsman.get('firstName', ''),
                        batsman.get('lastName', ''),
                        f"{batsman.get('firstName', '')} {batsman.get('lastName', '')}",
                        batsman.get('battingStyle', '')
                    ))
                    
                    # Calculate strike rate
                    strike_rate = 0
                    if batsman.get('ballsFaced', 0) > 0:
                        strike_rate = (batsman.get('runsScored', 0) / batsman.get('ballsFaced', 0)) * 100
                    
                    # Insert batting performance
                    cursor.execute('''
                    INSERT INTO batting_performances 
                    (player_id, player_name, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, how_out)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        batsman['playerID'],
                        f"{batsman.get('firstName', '')} {batsman.get('lastName', '')}",
                        batsman.get('runsScored', 0),
                        batsman.get('ballsFaced', 0),
                        batsman.get('fours', 0),
                        batsman.get('sixers', 0),
                        strike_rate,
                        1 if batsman.get('isOut') == '1' else 0,
                        batsman.get('howOut', '')
                    ))
        
        # Process bowling data
        if 'latestBowling' in match_data:
            bowling = match_data['latestBowling']
            for key, bowler in bowling.items():
                if isinstance(bowler, dict) and 'playerID' in bowler:
                    # Insert player
                    cursor.execute('''
                    INSERT OR IGNORE INTO players (player_id, first_name, last_name, full_name, bowling_style)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        bowler['playerID'],
                        bowler.get('firstName', ''),
                        bowler.get('lastName', ''),
                        f"{bowler.get('firstName', '')} {bowler.get('lastName', '')}",
                        bowler.get('bowlingStyle', '')
                    ))
                    
                    # Calculate economy
                    economy = 0
                    if bowler.get('balls', 0) > 0:
                        economy = (bowler.get('runs', 0) * 6) / bowler.get('balls', 0)
                    
                    # Insert bowling performance
                    cursor.execute('''
                    INSERT INTO bowling_performances
                    (match_id, player_id, player_name, overs, balls, runs_conceded, wickets, 
                     maidens, dot_balls, wides, no_balls, economy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        str(bowler.get('matchID', '')),
                        bowler['playerID'],
                        f"{bowler.get('firstName', '')} {bowler.get('lastName', '')}",
                        bowler.get('overs', '0'),
                        bowler.get('balls', 0),
                        bowler.get('runs', 0),
                        bowler.get('wickets', 0),
                        bowler.get('maidens', 0),
                        bowler.get('dotBalls', 0),
                        bowler.get('wides', 0),
                        bowler.get('noBalls', 0),
                        economy
                    ))
        
        # Process match/innings data
        if 'innings1Balls' in match_data:
            innings = match_data['innings1Balls']
            
            # Extract run rate
            run_rate = 0
            if '/' in innings.get('overs', '0'):
                overs_decimal = self.overs_to_decimal(innings.get('overs', '0.0'))
                if overs_decimal > 0:
                    run_rate = innings.get('runs', 0) / overs_decimal
            
            cursor.execute('''
            INSERT OR IGNORE INTO matches (match_id, team_name, total_runs, total_overs, run_rate)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                match_data.get('_id', {}).get('$oid', 'unknown'),
                innings.get('teamName', ''),
                innings.get('runs', 0),
                innings.get('overs', '0'),
                run_rate
            ))
        
        self.conn.commit()
    
    def overs_to_decimal(self, overs_str: str) -> float:
        """Convert overs like '20.3' to decimal 20.5"""
        if '.' in overs_str:
            overs, balls = overs_str.split('.')
            return float(overs) + (float(balls) / 6)
        return float(overs_str)
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame"""
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logger.error(f"Query error: {e}")
            return pd.DataFrame()