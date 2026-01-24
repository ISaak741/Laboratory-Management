from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from bootstrap import db

class ExperienceChercheur(db.Model):
    __tablename__ = "experience_chercheur"

    id: Mapped[int] = mapped_column(primary_key=True)

    id_experience: Mapped[int] = mapped_column(
        ForeignKey("experience.id"), nullable=False
    )

    id_chercheur: Mapped[int] = mapped_column(
        ForeignKey("chercheurs.id_chercheur"), nullable=False
    )

    experience: Mapped["Experience"] = relationship(
        "Experience",
        back_populates="experience_chercheurs",
        foreign_keys=[id_experience]
    )

    chercheur: Mapped["Chercheur"] = relationship(
        "Chercheur",
        back_populates="experience_chercheurs",
        foreign_keys=[id_chercheur]
    )

    # def __repr__(self):
    #     return f'<Laboratoire {self.nom}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
