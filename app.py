from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  
from config import Config
from models import db, User
from routes.auth import auth_bp
from routes.profile import profile_bp  
from routes.gifts import gifts_bp

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profile_bp, url_prefix="/profile")  # ✅ Register profile blueprint
    app.register_blueprint(gifts_bp, url_prefix='/gifts')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

app = create_app()

@app.route("/")
def home():
    return render_template("index.html")  

if __name__ == "__main__":
    app.run(debug=True)
