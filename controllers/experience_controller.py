from flask import Blueprint, jsonify, request
from models.experience import Experience
from models.mesure import Mesure
from models.experience_chercheur import ExperienceChercheur
from bootstrap import db
from datetime import datetime

experience_bp = Blueprint('experience', __name__)
experiencechercheur_bp = Blueprint('experiencechercheur', __name__)
mesure_bp = Blueprint('mesure', __name__)

@experience_bp.route('/experiences', methods=['GET'])
def get_experiences():
    experiences = Experience.query.all()
        
    return jsonify([{
        'id': exp.id,
        'titre': exp.titre,
        'descritption': exp.descritption,
        'chercheur': exp.experience_link.chercheur.nom,
        'mesure' :[
            {
        "valeur": mesure.valeur,
        "unite": mesure.unite,
        "horodatage": mesure.horodatage,
        "type_parametre": mesure.type_parametre,
        "id_experience": mesure.id_experience
        }
        for mesure in exp.mesure]
    } for exp in experiences])

@experience_bp.route('/experiences', methods=['POST'])
def create_experience():
    data = request.get_json()
    new_cher = Experience(
        titre=data['titre'],
        descritption=data['description'],
    ).save()
    new_experiencechercheur = ExperienceChercheur(
        id_experience = new_cher.id,
        id_chercheur = data['id_chercheur']
    ).save()
    
    return jsonify({'message': 'experience created', 'id_experience': new_cher.id}), 201

@experience_bp.route('/experiences/<int:id_experience>', methods=['GET'])
def get_experience(id_experience):
    cher = Experience.query.get_or_404(id_experience)
    return jsonify({
        'id': cher.id,
        'titre': cher.titre,
        'descritption': cher.descritption,
        'chercheur': cher.experience_link.chercheur.nom,
    })

@experience_bp.route('/experiences/<int:id_experience>', methods=['PUT'])
def update_experience(id_experience):
    cher = Experience.query.get_or_404(id_experience)
    data = request.get_json()
    
    cher.titre = data.get('titre', cher.titre)
    cher.descritption = data.get('descritption', cher.descritption)
    cher.save()
    
    return jsonify({'message': 'experience updated'})

@experience_bp.route('/experiences/<int:id_experience>', methods=['DELETE'])
def delete_experience(id_experience):
    cher = Experience.query.get_or_404(id_experience)
    cher.delete()
    return jsonify({'message': 'Chercheur deleted'})


@experience_bp.route('/mesures', methods=['POST'])
def add_mesure_to_experiecne():
    data = request.get_json()
    horodatage = datetime.fromisoformat(data['horodatage'])
    new_mesure = Mesure(
        valeur=data['valeur'],
        unite=data['unite'],
        horodatage=horodatage,
        type_parametre=data['type_parametre'],
        id_experience=data['id_experience'],
    ).save()
    
    return jsonify({'message': 'mesure add ro experience'}), 201