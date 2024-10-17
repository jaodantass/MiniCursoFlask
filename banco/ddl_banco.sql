-- Criação do banco de dados
CREATE DATABASE gerenciador_tarefas;

-- Utilizando o banco de dados criado
USE gerenciador_tarefas;

-- Criação da tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    papel ENUM('admin', 'usuario') DEFAULT 'usuario',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela de tarefas
CREATE TABLE tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    status ENUM('pendente', 'concluida') DEFAULT 'pendente',
    usuario_id INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nome_usuario, senha_hash, papel)
VALUES ('admin', 'scrypt:32768:8:1$FxdsNsROHjzviELP$40a336a7210a9634daba2b816bbd456c2556b0a49b0625a90f769532c77a15b83ef59e5fcb2c6632faaecfdcc624238f9d978a58d3a9222722581d5d4e272a77', 'admin');
