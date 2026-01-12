"""
User model for authentication and profile management
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from ..core.database import Base


class SubscriptionPlan(enum.Enum):
    """User subscription plans"""
    FREE = "free"
    PROFESSIONAL = "professional"
    TEAM = "team"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Subscription
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        SQLEnum(SubscriptionPlan),
        default=SubscriptionPlan.FREE,
        nullable=False
    )
    monthly_conversions_used: Mapped[int] = mapped_column(default=0)
    monthly_conversions_limit: Mapped[int] = mapped_column(default=5)  # Free plan limit

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
