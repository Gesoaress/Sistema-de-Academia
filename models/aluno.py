from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.pessoa import Pessoa


class Aluno(Pessoa):
    __tablename__ = "alunos"

    id = Column(Integer, ForeignKey("pessoas.id"), primary_key=True)
    _matricula = Column("matricula", Integer, unique=True)

    matriculas = relationship("Matricula", back_populates="aluno")  # relação 1:N

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }

    def __init__(self, nome, idade, matricula):
        super().__init__(nome, idade)
        self.matricula = matricula

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Matrícula deve ser um inteiro positivo.")
        self._matricula = valor

    def exibir_detalhes(self):
        if self.matriculas:
            nomes_modalidades = sorted([m.modalidade.nome for m in self.matriculas])
            modalidades_str = " | ".join(nomes_modalidades)
        else:
            modalidades_str = "Nenhuma modalidade cadastrada"
        print(f"Aluno: {self.nome}, Idade: {self.idade}, Matrícula: {self.matricula}, Modalidades: {modalidades_str}")
