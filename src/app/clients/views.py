from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.clients import crud
from src.app.clients.schemas import ClientCreateSchema
from src.app.clients.schemas import ClientSchema
from src.app.clients.schemas import ClientUpdateSchema
from src.app.core.models import db_helper

router = APIRouter(tags=["Clients"])


@router.post("/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: ClientCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_client(session=session, client=client_in)


@router.get("/", response_model=list[ClientSchema])
async def get_clients(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_clients(session=session)


@router.get("/{client_id}", response_model=ClientSchema)
async def get_client(
    client_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_client(client_id=client_id, session=session)


@router.patch("/{client_id}", response_model=ClientSchema)
async def update_client(
    client_id: int,
    client_update: ClientUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    client = await crud.get_client(client_id=client_id, session=session)
    return await crud.update_client(
        session=session, client=client, client_update=client_update
    )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    client = await crud.get_client(client_id=client_id, session=session)
    await crud.delete_client(session=session, client=client)
