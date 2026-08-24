from fastapi import APIRouter
from pydantic import BaseModel

from app.tools.kubernetes import (
    get_pods,
    get_deployments,
    get_services,
)
from app.analysis.incident_analyzer import investigate_application
from app.agent.agent import review_deployment, review_iac


router = APIRouter(prefix="/api", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    message = request.message.lower()

    if "pod" in message:
        return {
            "type": "kubernetes",
            "response": get_pods(),
        }

    if "deployment" in message:
        return {
            "type": "kubernetes",
            "response": get_deployments(),
        }

    if "service" in message:
        return {
            "type": "kubernetes",
            "response": get_services(),
        }

    if "incident" in message or "investigate" in message:
        return {
            "type": "incident",
            "response": investigate_application(
                "demo-app"
            ),
        }

    return {
        "type": "text",
        "response": (
            "I can help with Kubernetes status, "
            "incident investigation, deployment "
            "reviews and IaC reviews."
        ),
    }