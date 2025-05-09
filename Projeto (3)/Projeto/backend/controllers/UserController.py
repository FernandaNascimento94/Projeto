from flask import request, jsonify
from workers.UserWorker import UserWorker

class UserController:
    def __init__(self):
        self.worker = UserWorker()  # Inicializa o UserWorker

    def register(self):
        data = request.get_json()  # Obtém os dados do corpo da requisição
        if not data:
            return jsonify({'message': 'Dados não fornecidos'}), 400
        
        # Chama o método register do Worker para tratar o cadastro
        response = self.worker.register(data)
        return response

    def login(self):
        data = request.get_json()  # Obtém os dados do corpo da requisição
        if not data:
            return jsonify({'message': 'Dados não fornecidos'}), 400
        
        # Chama o método login do Worker para autenticação e geração do token
        response = self.worker.login(data)
        return response
    