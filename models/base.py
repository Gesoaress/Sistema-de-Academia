import logging

# Remove handlers antigos e configura do zero
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.WARNING)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta
from abc import ABCMeta

# Metaclass para resolver conflito entre SQLAlchemy e ABC (abstração)
class BaseMeta(DeclarativeMeta, ABCMeta):
    pass

# Base declarativa usando a metaclass personalizada
Base = declarative_base(metaclass=BaseMeta)

# Criação do engine SQLite (arquivo academia.db no mesmo diretório)
engine = create_engine("sqlite:///academia.db", echo=True)

# Criação da sessão para operar no banco
Session = sessionmaker(bind=engine)


