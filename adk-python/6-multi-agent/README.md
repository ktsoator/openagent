# Simple Multi-Agent Example

This example shows a small Google ADK multi-agent setup with one coordinator
agent and two specialists:

- `coordinator_agent`: receives the user request and routes it.
- `math_agent`: handles arithmetic and numeric reasoning.
- `writing_agent`: handles rewriting, polishing, summarization, and translation.

Because `root_agent` is configured with `sub_agents`, ADK will automatically
inject the built-in `transfer_to_agent` tool.

## What This Example Demonstrates

- How to define multiple ADK agents in native `Agent(...)` style
- How to route tasks from a coordinator to specialist agents
- How to attach simple Python tools to an agent
- How to keep model creation thin by using a small `create_model(...)` helper
- How to swap between OpenAI-compatible and Anthropic-compatible backends

## File Layout

- `agent/agent.py`: native ADK agent definitions and tool functions
- `agent/model_factory.py`: thin `create_model(model_name)` helper
- `agent/.env`: local environment variables for keys and base URLs
- `agent/.env.example`: placeholder environment template

## Agent Architecture

### `coordinator_agent`

The coordinator is the root agent. Its job is to:

- answer simple general questions directly
- transfer arithmetic and numeric reasoning tasks to `math_agent`
- transfer rewriting and language tasks to `writing_agent`

### `math_agent`

The math specialist has two tools:

- `multiply_numbers(a, b)`
- `add_numbers(a, b)`

Its instruction is intentionally strict:

- it must use tools for arithmetic
- it should not do mental math
- it should continue tool calls step by step until the full result is complete

### `writing_agent`

The writing specialist focuses on:

- rewriting
- polishing
- summarization
- translation
- tone adjustment

## Model Configuration

This project uses `LiteLlm` through a small helper:

```python
from .model_factory import create_model
```

You can create a model explicitly:

```python
model=create_model("openai/your-model-name")
```

or:

```python
model=create_model("anthropic/your-model-name")
```

### Current Example Behavior

In the current demo, the agents in `agent/agent.py` pass explicit model names
directly into `create_model(...)`.

That means:

- the provider is chosen in code
- the API key and base URL are still read from `.env`
- `MODEL_NAME` is only needed if you call `create_model()` without arguments

## Environment Variables

Use `KEY=value` format in `agent/.env`.

You can start by copying `agent/.env.example` to `agent/.env` and then
replacing the placeholder values.

### OpenAI-Compatible Example

```env
MODEL_NAME=openai/your-model-name
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://your-openai-compatible-base/v1
```

### Anthropic-Compatible Example

```env
MODEL_NAME=anthropic/your-model-name
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_API_BASE=https://your-anthropic-compatible-base
```

## How To Switch Models

### Option 1: Switch Models In Code

Edit the model strings in `agent/agent.py`.

Example:

```python
math_agent = Agent(
    model=create_model("openai/your-model-name"),
    ...
)
```

or:

```python
math_agent = Agent(
    model=create_model("anthropic/your-model-name"),
    ...
)
```

### Option 2: Use `.env` As The Default Source

If you want to choose the model only from environment variables, change your
code to call:

```python
model=create_model()
```

Then `create_model(...)` will fall back to `MODEL_NAME` from `.env`.

## Running The Example

From this example directory, start the ADK web app with your usual ADK command,
for example:

```bash
adk web
```

If you change `.env` or switch model settings, restart the ADK process so the
updated environment is reloaded.

## Example Usage

### Math Requests

- `Please calculate 37 * 18 + 9.`
- `What is 125 * 8 + 44?`

### Writing Requests

- `Rewrite this to sound more professional: Our product is very easy to use.`
- `Summarize this paragraph in one sentence.`
- `Translate this sentence into Chinese: We will ship the update tomorrow.`

### General Requests

- `What can you help me with?`
- `Route this task to the right specialist.`

## Notes

- This README intentionally uses placeholder URLs, keys, and model names.
- `create_model(...)` currently supports `openai/...` and `anthropic/...`.
- If you want different models for different agents, pass different model names
  to each `create_model(...)` call.
- If you want one shared model for all agents, use `create_model()` and control
  it through `.env`.
