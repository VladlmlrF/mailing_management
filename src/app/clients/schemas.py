from pydantic import BaseModel


class ClientBaseSchema(BaseModel):
    phone_number: str
    mobile_operator_code: str
    tag: str | None = None
    timezone: str


class ClientCreateSchema(ClientBaseSchema):
    pass


class ClientUpdateSchema(ClientBaseSchema):
    phone_number: str | None = None
    mobile_operator_code: str | None = None
    timezone: str | None = None


class ClientSchema(ClientBaseSchema):
    id: int
