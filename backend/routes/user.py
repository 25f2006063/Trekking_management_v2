from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Trek, Booking

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


# ---------------- VIEW ALL TREKS ----------------
@user_bp.route("/treks", methods=["GET"])
@jwt_required()
def get_all_treks():
    treks = Trek.query.all()

    return jsonify([
        t.to_dict() for t in treks
    ]), 200


# ---------------- BOOK TREK ----------------
@user_bp.route("/book/<int:trek_id>", methods=["POST"])
@jwt_required()
def book_trek(trek_id):
    user_id = get_jwt_identity()

    trek = db.session.get(Trek, trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    # Already booked check
    existing = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id
    ).first()

    if existing:
        return jsonify({"message": "Already booked"}), 400

    # Slot check
    booked_count = Booking.query.filter_by(trek_id=trek_id).count()

    if booked_count >= trek.total_slots:
        return jsonify({"message": "No slots available"}), 400

    booking = Booking(
        user_id=user_id,
        trek_id=trek_id
    )

    trek.available_slots = trek.total_slots - (booked_count + 1)

    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Trek booked successfully"}), 201


# ---------------- MY BOOKINGS ----------------
@user_bp.route("/my-bookings", methods=["GET"])
@jwt_required()
def my_bookings():
    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "booking_id": b.id,
            "trek_id": b.trek_id
        }
        for b in bookings
    ]), 200


# ---------------- CANCEL BOOKING ----------------
@user_bp.route("/cancel/<int:trek_id>", methods=["DELETE"])
@jwt_required()
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

    # Update slots after deletion
    booked_count = Booking.query.filter_by(trek_id=trek_id).count()
    trek.available_slots = trek.total_slots - booked_count

    db.session.commit()

    return jsonify({"message": "Booking cancelled"}), 200