from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app= Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.neighbors import Neighbor
    from app.models.boards import Board
    from app.models.comments import Comment

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Register Blueprints here
    from .routes.neighbors_routes import neighbor_bp
    app.register_blueprint(neighbor_bp)
    from .routes.board_routes import board_bp
    app.register_blueprint(board_bp)
    from .routes.comment_routes import comment_bp
    app.register_blueprint(comment_bp)
    
    
    CORS(app)
    return app