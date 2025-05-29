from .base import Base, engine, Session
from .pessoa import Pessoa
from .aluno import Aluno
from .instrutor import Instrutor
from .modalidade import Modalidade
from .matricula import Matricula

Base.metadata.create_all(engine)
