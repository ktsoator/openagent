from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import AliasChoices, BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(description="The action that needs to be completed.")
    owner: str = Field(
        default="unknown",
        description="The person responsible for the action item, or 'unknown' if not mentioned."
    )
    deadline: str = Field(
        default="unknown",
        validation_alias=AliasChoices("deadline", "due_date"),
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


root_agent = Agent(
    model=LiteLlm(model="ollama_chat/nemotron-3-super:cloud"),
    name="meeting_summary_agent",
    description="Extracts structured meeting summaries from free-form notes.",
    instruction=(
        "You are a meeting notes assistant. "
        "Given raw meeting notes, extract a concise summary, the decisions made, "
        "the action items, and any risks or blockers. "
        "Respond only with JSON that matches the provided schema. "
        "Use the exact field names summary, decisions, action_items, risks, "
        "and for each action item use task, owner, deadline."
    ),
    output_schema=MeetingSummaryOutput,
    output_key="meeting_summary",
    tools=[],
)
