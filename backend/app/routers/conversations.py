from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..db import get_db
from ..schemas import ConversationCreate, ConversationRead, ConversationUpdate, MessageCreate
from ..services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


def get_service(db=Depends(get_db)) -> ConversationService:  # type: ignore[valid-type]
    return ConversationService(db)


@router.get("/", response_model=List[ConversationRead])
def list_conversations(service: ConversationService = Depends(get_service)):
    return service.list_conversations()


@router.post("/", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, service: ConversationService = Depends(get_service)):
    return service.create_conversation(payload)


@router.get("/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: UUID, service: ConversationService = Depends(get_service)):
    conversation = service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation


@router.patch("/{conversation_id}", response_model=ConversationRead)
def update_conversation(
    conversation_id: UUID,
    payload: ConversationUpdate,
    service: ConversationService = Depends(get_service),
):
    conversation = service.update_conversation(conversation_id, payload)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: UUID, service: ConversationService = Depends(get_service)):
    success = service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")


@router.post("/{conversation_id}/messages", response_model=ConversationRead)
def add_message(
    conversation_id: UUID,
    payload: MessageCreate,
    service: ConversationService = Depends(get_service),
):
    conversation = service.add_message(conversation_id, payload)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation
