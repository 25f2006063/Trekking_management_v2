from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from extensions import db, bcrypt, jwt

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.staff import staff_bp

from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ FIX CORS
    CORS(app, supports_credentials=True)

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)

    # create tables + default admin
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(email="admin@trek.com").first()

        if not admin:
            hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")

            admin = User(
                name="Administrator",
                email="admin@trek.com",
                password=hashed_password,
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()
            print("Default admin created")

    @app.route("/")
    def home():
        return jsonify({"message": "Trekking Management API Running"})

    return app   


# create app
app = create_app()


# run server
if __name__ == "__main__":
    app.run(debug=True)