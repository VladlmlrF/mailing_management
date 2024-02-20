from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .client import Client
    from .campaign import Campaign


class Status(str, Enum):
    SENT = "SENT"
    PENDING = "PENDING"
    FAILED = "FAILED"


class Message(Base, table=True):
    created_at: datetime = Field(default_factory=datetime.now)
    status: Status = Field(default=Status.PENDING)
    campaign_id: int = Field(foreign_key="campaign.id")
    client_id: int = Field(foreign_key="client.id")
    campaign: "Campaign" = Relationship(back_populates="messages")
    client: "Client" = Relationship(back_populates="messages")
