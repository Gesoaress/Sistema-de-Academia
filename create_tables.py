from models.base import Base, engine
from models.pessoa import Pessoa
from models.aluno import Aluno
from models.instrutor import Instrutor
from models.modalidade import Modalidade


Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso.")
