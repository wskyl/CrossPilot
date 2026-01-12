"""
Content model for storing original content and adaptations
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..core.database import Base


class ContentType(enum.Enum):
    """Type of original content"""
    VIDEO = "video"
    ARTICLE = "article"
    AUDIO = "audio"
    IMAGE = "image"
    LIVE_RECORDING = "live_recording"
    NOTES = "notes"


class ContentStatus(enum.Enum):
    """Content processing status"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    READY = "ready"
    ERROR = "error"


class Content(Base):
    """Original content uploaded by user"""
    __tablename__ = "contents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Content info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[ContentType] = mapped_column(SQLEnum(ContentType), nullable=False)

    # File info
    original_file_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For video/audio

    # Analysis results
    status: Mapped[ContentStatus] = mapped_column(
        SQLEnum(ContentStatus),
        default=ContentStatus.PENDING
    )
    analysis_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    """
    Analysis result structure:
    {
        "key_points": ["point1", "point2"],
        "emotional_tone": "professional/humorous/friendly",
        "main_topics": ["topic1", "topic2"],
        "visual_elements": ["element1", "element2"],
        "style_fingerprint": {
            "language_style": "professional",
            "visual_style": "minimal",
            "pace": "fast"
        },
        "transcript": "full transcript if available"
    }
    """

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    adaptations: Mapped[List["Adaptation"]] = relationship(back_populates="content", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Content {self.title}>"


class Platform(enum.Enum):
    """Supported social media platforms"""
    DOUYIN = "douyin"        # 抖音
    KUAISHOU = "kuaishou"    # 快手
    XIAOHONGSHU = "xiaohongshu"  # 小红书
    WEIBO = "weibo"          # 微博
    BILIBILI = "bilibili"    # B站
    WECHAT_VIDEO = "wechat_video"  # 视频号
    WECHAT_ARTICLE = "wechat_article"  # 公众号
    ZHIHU = "zhihu"          # 知乎


class AdaptationStatus(enum.Enum):
    """Adaptation processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PUBLISHED = "published"
    ERROR = "error"


class Adaptation(Base):
    """Adapted content for specific platform"""
    __tablename__ = "adaptations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("contents.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Platform info
    platform: Mapped[Platform] = mapped_column(SQLEnum(Platform), nullable=False)

    # Adapted content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hashtags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Files
    adapted_file_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Status
    status: Mapped[AdaptationStatus] = mapped_column(
        SQLEnum(AdaptationStatus),
        default=AdaptationStatus.PENDING
    )

    # Publishing info
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    platform_post_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    platform_post_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Analytics
    analytics_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    """
    Analytics structure:
    {
        "views": 0,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "saves": 0,
        "completion_rate": 0.0  # for videos
    }
    """

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content: Mapped["Content"] = relationship(back_populates="adaptations")

    def __repr__(self) -> str:
        return f"<Adaptation {self.platform.value}: {self.title}>"
