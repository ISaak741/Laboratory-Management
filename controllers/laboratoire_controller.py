from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from models.chercheur import Chercheur
from models.laboratoire import Laboratoire

laboratoire_bp = Blueprint('laboratoire', __name__)

@laboratoire_bp.route('/laboratoires', methods=['GET'])
def get_laboratoires():
    laboratoires = Laboratoire.query.all()
    return jsonify([{
        'id_lab': lab.id_lab,
        'nom': lab.nom,
        'adresse': lab.adresse,
        'domaine': lab.domaine,
        'university': lab.university,
        'directeur': lab.directeur.nom if lab.directeur else 'Non Directeur pour le moment'
    } for lab in laboratoires])

@laboratoire_bp.route('/laboratoires', methods=['POST'])
def create_laboratoire():
    data = request.get_json()
    if not data or 'directeur_id' not in data or data['directeur_id'] is None:
        return jsonify({
            "error": "Bad Request",
            "message": "A laboratory must have a director. Please provide a valid 'directeur_id'."
        }), 400

    try:
        new_lab = Laboratoire(
            nom=data.get('nom'),
            adresse=data.get('adresse'),
            domaine=data.get('domaine'),
            university=data.get('university'),
            directeur_id=data.get('directeur_id')
        )
        new_lab.save()
        
        chercheur_directeur = Chercheur.query.get(new_lab.directeur_id)
        if chercheur_directeur:
            chercheur_directeur.id_lab = new_lab.id_lab
            chercheur_directeur.save()
            

        return jsonify({"message": "Laboratoire created successfully", "id": new_lab.id_lab}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Conflict",
            "message": "The provided 'directeur_id' does not exist in the researchers table."
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Server Error", "message": str(e)}), 500

@laboratoire_bp.route('/laboratoires/<int:id_lab>', methods=['GET'])
def get_laboratoire(id_lab):
    lab = Laboratoire.query.options(joinedload(Laboratoire.chercheurs)).get_or_404(id_lab)
    
    membres = [{
        "id_chercheur": cher.id_chercheur,
        "nom": cher.nom,
        "prenom": cher.prenom,
        "specialite": cher.specialite,
        "email": cher.email
    } for cher in lab.chercheurs]
    
    return jsonify({
        'id_lab': lab.id_lab,
        'nom': lab.nom,
        'adresse': lab.adresse,
        'domaine': lab.domaine,
        'university': lab.university,
        'directeur': lab.directeur.nom if lab.directeur else 'Non Directeur pour le moment',
        'liste_chercheurs': membres
    })
    
@laboratoire_bp.route('/laboratoires/<int:id_lab>', methods=['PUT'])
def update_laboratoire(id_lab):
    lab = Laboratoire.query.get_or_404(id_lab)
    data = request.get_json()

    lab.nom = data.get('nom', lab.nom)
    lab.adresse = data.get('adresse', lab.adresse)
    lab.domaine = data.get('domaine', lab.domaine)
    lab.university = data.get('university', lab.university)
    lab.directeur_id = data.get('directeur_id', lab.directeur_id)
    
    lab.save()
    
    return jsonify({'message': 'Laboratoire updated'})

@laboratoire_bp.route('/laboratoires/<int:id_lab>', methods=['DELETE'])
def delete_laboratoire(id_lab):
    lab = Laboratoire.query.get_or_404(id_lab)
    
    try:
        for chercheur in lab.chercheurs:
            chercheur.id_lab = None
        
        lab.delete()
        return jsonify({"message": f"Laboratoire {id_lab} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500