function showRegisterForm() {
    document.getElementById("login-section").style.display = "none";
    document.getElementById("register-section").style.display = "block";
    document.getElementById("task-section").style.display = "none";
}

function showLoginForm() {
    document.getElementById("register-section").style.display = "none";
    document.getElementById("login-section").style.display = "block";
    document.getElementById("task-section").style.display = "none";
}

function showTaskSection() {
    document.getElementById("login-section").style.display = "none";
    document.getElementById("register-section").style.display = "none";
    document.getElementById("task-section").style.display = "block";

    carregarTarefas();
}

// Login
async function loginUser(event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha: password })
    });

    const data = await response.json();

    if (data.token) {
        localStorage.setItem('token', data.token);
        alert('Login bem-sucedido!');
        showTaskSection();
    } else {
        alert('Erro no login: ' + (data.message || 'Credenciais inválidas'));
    }
}

// Cadastro
async function registerUser(event) {
    event.preventDefault();

    const name = document.getElementById("register-nome").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: name, email, senha: password })
    });

    const data = await response.json();

    if (data.message === 'Usuário cadastrado com sucesso') {
        alert('Cadastro bem-sucedido!');
        showLoginForm();
    } else {
        alert('Erro no cadastro: ' + (data.message || 'Erro desconhecido'));
    }
}

// Vincula os eventos
document.getElementById("login-form").addEventListener("submit", loginUser);
document.getElementById("register-form").addEventListener("submit", registerUser);

//tarefas
const API_URL = "http://localhost:5000";

// Criar nova tarefa
// Função para cadastrar tarefa
async function cadastrarTarefa(descricao, categoria, data_inicial, data_final) {
  try {
    const status = "Pendente";  // Atribui automaticamente o status como "Pendente"

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        descricao: descricao,
        categoria_nome: categoria,
        status: status,  // Status automaticamente atribuído
        data_inicial: data_inicial,
        data_final: data_final
      })
    });

    const data = await response.json();

    const resultado = document.getElementById('resultado');
    if (data.message) {
      resultado.style.color = 'green';
      resultado.textContent = data.message + (data.tarefa.id ? " ID da Tarefa: " + data.tarefa.id : '');
    } else if (data.error) {
      resultado.style.color = 'red';
      resultado.textContent = "Erro: " + data.error;
    }
  } catch (error) {
    const resultado = document.getElementById('resultado');
    resultado.style.color = 'red';
    resultado.textContent = "Erro ao conectar com o servidor!";
  }
}

// Adicionar o ouvinte de evento para o formulário
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById('tarefaForm');
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault();  // Impede o envio padrão do formulário

      // Obtendo os valores do formulário
      const descricao = document.getElementById('descricao').value;
      const categoria = document.getElementById('categoria').value;
      const data_inicial = document.getElementById('data_inicial').value;
      const data_final = document.getElementById('data_final').value;

      // Chamando a função assíncrona para cadastrar a tarefa
      cadastrarTarefa(descricao, categoria, data_inicial, data_final);
    });
  } else {
    console.error("Formulário não encontrado");
  }
});

// Carregar tarefas da API
async function carregarTarefas() {
  try {
    const response = await fetch(`${API_URL}/listar/tarefas`);
    const tarefas = await response.json();

    const lista = document.getElementById("lista-tarefas");
    lista.innerHTML = "";

    if (tarefas.length === 0) {
      lista.innerHTML = "<li>Nenhuma tarefa encontrada.</li>";
      return;
    }

    tarefas.forEach((tarefa) => {
      const item = document.createElement("li");
      item.textContent = `${tarefa.descricao} - Categoria: ${tarefa.categoria_nome} - Status: ${tarefa.status}`;
      lista.appendChild(item);
    });
  } catch (err) {
    console.error("Erro ao carregar tarefas:", err);
    alert("Erro ao carregar tarefas.");
  }
}
// Carregar ao abrir a págin
window.onload = carregarTarefas;


//editar

function editarTarefa(tarefaId) {
  fetch(`${API_URL}/${tarefaId}`)
      .then(response => response.json())
      .then(tarefa => {
          document.getElementById("editTarefaId").value = tarefa.id;
          document.getElementById("editDescricao").value = tarefa.descricao;
          document.getElementById("editDataInicial").value = tarefa.data_inicial.split('T')[0]; // Extrai a data no formato correto
          document.getElementById("editDataFinal").value = tarefa.data_final.split('T')[0];
          document.getElementById("editCategoria").value = tarefa.categoria_nome;

          document.getElementById("editModal").style.display = "block"; // Exibir o modal
      })
      .catch(error => console.error("Erro ao carregar dados da tarefa", error));
}

// Função para fechar o modal
function closeModal() {
  document.getElementById("editModal").style.display = "none";
}

// Função para enviar as alterações da tarefa para o backend
async function atualizarTarefa(event) {
  event.preventDefault();

  const tarefaId = document.getElementById("editTarefaId").value;
  const descricao = document.getElementById("editDescricao").value;
  const data_inicial = document.getElementById("editDataInicial").value;
  const data_final = document.getElementById("editDataFinal").value;
  const categoria = document.getElementById("editCategoria").value;

  try {
      const response = await fetch(`${API_URL}/${tarefaId}`, {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              descricao,
              data_inicial,
              data_final,
              categoria_nome: categoria,
          })
      });

      const data = await response.json();

      if (data.message) {
          alert(data.message);
          closeModal();
          carregarTarefas(); // Atualiza a lista após editar
      } else {
          alert("Erro ao atualizar tarefa");
      }
  } catch (error) {
      console.error("Erro ao atualizar tarefa", error);
      alert("Erro ao conectar com o servidor");
  }
}

// Ouve o evento de envio do formulário de edição
document.getElementById("editForm").addEventListener("submit", atualizarTarefa);

// Carregar as tarefas na inicialização da página
window.onload = carregarTarefas;