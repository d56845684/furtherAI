from typing import Iterable, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Conversation, Message
from ..schemas import ConversationCreate, ConversationUpdate, MessageCreate


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def list_conversations(self) -> Iterable[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.created_at.desc())
        )
        return self.session.execute(stmt).scalars().all()

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return self.session.execute(stmt).scalars().first()

    def create_conversation(self, payload: ConversationCreate) -> Conversation:
        conversation = Conversation(title=payload.title)
        self.session.add(conversation)
        self.session.flush()

        if payload.messages:
            for message in payload.messages:
                self._append_message(conversation, message)

        self.session.flush()
        reloaded = self.get_conversation(conversation.id)
        assert reloaded is not None  # for type-checkers
        return reloaded

    def update_conversation(self, conversation_id: UUID, payload: ConversationUpdate) -> Optional[Conversation]:
        conversation = self.session.get(Conversation, conversation_id)
        if not conversation:
            return None

        if payload.title is not None:
            conversation.title = payload.title

        self.session.flush()
        updated = self.get_conversation(conversation_id)
        return updated

    def delete_conversation(self, conversation_id: UUID) -> bool:
        conversation = self.session.get(Conversation, conversation_id)
        if not conversation:
            return False
        self.session.delete(conversation)
        return True

    def add_message(self, conversation_id: UUID, payload: MessageCreate) -> Optional[Conversation]:
        conversation = self.session.get(Conversation, conversation_id)
        if not conversation:
            return None
        self._append_message(conversation, payload)
        self.session.flush()
        updated = self.get_conversation(conversation_id)
        return updated

    def _append_message(self, conversation: Conversation, payload: MessageCreate) -> Message:
        message = Message(
            conversation_id=conversation.id,
            role=payload.role,
            content=payload.content,
            metadata=payload.metadata,
        )
        self.session.add(message)
        return message
