from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.campaigns.schemas import CampaignCreateSchema
from src.app.campaigns.schemas import CampaignUpdateSchema
from src.app.core.models import Campaign


async def create_campaign(
    session: AsyncSession, campaign: CampaignCreateSchema
) -> Campaign:
    """Create new campaign"""
    new_campaign = Campaign(
        start_time=campaign.start_time,
        message_text=campaign.message_text,
        filter_mobile_operator_code=campaign.filter_mobile_operator_code,
        filter_tag=campaign.filter_tag,
        end_time=campaign.end_time,
    )
    try:
        session.add(new_campaign)
        await session.commit()
        await session.refresh(new_campaign)
        return new_campaign
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_campaign(campaign_id: int, session: AsyncSession) -> Campaign | None:
    """Get campaign by id"""
    try:
        statement = select(Campaign).where(Campaign.id == campaign_id)
        campaign = await session.scalar(statement=statement)
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campaign {campaign_id} not found",
            )
        return campaign
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_campaigns(session: AsyncSession) -> list[Campaign]:
    """Get all campaigns"""
    try:
        statement = select(Campaign)
        result: Result = await session.execute(statement=statement)
        campaigns = result.scalars().all()
        return list(campaigns)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def update_campaign(
    session: AsyncSession, campaign: Campaign, campaign_update: CampaignUpdateSchema
) -> Campaign:
    """Update campaign"""
    try:
        for name, value in campaign_update.model_dump(exclude_unset=True).items():
            setattr(campaign, name, value)
        await session.commit()
        await session.refresh(campaign)
        return campaign
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_campaign(session: AsyncSession, campaign: Campaign) -> None:
    """Delete campaign"""
    try:
        await session.delete(campaign)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
