from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.clients.schemas import ClientCreateSchema
from src.app.clients.schemas import ClientUpdateSchema
from src.app.core.models import Client


async def create_client(session: AsyncSession, client: ClientCreateSchema) -> Client:
    """Create new client"""
    new_client = Client(
        phone_number=client.phone_number,
        mobile_operator_code=client.mobile_operator_code,
        tag=client.tag,
        timezone=client.timezone,
    )
    try:
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)
        return new_client
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_client(client_id: int, session: AsyncSession) -> Client | None:
    """Get client by id"""
    try:
        statement = select(Client).where(Client.id == client_id)
        client = await session.scalar(statement=statement)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client {client_id} not found",
            )
        return client
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_clients(session: AsyncSession) -> list[Client]:
    """Get all clients"""
    try:
        statement = select(Client)
        result: Result = await session.execute(statement=statement)
        clients = result.scalars().all()
        return list(clients)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def update_client(
    session: AsyncSession, client: Client, client_update: ClientUpdateSchema
) -> Client:
    """Update client"""
    try:
        for name, value in client_update.model_dump(exclude_unset=True).items():
            setattr(client, name, value)
        await session.commit()
        await session.refresh(client)
        return client
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_client(session: AsyncSession, client: Client) -> None:
    """Delete client"""
    try:
        await session.delete(client)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
