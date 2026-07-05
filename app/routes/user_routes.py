from flask import Blueprint
from app.middleware import roles_required
from app.controllers import user_controller as ctrl

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

@user_bp.route("", methods=["POST"])
@roles_required("admin")
def create_user():
    return ctrl.create_user()

@user_bp.route("", methods=["GET"])
@roles_required("admin")
def get_users():
    return ctrl.get_users()

@user_bp.route("/<int:user_id>", methods=["GET"])
@roles_required("admin")
def get_user(user_id):
    return ctrl.get_user(user_id)

@user_bp.route("/<int:user_id>", methods=["PUT"])
@roles_required("admin")
def update_user(user_id):
    return ctrl.update_user(user_id)

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@roles_required("admin")
def delete_user(user_id):
    return ctrl.delete_user(user_id)