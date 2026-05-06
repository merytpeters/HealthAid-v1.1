"""User Dashboard with personal information, bio-data,
health metrics"""

import uuid as uuid_lib

from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.api.core.base import Base


class UserDashboard(Base):
    """User Dashboard Model"""

    __tablename__ = "user_dashboards"

    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid_lib.uuid4()),
        index=True,
        autoincrement=False,
    )
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), unique=True)
    personal_info = Column(JSONB)
    bio_data = Column(JSONB)
    health_metrics = Column(JSONB)

    user = relationship("User", back_populates="dashboard")

    def __repr__(self):
        """String representation of Dashboard"""
        return f"<UserDashboard(id={self.id}, user_id={self.user_id})>"
