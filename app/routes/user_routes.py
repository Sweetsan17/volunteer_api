from flask import Blueprint
from app.middleware import roles_required
from app.controllers import user_controller as ctrl

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

