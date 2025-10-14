#!/bin/bash
# Quick setup script for Gemini API

echo "🏏 Cricket Chatbot - Gemini API Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    echo ""
    # Check if it has GOOGLE_API_KEY
    if grep -q "GOOGLE_API_KEY" .env; then
        echo "✅ .env already has GOOGLE_API_KEY"
        echo ""
        # Check if it's a placeholder
        if grep -q "your_" .env; then
            echo "⚠️  But it's still a placeholder. Please update it."
            echo ""
            echo "📝 Get your Gemini API key from:"
            echo "   https://makersuite.google.com/app/apikey"
            echo ""
            read -p "Enter your Gemini API key: " API_KEY
            sed -i.bak "s/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=$API_KEY/" .env
            echo "✅ Updated .env with your Gemini API key"
        else
            echo "✅ .env is properly configured!"
        fi
    else
        # Has old OPENAI_API_KEY, convert to GOOGLE_API_KEY
        echo "🔄 Converting from OpenAI to Gemini..."
        echo ""
        echo "📝 Get your Gemini API key from:"
        echo "   https://makersuite.google.com/app/apikey"
        echo ""
        read -p "Enter your Gemini API key: " API_KEY
        
        # Backup old .env
        cp .env .env.openai.backup
        
        # Create new .env with Gemini
        cat > .env << EOF
# Google Gemini API Key (required)
GOOGLE_API_KEY=$API_KEY

# Database configuration
DATABASE_PATH=cricket_stats.db

# Server configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Other settings
DEBUG=True
LOG_LEVEL=INFO
EOF
        echo "✅ Created new .env with Gemini API key"
        echo "✅ Old .env backed up as .env.openai.backup"
    fi
else
    # No .env exists, create new one
    echo "📝 Creating new .env file..."
    echo ""
    echo "Get your Gemini API key from:"
    echo "https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Enter your Gemini API key: " API_KEY
    
    cat > .env << EOF
# Google Gemini API Key (required)
GOOGLE_API_KEY=$API_KEY

# Database configuration
DATABASE_PATH=cricket_stats.db

# Server configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Other settings
DEBUG=True
LOG_LEVEL=INFO
EOF
    echo "✅ Created .env with your Gemini API key"
fi

echo ""
echo "======================================"
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd backend && python setup_database.py"
echo "  2. cd backend && python server.py"
echo "  3. (new terminal) cd frontend && streamlit run app.py"
echo ""

