"""
Tools for the cricket chatbot
Customized for your data structure
"""
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional, List
import pandas as pd
from database import CricketDatabase
import json

# Initialize database
db = CricketDatabase()

class PlayerStatsInput(BaseModel):
    player_name: str = Field(description="Name of the cricket player")

class ComparePlayersInput(BaseModel):
    player1: str = Field(description="First player name")
    player2: str = Field(description="Second player name")
    metric: str = Field(description="Metric to compare: runs, wickets, average, economy")

def get_player_batting_stats(player_name: str) -> str:
    """Get batting statistics for a player"""
    query = f"""
    SELECT 
        player_name,
        COUNT(*) as innings,
        SUM(runs_scored) as total_runs,
        AVG(runs_scored) as average_runs,
        MAX(runs_scored) as highest_score,
        AVG(strike_rate) as avg_strike_rate,
        SUM(fours) as total_fours,
        SUM(sixes) as total_sixes,
        SUM(balls_faced) as total_balls
    FROM batting_performances
    WHERE LOWER(player_name) LIKE LOWER('%{player_name}%')
    GROUP BY player_name
    """
    
    result = db.execute_query(query)
    
    if result.empty:
        return f"No batting data found for {player_name}"
    
    stats = result.iloc[0]
    return f"""
    Batting Statistics for {stats['player_name']}:
    - Innings: {int(stats['innings'])}
    - Total Runs: {int(stats['total_runs'])}
    - Average: {stats['average_runs']:.2f}
    - Highest Score: {int(stats['highest_score'])}
    - Strike Rate: {stats['avg_strike_rate']:.2f}
    - Total Fours: {int(stats['total_fours'])}
    - Total Sixes: {int(stats['total_sixes'])}
    - Balls Faced: {int(stats['total_balls'])}
    """

def get_player_bowling_stats(player_name: str) -> str:
    """Get bowling statistics for a player"""
    query = f"""
    SELECT 
        player_name,
        COUNT(*) as matches,
        SUM(wickets) as total_wickets,
        SUM(runs_conceded) as total_runs,
        AVG(economy) as avg_economy,
        SUM(maidens) as total_maidens,
        SUM(dot_balls) as total_dots,
        SUM(balls) as total_balls
    FROM bowling_performances
    WHERE LOWER(player_name) LIKE LOWER('%{player_name}%')
    GROUP BY player_name
    """
    
    result = db.execute_query(query)
    
    if result.empty:
        return f"No bowling data found for {player_name}"
    
    stats = result.iloc[0]
    
    # Calculate bowling average
    bowling_avg = 0
    if stats['total_wickets'] > 0:
        bowling_avg = stats['total_runs'] / stats['total_wickets']
    
    return f"""
    Bowling Statistics for {stats['player_name']}:
    - Matches: {int(stats['matches'])}
    - Wickets: {int(stats['total_wickets'])}
    - Runs Conceded: {int(stats['total_runs'])}
    - Bowling Average: {bowling_avg:.2f}
    - Economy Rate: {stats['avg_economy']:.2f}
    - Maidens: {int(stats['total_maidens'])}
    - Dot Balls: {int(stats['total_dots'])}
    - Total Balls: {int(stats['total_balls'])}
    """

def compare_players(player1: str, player2: str, metric: str) -> str:
    """Compare two players on a specific metric"""
    
    if metric.lower() in ['runs', 'batting', 'average']:
        query = f"""
        SELECT 
            player_name,
            SUM(runs_scored) as total_runs,
            AVG(runs_scored) as average,
            AVG(strike_rate) as strike_rate
        FROM batting_performances
        WHERE LOWER(player_name) LIKE LOWER('%{player1}%')
           OR LOWER(player_name) LIKE LOWER('%{player2}%')
        GROUP BY player_name
        """
    elif metric.lower() in ['wickets', 'bowling', 'economy']:
        query = f"""
        SELECT 
            player_name,
            SUM(wickets) as total_wickets,
            AVG(economy) as economy,
            SUM(runs_conceded) as runs_conceded
        FROM bowling_performances
        WHERE LOWER(player_name) LIKE LOWER('%{player1}%')
           OR LOWER(player_name) LIKE LOWER('%{player2}%')
        GROUP BY player_name
        """
    else:
        return f"Invalid metric. Choose from: runs, wickets, average, economy"
    
    result = db.execute_query(query)
    
    if len(result) < 2:
        return f"Could not find data for both {player1} and {player2}"
    
    comparison = f"Comparison of {player1} vs {player2}:\n\n"
    for _, row in result.iterrows():
        if metric.lower() in ['runs', 'batting', 'average']:
            comparison += f"{row['player_name']}:\n"
            comparison += f"  - Total Runs: {int(row['total_runs'])}\n"
            comparison += f"  - Average: {row['average']:.2f}\n"
            comparison += f"  - Strike Rate: {row['strike_rate']:.2f}\n\n"
        else:
            comparison += f"{row['player_name']}:\n"
            comparison += f"  - Total Wickets: {int(row['total_wickets'])}\n"
            comparison += f"  - Economy: {row['economy']:.2f}\n\n"
    
    return comparison

def get_top_performers(category: str = "batsmen", limit: int = 5) -> str:
    """Get top performers in batting or bowling"""
    
    if category.lower() in ['batsmen', 'batting', 'runs']:
        query = f"""
        SELECT 
            player_name,
            SUM(runs_scored) as total_runs,
            AVG(runs_scored) as average,
            COUNT(*) as innings
        FROM batting_performances
        GROUP BY player_name
        HAVING innings >= 2
        ORDER BY total_runs DESC
        LIMIT {limit}
        """
        title = "Top Batsmen"
    elif category.lower() in ['bowlers', 'bowling', 'wickets']:
        query = f"""
        SELECT 
            player_name,
            SUM(wickets) as total_wickets,
            AVG(economy) as economy,
            COUNT(*) as matches
        FROM bowling_performances
        GROUP BY player_name
        HAVING matches >= 2
        ORDER BY total_wickets DESC
        LIMIT {limit}
        """
        title = "Top Bowlers"
    else:
        return "Invalid category. Choose 'batsmen' or 'bowlers'"
    
    result = db.execute_query(query)
    
    if result.empty:
        return f"No data found for {category}"
    
    response = f"{title} (Top {limit}):\n\n"
    for i, row in result.iterrows():
        if category.lower() in ['batsmen', 'batting', 'runs']:
            response += f"{i+1}. {row['player_name']}: {int(row['total_runs'])} runs (Avg: {row['average']:.2f})\n"
        else:
            response += f"{i+1}. {row['player_name']}: {int(row['total_wickets'])} wickets (Eco: {row['economy']:.2f})\n"
    
    return response

def get_match_summary() -> str:
    """Get summary of matches in database"""
    query = """
    SELECT 
        COUNT(*) as total_matches,
        AVG(total_runs) as avg_runs,
        MAX(total_runs) as highest_score,
        MIN(total_runs) as lowest_score
    FROM matches
    """
    
    result = db.execute_query(query)
    
    if result.empty or result.iloc[0]['total_matches'] == 0:
        return "No match data available"
    
    stats = result.iloc[0]
    return f"""
    Match Summary:
    - Total Matches: {int(stats['total_matches'])}
    - Average Team Score: {stats['avg_runs']:.1f}
    - Highest Team Score: {int(stats['highest_score'])}
    - Lowest Team Score: {int(stats['lowest_score'])}
    """

def analyze_recent_form(player_name: str) -> str:
    """Analyze recent form of a player"""
    query = f"""
    SELECT 
        runs_scored,
        balls_faced,
        strike_rate,
        fours,
        sixes
    FROM batting_performances
    WHERE LOWER(player_name) LIKE LOWER('%{player_name}%')
    ORDER BY id DESC
    LIMIT 5
    """
    
    result = db.execute_query(query)
    
    if result.empty:
        return f"No recent data found for {player_name}"
    
    recent_runs = result['runs_scored'].tolist()
    avg_recent = sum(recent_runs) / len(recent_runs)
    
    form = "🔥 HOT" if avg_recent > 30 else "📈 GOOD" if avg_recent > 15 else "📉 NEEDS IMPROVEMENT"
    
    return f"""
    Recent Form for {player_name} (Last {len(recent_runs)} innings):
    - Recent Scores: {', '.join(map(str, recent_runs))}
    - Average in Recent Games: {avg_recent:.1f}
    - Form: {form}
    """

# Create LangChain tools
player_batting_tool = Tool(
    name="get_player_batting_stats",
    func=get_player_batting_stats,
    description="Get batting statistics for a specific player"
)

player_bowling_tool = Tool(
    name="get_player_bowling_stats",
    func=get_player_bowling_stats,
    description="Get bowling statistics for a specific player"
)

comparison_tool = StructuredTool.from_function(
    func=compare_players,
    name="compare_players",
    description="Compare two players on batting or bowling metrics",
    args_schema=ComparePlayersInput
)

top_performers_tool = Tool(
    name="get_top_performers",
    func=get_top_performers,
    description="Get top batsmen or bowlers"
)

match_summary_tool = Tool(
    name="get_match_summary",
    func=get_match_summary,
    description="Get summary of all matches"
)

form_analysis_tool = Tool(
    name="analyze_recent_form",
    func=analyze_recent_form,
    description="Analyze recent form of a player"
)

# List of all tools
ALL_TOOLS = [
    player_batting_tool,
    player_bowling_tool,
    comparison_tool,
    top_performers_tool,
    match_summary_tool,
    form_analysis_tool
]