from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


question_answering_agent = Agent(
    model=LiteLlm(model="ollama_chat/nemotron-3-super:cloud"),
    name="question_answering_agent",
    description="Travel preference question answering agent",
    instruction="""
    You are a helpful travel assistant that answers questions about the user's travel preferences.

    Here is some information about the user:
    Name: 
    {user_name}
    Travel Preferences: 
    {user_preferences}
    """,
)
