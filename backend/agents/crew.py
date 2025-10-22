"""Crew orchestration for contract analysis."""
from crewai import Crew

from .agents import get_contract_analyst, get_risk_detector
from .tasks import get_analysis_task, get_risk_detection_task


def create_contract_crew(stt_text: str, ocr_text: str, enable_risk_detection: bool = False) -> Crew:
    """
    Create crew for contract analysis.

    Args:
        stt_text: Transcribed speech text
        ocr_text: Extracted document text
        enable_risk_detection: Whether to enable risk detection agent

    Returns:
        Configured crew
    """
    combined_text = f"[음성 대화]\n{stt_text}\n\n[문서 내용]\n{ocr_text}"

    # Setup analyst
    analyst = get_contract_analyst()
    analysis_task = get_analysis_task(analyst, combined_text)

    agents = [analyst]
    tasks = [analysis_task]

    # Optionally add risk detection
    if enable_risk_detection:
        risk_detector = get_risk_detector()
        risk_task = get_risk_detection_task(risk_detector, analysis_task)
        agents.append(risk_detector)
        tasks.append(risk_task)

    return Crew(agents=agents, tasks=tasks, verbose=True)


def analyze_contract(stt_text: str, ocr_text: str, enable_risk_detection: bool = False) -> str:
    """
    Analyze contract using crew.

    Args:
        stt_text: Transcribed speech text
        ocr_text: Extracted document text
        enable_risk_detection: Whether to enable risk detection

    Returns:
        Analysis results
    """
    crew = create_contract_crew(stt_text, ocr_text, enable_risk_detection)
    result = crew.kickoff()

    # Combine results if risk detection enabled
    if enable_risk_detection and len(result.tasks_output) > 1:
        summary = result.tasks_output[0].raw
        risks = result.tasks_output[1].raw
        return f"## 계약서 요약\n\n{summary}\n\n## 위험 요소 분석\n\n{risks}"

    return result.raw
