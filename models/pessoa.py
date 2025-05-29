from sqlalchemy import Column, Integer, String
from models.base import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True)
    _nome = Column("nome", String)
    _idade = Column("idade", Integer)
    tipo = Column(String)

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "pessoa",
    }

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or len(valor) < 3:
            raise ValueError("Nome deve ter ao menos 3 caracteres.")
        self._nome = valor.strip()

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("Idade deve ser inteiro positivo.")
        self._idade = valor

    def exibir_detalhes(self):
        print(f"Pessoa: {self.nome}, Idade: {self.idade}")
