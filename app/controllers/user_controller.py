from flask import request, jsonify
from app.extensions import db
from app.models.user_model import User
from app.utils import utc_now


def validate_user_payload(data, user_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    username = data.get("username")
    if username is None or str(username).strip() == "":
        errors.append("username is required.")

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")
    elif str(email).strip():
        q = User.query.filter(User.email == str(email).strip())
        if user_id:
            q = q.filter(User.id != user_id)
        if q.first():
            errors.append("Email address already exists.")

    password = data.get("password")
    if password is None or str(password).strip() == "":
        errors.append("password is required.")

    return errors


def create_user():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = validate_user_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_user = User(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify({"message": "User created successfully.", "user": new_user.to_dict()}),
        201,
    )


def get_users(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200


def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = validate_user_payload(data, user_id=user_id)
    if errors:
        return jsonify({"errors": errors}), 400

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if "password" in data:
        user.set_password(data["password"])
    user.updated_at = utc_now()

    db.session.commit()

    return (
        jsonify({"message": "User updated successfully.", "user": user.to_dict()}),
        200,
    )


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully."}), 200
