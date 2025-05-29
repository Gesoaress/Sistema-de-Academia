from models.aluno import Aluno
from models.instrutor import Instrutor
from models.modalidade import Modalidade
from models.matricula import Matricula


class AlunoService:
    @staticmethod
    def editar(session, aluno_id, nome=None, idade=None, matricula=None):
        aluno = session.query(Aluno).get(aluno_id)
        if not aluno:
            print("Aluno não encontrado.")
            return
        if nome:
            aluno.nome = nome
        if idade:
            aluno.idade = idade
        if matricula:
            aluno.matricula = matricula
        session.commit()
        print("Aluno atualizado com sucesso.")

    @staticmethod
    def excluir(session, aluno_id):
        aluno = session.query(Aluno).get(aluno_id)
        if aluno:
            session.delete(aluno)
            session.commit()
            print("Aluno excluído com sucesso.")
        else:
            print("Aluno não encontrado.")


class InstrutorService:
    @staticmethod
    def editar(session, instrutor_id, nome=None, idade=None, cref=None):
        instrutor = session.query(Instrutor).get(instrutor_id)
        if not instrutor:
            print("Instrutor não encontrado.")
            return
        if nome:
            instrutor.nome = nome
        if idade:
            instrutor.idade = idade
        if cref:
            instrutor.cref = cref
        session.commit()
        print("Instrutor atualizado com sucesso.")

    @staticmethod
    def excluir(session, instrutor_id):
        instrutor = session.query(Instrutor).get(instrutor_id)
        if instrutor:
            session.delete(instrutor)
            session.commit()
            print("Instrutor excluído com sucesso.")
        else:
            print("Instrutor não encontrado.")


class ModalidadeService:
    @staticmethod
    def editar(session, modalidade_id, nome=None, descricao=None):
        modalidade = session.query(Modalidade).get(modalidade_id)
        if not modalidade:
            print("Modalidade não encontrada.")
            return
        if nome:
            modalidade.nome = nome
        if descricao is not None:
            modalidade.descricao = descricao
        session.commit()
        print("Modalidade atualizada com sucesso.")

    @staticmethod
    def excluir(session, modalidade_id):
        modalidade = session.query(Modalidade).get(modalidade_id)
        if modalidade:
            session.delete(modalidade)
            session.commit()
            print("Modalidade excluída com sucesso.")
        else:
            print("Modalidade não encontrada.")


class MatriculaService:
    @staticmethod
    def matricular(session, aluno_id, modalidade_id):
        matricula_existente = session.query(Matricula).filter_by(aluno_id=aluno_id, modalidade_id=modalidade_id).first()
        if matricula_existente:
            print("Aluno já está matriculado nessa modalidade.")
            return
        nova_matricula = Matricula(aluno_id=aluno_id, modalidade_id=modalidade_id)
        session.add(nova_matricula)
        session.commit()
        print("Aluno matriculado com sucesso.")

    @staticmethod
    def cancelar(session, aluno_id, modalidade_id):
        matricula = session.query(Matricula).filter_by(aluno_id=aluno_id, modalidade_id=modalidade_id).first()
        if matricula:
            session.delete(matricula)
            session.commit()
            print("Matrícula cancelada com sucesso.")
        else:
            print("Matrícula não encontrada.")

    @staticmethod
    def listar_alunos_por_modalidade(session, modalidade_id):
        modalidade = session.query(Modalidade).get(modalidade_id)
        if not modalidade:
            print("Modalidade não encontrada.")
            return
        print(f"\nAlunos matriculados em {modalidade.nome}:")
        for matricula in modalidade.matriculas:
            print(f"- {matricula.aluno.nome} (ID: {matricula.aluno.id})")

    @staticmethod
    def relatorio_quantidade_alunos_por_modalidade(session):
        modalidades = session.query(Modalidade).all()
        print("\nRelatório - Quantidade de alunos por modalidade:")
        for modalidade in modalidades:
            qtd = len(modalidade.matriculas)
            print(f"{modalidade.nome}: {qtd} aluno(s)")
