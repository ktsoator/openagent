from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


root_agent = Agent(
    model=LiteLlm(model="ollama_chat/nemotron-3-super:cloud"),
    name="litellm_agent",
    description="Simple assistant",
    instruction="Be helpful and concise.",
)
