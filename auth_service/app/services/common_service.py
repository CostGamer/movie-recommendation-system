from typing import Any

from auth_service.app.DB.models.pydantic_models import EventP, EventType
from auth_service.app.repo.events_repo import EventsRepo
from fastapi import Request


class EventsService:
    def __init__(
        self,
        event_repo: EventsRepo,
        request: Request,
    ) -> None:
        self._event_repo = event_repo
        self._request = request

    async def _create_event(
        self,
        event_type: EventType,
        payload: dict[str, Any],
        user_id: str | None = None,
    ) -> None:
        client_ip = {
            "client_ip": (
                self._request.client.host if self._request.client else "Unknown"
            )
        }
        payload.update(client_ip)
        event = EventP(
            user_id=user_id,
            event_type=event_type,
            payload=payload,
        )
        await self._event_repo.insert_event_to_db(event)
