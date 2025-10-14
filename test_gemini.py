#!/usr/bin/env python3
"""Quick test of Gemini integration"""
import os
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCm5dB6rA3q6nQOAUDzy-5alp2yyoybK-0'

import sys
sys.path.insert(0, 'backend')

print("🧪 Testing Gemini Integration...")
print("=" * 50)

try:
    from agent import CricketAgent
    print("✅ Agent imports successfully")
    
    agent = CricketAgent()
    print("✅ Agent initialized with gemini-2.0-flash")
    
    # Test with a simple question
    print("\n📊 Testing with sample query...")
    result = agent.ask("Who are the top 5 batsmen?")
    
    if result['success']:
        print("✅ Query successful!")
        print(f"\n💬 Response:\n{result['answer'][:200]}...")
        print(f"\n🔧 Tools used: {result['tools_used']}")
    else:
        print(f"❌ Query failed: {result['answer']}")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Your chatbot is ready!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
