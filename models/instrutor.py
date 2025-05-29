from sqlalchemy import Column, Integer, ForeignKey, String
from models.pessoa import Pessoa

class Instrutor(Pessoa):
    __tablename__ = "instrutores"

    id = Column(Integer, ForeignKey("pessoas.id"), primary_key=True)
    _cref = Column("cref", String, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "instrutor",
    }

    def __init__(self, nome, idade, cref):
        super().__init__(nome, idade)
        self.cref = cref

    @property
    def cref(self):
        return self._cref

    @cref.setter
    def cref(self, valor):
        if not valor or len(valor.strip()) < 5:
            raise ValueError("CREF inválido, deve ter ao menos 5 caracteres.")
        self._cref = valor.strip()

    def exibir_detalhes(self):
        print(f"Instrutor: {self.nome}, Idade: {self.idade}, CREF: {self.cref}")
