"""
Content API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.content import ContentType, Platform
from ...schemas.content import (
    ContentCreate, ContentResponse,
    AdaptationCreate, AdaptationResponse, AdaptationPreview,
    PLATFORM_CONFIGS, PlatformConfig
)
from ...services.content_service import content_service
from ...services.storage_service import storage_service

router = APIRouter(prefix="/contents", tags=["Content"])


@router.post("/upload", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def upload_content(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(None),
    content_type: ContentType = Form(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload new content for processing"""
    user_id = int(current_user["user_id"])

    # Upload file to storage
    file_content = await file.read()
    file_url = await storage_service.upload_file(
        user_id=user_id,
        file_content=file_content,
        filename=file.filename,
        content_type=file.content_type,
        folder="original"
    )

    # Create content entry
    content_data = ContentCreate(
        title=title,
        description=description,
        content_type=content_type,
        original_file_url=file_url
    )

    content = await content_service.create_content(db, user_id, content_data)

    # Trigger async analysis (in production, would use background task)
    content = await content_service.analyze_content(db, content)

    return ContentResponse.model_validate(content)


@router.get("/", response_model=List[ContentResponse])
async def list_contents(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all contents for current user"""
    user_id = int(current_user["user_id"])
    contents = await content_service.list_user_contents(db, user_id, skip, limit)
    return [ContentResponse.model_validate(c) for c in contents]


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get content by ID"""
    user_id = int(current_user["user_id"])
    content = await content_service.get_content(db, content_id, user_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return ContentResponse.model_validate(content)


@router.post("/{content_id}/analyze", response_model=ContentResponse)
async def analyze_content(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Trigger content analysis"""
    user_id = int(current_user["user_id"])
    content = await content_service.get_content(db, content_id, user_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    content = await content_service.analyze_content(db, content)
    return ContentResponse.model_validate(content)


@router.post("/{content_id}/adapt/preview", response_model=List[AdaptationPreview])
async def preview_adaptations(
    content_id: int,
    target_platforms: List[Platform],
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate preview of adaptations for selected platforms"""
    user_id = int(current_user["user_id"])
    content = await content_service.get_content(db, content_id, user_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    previews = await content_service.generate_adaptations_preview(db, content, target_platforms)
    return previews


@router.post("/{content_id}/adapt", response_model=List[AdaptationResponse])
async def create_adaptations(
    content_id: int,
    previews: List[AdaptationPreview],
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create adaptations from previews"""
    user_id = int(current_user["user_id"])
    content = await content_service.get_content(db, content_id, user_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    adaptations = []
    for preview in previews:
        adaptation = await content_service.create_adaptation(db, content, preview, user_id)
        adaptations.append(AdaptationResponse.model_validate(adaptation))

    return adaptations


@router.get("/{content_id}/adaptations", response_model=List[AdaptationResponse])
async def list_content_adaptations(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all adaptations for a content"""
    user_id = int(current_user["user_id"])
    adaptations = await content_service.list_content_adaptations(db, content_id, user_id)
    return [AdaptationResponse.model_validate(a) for a in adaptations]


@router.get("/platforms/config", response_model=List[PlatformConfig])
async def get_platform_configs():
    """Get configuration for all supported platforms"""
    return list(PLATFORM_CONFIGS.values())
