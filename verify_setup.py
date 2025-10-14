#!/usr/bin/env python3
"""
Quick verification script for cricket chatbot setup
"""
import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_name} - {e}")
        return False

def main():
    print("🏏 Cricket Chatbot - Setup Verification\n")
    print("=" * 50)
    
    # Check files
    print("\n📁 Checking Files:")
    files_ok = all([
        check_file("data/cricket_data.json", "Cricket data"),
        check_file("backend/database.py", "Database module"),
        check_file("backend/cricket_tools.py", "Cricket tools"),
        check_file("backend/agent.py", "AI agent"),
        check_file("backend/server.py", "FastAPI server"),
        check_file("frontend/app.py", "Streamlit frontend"),
        check_file("requirements.txt", "Requirements file"),
    ])
    
    # Check .env
    print("\n🔑 Checking Configuration:")
    env_exists = check_file(".env", "Environment file")
    if env_exists:
        with open(".env", "r") as f:
            content = f.read()
            has_key = "GOOGLE_API_KEY" in content and "your_" not in content
            if has_key:
                print("   ✅ Google Gemini API key appears to be set")
            else:
                print("   ⚠️  Google Gemini API key not configured properly")
                env_exists = False
    else:
        print("   ⚠️  Create .env file with your Google Gemini API key")
    
    # Check packages
    print("\n📦 Checking Python Packages:")
    packages_ok = all([
        check_import("langchain", "LangChain"),
        check_import("langchain_google_genai", "LangChain Google Genai"),
        check_import("google.generativeai", "Google Generative AI"),
        check_import("fastapi", "FastAPI"),
        check_import("uvicorn", "Uvicorn"),
        check_import("streamlit", "Streamlit"),
        check_import("pandas", "Pandas"),
    ])
    
    # Check backend imports
    print("\n🔧 Checking Backend Modules:")
    sys.path.insert(0, "backend")
    backend_ok = all([
        check_import("database", "Database module"),
        check_import("cricket_tools", "Cricket tools"),
        check_import("agent", "AI agent"),
        check_import("server", "FastAPI server"),
    ])
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:\n")
    
    if files_ok and packages_ok and backend_ok:
        print("✅ All core components are ready!")
        if env_exists:
            print("✅ Configuration complete!")
            print("\n🚀 Ready to start:")
            print("   1. cd backend && python setup_database.py")
            print("   2. cd backend && python server.py")
            print("   3. (new terminal) cd frontend && streamlit run app.py")
        else:
            print("⚠️  Next step: Create .env file with Google Gemini API key")
            print("   Get your key from: https://makersuite.google.com/app/apikey")
            print("   See SETUP_GUIDE.md for instructions")
    else:
        print("❌ Some issues found. Please fix them before proceeding.")
        if not packages_ok:
            print("   Run: pip install -r requirements.txt")
        if not files_ok:
            print("   Check that all project files are present")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()

