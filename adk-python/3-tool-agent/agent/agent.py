from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


def to_uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b



root_agent = Agent(
    model=LiteLlm(model="ollama_chat/nemotron-3-super:cloud"),
    name="tool_agent",
    description="A simple assistant with basic tools.",
    instruction="You are a helpful and concise assistant. Use the tools when helpful.",
    tools=[to_uppercase, add_numbers],
)
