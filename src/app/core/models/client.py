from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class Client(Base, table=True):
    phone_number: str = Field(unique=True, index=True)
    mobile_operator_code: str
    tag: str | None = None
    timezone: str
    messages: list["Message"] = Relationship(back_populates="client")
