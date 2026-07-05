from datetime import datetime
from flask import request, jsonify
from app.extensions import db
from app.models.user_model import User

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

