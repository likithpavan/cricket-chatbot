"""
# Cricket Stats AI Chatbot 🏏

An AI-powered chatbot for analyzing cricket statistics using your custom JSON data.

## Features
- Natural language cricket queries
- Player batting & bowling statistics
- Player comparisons
- Top performers rankings
- Recent form analysis
- Match summaries

## Setup Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Add Google Gemini API Key
1. Get API key from [makersuite.google.com](https://makersuite.google.com/app/apikey)
2. Add to `.env` file:
```
GOOGLE_API_KEY=your-key-here
```

### 3. Setup Database
1. Place your JSON file in `data/cricket_data.json`
2. Run setup:
```bash
cd backend
python setup_database.py
```

### 4. Start Backend Server
```bash
cd backend
python server.py
```

### 5. Start Frontend
Open new terminal:
```bash
cd frontend
streamlit run app.py
```

## Sample Questions
- "What are Amit Pardeshi's batting stats?"
- "Compare Sharath and Shrawan's bowling"
- "Who are the top 5 batsmen?"
- "Show me Ram Charan's recent form"
- "Which player has the most wickets?"

## Project Structure
```
cricket-chatbot/
├── data/               # Your JSON data
├── backend/            # AI agent and tools
│   ├── database.py     # Database manager
│   ├── cricket_tools.py # Cricket analysis tools
│   ├── agent.py        # LangChain agent
│   └── server.py       # FastAPI server
├── frontend/           # User interface
│   └── app.py          # Streamlit app
├── .env                # API keys
└── requirements.txt    # Dependencies
```

## Technologies Used
- LangChain for AI orchestration
- OpenAI GPT for natural language
- SQLite for data storage
- FastAPI for backend API
- Streamlit for frontend UI
"""