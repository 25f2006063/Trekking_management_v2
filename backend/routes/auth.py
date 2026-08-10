from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from extensions import db, bcrypt
from models import User

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.route("/")
def test():
    return {
        "message": "Auth Blueprint Working"
    }
# ---------------- REGISTER ---------------- #
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone") 

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required."
        }), 400 
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered."
        }), 409 

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8") 

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        phone=phone,
        role="user"
    ) 

    db.session.add(user)
    db.session.commit() 

    return jsonify({
        "message": "User registered successfully."
    }), 201 

# ---------------- LOGIN ---------------- #
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    # 🔥 ADD THIS BLOCK CHECK
    if user.is_blocked:
        return jsonify({
            "message": "Your account is blacklisted. Contact admin."
        }), 403

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

# ---------------- PROFILE ---------------- #
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "phone": user.phone
    })