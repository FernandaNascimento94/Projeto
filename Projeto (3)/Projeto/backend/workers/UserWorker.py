from repositories.UserRepository import UserRepository
import jwt, datetime
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class UserWorker:
    def __init__(self):
        self.repository = UserRepository()
        # Carregar chave secreta de um arquivo
        try:
            self.chaveCriptografia = open("secretkey.config").read().strip()
        except FileNotFoundError:
            raise Exception("Arquivo 'secretkey.config' não encontrado.")
    
    def login(self, data):
        email = data.get('email')
        senha = data.get('senha')
        user = self.repository.getUserByEmail(email)

        if user and check_password_hash(user['senha'], senha):
            token = jwt.encode(
                {
                    'user_id': user['id'], 
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                key=self.chaveCriptografia,  # Usando a chave criptografada
                algorithm="HS256"
            )

            # Retorna o token com a informação de "Bearer"
            return jsonify({'token': token}), 200
    
        return jsonify({'message': 'Credenciais inválidas'}), 401


    def register(self, data):
        nome = data.get('nome')
        email = data.get('email')
        senha = generate_password_hash(data.get('senha'))

        # Chama o repositório para criar o usuário
        return self.repository.createUser(nome, email, senha)

