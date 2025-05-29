import logging
logging.basicConfig()

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

from models.base import Session
from models.aluno import Aluno
from models.instrutor import Instrutor
from models.modalidade import Modalidade
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from models.matricula import Matricula

# Cria uma sessão global para ser usada pelas funções
# (Para aplicações maiores, considerar padrões de gestão de sessão mais robustos)
session = Session()

# --- Funções de Listagem ---

def listar_alunos():
    """Lista todos os alunos cadastrados."""
    try:
        alunos = session.query(Aluno).order_by(Aluno._nome).all()
        print("\n=== Lista de Alunos ===")
        if not alunos:
            print("Nenhum aluno cadastrado.")
            return False # Indica que a lista está vazia
        for aluno in alunos:
            # Usar o método exibir_detalhes se disponível e útil, ou formatar aqui
            print(f"ID: {aluno.id}, Nome: {aluno.nome}, Idade: {aluno.idade}, Matrícula: {aluno.matricula}")
        return True # Indica que há alunos para escolher
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return False

def listar_instrutores():
    """Lista todos os instrutores cadastrados."""
    try:
        instrutores = session.query(Instrutor).order_by(Instrutor._nome).all()
        print("\n=== Lista de Instrutores ===")
        if not instrutores:
            print("Nenhum instrutor cadastrado.")
            return False
        for instrutor in instrutores:
            print(f"ID: {instrutor.id}, Nome: {instrutor.nome}, Idade: {instrutor.idade}, CREF: {instrutor.cref}")
        return True
    except Exception as e:
        print(f"Erro ao listar instrutores: {e}")
        return False

def listar_modalidades():
    """Lista todas as modalidades cadastradas."""
    try:
        modalidades = session.query(Modalidade).order_by(Modalidade.nome).all()
        print("\n=== Lista de Modalidades ===")
        if not modalidades:
            print("Nenhuma modalidade cadastrada.")
            return False
        for m in modalidades:
            print(f"ID: {m.id}, Nome: {m.nome}")
        return True
    except Exception as e:
        print(f"Erro ao listar modalidades: {e}")
        return False

# --- Funções de Consulta Específica ---

def listar_matriculas_do_aluno():
    """Lista as modalidades em que um aluno específico está matriculado."""
    if not listar_alunos(): # Só prossegue se houver alunos
        return
    try:
        aluno_id = int(input("\nDigite o ID do aluno para ver as matrículas: "))
        # Usar joinedload para carregar eficientemente as matrículas e modalidades associadas
        aluno = session.query(Aluno).options(
            joinedload(Aluno.matriculas).joinedload(Matricula.modalidade)
        ).filter_by(id=aluno_id).first()

        if not aluno:
            print("Aluno não encontrado.")
            return

        print(f"\n=== Modalidades do Aluno: {aluno.nome} ===")
        if not aluno.matriculas:
            print("Nenhuma modalidade encontrada para este aluno.")
            return

        # Ordenar as modalidades por nome para melhor visualização
        matriculas_ordenadas = sorted(aluno.matriculas, key=lambda m: m.modalidade.nome)
        for m in matriculas_ordenadas:
            print(f"- Modalidade: {m.modalidade.nome} (ID: {m.modalidade.id})")

    except ValueError:
        print("Entrada inválida. Por favor, digite um número para o ID.")
    except Exception as e:
        print(f"Erro ao listar matrículas do aluno: {e}")

# --- Funções de Adição ---

def adicionar_aluno():
    """Adiciona um novo aluno ao sistema."""
    try:
        nome = input("Nome do aluno: ").strip()
        if not nome:
            print("Nome não pode ser vazio.")
            return

        idade_str = input("Idade: ")
        idade = int(idade_str)

        matricula_str = input("Matrícula (número): ")
        matricula = int(matricula_str)

        # Cria a instância do aluno (validações podem ocorrer no setter)
        novo_aluno = Aluno(nome=nome, idade=idade, matricula=matricula)
        session.add(novo_aluno)
        session.commit()
        print(f"Aluno '{novo_aluno.nome}' adicionado com sucesso (ID: {novo_aluno.id}).")

    except ValueError:
        print("Erro: Idade e Matrícula devem ser números inteiros válidos.")
        session.rollback()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade: Possivelmente a matrícula '{matricula_str}' já existe. {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar aluno: {e}")

def adicionar_instrutor():
    """Adiciona um novo instrutor ao sistema."""
    try:
        nome = input("Nome do instrutor: ").strip()
        if not nome:
            print("Nome não pode ser vazio.")
            return

        idade_str = input("Idade: ")
        idade = int(idade_str)

        cref = input("CREF: ").strip()

        # Cria a instância (validações podem ocorrer no setter)
        novo_instrutor = Instrutor(nome=nome, idade=idade, cref=cref)
        session.add(novo_instrutor)
        session.commit()
        print(f"Instrutor '{novo_instrutor.nome}' adicionado com sucesso (ID: {novo_instrutor.id}).")

    except ValueError as e:
        # Captura erros de validação dos setters (idade, cref)
        print(f"Erro de validação: {e}")
        session.rollback()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade: Possivelmente o CREF '{cref}' já existe. {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar instrutor: {e}")

def adicionar_modalidade():
    """Adiciona uma nova modalidade ao sistema."""
    try:
        nome = input("Nome da nova modalidade: ").strip()
        if not nome:
            print("Nome da modalidade não pode ser vazio.")
            return

        # Verificar se já existe
        existente = session.query(Modalidade).filter_by(nome=nome).first()
        if existente:
            print(f"Modalidade '{nome}' já existe.")
            return

        nova_modalidade = Modalidade(nome=nome)
        session.add(nova_modalidade)
        session.commit()
        print(f"Modalidade '{nova_modalidade.nome}' adicionada com sucesso (ID: {nova_modalidade.id}).")

    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade ao adicionar modalidade: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar modalidade: {e}")

# --- Função de Matrícula (Revisada) ---

def matricular_aluno_em_modalidade():
    """Matricula um aluno existente em uma modalidade existente."""
    if not listar_alunos(): return
    try:
        aluno_id = int(input("\nDigite o ID do aluno que deseja matricular: "))
        # Carrega o aluno e suas matrículas/modalidades associadas
        aluno = session.query(Aluno).options(
            joinedload(Aluno.matriculas).joinedload(Matricula.modalidade)
        ).filter_by(id=aluno_id).first()

        if not aluno:
            print(f"Aluno com ID {aluno_id} não encontrado.")
            return

        if not listar_modalidades(): return
        mod_id = int(input("\nDigite o ID da modalidade para matrícula: "))
        # Busca a modalidade pelo ID
        modalidade = session.get(Modalidade, mod_id)

        if not modalidade:
            print(f"Modalidade com ID {mod_id} não encontrada.")
            return

        # Verifica se a matrícula já existe na coleção carregada do aluno
        # Esta verificação é feita em memória nos dados já carregados
        matricula_existente = None
        for m in aluno.matriculas:
            if m.modalidade_id == modalidade.id:
                matricula_existente = m
                break

        if matricula_existente:
            print(f"O aluno '{aluno.nome}' já está matriculado na modalidade '{modalidade.nome}'.")
            return

        # Se não existe, cria a nova matrícula
        # O construtor da Matricula espera as instâncias de Aluno e Modalidade
        nova_matricula = Matricula(aluno=aluno, modalidade=modalidade)
        session.add(nova_matricula)
        # Opcional: adicionar a nova matrícula à coleção do aluno em memória
        # aluno.matriculas.append(nova_matricula) # SQLAlchemy geralmente faz isso automaticamente

        session.commit()
        print(f"Aluno '{aluno.nome}' matriculado com sucesso na modalidade '{modalidade.nome}'.")

    except ValueError:
        print("Entrada inválida. Por favor, use apenas números para os IDs.")
        session.rollback() # Garante rollback em caso de erro de conversão
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade ao matricular: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao matricular aluno: {e}")
        # Para depuração mais detalhada:
        # logging.exception("Erro detalhado ao matricular aluno:")

# --- Funções de Edição --- (Implementação Nova)

def editar_aluno():
    """Edita os dados de um aluno existente."""
    if not listar_alunos(): return
    try:
        aluno_id = int(input("\nDigite o ID do aluno que deseja editar: "))
        aluno = session.get(Aluno, aluno_id)

        if not aluno:
            print(f"Aluno com ID {aluno_id} não encontrado.")
            return

        print(f"\nEditando Aluno: {aluno.nome} (ID: {aluno.id})")
        print(f"Deixe em branco para manter o valor atual.")

        # Pedir novos dados
        novo_nome = input(f"Novo nome ({aluno.nome}): ").strip()
        nova_idade_str = input(f"Nova idade ({aluno.idade}): ").strip()
        nova_matricula_str = input(f"Nova matrícula ({aluno.matricula}): ").strip()

        # Atualizar apenas se novos valores foram fornecidos
        if novo_nome:
            aluno.nome = novo_nome
        if nova_idade_str:
            aluno.idade = int(nova_idade_str) # Pode gerar ValueError
        if nova_matricula_str:
            aluno.matricula = int(nova_matricula_str) # Pode gerar ValueError ou IntegrityError

        session.commit()
        print(f"Dados do aluno '{aluno.nome}' atualizados com sucesso.")

    except ValueError:
        print("Erro: Idade e Matrícula devem ser números inteiros válidos.")
        session.rollback()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade: Possivelmente a nova matrícula '{nova_matricula_str}' já existe. {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao editar aluno: {e}")

def editar_instrutor():
    """Edita os dados de um instrutor existente."""
    if not listar_instrutores(): return
    try:
        instrutor_id = int(input("\nDigite o ID do instrutor que deseja editar: "))
        instrutor = session.get(Instrutor, instrutor_id)

        if not instrutor:
            print(f"Instrutor com ID {instrutor_id} não encontrado.")
            return

        print(f"\nEditando Instrutor: {instrutor.nome} (ID: {instrutor.id})")
        print(f"Deixe em branco para manter o valor atual.")

        # Pedir novos dados
        novo_nome = input(f"Novo nome ({instrutor.nome}): ").strip()
        nova_idade_str = input(f"Nova idade ({instrutor.idade}): ").strip()
        novo_cref = input(f"Novo CREF ({instrutor.cref}): ").strip()

        # Atualizar apenas se novos valores foram fornecidos
        if novo_nome:
            instrutor.nome = novo_nome
        if nova_idade_str:
            instrutor.idade = int(nova_idade_str) # Pode gerar ValueError
        if novo_cref:
            instrutor.cref = novo_cref # Pode gerar ValueError (validação no setter)

        session.commit()
        print(f"Dados do instrutor '{instrutor.nome}' atualizados com sucesso.")

    except ValueError as e:
        # Captura erros de validação dos setters (idade, cref)
        print(f"Erro de validação: {e}")
        session.rollback()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade: Possivelmente o novo CREF '{novo_cref}' já existe. {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao editar instrutor: {e}")

# --- Funções de Exclusão --- (Implementação Nova para Instrutor)

def apagar_aluno():
    """Apaga um aluno existente do sistema."""
    if not listar_alunos(): return
    try:
        aluno_id = int(input("\nDigite o ID do aluno que deseja apagar: "))
        aluno = session.get(Aluno, aluno_id)

        if not aluno:
            print(f"Aluno com ID {aluno_id} não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja apagar o aluno '{aluno.nome}' (ID: {aluno.id})? \nIsso também removerá todas as suas matrículas. (s/n): ").lower()

        if confirmacao == 's':
            # SQLAlchemy deve cuidar da exclusão em cascata das matrículas se configurado corretamente
            # (cascade="all, delete-orphan" na relação Aluno.matriculas)
            # Vamos verificar se a cascata está configurada em aluno.py
            # Se não estiver, precisaríamos apagar as matrículas manualmente primeiro:
            # session.query(Matricula).filter_by(aluno_id=aluno.id).delete()
            session.delete(aluno)
            session.commit()
            print(f"Aluno '{aluno.nome}' apagado com sucesso.")
        else:
            print("Operação cancelada.")

    except ValueError:
        print("Entrada inválida. Por favor, digite um número para o ID.")
        session.rollback()
    except IntegrityError as e:
        # Pode ocorrer se houver outras dependências não configuradas para cascata
        session.rollback()
        print(f"Erro de integridade ao apagar aluno: {e}. Verifique dependências.")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao apagar aluno: {e}")

def apagar_instrutor():
    """Apaga um instrutor existente do sistema."""
    if not listar_instrutores(): return
    try:
        instrutor_id = int(input("\nDigite o ID do instrutor que deseja apagar: "))
        instrutor = session.get(Instrutor, instrutor_id)

        if not instrutor:
            print(f"Instrutor com ID {instrutor_id} não encontrado.")
            return

        # IMPORTANTE: Verificar se o instrutor está associado a alguma Modalidade ou Aula
        # Se estiver, a exclusão direta pode falhar devido a restrições de chave estrangeira.
        # Precisamos decidir a política: impedir exclusão, desassociar ou excluir em cascata.
        # Assumindo que não podemos apagar instrutor com dependências (mais seguro).

        # Exemplo de verificação (adaptar se houver relação Instrutor -> Modalidade/Aula):
        # aulas_associadas = session.query(AlgumaClasseAula).filter_by(instrutor_id=instrutor.id).count()
        # if aulas_associadas > 0:
        #     print(f"Erro: Instrutor '{instrutor.nome}' está associado a {aulas_associadas} aulas/modalidades.")
        #     print("Não é possível apagar. Reatribua ou remova as associações primeiro.")
        #     return

        confirmacao = input(f"Tem certeza que deseja apagar o instrutor '{instrutor.nome}' (ID: {instrutor.id})? (s/n): ").lower()

        if confirmacao == 's':
            session.delete(instrutor)
            session.commit()
            print(f"Instrutor '{instrutor.nome}' apagado com sucesso.")
        else:
            print("Operação cancelada.")

    except ValueError:
        print("Entrada inválida. Por favor, digite um número para o ID.")
        session.rollback()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade ao apagar instrutor: {e}. Verifique se ele está associado a aulas/modalidades.")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao apagar instrutor: {e}")

# --- Menu Principal --- (Atualizado com novas opções)

def menu():
    """Exibe o menu principal e processa a escolha do usuário."""
    while True:
        print("\n========= Sistema de Gerenciamento Academia ==========")
        print("--- Listar ---")
        print(" 1 - Listar Alunos")
        print(" 2 - Listar Instrutores")
        print(" 3 - Listar Modalidades")
        print(" 4 - Listar Modalidades de um Aluno")
        print("--- Adicionar ---")
        print(" 5 - Adicionar Aluno")
        print(" 6 - Adicionar Instrutor")
        print(" 7 - Adicionar Modalidade")
        print("--- Matricular ---")
        print(" 8 - Matricular Aluno em Modalidade")
        print("--- Editar ---")
        print(" 9 - Editar Aluno")
        print("10 - Editar Instrutor")
        print("--- Apagar ---")
        print("11 - Apagar Aluno")
        print("12 - Apagar Instrutor")
        print("--- Sair ---")
        print("13 - Sair")
        print("====================================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_alunos()
        elif opcao == "2":
            listar_instrutores()
        elif opcao == "3":
            listar_modalidades()
        elif opcao == "4":
            listar_matriculas_do_aluno()
        elif opcao == "5":
            adicionar_aluno()
        elif opcao == "6":
            adicionar_instrutor()
        elif opcao == "7":
            adicionar_modalidade()
        elif opcao == "8":
            matricular_aluno_em_modalidade()
        elif opcao == "9":
            editar_aluno()
        elif opcao == "10":
            editar_instrutor()
        elif opcao == "11":
            apagar_aluno()
        elif opcao == "12":
            apagar_instrutor()
        elif opcao == "13":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

# --- Ponto de Entrada --- 

if __name__ == "__main__":
    # Opcional: Criar tabelas se não existirem (geralmente feito separadamente)
    # from models.base import Base, engine
    # Base.metadata.create_all(engine)
    
    print("Bem-vindo ao Sistema de Gerenciamento da Academia!")
    menu() # Inicia o loop do menu
    session.close() # Fecha a sessão ao sair do programa
    print("Sessão com o banco de dados fechada.")

