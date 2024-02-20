from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.core.models import db_helper
from src.app.messages import crud
from src.app.messages.schemas import MessageCreateSchema
from src.app.messages.schemas import MessageSchema
from src.app.messages.schemas import MessageUpdateSchema

router = APIRouter(tags=["Messages"])


@router.post("/", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_in: MessageCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_message(session=session, message=message_in)


@router.get("/", response_model=list[MessageSchema])
async def get_messages(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_messages(session=session)


@router.get("/{message_id}", response_model=MessageSchema)
async def get_message(
    message_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_message(message_id=message_id, session=session)


@router.patch("/{message_id}", response_model=MessageSchema)
async def update_message(
    message_id: int,
    message_update: MessageUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    message = await crud.get_message(message_id=message_id, session=session)
    return await crud.update_message(
        session=session, message=message, message_update=message_update
    )


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    message = await crud.get_message(message_id=message_id, session=session)
    await crud.delete_message(session=session, message=message)
