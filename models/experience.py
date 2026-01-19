from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from bootstrap import db
# from models.experience_chercheur import ExperienceChercheur

class Experience(db.Model):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key = True)
    titre: Mapped[str] = mapped_column(String)
    descritption: Mapped[str] = mapped_column(String)

    experience_link: Mapped["ExperienceChercheur"] = relationship(
        "ExperienceChercheur",
        back_populates="experience",
    )
    mesure: Mapped[list["Mesure"]] = relationship(
        "Mesure",
        back_populates="experience",
    )
    
    def __repr__(self):
        return f'<experience {self.nom}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self