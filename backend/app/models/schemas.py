from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    response: str


class ToolResult(BaseModel):
    tool: str
    success: bool
    data: object
    error: str | None = None