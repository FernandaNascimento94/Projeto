CREATE DATABASE gerenciador_tarefas;
USE gerenciador_tarefas;

-- Tabela de usuários
create table usuario(
    id int AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

-- Tabela de categorias
CREATE TABLE categoria (
    id INT AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    usuario_id INT not null,
    PRIMARY KEY(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- Tabela de tarefas
CREATE table tarefa(
    id INT AUTO_INCREMENT,
    tarefa VARCHAR(100) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_incial DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_final DATETIME,
    status ENUM('pendente', 'em_andamento', 'concluida') DEFAULT 'pendente',
    usuario_id INT NOT NULL,
    categoria_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);

insert into usuario(nome, email, senha)
values("Admin", "admin@gmail.com", "1234");

insert into categoria(nome, usuario_id)
values("casa", 1);

insert into tarefa(tarefa, data_incial,data_final,usuario_id, categoria_id)
values("fazer compras", 23/04/2015, 24/04/2015, 1, 1);