import os

from crewai import Agent, LLM
from crewai.tools import tool


@tool("support_hours")
def support_hours() -> str:
    """Return the support team's published hours."""
    return "Support is available Monday to Friday, 09:00-17:00 UTC."


agent = Agent(
    role="Support assistant",
    goal="Answer support questions accurately using the available tools.",
    backstory="You are a concise support assistant. Use support_hours for questions about hours.",
    llm=LLM(model=os.getenv("MODEL", "openai/gpt-6.1-sol"), api="responses"),
    tools=[support_hours],
    max_iter=5,
)
