from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from decorators.auth import staff_required
from models import Trek, Booking 
from extensions import db, bcrypt, jwt

staff_bp = Blueprint("staff", __name__, url_prefix="/api/staff")


# ---------------- VIEW ASSIGNED TREKS ----------------
@staff_bp.route("/treks", methods=["GET"])
@jwt_required()
@staff_required
def get_assigned_treks():

    user_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(assigned_staff_id=user_id).all()

    result = []

    for t in treks:
        participants = Booking.query.filter_by(trek_id=t.id).count()
    result.append({
        "id": t.id,
        "title": t.title,
        "location": t.location,   # ✅ ADD THIS
        "start_date": t.start_date.isoformat(),
        "end_date": t.end_date.isoformat(),
        "participants": participants,
        "available_slots": t.available_slots,
        "total_slots": t.total_slots,
        "status": t.status
    })

    return jsonify({"treks": result}), 200

# ---------------- VIEW BOOKINGS FOR TREK ----------------
@staff_bp.route("/treks/<int:trek_id>/bookings", methods=["GET"])
@jwt_required()
@staff_required
def get_trek_bookings(trek_id):

    user_id = int(get_jwt_identity())
    trek = Trek.query.get(trek_id)

    if not trek or trek.assigned_staff_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id).all()

    result = []

    for b in bookings:
        result.append({
            "id": b.id,
            "name": b.user.name if b.user else "N/A",
            "email": b.user.email if b.user else "N/A"
        })

    return jsonify({
        "bookings": result,
        "status": trek.status
    }), 200

# ---------------- TREK STATUS ----------------
@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
@staff_required
def update_status(trek_id):

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Not found"}), 404

    data = request.get_json()
    trek.status = data.get("status")

    db.session.commit()

    return jsonify({"message": "Updated"}), 200


@staff_bp.route("/dashboard")
@jwt_required()
def staff_dashboard():

    staff_id = int(get_jwt_identity())

    treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()

    data = []
    total_participants = 0
    ongoing = 0

    for t in treks:
        participants = Booking.query.filter_by(trek_id=t.id).count()
        total_participants += participants

        if t.status == "approved":
            ongoing += 1

        data.append({
            "id": t.id,
            "title": t.title,
            "start_date": t.start_date.isoformat(),
            "end_date": t.end_date.isoformat(),
            "status": t.status,
            "available_slots": t.available_slots,
            "total_slots": t.total_slots,
            "participants": participants
        })

    return jsonify({
        "treks": data,
        "stats": {
            "assigned_treks": len(data),
            "total_participants": total_participants,
            "ongoing_treks": ongoing
        }
    })