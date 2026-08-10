from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.auth import user_required
from extensions import db
from models import Trek, Booking

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


# ---------------- VIEW ALL TREKS ----------------
@user_bp.route("/treks", methods=["GET"])
@jwt_required()
@user_required
def get_all_treks():
    treks = Trek.query.all()
    return jsonify([t.to_dict() for t in treks]), 200


# ---------------- BOOK TREK ----------------
@user_bp.route("/bookings", methods=["POST"])
@jwt_required()
@user_required
def book_trek():
    user_id = get_jwt_identity()
    data = request.get_json()

    trek_id = data.get("trek_id")
    trek = db.session.get(Trek, trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    # ❌ Already booked
    existing = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id
    ).first()

    if existing:
        return jsonify({"message": "Already booked"}), 400

    # ❌ SLOT CHECK
    booked_count = Booking.query.filter_by(trek_id=trek_id).count()
    if booked_count >= trek.total_slots:
        return jsonify({"message": "No slots available"}), 400

    # 🔥 DATE COLLISION CHECK
    user_bookings = Booking.query.filter_by(user_id=user_id).all()

    for b in user_bookings:
        existing_trek = db.session.get(Trek, b.trek_id)

        if not (
            trek.end_date < existing_trek.start_date or
            trek.start_date > existing_trek.end_date
        ):
            return jsonify({
                "message": "You already have a trek in this date range"
            }), 400

    # ✅ CREATE BOOKING
    booking = Booking(user_id=user_id, trek_id=trek_id)

    db.session.add(booking)

    # update slots
    trek.available_slots = trek.total_slots - (booked_count + 1)

    db.session.commit()

    return jsonify({"message": "Trek booked successfully"}), 201


# ---------------- MY BOOKINGS ----------------
@user_bp.route("/bookings", methods=["GET"])
@jwt_required()
@user_required
def my_bookings():
    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id).all()

    result = []

    for b in bookings:
        trek = db.session.get(Trek, b.trek_id)

        result.append({
            "id": b.id,
            "trek_id": trek.id,
            "trek_title": trek.title,
            "trek_location": trek.location,
            "start_date": trek.start_date.isoformat(),
            "end_date": trek.end_date.isoformat(),
            "status": trek.status
        })

    return jsonify(result), 200


# ---------------- CANCEL BOOKING ----------------
@user_bp.route("/bookings/<int:trek_id>", methods=["DELETE"])
@jwt_required()
@user_required
def cancel_booking(trek_id):
    user_id = get_jwt_identity()

    booking = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id
    ).first()

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    trek = db.session.get(Trek, trek_id)

    db.session.delete(booking)

    # update slots after cancel
    booked_count = Booking.query.filter_by(trek_id=trek_id).count()
    trek.available_slots = trek.total_slots - booked_count

    db.session.commit()

    return jsonify({"message": "Booking cancelled"}), 200