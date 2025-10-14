# 🔑 Update Your .env File for Gemini

## Current Issue

Your `.env` file has the Gemini API key but with the wrong variable name:

```bash
# WRONG - Old OpenAI variable name
OPENAI_API_KEY=AIzaSyCm5dB6rA3q6nQOAUDzy-5alp2yyoybK-0
```

## Quick Fix

Run this command to update your `.env` file:

```bash
cd /Users/likithpavanrouthu/Downloads/cricket-chatbot

# Create new .env with Gemini key
cat > .env << 'EOF'
# Google Gemini API Key (required)
GOOGLE_API_KEY=AIzaSyCm5dB6rA3q6nQOAUDzy-5alp2yyoybK-0

# Database configuration
DATABASE_PATH=cricket_stats.db

# Server configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Other settings
DEBUG=True
LOG_LEVEL=INFO
EOF

echo "✅ .env file updated for Gemini!"
```

## Or Edit Manually

Open `.env` in any text editor and change:

**FROM**:
```
OPENAI_API_KEY=AIzaSyCm5dB6rA3q6nQOAUDzy-5alp2yyoybK-0
```

**TO**:
```
GOOGLE_API_KEY=AIzaSyCm5dB6rA3q6nQOAUDzy-5alp2yyoybK-0
```

That's it! Just change `OPENAI_API_KEY` to `GOOGLE_API_KEY`.

## Verify It Worked

After updating, run:

```bash
python verify_setup.py
```

You should see:
```
✅ Google Gemini API key appears to be set
✅ All core components are ready!
```

## Then Start Your Chatbot

```bash
# 1. Setup database
cd backend
python setup_database.py

# 2. Start backend
python server.py

# 3. Start frontend (new terminal)
cd frontend
streamlit run app.py
```

---

**That's all you need to do!** Just rename the variable from `OPENAI_API_KEY` to `GOOGLE_API_KEY` in your `.env` file.

