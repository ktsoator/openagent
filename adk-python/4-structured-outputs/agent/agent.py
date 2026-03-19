from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(description="The action that needs to be completed.")
    owner: str = Field(
        default="unknown",
        description="The person responsible for the action item, or 'unknown' if not mentioned."
    )
    deadline: str = Field(
        default="unknown",
        description="The deadline for the action item, or 'unknown' if not mentioned."
    )


class MeetingSummaryOutput(BaseModel):
    summary: str = Field(description="A concise summary of the meeting.")
    decisions: list[str] = Field(
        default_factory=list,
        description="Key decisions made during the meeting."
    )
    action_items: list[ActionItem] = Field(
        default_factory=list,
        description="Action items extracted from the meeting notes."
    )
    risks: list[str] = Field(
        default_factory=list,
        description="Potential risks or blockers mentioned in the meeting."
    )


PROMPT = (Path(__file__).with_name("prompt.md")).read_text(encoding="utf-8")


root_agent = Agent(
    model=LiteLlm(model="ollama_chat/nemotron-3-super:cloud"),
    name="meeting_summary_agent",
    description="Extracts structured meeting summaries from free-form notes.",
    instruction=PROMPT,
    output_schema=MeetingSummaryOutput,
    output_key="meeting_summary",
    tools=[],
)
