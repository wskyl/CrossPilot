"""
Content schemas for API request/response
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from ..models.content import ContentType, ContentStatus, Platform, AdaptationStatus


class ContentBase(BaseModel):
    """Base content schema"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    content_type: ContentType


class ContentCreate(ContentBase):
    """Schema for content upload"""
    original_file_url: str


class ContentAnalysis(BaseModel):
    """Schema for content analysis result"""
    key_points: List[str]
    emotional_tone: str
    main_topics: List[str]
    visual_elements: List[str]
    style_fingerprint: dict
    transcript: Optional[str] = None


class ContentResponse(ContentBase):
    """Schema for content response"""
    id: int
    user_id: int
    original_file_url: str
    file_size: Optional[int]
    duration_seconds: Optional[int]
    status: ContentStatus
    analysis_result: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Platform configurations
class PlatformConfig(BaseModel):
    """Platform-specific configuration"""
    platform: Platform
    name: str
    display_name: str
    max_duration_seconds: Optional[int]
    aspect_ratio: str
    max_title_length: int
    max_caption_length: int
    supported_formats: List[str]
    style_keywords: List[str]


PLATFORM_CONFIGS = {
    Platform.DOUYIN: PlatformConfig(
        platform=Platform.DOUYIN,
        name="douyin",
        display_name="抖音",
        max_duration_seconds=60,
        aspect_ratio="9:16",
        max_title_length=55,
        max_caption_length=300,
        supported_formats=["mp4"],
        style_keywords=["快节奏", "强冲击", "音乐驱动", "悬念", "互动"]
    ),
    Platform.KUAISHOU: PlatformConfig(
        platform=Platform.KUAISHOU,
        name="kuaishou",
        display_name="快手",
        max_duration_seconds=60,
        aspect_ratio="9:16",
        max_title_length=50,
        max_caption_length=200,
        supported_formats=["mp4"],
        style_keywords=["接地气", "真实", "生活化"]
    ),
    Platform.XIAOHONGSHU: PlatformConfig(
        platform=Platform.XIAOHONGSHU,
        name="xiaohongshu",
        display_name="小红书",
        max_duration_seconds=300,
        aspect_ratio="3:4",
        max_title_length=20,
        max_caption_length=1000,
        supported_formats=["mp4", "jpg", "png"],
        style_keywords=["精致", "实用", "获得感", "种草"]
    ),
    Platform.WEIBO: PlatformConfig(
        platform=Platform.WEIBO,
        name="weibo",
        display_name="微博",
        max_duration_seconds=900,
        aspect_ratio="16:9",
        max_title_length=30,
        max_caption_length=140,
        supported_formats=["mp4", "jpg", "png", "gif"],
        style_keywords=["热点", "简洁", "话题"]
    ),
    Platform.BILIBILI: PlatformConfig(
        platform=Platform.BILIBILI,
        name="bilibili",
        display_name="B站",
        max_duration_seconds=None,  # No limit
        aspect_ratio="16:9",
        max_title_length=80,
        max_caption_length=2000,
        supported_formats=["mp4", "flv"],
        style_keywords=["有梗", "深度", "社区互动", "弹幕文化"]
    ),
    Platform.WECHAT_VIDEO: PlatformConfig(
        platform=Platform.WECHAT_VIDEO,
        name="wechat_video",
        display_name="视频号",
        max_duration_seconds=3600,
        aspect_ratio="16:9",
        max_title_length=30,
        max_caption_length=1000,
        supported_formats=["mp4"],
        style_keywords=["深度", "专业", "共鸣"]
    ),
    Platform.WECHAT_ARTICLE: PlatformConfig(
        platform=Platform.WECHAT_ARTICLE,
        name="wechat_article",
        display_name="公众号",
        max_duration_seconds=None,
        aspect_ratio="1:1",  # Cover image
        max_title_length=64,
        max_caption_length=None,  # Long form
        supported_formats=["html", "jpg", "png"],
        style_keywords=["深度", "专业", "图文并茂"]
    ),
    Platform.ZHIHU: PlatformConfig(
        platform=Platform.ZHIHU,
        name="zhihu",
        display_name="知乎",
        max_duration_seconds=None,
        aspect_ratio="16:9",
        max_title_length=50,
        max_caption_length=None,  # Long form
        supported_formats=["mp4", "jpg", "png"],
        style_keywords=["理性", "深度", "数据支撑"]
    ),
}


class AdaptationBase(BaseModel):
    """Base adaptation schema"""
    platform: Platform
    title: str = Field(..., min_length=1, max_length=500)
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None


class AdaptationCreate(BaseModel):
    """Schema for creating adaptation request"""
    content_id: int
    target_platforms: List[Platform]


class AdaptationUpdate(BaseModel):
    """Schema for updating adaptation"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None


class AdaptationResponse(AdaptationBase):
    """Schema for adaptation response"""
    id: int
    content_id: int
    user_id: int
    adapted_file_url: Optional[str]
    thumbnail_url: Optional[str]
    status: AdaptationStatus
    published_at: Optional[datetime]
    platform_post_url: Optional[str]
    analytics_data: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdaptationPreview(BaseModel):
    """Schema for adaptation preview (before saving)"""
    platform: Platform
    platform_config: PlatformConfig
    suggested_title: str
    suggested_caption: str
    suggested_hashtags: List[str]
    thumbnail_preview_url: Optional[str]
    estimated_duration_seconds: Optional[int]
