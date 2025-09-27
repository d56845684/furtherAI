from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    role: str
    content: str
    metadata: Optional[dict[str, Any]] = None


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    title: str = Field(..., max_length=255)


class ConversationCreate(ConversationBase):
    messages: Optional[List[MessageCreate]] = None


class ConversationUpdate(BaseModel):
    title: Optional[str] = None


class ConversationRead(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class AgentQuery(BaseModel):
    conversation_id: Optional[UUID] = None
    question: str
    datasource: str = Field(..., description="Target data source identifier")
    datasource_config: dict[str, Any] = Field(default_factory=dict)
    reasoning_steps: Optional[int] = None
    enable_mcp: Optional[bool] = None
    enable_tool_calling: Optional[bool] = None


class AgentResponse(BaseModel):
    conversation_id: UUID
    answer: str
    sql: Optional[str] = None
    diagnostics: dict[str, Any] = Field(default_factory=dict)
