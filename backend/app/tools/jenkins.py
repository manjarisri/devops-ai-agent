from typing import Any

import requests

from app.config import settings


def is_jenkins_configured() -> bool:
    return bool(
        settings.JENKINS_URL
        and settings.JENKINS_USERNAME
        and settings.JENKINS_TOKEN
    )


def get_jenkins_status() -> dict[str, Any]:
    """
    Check Jenkins connectivity.
    """

    if not is_jenkins_configured():
        return {
            "configured": False,
            "status": "not_configured",
            "message": (
                "Jenkins integration is not configured yet."
            ),
        }

    try:
        response = requests.get(
            f"{settings.JENKINS_URL}/api/json",
            auth=(
                settings.JENKINS_USERNAME,
                settings.JENKINS_TOKEN,
            ),
            timeout=10,
        )

        response.raise_for_status()

        return {
            "configured": True,
            "status": "connected",
            "jenkins_url": settings.JENKINS_URL,
        }

    except requests.RequestException as exc:
        return {
            "configured": True,
            "status": "error",
            "message": str(exc),
        }


def get_jenkins_jobs() -> list[dict[str, Any]]:
    """
    Return Jenkins jobs.
    """

    if not is_jenkins_configured():
        return []

    try:
        response = requests.get(
            f"{settings.JENKINS_URL}/api/json",
            params={
                "tree": (
                    "jobs[name,url,color]"
                )
            },
            auth=(
                settings.JENKINS_USERNAME,
                settings.JENKINS_TOKEN,
            ),
            timeout=10,
        )

        response.raise_for_status()

        return response.json().get("jobs", [])

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Jenkins error: {str(exc)}"
        )