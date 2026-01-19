# from flask import Flask,request,url_for
# from markupsafe import escape
from .models import chercheur,laboratoire,Base
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

# Base.metadata.create_all(engine)
# app = Flask(__name__)

@app.route('/')
def index():
    return 'index'
@app.route('/add_lab/<int:id>/<string:nom>/<string:adresse>/<string:domaine>/<string:directeur>/<string:university>',methods=['GET'])
def add_lab(id, nom, adresse, domaine, directeur, university):
    db = SessionLocal()
    labo = laboratoire(
        nom = nom,
        adresse = adresse,
        domaine = domaine,
        directeur = directeur,
        university = university,
    )
    db.add(labo)
    db.commit()
    db.close()
    return f"{id}: {nom} {adresse} - {domaine} - {directeur} - {university}"
@app.route('/view_lab/<int:id>',methods=['GET'])
def view_lab(id):
    db = SessionLocal()
    item = db.get(laboratoire,id)
    # db.commit()
    db.close()
    return f"{id}: {item.nom} {item.adresse} - {item.domaine} - {item.directeur} - {item.university}"
@app.route('/add_chercheur/<int:id>/<string:nom>/<string:prenom>/<string:specialite>/<string:email>/<int:lab>',methods=['GET'])
def add_chercheur(id, nom, prenom, specialite, email, lab):
    db = SessionLocal()
    cherch = chercheur(
        nom = nom,
        prenom = prenom,
        specialite = specialite,
        email = email,
        id_lab = lab,
    )
    db.add(cherch)
    db.commit()
    db.close()
    return f"{id}: {nom} {prenom} - {specialite} - {email} - {lab}"



