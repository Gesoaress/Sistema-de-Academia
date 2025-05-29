# -*- coding: utf-8 -*-
"""Definição dos Modelos SQLAlchemy para o Sistema de Gestão de Ginásio."""

import datetime
from abc import ABC, abstractmethod

from sqlalchemy import (Column, Integer, String, Date, DateTime, ForeignKey,
                    create_engine, event)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, validates
from sqlalchemy.ext.hybrid import hybrid_property

# Base declarativa para os modelos SQLAlchemy
Base = declarative_base()

# --- Classe Abstrata e Herança Mapeada ---

class Pessoa(Base):
    """Classe base mapeada para representar uma Pessoa no sistema.

    Utiliza herança joined-table.
    """
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    contacto = Column(String(100))
    # Coluna para identificar o tipo de subclasse (necessário para herança mapeada)
    tipo = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': tipo
    }

    def __init__(self, nome, contacto):
        self.nome = nome
        self.contacto = contacto

    # Método abstrato (não diretamente mapeado, mas define o contrato)
    @abstractmethod
    def display_details(self):
        """Método abstrato para exibir detalhes específicos da subclasse."""
        pass

# --- Classes Concretas ---

class Membro(Pessoa):
    """Representa um Membro do ginásio, herdando de Pessoa."""
    __tablename__ = 'membros'
    # Chave primária que também é chave estrangeira para a tabela 'pessoas'
    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    data_adesao = Column(Date, default=datetime.date.today)
    tipo_subscricao = Column(String(50))
    _estado_pagamento = Column("estado_pagamento", String(20), default='Pendente') # Mapeia para coluna 'estado_pagamento'

    # Relacionamento com Reservas (um membro pode ter várias reservas)
    reservas = relationship("Reserva", back_populates="membro")

    # Atributo de classe (não persistido diretamente no ORM desta forma)
    # A contagem real seria feita via query (e.g., session.query(Membro).count())
    # Mantemos como atributo Python para demonstração do requisito POO.
    total_membros = 0

    __mapper_args__ = {
        'polymorphic_identity': 'membro',
    }

    def __init__(self, nome, contacto, data_adesao=None, tipo_subscricao='Mensal', estado_pagamento='Pendente'):
        super().__init__(nome, contacto)
        self.data_adesao = data_adesao if data_adesao else datetime.date.today()
        self.tipo_subscricao = tipo_subscricao
        self._estado_pagamento = estado_pagamento
        Membro.total_membros += 1 # Incrementa o contador da classe Python

    # Implementação do método 'abstrato' (Polimorfismo)
    def display_details(self):
        print(f"Membro: {self.nome} (ID: {self.id})")
        print(f"  Contacto: {self.contacto}")
        print(f"  Adesão: {self.data_adesao.strftime('%Y-%m-%d')}")
        print(f"  Subscrição: {self.tipo_subscricao}")
        print(f"  Pagamento: {self.estado_pagamento}")

    # Encapsulamento com property (getter)
    @hybrid_property
    def estado_pagamento(self):
        return self._estado_pagamento

    # Setter para a property
    @estado_pagamento.setter
    def estado_pagamento(self, estado):
        if estado not in ['Pago', 'Pendente', 'Atrasado']:
            raise ValueError("Estado de pagamento inválido.")
        self._estado_pagamento = estado

    # Método de classe (requisito POO)
    @classmethod
    def get_total_membros_registados_instancia(cls):
        """Retorna o contador de instâncias criadas em memória."""
        # Nota: Este método retorna o contador Python, não o número de registos no BD.
        # Para obter o número real no BD, usar-se-ia uma query.
        return cls.total_membros

    # Validação de dados com SQLAlchemy
    @validates('contacto')
    def validate_contacto(self, key, contacto):
        if '@' not in contacto and not contacto.isdigit(): # Exemplo simples
             raise ValueError("Contacto deve ser um email ou número de telefone válido.")
        return contacto

class Instrutor(Pessoa):
    """Representa um Instrutor do ginásio, herdando de Pessoa."""
    __tablename__ = 'instrutores'
    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    especializacao = Column(String(100))

    # Relacionamento com Aulas (um instrutor pode lecionar várias aulas)
    aulas_lecionadas = relationship("AulaGinastica", back_populates="instrutor")

    __mapper_args__ = {
        'polymorphic_identity': 'instrutor',
    }

    def __init__(self, nome, contacto, especializacao):
        super().__init__(nome, contacto)
        self.especializacao = especializacao

    # Implementação do método 'abstrato' (Polimorfismo)
    def display_details(self):
        print(f"Instrutor: {self.nome} (ID: {self.id})")
        print(f"  Contacto: {self.contacto}")
        print(f"  Especialização: {self.especializacao}")

class AulaGinastica(Base):
    """Representa uma Aula oferecida pelo ginásio."""
    __tablename__ = 'aulas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    horario = Column(String(50)) # Simplificado como String, poderia ser DateTime
    capacidade_max = Column(Integer, default=20)

    # Chave estrangeira para Instrutor
    instrutor_id = Column(Integer, ForeignKey('instrutores.id'))
    # Relacionamento com Instrutor (uma aula tem um instrutor)
    instrutor = relationship("Instrutor", back_populates="aulas_lecionadas")

    # Relacionamento com Reservas (uma aula pode ter várias reservas)
    reservas = relationship("Reserva", back_populates="aula", cascade="all, delete-orphan")

    def __init__(self, nome, horario, capacidade_max, instrutor_id):
        self.nome = nome
        self.horario = horario
        self.capacidade_max = capacidade_max
        self.instrutor_id = instrutor_id

    def display_details(self):
        instrutor_nome = self.instrutor.nome if self.instrutor else 'N/A'
        vagas = self.capacidade_max - len(self.reservas)
        print(f"Aula: {self.nome} (ID: {self.id})")
        print(f"  Horário: {self.horario}")
        print(f"  Instrutor: {instrutor_nome}")
        print(f"  Capacidade: {len(self.reservas)}/{self.capacidade_max} (Vagas: {vagas})")

    def esta_cheia(self):
        return len(self.reservas) >= self.capacidade_max

class Reserva(Base):
    """Representa a associação entre um Membro e uma Aula (reserva)."""
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    data_reserva = Column(DateTime, default=datetime.datetime.utcnow)

    # Chaves estrangeiras
    membro_id = Column(Integer, ForeignKey('membros.id'), nullable=False)
    aula_id = Column(Integer, ForeignKey('aulas.id'), nullable=False)

    # Relacionamentos
    membro = relationship("Membro", back_populates="reservas")
    aula = relationship("AulaGinastica", back_populates="reservas")

    def __init__(self, membro_id, aula_id):
        self.membro_id = membro_id
        self.aula_id = aula_id

class Equipamento(Base):
    """Representa um Equipamento do ginásio."""
    __tablename__ = 'equipamentos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50))
    data_ultima_manutencao = Column(Date, nullable=True)

    def __init__(self, nome, tipo, data_ultima_manutencao=None):
        self.nome = nome
        self.tipo = tipo
        self.data_ultima_manutencao = data_ultima_manutencao

    def display_details(self):
        data_manut = self.data_ultima_manutencao.strftime('%Y-%m-%d') if self.data_ultima_manutencao else 'Nenhuma'
        print(f"Equipamento: {self.nome} (ID: {self.id})")
        print(f"  Tipo: {self.tipo}")
        print(f"  Última Manutenção: {data_manut}")

    def registar_manutencao(self, data=None):
        self.data_ultima_manutencao = data if data else datetime.date.today()

# --- Configuração do Banco de Dados e Sessão ---

def setup_database(db_name='ginásio.db'):
    """Configura o engine e cria as tabelas no banco de dados SQLite."""
    engine = create_engine(f'sqlite:///{db_name}')
    Base.metadata.create_all(engine) # Cria as tabelas se não existirem
    return engine

def create_session(engine):
    """Cria uma fábrica de sessões SQLAlchemy."""
    Session = sessionmaker(bind=engine)
    return Session()

# Exemplo de como usar (será movido para main.py depois)
if __name__ == '__main__':
    print("Definição dos modelos SQLAlchemy carregada.")
    # Configura o banco de dados (cria o ficheiro ginásio.db e as tabelas)
    engine = setup_database()
    print(f"Banco de dados 'ginásio.db' configurado e tabelas criadas.")

    # Cria uma sessão
    session = create_session(engine)
    print("Sessão SQLAlchemy criada.")

    # Exemplo de contagem de membros usando query (forma correta com ORM)
    total_membros_db = session.query(Membro).count()
    print(f"Total de membros no banco de dados: {total_membros_db}")
    print(f"Contador de instâncias Membro (Python): {Membro.get_total_membros_registados_instancia()}")

    session.close()
    print("Sessão fechada.")

