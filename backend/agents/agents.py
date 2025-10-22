"""Agent definitions for contract analysis."""
from crewai import Agent
from langchain_openai import ChatOpenAI

from config import get_settings
from .prompts import (
    ANALYST_BACKSTORY,
    ANALYST_GOAL,
    ANALYST_ROLE,
    RISK_DETECTOR_BACKSTORY,
    RISK_DETECTOR_GOAL,
    RISK_DETECTOR_ROLE,
)


def get_llm() -> ChatOpenAI:
    """Get configured LLM instance."""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.openai_model_name,
        api_key=settings.openai_api_key,
        temperature=0.1,
    )


def get_contract_analyst() -> Agent:
    """Get contract analyst agent."""
    return Agent(
        role=ANALYST_ROLE,
        goal=ANALYST_GOAL,
        backstory=ANALYST_BACKSTORY,
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )


def get_risk_detector() -> Agent:
    """Get risk detector agent."""
    return Agent(
        role=RISK_DETECTOR_ROLE,
        goal=RISK_DETECTOR_GOAL,
        backstory=RISK_DETECTOR_BACKSTORY,
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )
