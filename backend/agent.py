"""
LangChain Agent for Cricket Chatbot - Using Google Gemini
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from cricket_tools import ALL_TOOLS
import os
from dotenv import load_dotenv

load_dotenv()

class CricketAgent:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Fast and efficient (or use gemini-2.5-flash for better results)
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True  # Fix for system messages
        )
        
        # Create prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert cricket statistics analyst. 
            You have access to detailed cricket data including batting and bowling performances.
            
            Use the available tools to answer questions accurately:
            - get_player_batting_stats: For batting statistics
            - get_player_bowling_stats: For bowling statistics  
            - compare_players: To compare two players
            - get_top_performers: For rankings
            - get_match_summary: For match overviews
            - analyze_recent_form: For form analysis
            
            Always provide specific numbers from the database.
            If you don't have data, clearly state that."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent (using tool calling for Gemini)
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=ALL_TOOLS,
            prompt=self.prompt
        )
        
        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=ALL_TOOLS,
            verbose=True,
            return_intermediate_steps=True
        )
        
        # Memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def ask(self, question: str) -> dict:
        """Process a question and return answer"""
        try:
            response = self.agent_executor.invoke({
                "input": question
            })
            
            # Extract tool usage info
            tools_used = []
            if "intermediate_steps" in response:
                for step in response["intermediate_steps"]:
                    if len(step) >= 2:
                        action = step[0]
                        tools_used.append(action.tool)
            
            return {
                "answer": response["output"],
                "tools_used": tools_used,
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "tools_used": [],
                "success": False
            }
