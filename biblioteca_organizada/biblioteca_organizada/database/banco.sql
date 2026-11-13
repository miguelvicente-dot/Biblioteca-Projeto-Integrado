-- PROJETO INTEGRADO — SISTEMA DE BIBLIOTECA
-- MySQL / MariaDB (XAMPP)
CREATE DATABASE IF NOT EXISTS biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE biblioteca;

-- Tabelas do modelo fornecido
CREATE TABLE IF NOT EXISTS leitor (
    id_leitor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS livro (
    id_livro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    ano_publicacao SMALLINT
);

CREATE TABLE IF NOT EXISTS autor (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS livro_autor (
    id_livro INT NOT NULL,
    id_autor INT NOT NULL,
    PRIMARY KEY (id_livro, id_autor),
    CONSTRAINT fk_livro_autor_livro FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
      ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_livro_autor_autor FOREIGN KEY (id_autor) REFERENCES autor(id_autor)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_leitor INT NOT NULL,
    id_livro INT NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_prevista DATE NOT NULL,
    data_devolucao DATE,
    CONSTRAINT fk_emprestimo_leitor FOREIGN KEY (id_leitor) REFERENCES leitor(id_leitor)
      ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_emprestimo_livro FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
      ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabelas complementares para autenticação, reservas e contato
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_leitor INT NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario_leitor FOREIGN KEY (id_leitor) REFERENCES leitor(id_leitor)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_leitor INT NOT NULL,
    id_livro INT NOT NULL,
    data_reserva DATE NOT NULL,
    status ENUM('Pendente','Aprovada','Cancelada','Concluída') NOT NULL DEFAULT 'Pendente',
    CONSTRAINT fk_reserva_leitor FOREIGN KEY (id_leitor) REFERENCES leitor(id_leitor)
      ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_reserva_livro FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
      ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS contato (
    id_contato INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    assunto VARCHAR(150) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio DATETIME NOT NULL
);

-- Dados iniciais para testar o catálogo
INSERT IGNORE INTO livro (titulo,isbn,ano_publicacao) VALUES
('Dom Casmurro','9788535910663',1899),
('O Pequeno Príncipe','9788522031445',1943),
('A Revolução dos Bichos','9788535909555',1945),
('O Hobbit','9788595084742',1937),
('Capitães da Areia','9788503009491',1937);

INSERT IGNORE INTO autor (nome,nacionalidade) VALUES
('Machado de Assis','Brasileira'),
('Antoine de Saint-Exupéry','Francesa'),
('George Orwell','Britânica'),
('J. R. R. Tolkien','Britânica'),
('Jorge Amado','Brasileira');

INSERT IGNORE INTO livro_autor (id_livro,id_autor)
SELECT l.id_livro,a.id_autor FROM livro l JOIN autor a
ON (l.titulo='Dom Casmurro' AND a.nome='Machado de Assis')
OR (l.titulo='O Pequeno Príncipe' AND a.nome='Antoine de Saint-Exupéry')
OR (l.titulo='A Revolução dos Bichos' AND a.nome='George Orwell')
OR (l.titulo='O Hobbit' AND a.nome='J. R. R. Tolkien')
OR (l.titulo='Capitães da Areia' AND a.nome='Jorge Amado');
