# Structured Outputs Demo

This example shows how to use a Google ADK agent with a Pydantic schema to extract a structured meeting summary from free-form meeting notes.

The agent code is in [agent/agent.py](/Users/ktsoator/projects/openagent/adk-python/4-structured-outputs/agent/agent.py).

## What This Agent Returns

The agent produces JSON with this shape:

```json
{
  "summary": "string",
  "decisions": ["string"],
  "action_items": [
    {
      "task": "string",
      "owner": "string",
      "deadline": "string"
    }
  ],
  "risks": ["string"]
}
```

Notes:

- If `owner` is missing, it defaults to `"unknown"`.
- If `deadline` is missing, it defaults to `"unknown"`.
- `due_date` is also accepted and mapped to `deadline`.
- If `decisions`, `action_items`, or `risks` are missing, they default to empty arrays.
- The agent should always return JSON. Even for non-meeting input, it should return a valid fallback object instead of plain text.

## Run

Run in CLI mode:

```bash
adk run agent
```

Or start the Web UI:

```bash
adk web
```

Then select the `agent` app in the UI.

## Test Input

Paste this into the CLI or Web UI:

```text
Please extract a structured meeting summary from these notes:

The product, engineering, and operations teams met to discuss the new login flow.
They decided to start a gradual rollout of the new login page next Monday for 10% of users.
Alice will confirm analytics tracking with the frontend team by March 22.
Bob will prepare the customer support FAQ by March 24.
One risk mentioned in the meeting was that the SMS verification service has occasional timeouts, which may affect login success rates.
```

## Example Output

```json
{
  "summary": "The product, engineering, and operations teams met to discuss the new login flow and agreed on a gradual rollout starting next Monday for 10% of users, with specific action items assigned to Alice and Bob, and a noted risk regarding SMS verification service timeouts.",
  "decisions": [
    "Start a gradual rollout of the new login page next Monday for 10% of users"
  ],
  "action_items": [
    {
      "task": "Confirm analytics tracking with the frontend team",
      "owner": "Alice",
      "deadline": "March 22"
    },
    {
      "task": "Prepare the customer support FAQ",
      "owner": "Bob",
      "deadline": "March 24"
    }
  ],
  "risks": [
    "The SMS verification service has occasional timeouts, which may affect login success rates"
  ]
}
```
