"""User Dashboard Crud"""

from sqlalchemy.orm import Session

# from backend.lib.utils.user_dashboard import
from backend.lib.errorlib.auth import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from backend.app.models.individual_users.user_dashboard import UserDashboard


def get_user_dashboard_by_id():
    pass


def create_dashboard():
    pass


def update_health_metrics():
    pass
