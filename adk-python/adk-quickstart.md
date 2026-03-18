# ADK Python Quickstart

This guide provides a simple introduction to creating and running a first Python agent with the Agent Development Kit (ADK).

The quickstart workflow is:

1. Create a new project directory
2. Create and activate a Python virtual environment
3. Install ADK
4. Generate an agent with `adk create`
5. Launch the local web interface with `adk web`

An optional section at the end shows how to switch from Google AI to a local Ollama model.

## 1. Prerequisites

Before you begin, make sure the following are available:

- `python3`
- `pip`
- A terminal environment

You can verify Python with:

```bash
python3 --version
```

## 2. Create a Project Directory

Create a new working directory and move into it:

```bash
mkdir adk-quickstart
cd adk-quickstart
```

All commands below should be run from this directory unless noted otherwise.

## 3. Create a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Once activated, your shell prompt will typically show `(.venv)`.

## 4. Install ADK

Install the ADK package:

```bash
python -m pip install google-adk
```

To confirm that the installation completed successfully:

```bash
adk --help
```

If the CLI is available, you should see commands such as `create`, `run`, and `web`.

## 5. Create Your First Agent

Run the following command:

```bash
adk create hello_agent
```

Avoid overly generic directory names. A descriptive, lowercase `snake_case` name such as `hello_agent` is easier to understand and scales better as additional agents are added to the same workspace.

This command creates a new agent directory in the current project, for example:

```text
adk-quickstart/
└── hello_agent/
    ├── __init__.py
    ├── agent.py
    └── .env
```

### Understand the setup choices

During agent creation, ADK asks you to make two decisions:

1. Which model should be used for the root agent
2. Which backend should be used to access that model

You will see an interactive prompt similar to the following:

```text
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1

1. Google AI
2. Vertex AI
Choose a backend (1, 2): 1

Don't have API Key? Create one in AI Studio: https://aistudio.google.com/apikey

Enter Google API key:
```

#### Model options

`1. gemini-2.5-flash`

This is the most straightforward option for a first project. It is suitable when the goal is to validate the end-to-end ADK workflow with minimal setup.

Typical reasons to choose this option:

- You want the quickest path to a working agent
- You are evaluating ADK for the first time
- You want to reduce the number of manual configuration steps

`2. Other models (fill later)`

This option creates the project structure without committing to a specific default model during initialization. It is useful when you already know that you will replace the generated model configuration after project creation.

Typical reasons to choose this option:

- You plan to use a local model such as Ollama
- You intend to connect to another provider later
- You prefer to edit `agent.py` manually after scaffolding is created

For an initial quickstart, this option is generally less convenient because it shifts more configuration work to the post-creation step.

#### Backend options

`1. Google AI`

This is the recommended backend for a first local project. It typically requires only a Google AI API key and is the easiest way to get started quickly.

Typical reasons to choose this option:

- You want the simplest local development experience
- You are following a quickstart or tutorial
- You do not need Google Cloud project-level configuration yet

`2. Vertex AI`

This option is intended for Google Cloud-based environments and is better suited to users who already work within GCP and need project, region, and enterprise-oriented controls.

Typical reasons to choose this option:

- You are deploying within a Google Cloud environment
- You need Vertex AI-specific infrastructure and governance
- Your team already standardizes on GCP services

For a first project, Vertex AI usually introduces unnecessary setup complexity.

### Recommended selection for a first project

For a first ADK agent, the recommended path is:

- Select `1` for the model: `gemini-2.5-flash`
- Select `1` for the backend: `Google AI`
- Enter a valid Google AI API key

This combination is recommended because it provides the shortest and most reliable path to a working local setup. It minimizes configuration overhead and makes troubleshooting easier if an issue occurs during the initial run.

Choose a different path only if you already know that your project requires it. For example:

- Choose `Other models (fill later)` if you plan to replace the default model with Ollama or another provider immediately after creation
- Choose `Vertex AI` if you are intentionally building against Google Cloud infrastructure from the beginning

If you do not already have a Google AI API key, you can create one at:

https://aistudio.google.com/apikey

## 6. Review the Generated Files

After creation, the most important files are:

- `hello_agent/agent.py`
- `hello_agent/.env`

### `hello_agent/agent.py`

This file defines the root agent for your application.

### `hello_agent/.env`

If you selected `Google AI`, the file will typically contain values similar to:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_api_key
```

## 7. Run the ADK Web Interface

Run `adk web` from the parent directory that contains your agent folder. In this example, that means the `adk-quickstart` directory, not the `hello_agent/` directory itself.

Start the local web UI with:

```bash
adk web
```

You can also make the target explicit:

```bash
adk web .
```

Here, `.` means the current directory, and ADK will scan its subdirectories for agents.

If the setup is correct, ADK will detect the `hello_agent/` agent and start the local web application.

## 8. Test the Agent

After starting `adk web`:

1. Open the ADK web UI in your browser
2. Select the `hello_agent` agent
3. Send a simple message such as:

```text
Hello
```

or:

```text
What can you do?
```

If the agent responds successfully, your first ADK agent is running correctly.

## 9. Common Issues

### Running `adk web` from the wrong directory

This is a common mistake.

Less reliable:

```bash
cd hello_agent
adk web
```

Recommended:

```bash
cd adk-quickstart
adk web
```

ADK expects to scan a directory that contains one or more agent subdirectories.

### `adk` command not found

This usually means the virtual environment is not active. Activate it again:

```bash
source .venv/bin/activate
```

If needed, confirm that ADK is installed:

```bash
python -m pip show google-adk
```

### Invalid or missing API key

If you selected `Google AI`, a valid `GOOGLE_API_KEY` is required.

You can inspect the environment file with:

```bash
cat hello_agent/.env
```

## 10. Minimal End-to-End Example

If you want the shortest possible setup flow, the following is sufficient:

```bash
mkdir adk-quickstart
cd adk-quickstart

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install google-adk

adk create hello_agent
adk web
```

## 11. Optional: Use a Local Ollama Model

If you prefer to run a local model instead of Google AI, you can update the generated agent to use Ollama through `LiteLlm`. This is optional and is not required for the initial quickstart.

### Install the additional dependency

```bash
python -m pip install litellm
```

### Update `hello_agent/agent.py`

Replace the model configuration with a `LiteLlm` example such as:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm


root_agent = Agent(
    model=LiteLlm(model="ollama_chat/qwen2.5:7b"),
    name="hello_agent",
    description="Example ADK agent",
    instruction="You are a helpful assistant.",
)
```

Important notes:

- `LiteLlm` must be imported explicitly
- The model name after `ollama_chat/` must match a model installed on your local machine

You can verify available local models with:

```bash
ollama list
```

### Configure the Ollama endpoint

```bash
export OLLAMA_API_BASE="http://localhost:11434"
```

Then restart the web UI:

```bash
adk web
```

## 12. Suggested Next Steps

After your first agent is running, a few natural next steps are:

- Add tools to the agent
- Refine the instruction prompt
- Explore multi-agent workflows
- Connect to alternative model providers
- Use `adk run` for command-line testing

## References

- ADK Python Quickstart: https://google.github.io/adk-docs/get-started/python/
- ADK Models: https://google.github.io/adk-docs/agents/models/
- ADK CLI help: `adk --help`
