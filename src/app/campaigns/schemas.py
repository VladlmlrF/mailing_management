from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator


class CampaignBaseSchema(BaseModel):
    start_time: datetime
    message_text: str
    filter_mobile_operator_code: str | None
    filter_tag: str | None
    end_time: datetime

    @field_validator("start_time", "end_time")
    def remove_tzinfo(cls, value):
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value


class CampaignCreateSchema(CampaignBaseSchema):
    pass


class CampaignUpdateSchema(CampaignBaseSchema):
    start_time: datetime | None = None
    message_text: str | None = None
    filter_mobile_operator_code: str | None = None
    filter_tag: str | None = None
    end_time: datetime | None = None


class CampaignSchema(CampaignBaseSchema):
    id: int
