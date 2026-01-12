"""
Platform account model for connected social media accounts
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base
from .content import Platform


class PlatformAccount(Base):
    """Connected platform accounts for publishing"""
    __tablename__ = "platform_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Platform info
    platform: Mapped[Platform] = mapped_column(nullable=False)
    platform_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    platform_username: Mapped[str] = mapped_column(String(255), nullable=False)

    # OAuth tokens
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<PlatformAccount {self.platform.value}: {self.platform_username}>"
