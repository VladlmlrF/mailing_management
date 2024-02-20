from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.campaigns import crud
from src.app.campaigns.schemas import CampaignCreateSchema
from src.app.campaigns.schemas import CampaignSchema
from src.app.campaigns.schemas import CampaignUpdateSchema
from src.app.core.models import db_helper


router = APIRouter(tags=["Campaigns"])


@router.post("/", response_model=CampaignSchema, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_in: CampaignCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_campaign(session=session, campaign=campaign_in)


@router.get("/", response_model=list[CampaignSchema])
async def get_campaigns(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_campaigns(session=session)


@router.get("/{campaign_id}", response_model=CampaignSchema)
async def get_campaign(
    campaign_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_campaign(campaign_id=campaign_id, session=session)


@router.patch("/{campaign_id}", response_model=CampaignSchema)
async def update_client(
    campaign_id: int,
    campaign_update: CampaignUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    campaign = await crud.get_campaign(campaign_id=campaign_id, session=session)
    return await crud.update_campaign(
        session=session, campaign=campaign, campaign_update=campaign_update
    )


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    campaign = await crud.get_campaign(campaign_id=campaign_id, session=session)
    await crud.delete_campaign(session=session, campaign=campaign)
