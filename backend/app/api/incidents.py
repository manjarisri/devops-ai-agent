from fastapi import APIRouter, HTTPException

from app.analysis.incident_analyzer import (
    investigate_application,
)
from app.agent.agent import analyze_incident


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"],
)


@router.get("/{app_name}")
def investigate(
    app_name: str,
    namespace: str = "default",
):

    try:

        evidence = investigate_application(
            app_name=app_name,
            namespace=namespace,
        )

        analysis = analyze_incident(
            evidence
        )

        return {
            "evidence": evidence,
            "analysis": analysis,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )