import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime


class TarefaRepository:
    def __init__(self, port=3307):
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="gerenciador_tarefas", port=port
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def list(self, categoria_id=None, status=None):
        try:
            query = """
                SELECT t.tarefa AS descricao, c.nome AS categoria_nome, t.status
                FROM tarefa t
                JOIN categoria c ON t.categoria_id = c.id
                WHERE 1 = 1
            """
            params = []

            if categoria_id:
                query += " AND t.categoria_id = %s"
                params.append(categoria_id)

            if status:
                query += " AND t.status = %s"
                params.append(status)

            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            return {"error": str(e)}, 500
        
    def criar(self, descricao, categoria, data_inicial, data_final):
        try:
            # Aqui você implementaria a lógica para inserir a tarefa no banco de dados
            query = """
                INSERT INTO tarefa (descricao, categoria, data_inicial, data_final)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (descricao, categoria, data_inicial, data_final))  
            self.cursor.connection.commit()  # Confirma a transação

            # Retorna os dados da tarefa inserida, incluindo o id gerado
            return {
                "id": self.cursor.lastrowid,
                "descricao": descricao,
                "categoria": categoria,
                "data_inicial": data_inicial,
                "data_final": data_final
            }
        except mysql.connector.Error as e:  # Especificando o erro do MySQL
            self.cursor.connection.rollback()  # Em caso de erro, faz rollback da transação
            raise Exception(f"Erro ao criar tarefa: {e}")
        finally:
            # Fechando o cursor e a conexão, se necessário
            self.cursor.close()
            self.cursor.connection.close()
        

    def editar_tarefa(self, tarefa_id, tarefa, data_inicial, data_final, status, categoria_id):
        try:
            # Verificar se a tarefa existe
            self.cursor.execute("SELECT * FROM tarefa WHERE id = %s", (tarefa_id,))
            tarefa_existente = self.cursor.fetchone()
            if not tarefa_existente:
                raise Exception("Tarefa não encontrada.")

            # Validar o formato das datas
            try:
                data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
                data_final = datetime.strptime(data_final, "%Y-%m-%d")
            except ValueError:
                raise Exception("Formato de data inválido. Use o formato AAAA-MM-DD.")

            # Atualizar a tarefa no banco de dados
            query = """
                UPDATE tarefa
                SET tarefa = %s, data_inicial = %s, data_final = %s, status = %s, categoria_id = %s
                WHERE id = %s
            """
            self.cursor.execute(query, (tarefa, data_inicial, data_final, status, categoria_id, tarefa_id))
            self.conn.commit()  # Confirmar a transação

            # Retornar os dados da tarefa atualizada
            return {
                "id": tarefa_id,
                "tarefa": tarefa,
                "data_inicial": data_inicial,
                "data_final": data_final,
                "status": status,
                "categoria_id": categoria_id
            }
        except mysql.connector.Error as e:
            # Erro ao tentar executar a query ou outro erro relacionado ao banco
            print(f"Erro no banco de dados: {e}")
            raise
        except Exception as e:
            # Erro de lógica, como formato de data inválido ou tarefa não encontrada
            print(f"Erro na atualização da tarefa: {e}")
            raise
        finally:
            # Fechar o cursor e a conexão após a operação
            self.cursor.close()
            self.conn.close()

    def close(self):
        # Fechar a conexão com o banco
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def deletar(self, tarefa_id, usuario_id):
        try:
            # Excluir a tarefa
            self.cursor.execute("DELETE FROM tarefa WHERE id=%s AND usuario_id=%s", (tarefa_id, usuario_id))
            self.conn.commit()
            return {'message': 'Tarefa excluída'}
        except mysql.connector.Error as e:
            return {'error': str(e)}, 500

    def filtrar_por_categoria(self, usuario_id, categoria_id):
        try:
            return self.list(usuario_id, categoria_id=categoria_id)
        except mysql.connector.Error as e:
            return {'error': str(e)}, 500

    def filtrar_por_status(self, usuario_id, status):
        try:
            return self.list(usuario_id, status=status)
        except mysql.connector.Error as e:
            return {'error': str(e)}, 500
