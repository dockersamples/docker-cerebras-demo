import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

local_agent = Agent(
    model=LiteLlm(
        model=f"openai/{os.environ.get('LOCAL_AGENT_CHAT_MODEL')}",
        api_base=os.environ.get("LOCAL_AGENT_BASE_URL"),
        api_key="tada",
        temperature=0.0,
    ),
    name=os.environ.get("LOCAL_AGENT_NAME"),
    description=os.environ.get("LOCAL_AGENT_DESCRIPTION"),
    instruction=os.environ.get("LOCAL_AGENT_INSTRUCTION"),
)
