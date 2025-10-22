"""Task definitions for contract analysis."""
from crewai import Agent, Task

from .prompts import ANALYSIS_TASK_DESCRIPTION, RISK_DETECTION_TASK_DESCRIPTION


def get_analysis_task(agent: Agent, combined_text: str) -> Task:
    """Get contract analysis task."""
    return Task(
        description=ANALYSIS_TASK_DESCRIPTION.format(combined_text=combined_text),
        agent=agent,
        expected_output="명확하고 간결한 계약서 요약",
    )


def get_risk_detection_task(agent: Agent, context_task: Task) -> Task:
    """Get risk detection task."""
    return Task(
        description=RISK_DETECTION_TASK_DESCRIPTION,
        agent=agent,
        expected_output="위험 요소 목록과 구체적인 대응 방안",
        context=[context_task],
    )
