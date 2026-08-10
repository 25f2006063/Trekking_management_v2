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
    bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()

    recent = []
    for b in bookings:
        recent.append({
            "id": b.id,
            "user": b.user.name if b.user else "N/A",
            "trek": b.trek.title if b.trek else "N/A",
            "date": b.booking_date.strftime("%Y-%m-%d"),
            "status": b.status
        })

    return jsonify({
        "stats": {
            "Users": User.query.filter_by(role="user").count(),
            "Staff": User.query.filter_by(role="staff").count(),
            "Treks": Trek.query.count(),
            "Bookings": Booking.query.count()
        },
        "recent_bookings": recent
    }), 200

# ---------------- CREATE TREK ----------------
@admin_bp.route("/treks", methods=["POST"])
@jwt_required()
@admin_required
def create_trek():
    data = request.get_json()

    # Validate request
    if not data:
        return jsonify({"message": "No data received"}), 400

    #  Required fields check
    required_fields = [
        "title", "location", "description",
        "difficulty", "price", "duration",
        "total_slots", "start_date", "end_date"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    # Validate difficulty
    if data["difficulty"] not in DIFFICULTY_LEVELS:
        return jsonify({"message": "Invalid difficulty"}), 400

    try:
        #  Convert types properly
        price = int(data["price"])
        duration = int(data["duration"])
        total_slots = int(data["total_slots"])

        # Convert date format (YYYY-MM-DD expected)
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

        #  Date validation
        if end_date < start_date:
            return jsonify({"message": "End date must be after start date"}), 400

        #  Create Trek
        trek = Trek(
            title=data["title"],
            location=data["location"],
            description=data["description"],
            difficulty=data["difficulty"],
            price=price,
            duration=duration,
            total_slots=total_slots,
            available_slots=total_slots,
            start_date=start_date,
            end_date=end_date,

            assigned_staff_id=None   
        )

        db.session.add(trek)
        db.session.commit()

        return jsonify({
            "message": "Trek created successfully",
            "trek": trek.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"message": "Invalid number or date format"}), 400

    except Exception as e:
        print(" SERVER ERROR:", e)   # Debug in terminal
        return jsonify({"message": "Internal server error"}), 500


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
        phone=data.get("phone"),
        password=hashed,
        role="staff"
        
        # status=data.get("status", "active")
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({"message": "Staff created"}), 201  

# ---------------- GET STAFF ----------------
@admin_bp.route("/staff", methods=["GET"])
@jwt_required()
@admin_required
def get_staff():
    staff_users = User.query.filter_by(role="staff").all()

    result = []

    for s in staff_users:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "phone": s.phone,
            "is_blocked": s.is_blocked,
            "status": "blacklisted" if s.is_blocked else "active"
        })

    return jsonify(result), 200

# ---------------- TOGGLE STAFF STATUS ----------------
@admin_bp.route("/staff/<int:staff_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def toggle_staff_status(staff_id):
    staff = db.session.get(User, staff_id)

    if not staff or staff.role != "staff":
        return jsonify({"message": "Staff not found"}), 404

    # 🔥 toggle
    staff.is_blocked = not staff.is_blocked

    # 🔥 IF BLOCKED → REMOVE FROM TREKS
    if staff.is_blocked:
        treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()

        for t in treks:
            t.assigned_staff_id = None
            t.status = "Pending"   # 🔥 important

    db.session.commit()

    return jsonify({
        "message": "Status updated",
        "is_blocked": staff.is_blocked
    }), 200 


# ---------------- ASSIGN STAFF ----------------#
@admin_bp.route("/assign-staff/<int:trek_id>", methods=["PUT"])
@jwt_required()
@admin_required
def assign_staff(trek_id):
    data = request.get_json()
    staff_id = data.get("staff_id")

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    staff = User.query.get(staff_id)

    if not staff or staff.role != "staff":
        return jsonify({"message": "Invalid staff"}), 400


    if staff.is_blocked:
        return jsonify({"message": "Staff is blacklisted"}), 400

    
    conflicting_trek = Trek.query.filter(
        Trek.assigned_staff_id == staff_id,
        Trek.id != trek_id,
        Trek.start_date <= trek.end_date,
        Trek.end_date >= trek.start_date
    ).first()

    if conflicting_trek:
        return jsonify({
            "message": "Staff already assigned to another trek in this time period"
        }), 400

   
    trek.assigned_staff_id = staff_id
    trek.status = "Open"   # or "Assigned"
    db.session.commit()

    return jsonify({"message": "Staff assigned successfully"}), 200

# ---------------- Delete trek ----------------
@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if not trek:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(trek)
    db.session.commit()

    return jsonify({"message": "Deleted"}), 200  

# ---------------- user/admin ----------------
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_users():
    users = User.query.filter_by(role="user").all()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "is_blocked": u.is_blocked,
            "status": "Blacklisted" if u.is_blocked else "Active"
        })

    return jsonify(result), 200  

# ---------------- USER-blacklist/whitelist ----------------
@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def toggle_user_status(user_id):
    user = db.session.get(User, user_id)

    if not user or user.role != "user":
        return jsonify({"message": "User not found"}), 404

    user.is_blocked = not user.is_blocked

    db.session.commit()

    return jsonify({
        "message": "Status updated",
        "is_blocked": user.is_blocked
    }), 200  

# ---------------- GET ALL BOOKINGS (ADMIN) ----------------

@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def get_all_bookings():
    bookings = Booking.query.all()

    result = []

    for b in bookings:
        result.append({
            "id": b.id,
            "user": b.user.name if b.user else "N/A",
            "trek": b.trek.title if b.trek else "N/A",
            "date": b.booking_date.strftime("%Y-%m-%d"),
            "status": b.status
        })

    return jsonify(result), 200