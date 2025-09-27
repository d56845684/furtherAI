from fastapi import APIRouter, Depends, HTTPException, status

from ..db import get_db
from ..schemas import AgentQuery, AgentResponse
from ..services.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])


def get_service(db=Depends(get_db)) -> AgentService:  # type: ignore[valid-type]
    return AgentService(db)


@router.post("/ask", response_model=AgentResponse)
def ask_agent(payload: AgentQuery, service: AgentService = Depends(get_service)):
    try:
        result = service.ask(payload)
        return AgentResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
