import asyncio
import logging
import textwrap

from dotenv import load_dotenv
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import question_answering_agent

load_dotenv()
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def print_section(title: str) -> None:
    line = "=" * 56
    print(f"\n{line}\n{title}\n{line}")


async def main() -> None:
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    initial_state = {
        "user_name": "Mia Chen",
        "user_preferences": """
            I love coastal cities, local food tours, and art museums.
            I prefer spring or autumn trips instead of peak summer.
            My favorite kind of vacation is a relaxed 4 to 5 day city break.
            I usually choose places with good public transportation and walkable neighborhoods.
        """,
    }

    app_name = "Travel Buddy"
    user_id = "mia_chen"
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state=initial_state,
    )
    print_section("Travel Buddy")
    logger.info("Created new session: %s", session.id)

    runner = Runner(
        agent=question_answering_agent,
        app_name=app_name,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("Ask about Mia's travel preferences. Type 'exit' to quit.")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit", "q"}:
            logger.info("Exiting chat loop.")
            break
        if not question:
            question = "What kind of trip would Mia probably enjoy most?"

        new_message = types.Content(
            role="user",
            parts=[types.Part(text=question)],
        )

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("Agent", event.content.parts[0].text)

    await runner.close()

    print_section("Final Session State")
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id,
    )

    if session is not None:
        for key, value in session.state.items():
            cleaned_value = textwrap.dedent(str(value)).strip()
            print(key, cleaned_value)


if __name__ == "__main__":
    asyncio.run(main())
