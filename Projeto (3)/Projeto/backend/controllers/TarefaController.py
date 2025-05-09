from flask import request, jsonify
from workers.TarefaWorker import TarefaWorker
from datetime import datetime

class TarefaController:
    def __init__(self):
        self.worker = TarefaWorker()

    def cadastrar_tarefa(self):
        # Recebe os dados da requisição
        dados = request.get_json()

        # Campos obrigatórios para criar a tarefa
        campos_obrigatorios = ['descricao', 'categoria', 'data_inicial', 'data_final']
        
        # Verificar se todos os campos obrigatórios estão presentes
        campos_faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
        if campos_faltando:
            return jsonify({'error': f'Campos obrigatórios faltando: {", ".join(campos_faltando)}'}), 400

        # Validar formato das datas (YYYY-MM-DD)
        try:
            data_inicial = datetime.strptime(dados['data_inicial'], "%Y-%m-%d")
            data_final = datetime.strptime(dados['data_final'], "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use o formato AAAA-MM-DD.'}), 400

        # Chama o worker para criar a tarefa
        try:
            tarefa_criada = self.worker.criar(dados['descricao'], dados['categoria'], data_inicial, data_final)
            return jsonify({'message': 'Tarefa criada com sucesso.', 'tarefa': tarefa_criada}), 201
        except Exception as e:
            return jsonify({'error': f'Erro ao criar tarefa: {str(e)}'}), 500


    # Listar tarefas com filtros opcionais (categoria_id e status)
    def listar(self):
        categoria_id = request.args.get('categoria_id')
        status = request.args.get('status')
        return jsonify(self.worker.listar(categoria_id=categoria_id, status=status))


    # Atualizar tarefa
    def editar_tarefa(self, tarefa_id):
        dados = request.get_json()

        # Verificar se os campos obrigatórios estão presentes
        campos_obrigatorios = ['tarefa', 'data_inicial', 'data_final', 'status', 'categoria_id']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({'error': f'{campo} é obrigatório'}), 400

        try:
            # Chamar o Worker para editar a tarefa
            tarefa_atualizada = self.worker.editar(tarefa_id, dados['tarefa'], dados['data_inicial'], dados['data_final'], dados['status'], dados['categoria_id'])
            return jsonify({'message': 'Tarefa atualizada com sucesso.', 'tarefa': tarefa_atualizada}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # Deletar tarefa
    def deletar(self, tarefa_id, categoria_id):
        usuario_id = request.args.get('usuario_id')
        if not usuario_id:
            return jsonify({'error': 'usuario_id é obrigatório'}), 400
        return jsonify(self.worker.deletar(tarefa_id, categoria_id, usuario_id))
