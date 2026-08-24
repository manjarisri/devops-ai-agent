from fastapi import APIRouter

from app.agent.agent import (
    review_deployment,
    review_iac,
)


router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"],
)


@router.post("/deployment")
def deployment_review(payload: dict):

    content = payload.get(
        "content",
        "",
    )

    return review_deployment(content)


@router.post("/iac")
def iac_review(payload: dict):

    content = payload.get(
        "content",
        "",
    )

    iac_type = payload.get(
        "iac_type",
        "terraform",
    )

    return review_iac(
        content,
        iac_type,
    )