from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.core.models import Message
from src.app.messages.schemas import MessageCreateSchema
from src.app.messages.schemas import MessageUpdateSchema


async def create_message(
    session: AsyncSession, message: MessageCreateSchema
) -> Message:
    """Create new message"""
    new_message = Message(
        created_at=message.created_at,
        status=message.status,
        campaign_id=message.campaign_id,
        client_id=message.client_id,
    )
    try:
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_message(message_id: int, session: AsyncSession) -> Message | None:
    """Get message by id"""
    try:
        statement = select(Message).where(Message.id == message_id)
        message = await session.scalar(statement=statement)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Message {message_id} not found",
            )
        return message
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_messages(session: AsyncSession) -> list[Message]:
    """Get all messages"""
    try:
        statement = select(Message)
        result: Result = await session.execute(statement=statement)
        messages = result.scalars().all()
        return list(messages)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def update_message(
    session: AsyncSession, message: Message, message_update: MessageUpdateSchema
) -> Message:
    """Update message"""
    try:
        for name, value in message_update.model_dump(exclude_unset=True).items():
            setattr(message, name, value)
        await session.commit()
        await session.refresh(message)
        return message
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_message(session: AsyncSession, message: Message) -> None:
    """Delete message"""
    try:
        await session.delete(message)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
