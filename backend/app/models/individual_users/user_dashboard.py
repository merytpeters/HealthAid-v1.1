"""User Dashboard with personal information, bio-data,
health metrics"""
from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.models.base import Base


class UserDashboard(Base):
    """User Dashboard Model"""
    __tablename__ = "user_dashboards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), unique=True)
    personal_info = Column(JSON)
    bio_data = Column(JSON)
    health_metrics = Column(JSON)
    
    user = relationship("User", back_populates="dashboard")

    def __repr__(self):
        """String representation of Dashboard"""
        return f"<UserDashboard(id={self.id}, user_id={self.user_id})>"
    