from flask import Flask, request
from flask_cors import CORS
from controllers.TarefaController import TarefaController
from controllers.UserController import UserController
from repositories.TarefaRepository import TarefaRepository

# Inicializando o aplicativo Flask
api = Flask(__name__)

# Habilitando CORS (Cross-Origin Resource Sharing) para o frontend
CORS(api)

# Criando as instâncias dos controladores
tarefaController = TarefaController()
userController = UserController()

# Rota para registro de novo usuário
@api.route('/register', methods=['POST'])
def register():
    return userController.register()

# Rota para login do usuário
@api.route('/login', methods=['POST'])
def login():
    return userController.login()

# Rota para criar uma tarefa e categoria
@api.route('/tarefas', methods=['POST'])
def cadastrar_tarefa():
    data = request.get_json()
    repo = TarefaRepository()
    return repo.cadastrar_tarefa(data)

# Rota para listar todas as tarefas
@api.route('/listar/tarefas', methods=['GET'])
def listar_tarefas():
    return tarefaController.listar()

# Rota para atualizar uma tarefa
@api.route('/atualizar/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    return tarefaController.atualizar(tarefa_id)

# Rota para deletar uma tarefa
@api.route('/deletar/tarefas/<int:tarefa_id>', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    return tarefaController.deletar(tarefa_id)

# Rota para filtrar tarefas por categoria
@api.route('/tarefas/categoria/<int:categoria_id>', methods=['GET'])
def filtrar_por_categoria(categoria_id):
    return tarefaController.filtrar_por_categoria(categoria_id)

# Rota para filtrar tarefas por status
@api.route('/tarefas/status', methods=['GET'])
def filtrar_por_status():
    status = request.args.get('status')  # Filtra pelo status passado como parâmetro
    return tarefaController.filtrar_por_status(status)

# Rodar a aplicação Flask
if __name__ == '__main__':
    api.run(debug=True)
