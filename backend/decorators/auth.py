from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models import User


def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # 🔥 NEW: BLOCK CHECK
        if user.is_blocked:
            return jsonify({
                "message": "Your account is blocked by admin"
            }), 403

        if user.role != "admin":
            return jsonify({
                "message": "Admin access required."
            }), 403

        return fn(*args, **kwargs)

    return wrapper 

def staff_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # 🔥 NEW: BLOCK CHECK
        if user.is_blocked:
            return jsonify({
                "message": "Your account is blocked by admin"
            }), 403

        if user.role != "staff":
            return jsonify({
                "message": "Staff access required."
            }), 403

        return fn(*args, **kwargs)

    return wrapper  

def user_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user:
            return jsonify({
                "message": "User not found."
            }), 404

        # 🔥 BLOCK CHECK
        if user.is_blocked:
            return jsonify({
                "message": "Your account is blocked by admin"
            }), 403

        if user.role != "user":
            return jsonify({
                "message": "User access required."
            }), 403

        return fn(*args, **kwargs)

    return wrapper