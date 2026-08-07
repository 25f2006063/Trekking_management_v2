from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from decorators.auth import admin_required
from extensions import db, bcrypt
from models import User, Trek, Booking
from constants import DIFFICULTY_LEVELS

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# ---------------- DASHBOARD ----------------
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
def dashboard():
    return jsonify({
        "users": User.query.filter_by(role="user").count(),
        "staff": User.query.filter_by(role="staff").count(),
        "treks": Trek.query.count(),
        "bookings": Booking.query.count()
    }), 200


# ---------------- CREATE TREK ----------------
@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
@admin_required
def create_trek():
    data = request.get_json()

    difficulty = data.get("difficulty")

    if difficulty not in DIFFICULTY_LEVELS:
        return jsonify({"message": "Invalid difficulty"}), 400

    try:
        start = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except:
        return jsonify({"message": "Invalid date"}), 400

    trek = Trek(
        title=data.get("title"),
        location=data.get("location"),
        description=data.get("description"),
        difficulty=difficulty,
        price=data.get("price"),
        duration=data.get("duration"),
        total_slots=data.get("total_slots"),
        available_slots=data.get("total_slots"),
        start_date=start,
        end_date=end
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created",
        "trek": trek.to_dict()
    }), 201


# ---------------- GET TREKS ----------------
@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
@admin_required
def get_treks():
    treks = Trek.query.all()
    return jsonify([t.to_dict() for t in treks]), 200


# ---------------- UPDATE TREK ----------------
@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if not trek:
        return jsonify({"message": "Not found"}), 404

    data = request.get_json()

    booked = Booking.query.filter_by(trek_id=trek_id).count()

    if "total_slots" in data:
        new_total = data["total_slots"]

        if new_total < booked:
            return jsonify({"message": "Cannot reduce below booked"}), 400

        trek.total_slots = new_total
        trek.available_slots = new_total - booked

    db.session.commit()

    return jsonify({
        "message": "Updated",
        "trek": trek.to_dict()
    }), 200


# ---------------- CREATE STAFF ----------------
@admin_bp.route("/staff", methods=["POST"])
@jwt_required()
@admin_required
def create_staff():
    data = request.get_json()

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "All fields required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email exists"}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    staff = User(
        name=data["name"],
        email=data["email"],
        password=hashed,
        role="staff"
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({"message": "Staff created"}), 201


# ---------------- ASSIGN STAFF ----------------
@admin_bp.route("/treks/<int:trek_id>/assign-staff", methods=["PUT"])
@jwt_required()
@admin_required
def assign_staff(trek_id):
    data = request.get_json()

    staff_id = data.get("staff_id")

    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    staff = db.session.get(User, staff_id)
    if not staff or staff.role != "staff":
        return jsonify({"message": "Invalid staff"}), 400

    trek.assigned_staff_id = staff_id

    db.session.commit()

    return jsonify({"message": "Staff assigned"}), 200