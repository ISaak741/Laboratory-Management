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
    
    # including Laboratoire Model for Migration and it's Controller
    from models.laboratoire import Laboratoire
    from controllers.laboratoire_controller import laboratoire_bp
    app.register_blueprint(laboratoire_bp)
    
    from models.chercheur import Chercheur
    from controllers.chercheur_controller import chercheur_bp
    app.register_blueprint(chercheur_bp)

    from models.experience import Experience
    from models.mesure import Mesure
    from models.experience_chercheur import ExperienceChercheur
    from controllers.experience_controller import experience_bp,experiencechercheur_bp,mesure_bp
    # from controllers.chercheur_controller import experiencechercheur_bp
    app.register_blueprint(experience_bp)
    app.register_blueprint(experiencechercheur_bp)
    app.register_blueprint(mesure_bp)

    
    from controllers.home_controller import home_bp
    app.register_blueprint(home_bp)

    return app