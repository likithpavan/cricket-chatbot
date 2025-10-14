import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics AI",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimal design
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Title styling */
    h1 {
        color: white;
        text-align: center;
        font-weight: 300;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>⚡ CRICKET ANALYTICS AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Powered by Advanced AI • Real-time Stats</p>", unsafe_allow_html=True)

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your Cricket Analytics Assistant. Ask me anything about player statistics, match data, or performance analysis."
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🏏" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about cricket statistics..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant", avatar="🏏"):
        with st.spinner("Analyzing cricket data..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"question": prompt},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.write(data["answer"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"]
                    })
                else:
                    st.error("Failed to get response. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Please ensure server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Minimal footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: white; font-size: 12px;'>Type your question and press Enter</p>", unsafe_allow_html=True)