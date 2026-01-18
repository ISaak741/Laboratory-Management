from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from bootstrap import db

class Laboratoire(db.Model):
    __tablename__ = 'laboratoires' 

    id_lab: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    adresse: Mapped[str] = mapped_column(String(255), nullable=False)
    domaine: Mapped[str] = mapped_column(String(100), nullable=False)
    university: Mapped[str] = mapped_column(String(150), nullable=False)

    directeur_id: Mapped[int] = mapped_column(ForeignKey("chercheurs.id_chercheur"), nullable=False)

    # setting up relationship with Chercheur for easy access to the director details
    directeur: Mapped["Chercheur"] = relationship(
        "Chercheur", 
        back_populates="laboratoire_dirige",
        foreign_keys=[directeur_id]
    )
    
    # setting up a hasmany relationship with Chercheur
    chercheurs: Mapped[list["Chercheur"]] = relationship(
        "Chercheur", 
        back_populates="membership",
        foreign_keys="[Chercheur.id_lab]"
    )

    def __repr__(self):
        return f'<Laboratoire {self.nom}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self