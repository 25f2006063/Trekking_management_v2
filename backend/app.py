from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, bcrypt, jwt 

from models import User, Trek, Booking


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(email="admin@trek.com").first()

        if not admin:
            hashed_password = bcrypt.generate_password_hash(
                "admin123"
            ).decode("utf-8")

            admin = User(
                name="Administrator",
                email="admin@trek.com",
                password=hashed_password,
                phone="9999999999",
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

            print("Default admin created")

    @app.route("/")
    def home():
        return jsonify({
            "message": "Trekking Management API Running"
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)