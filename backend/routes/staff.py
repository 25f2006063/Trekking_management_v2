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

    treks = Trek.query.filter_by(assigned_staff_id=user_id).all()

    result = [t.to_dict() for t in treks]

    return jsonify(result), 200



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

    return jsonify([b.to_dict() for b in bookings]), 200

# ---------------- TREK STATUS ----------------
@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
@staff_required
def update_status(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Not found"}), 404

    data = request.get_json()

    trek.status = data.get("status")   # ✅ dynamic

    db.session.commit()

    return jsonify({"message": "Updated"}), 200


@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@staff_required
def staff_dashboard():
    user_id = get_jwt_identity()

    treks = Trek.query.filter_by(assigned_staff_id=user_id).all()

    total_treks = len(treks)

    ongoing = len([t for t in treks if t.status.lower() == "ongoing"])

    total_participants = sum(
        Booking.query.filter_by(trek_id=t.id).count() for t in treks
    )

    return jsonify({
        "assigned_treks": total_treks,
        "ongoing_treks": ongoing,
        "total_participants": total_participants
    }), 200