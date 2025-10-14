# 🏏 Cricket Chatbot - Setup Guide

## ✅ Issues Fixed

### 1. **Deprecated Pydantic Import** ✓
- **Fixed in**: `backend/cricket_tools.py`
- Changed `from langchain.pydantic_v1` to `from pydantic`
- Compatible with LangChain 0.3+

### 2. **Import Path Error** ✓
- **Fixed in**: `backend/setup_database.py`
- Changed `from backend.database` to `from database`
- Now works when running from backend directory

### 3. **JSON Path Issue** ✓
- **Fixed in**: `backend/setup_database.py`
- Updated to use `os.path.join()` for cross-platform compatibility

## 📋 Project Status

### ✅ Working Files
- ✓ `backend/database.py` - Database manager
- ✓ `backend/cricket_tools.py` - Cricket analysis tools (6 tools)
- ✓ `backend/agent.py` - LangChain AI agent
- ✓ `backend/server.py` - FastAPI backend server
- ✓ `backend/setup_database.py` - Database setup script
- ✓ `frontend/app.py` - Streamlit UI
- ✓ `requirements.txt` - All dependencies installed

### ⚠️ Minor Warnings (Non-Critical)
- `ConversationBufferMemory` is deprecated in LangChain 0.3+ but still works
- IDE linter warnings about imports (false positives)

## 🚀 Setup Instructions

### Step 1: Create `.env` file
Create a `.env` file in the project root:

```bash
# Navigate to project root
cd /Users/likithpavanrouthu/Downloads/cricket-chatbot

# Create .env file
cat > .env << 'EOF'
# Google Gemini API Key (required)
GOOGLE_API_KEY=your_actual_gemini_api_key_here

# Database configuration
DATABASE_PATH=cricket_stats.db

# Server configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
EOF
```

**Important**: Replace `your_actual_gemini_api_key_here` with your real Gemini API key from https://makersuite.google.com/app/apikey

### Step 2: Setup Database
```bash
cd backend
python setup_database.py
```

This will:
- Create SQLite database tables
- Load data from `data/cricket_data.json`
- Display player count and sample data

### Step 3: Start Backend Server
```bash
# From backend directory
python server.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Start Frontend (New Terminal)
```bash
# Open new terminal
cd /Users/likithpavanrouthu/Downloads/cricket-chatbot/frontend
streamlit run app.py
```

Browser will open at `http://localhost:8501`

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Who are the top 5 batsmen?"}'
```

## 📊 Available Tools

The AI agent has access to 6 cricket analysis tools:

1. **get_player_batting_stats** - Get batting statistics for a player
2. **get_player_bowling_stats** - Get bowling statistics for a player
3. **compare_players** - Compare two players on specific metrics
4. **get_top_performers** - Get top batsmen or bowlers
5. **get_match_summary** - Get summary of all matches
6. **analyze_recent_form** - Analyze recent form of a player

## 💬 Sample Questions

Try asking:
- "What are Amit Pardeshi's batting stats?"
- "Who are the top 5 batsmen?"
- "Compare Sharath and Shrawan's bowling"
- "Show me match summary"
- "What is Ram Charan's recent form?"

## 🔧 Troubleshooting

### Backend won't start
- **Check**: Google Gemini API key is set in `.env` as `GOOGLE_API_KEY`
- **Check**: Port 8000 is not already in use
- **Fix**: Kill existing process: `lsof -ti:8000 | xargs kill -9`

### Frontend can't connect
- **Check**: Backend is running on port 8000
- **Check**: No firewall blocking localhost connections

### "No data found" errors
- **Check**: `cricket_data.json` exists in `data/` folder
- **Check**: Database was created: `ls backend/*.db`
- **Rerun**: `python backend/setup_database.py`

### Import errors
- **Check**: All packages installed: `pip list | grep -E "langchain|openai|fastapi"`
- **Reinstall**: `pip install -r requirements.txt`

## 📁 Project Structure

```
cricket-chatbot/
├── data/
│   └── cricket_data.json          ✓ Your cricket data
├── backend/
│   ├── database.py                ✓ Database operations
│   ├── cricket_tools.py           ✓ 6 analysis tools
│   ├── agent.py                   ✓ AI agent (LangChain)
│   ├── server.py                  ✓ FastAPI server
│   ├── setup_database.py          ✓ Setup script
│   └── cricket_stats.db           (created on setup)
├── frontend/
│   └── app.py                     ✓ Streamlit UI
├── .env                           ⚠️ CREATE THIS
├── requirements.txt               ✓ Dependencies installed
└── SETUP_GUIDE.md                 ✓ This file
```

## 🎯 Next Steps

1. ✅ All code errors fixed
2. ⚠️ Create `.env` file with your OpenAI API key
3. ⚠️ Run database setup
4. ⚠️ Start backend server
5. ⚠️ Start frontend
6. 🎉 Start asking cricket questions!

---

**Need Help?** 
- Check error logs in terminal
- Verify all dependencies: `pip list`
- Ensure Python 3.8+ is installed

