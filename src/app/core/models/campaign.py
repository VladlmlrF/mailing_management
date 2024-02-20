from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class Campaign(Base, table=True):
    start_time: datetime
    message_text: str
    filter_mobile_operator_code: str | None = None
    filter_tag: str | None = None
    end_time: datetime
    messages: list["Message"] = Relationship(back_populates="campaign")
