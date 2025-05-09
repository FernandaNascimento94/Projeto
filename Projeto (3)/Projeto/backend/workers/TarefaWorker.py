from repositories.TarefaRepository import TarefaRepository
from datetime import datetime

class TarefaWorker:
    def __init__(self):
        self.repo = TarefaRepository()

    # Criar nova tarefa
    def criar(self, descricao, categoria, data_inicial, data_final):
        # 1. Validar se os dados estão corretos
        if not descricao or not categoria or not data_inicial or not data_final:
            raise ValueError("Todos os campos (descricao, categoria, data_inicial, data_final) são obrigatórios.")
        
        # 2. Verificar se a data inicial não é maior que a data final
        if data_inicial > data_final:
            raise ValueError("A data inicial não pode ser maior que a data final.")

        # 3. Criar a tarefa chamando o repositório
        try:
            tarefa_criada = self.repo.criar(descricao, categoria, data_inicial, data_final)
            return tarefa_criada
        except Exception as e:
            raise Exception(f"Erro ao criar tarefa: {str(e)}")

    # Listar tarefas, com filtro opcional por categoria ou status
    def listar(self, categoria_id=None, status=None):
        return self.repo.list(categoria_id=categoria_id, status=status)


    def editar(self, tarefa_id, tarefa, data_inicial, data_final, status, categoria_id):
        try:
            # Validar formato de data
            data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
            data_final = datetime.strptime(data_final, "%Y-%m-%d")
        except ValueError:
            raise Exception("Formato de data inválido. Use o formato AAAA-MM-DD.")

        # Chamar o repositório para editar a tarefa
        tarefa_atualizada = self.repo.editar_tarefa(tarefa_id, tarefa, data_inicial, data_final, status, categoria_id)
        return tarefa_atualizada

    def deletar(self, tarefa_id, usuario_id):
        return self.repo.deletar(tarefa_id, usuario_id)


    # Filtrar por categoria
    def filtrar_por_categoria(self, usuario_id, categoria_id):
        return self.repo.filtrar_por_categoria(usuario_id, categoria_id)

    # Filtrar por status
    def filtrar_por_status(self, usuario_id, status):
        return self.repo.filtrar_por_status(usuario_id, status)
