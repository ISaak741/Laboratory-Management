from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from bootstrap import db

class Chercheur(db.Model):
    __tablename__ = 'chercheurs'

    id_chercheur: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    specialite: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)


    id_lab: Mapped[int] = mapped_column(ForeignKey("laboratoires.id_lab"), nullable=True)
    membership : Mapped["Laboratoire"] = relationship(
        "Laboratoire", 
        back_populates="chercheurs",
        foreign_keys=[id_lab]
    )

    laboratoire_dirige: Mapped["Laboratoire"] = relationship(
        "Laboratoire", 
        back_populates="directeur",
        foreign_keys="[Laboratoire.directeur_id]"
    )
    
    @property
    def laboratoire(self):
        return self.laboratoire_dirige or self.membership

    def __repr__(self):
        return f'<Chercheur {self.nom} {self.prenom}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self