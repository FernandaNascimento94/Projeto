from flask import jsonify
import mysql.connector

class UserRepository:
    def __init__(self, port=3307):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="gerenciador_tarefas", port=port)
        self.cursor = self.conn.cursor(dictionary=True)

    def getUserByEmail(self, email):
        self.cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        return self.cursor.fetchone()

    def createUser(self, nome, email, senha):
        try:
            self.cursor.execute(
                "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha))
            self.conn.commit()
            return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
        except mysql.connector.IntegrityError:
            return jsonify({'message': 'Email já cadastrado'}), 400

