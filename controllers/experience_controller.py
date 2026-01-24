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
        'description': exp.description,
        'chercheur': [
            {'id': cher.id_chercheur, 'nom': cher.nom_complet} for cher in exp.chercheurs
        ],
        'mesures': len(exp.mesure)
    } for exp in experiences])

@experience_bp.route('/experiences', methods=['POST'])
def create_experience():
    data = request.get_json()
    exp = Experience(
        titre=data['titre'],
        description=data['description'],
    ).save()

    for id in data['selected_ids']:
        ExperienceChercheur(
            id_experience = exp.id,
            id_chercheur = id
        ).save()

    return jsonify({'message': 'experience created', 'id_experience': exp.id}), 201

@experience_bp.route('/experiences/<int:id_experience>', methods=['GET'])
def get_experience(id_experience):
    exp = Experience.query.get_or_404(id_experience)
    return jsonify({
        'id': exp.id,
        'titre': exp.titre,
        'description': exp.description,
        'chercheurs': [
            {'id': cher.id_chercheur, 'nom': cher.nom_complet} for cher in exp.chercheurs
        ]
    })

@experience_bp.route('/experiences/<int:id_experience>', methods=['PUT'])
def update_experience(id_experience):

    experience = Experience.query.get_or_404(id_experience)
    data = request.get_json()

    experience.titre = data.get('titre', experience.titre)
    experience.description = data.get('description', experience.description)

    if "selected_ids" in data:
        new_ids = set(data["selected_ids"])

        current_links = experience.experience_chercheurs
        current_ids = {link.id_chercheur for link in current_links}

        for link in current_links:
            if link.id_chercheur not in new_ids:
                db.session.delete(link)

        ids_to_add = new_ids - current_ids
        for cher_id in ids_to_add:
            db.session.add(
                ExperienceChercheur(
                    id_experience=experience.id,
                    id_chercheur=cher_id
                )
            )

    db.session.commit()

    return jsonify({'message': 'Experience updated successfully'})


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

@experience_bp.route('/mesures', methods=['GET'])
def get_mesures():
    mesures = Mesure.query.all()

    return jsonify([{
        'id': m.id,
        'valeur': m.valeur,
        'unite': m.unite,
        'horodatage': m.horodatage.isoformat() if m.horodatage else None,
        'type_parametre': m.type_parametre,
        'id_experience': m.id_experience,
        # Access the related experience object to get the title
        'experience_titre': m.experience.titre if m.experience else "N/A"
    } for m in mesures]), 200

@experience_bp.route('/mesures/<int:id_mesure>', methods=['DELETE'])
def delete_mesure(id_mesure):
    mesure = Mesure.query.get_or_404(id_mesure)
    mesure.delete()
    return jsonify({'message': 'Mesure supprimée avec succès'}), 200
