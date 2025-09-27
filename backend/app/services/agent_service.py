from typing import Dict

from sqlalchemy.orm import Session

from ..agents.sql_agent import SQLAgent
from ..schemas import AgentQuery, ConversationCreate, MessageCreate
from .conversation_service import ConversationService


class AgentService:
    def __init__(self, session: Session):
        self.session = session
        self.conversations = ConversationService(session)
        self.agent = SQLAgent()

    def ask(self, payload: AgentQuery) -> Dict[str, object]:
        conversation = None
        if payload.conversation_id:
            conversation = self.conversations.get_conversation(payload.conversation_id)
            if not conversation:
                raise ValueError("Conversation not found")

        if not conversation:
            conversation = self.conversations.create_conversation(
                ConversationCreate(title="Untitled Conversation")
            )

        self.conversations.add_message(
            conversation.id,
            MessageCreate(role="user", content=payload.question, metadata={"datasource": payload.datasource}),
        )

        result = self.agent.run(
            question=payload.question,
            datasource=payload.datasource,
            datasource_config=payload.datasource_config,
            reasoning_steps=payload.reasoning_steps,
            enable_mcp=payload.enable_mcp,
            enable_tool_calling=payload.enable_tool_calling,
        )

        self.conversations.add_message(
            conversation.id,
            MessageCreate(
                role="assistant",
                content=result.get("answer", ""),
                metadata={"sql": result.get("sql"), "diagnostics": result.get("diagnostics")},
            ),
        )

        return {**result, "conversation_id": conversation.id}
