from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator

from src.app.core.models import Status


class MessageBaseSchema(BaseModel):
    created_at: datetime
    status: Status
    campaign_id: int
    client_id: int

    @field_validator("created_at")
    def remove_tzinfo(cls, value):
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value


class MessageCreateSchema(MessageBaseSchema):
    pass


class MessageUpdateSchema(MessageBaseSchema):
    created_at: datetime | None = None
    status: Status | None = None
    campaign_id: int | None = None
    client_id: int | None = None


class MessageSchema(MessageBaseSchema):
    id: int
