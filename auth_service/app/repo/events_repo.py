from typing import Type

from auth_service.app.DB.models.beanie_models import Event
from auth_service.app.DB.models.pydantic_models import EventP
from beanie import Document


class EventsRepo:
    def __init__(self, event_model: Type[Document]):
        self._event_model = event_model

    async def insert_event_to_db(self, event_data: EventP) -> Document | None:
        event = Event(
            aggregate_id=event_data.user_id,
            event_type=event_data.event_type,
            payload=event_data.payload,
        )
        return await self._event_model.insert_one(event)
