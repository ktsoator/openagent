from google.adk.agents.llm_agent import Agent

from .model_factory import create_model


def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers. Use this for addition steps."""
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    """Return the product of two integers. Use this for multiplication steps."""
    return a * b


math_agent = Agent(
    model=create_model("anthropic/claude-opus-4-6"),
    name="math_agent",
    description="Specialist for arithmetic, calculations, and number reasoning.",
    instruction="""
    You are a math specialist.

    Available tools:
    - `multiply_numbers(a, b)`: use for multiplication.
    - `add_numbers(a, b)`: use for addition.

    Rules:
    - For any arithmetic task, you must use tools for every calculation step.
    - Never do arithmetic mentally.
    - If the expression has multiple steps, call tools step by step until the
      full result is computed.
    - After receiving one tool result, check whether another arithmetic step is
      still needed. If yes, call the next tool instead of answering.
    - Do not answer the user until all required calculation steps are finished.
    - Keep the final answer concise and include the final numeric result.

    If the user mainly wants rewriting, polishing, summarization, tone editing,
    or translation, transfer control back to the parent agent.
    """,
    tools=[add_numbers, multiply_numbers],
    disallow_transfer_to_peers=True,
)


writing_agent = Agent(
    model=create_model("anthropic/claude-opus-4-6"),
    name="writing_agent",
    description="Specialist for rewriting, polishing, summarizing, and translation.",
    instruction="""
    You are a writing specialist.

    Responsibilities:
    - Rewrite, polish, summarize, and translate text.
    - Match the user's requested language and tone.
    - Prefer clear, natural, concise wording.

    If the task is mainly about calculations or numeric reasoning, transfer
    control back to the parent agent.
    """,
    disallow_transfer_to_peers=True,
)


root_agent = Agent(
    model=create_model("anthropic/claude-opus-4-6"),
    name="coordinator_agent",
    description="Routes requests to the best specialist and handles simple general questions.",
    instruction="""
    You are the coordinator of a simple multi-agent assistant.

    Routing rules:
    - Transfer arithmetic, calculation, and number reasoning tasks to `math_agent`.
    - Transfer rewriting, polishing, summarizing, translation, and tone editing
      tasks to `writing_agent`.
    - If the request is simple and clearly within your scope, answer directly.

    Be helpful and concise.
    """,
    sub_agents=[math_agent, writing_agent],
)
