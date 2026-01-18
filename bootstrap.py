import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Models Loading and Blueprints Registration
    # from models.post import Post
    # from controllers.post_controller import post_bp
    # app.register_blueprint(post_bp)
    from controllers.home_controller import home_bp
    app.register_blueprint(home_bp)

    return app