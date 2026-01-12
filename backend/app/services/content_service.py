"""
Content processing service for analysis and adaptation
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.content import Content, Adaptation, ContentStatus, AdaptationStatus, Platform
from ..schemas.content import ContentCreate, AdaptationCreate, AdaptationResponse, AdaptationPreview
from .ai_service import ai_service


class ContentService:
    """Service for content management and processing"""

    async def create_content(
        self,
        db: AsyncSession,
        user_id: int,
        content_data: ContentCreate
    ) -> Content:
        """Create new content entry"""
        content = Content(
            user_id=user_id,
            title=content_data.title,
            description=content_data.description,
            content_type=content_data.content_type,
            original_file_url=content_data.original_file_url,
            status=ContentStatus.PENDING
        )
        db.add(content)
        await db.commit()
        await db.refresh(content)
        return content

    async def get_content(
        self,
        db: AsyncSession,
        content_id: int,
        user_id: int
    ) -> Optional[Content]:
        """Get content by ID"""
        result = await db.execute(
            select(Content).where(
                Content.id == content_id,
                Content.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def list_user_contents(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[Content]:
        """List all contents for a user"""
        result = await db.execute(
            select(Content)
            .where(Content.user_id == user_id)
            .order_by(Content.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def analyze_content(
        self,
        db: AsyncSession,
        content: Content
    ) -> Content:
        """Run AI analysis on content"""
        content.status = ContentStatus.ANALY
        await db.commit()

        try:
            # Get content text (in real implementation, would extract from file)
            content_text = content.description or content.title

            # Run AI analysis
            analysis = await ai_service.analyze_content(
                content_text=content_text,
                content_type=content.content_type
            )

            content.analysis_result = analysis.model_dump()
            content.status = ContentStatus.READY

        except Exception as e:
            content.status = ContentStatus.ERROR
            content.analysis_result = {"error": str(e)}

        await db.commit()
        await db.refresh(content)
        return content

    async def generate_adaptations_preview(
        self,
        db: AsyncSession,
        content: Content,
        target_platforms: List[Platform]
    ) -> List[AdaptationPreview]:
        """Generate preview of adaptations for multiple platforms"""

        if not content.analysis_result:
            content = await self.analyze_content(db, content)

        previews = []
        from ..schemas.content import ContentAnalysis
        analysis = ContentAnalysis(**content.analysis_result)

        for platform in target_platforms:
            preview = await ai_service.generate_adaptation(
                original_content=content.description or content.title,
                analysis=analysis,
                target_platform=platform
            )
            previews.append(preview)

        return previews

    async def create_adaptation(
        self,
        db: AsyncSession,
        content: Content,
        preview: AdaptationPreview,
        user_id: int
    ) -> Adaptation:
        """Create adaptation from preview"""
        adaptation = Adaptation(
            content_id=content.id,
            user_id=user_id,
            platform=preview.platform,
            title=preview.suggested_title,
            caption=preview.suggested_caption,
            hashtags=preview.suggested_hashtags,
            status=AdaptationStatus.PENDING
        )
        db.add(adaptation)
        await db.commit()
        await db.refresh(adaptation)
        return adaptation

    async def get_adaptation(
        self,
        db: AsyncSession,
        adaptation_id: int,
        user_id: int
    ) -> Optional[Adaptation]:
        """Get adaptation by ID"""
        result = await db.execute(
            select(Adaptation).where(
                Adaptation.id == adaptation_id,
                Adaptation.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def list_content_adaptations(
        self,
        db: AsyncSession,
        content_id: int,
        user_id: int
    ) -> List[Adaptation]:
        """List all adaptations for a content"""
        result = await db.execute(
            select(Adaptation)
            .where(
                Adaptation.content_id == content_id,
                Adaptation.user_id == user_id
            )
            .order_by(Adaptation.created_at.desc())
        )
        return list(result.scalars().all())


# Create singleton instance
content_service = ContentService()
