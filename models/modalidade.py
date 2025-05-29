from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Modalidade(Base):
    __tablename__ = "modalidades"

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)  # nome obrigatório e único
    descricao = Column(String, nullable=True)  # descrição opcional

    matriculas = relationship("Matricula", back_populates="modalidade", cascade="all, delete-orphan")
    # Cascade para remover matrículas quando modalidade for removida, se desejado

    def __init__(self, nome, descricao=""):
        self.nome = nome
        self.descricao = descricao

    def exibir_detalhes(self):
        print(f"Modalidade: {self.nome}, Descrição: {self.descricao if self.descricao else 'Sem descrição'}")
