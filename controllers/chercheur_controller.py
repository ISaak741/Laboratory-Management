from flask import Blueprint, jsonify, request
from models.chercheur import Chercheur
from bootstrap import db

chercheur_bp = Blueprint('chercheur', __name__)

@chercheur_bp.route('/chercheurs', methods=['GET'])
def get_chercheurs():
    chercheurs = Chercheur.query.all()
    return jsonify([{
        'id_chercheur': cher.id_chercheur,
        'nom': cher.nom,
        'prenom': cher.prenom,
        'specialite': cher.specialite,
        'email': cher.email,
        'laboratoire': cher.laboratoire.nom if cher.laboratoire else 'Aucun laboratoire assigné'
    } for cher in chercheurs])

@chercheur_bp.route('/chercheurs', methods=['POST'])
def create_chercheur():
    data = request.get_json()
    new_cher = Chercheur(
        nom=data['nom'],
        prenom=data['prenom'],
        specialite=data.get('specialite'),
        email=data['email'],
        id_lab=data.get('id_lab')
    ).save()

    return jsonify({'message': 'Chercheur created', 'id_chercheur': new_cher.id_chercheur}), 201

@chercheur_bp.route('/chercheurs/<int:id_chercheur>', methods=['GET'])
def get_chercheur(id_chercheur):
    cher = Chercheur.query.get_or_404(id_chercheur)
    return jsonify({
        'id_chercheur': cher.id_chercheur,
        'nom': cher.nom,
        'prenom': cher.prenom,
        'specialite': cher.specialite,
        'email': cher.email,
        'laboratoire': cher.laboratoire.nom if cher.laboratoire else 'Aucun laboratoire assigné',
        'experiences': [
            {'id': exp.id, 'titre': exp.titre, 'nb_mesures': len(exp.mesure) } for exp in cher.experiences
        ]
    })

@chercheur_bp.route('/chercheurs/<int:id_chercheur>', methods=['PUT'])
def update_chercheur(id_chercheur):
    cher = Chercheur.query.get_or_404(id_chercheur)
    data = request.get_json()

    cher.nom = data.get('nom', cher.nom)
    cher.prenom = data.get('prenom', cher.prenom)
    cher.specialite = data.get('specialite', cher.specialite)
    cher.email = data.get('email', cher.email)
    cher.id_lab = data.get('id_lab', cher.id_lab)

    cher.save()

    return jsonify({'message': 'Chercheur updated'})

@chercheur_bp.route('/chercheurs/<int:id_chercheur>', methods=['DELETE'])
def delete_chercheur(id_chercheur):
    cher = Chercheur.query.get_or_404(id_chercheur)
    cher.delete()
    return jsonify({'message': 'Chercheur deleted'})
