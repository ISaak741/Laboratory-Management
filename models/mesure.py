from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey,Float,DateTime
from bootstrap import db


class Mesure(db.Model):
    __tablename__ = "mesure"

    id: Mapped[int] = mapped_column(primary_key = True)
    valeur: Mapped[float] = mapped_column(Float)
    unite: Mapped[str] = mapped_column(String)
    horodatage: Mapped[DateTime] = mapped_column(DateTime)
    type_parametre: Mapped[str] = mapped_column(String)
    id_experience: Mapped[int] = mapped_column(ForeignKey("experience.id"), nullable=False)

    experience: Mapped["Experience"] = relationship(
        "Experience",
        back_populates="mesure",
        foreign_keys=[id_experience]
    )

    def __repr__(self):
        return f'<Mesure {self.nom}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
