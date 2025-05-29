from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    modalidade_id = Column(Integer, ForeignKey("modalidades.id"), nullable=False)

    aluno = relationship("Aluno", back_populates="matriculas")
    modalidade = relationship("Modalidade", back_populates="matriculas")

    def __init__(self, aluno, modalidade):
        if aluno is None or modalidade is None:
            raise ValueError("Aluno e Modalidade não podem ser None")
        self.aluno = aluno
        self.modalidade = modalidade

    def exibir_detalhes(self):
        print(f"Aluno: {self.aluno.nome} matriculado em: {self.modalidade.nome}")
