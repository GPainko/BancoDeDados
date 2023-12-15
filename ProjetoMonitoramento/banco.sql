-- Cria o banco de dados monitoramento
CREATE DATABASE IF NOT EXISTS monitoramento;
USE monitoramento;

-- Cria tabela imagens para armazenar imagens e horário do armazenamento
CREATE TABLE IF NOT EXISTS imagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imagem BLOB NOT NULL,
    horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria tabela cliente para armazenar nome, cpf, localização, número de câmeras
CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    localizacao VARCHAR(255) NOT NULL,
    numero_cameras INT NOT NULL
);

-- Cria tabela camera para armazenar nome da câmera e qual cliente é o dono
CREATE TABLE IF NOT EXISTS camera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cliente_id INT,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- Stored Procedure para inserir um novo cliente
DELIMITER //
CREATE PROCEDURE AddCliente(IN p_nome VARCHAR(255), IN p_cpf VARCHAR(14), IN p_localizacao VARCHAR(255), IN p_numero_cameras INT)
BEGIN
    INSERT INTO cliente(nome, cpf, localizacao, numero_cameras) VALUES (p_nome, p_cpf, p_localizacao, p_numero_cameras);
END//
DELIMITER ;

-- Trigger para verificar inserção de nova câmera
DELIMITER //
CREATE TRIGGER BeforeCameraInsert
BEFORE INSERT ON camera FOR EACH ROW
BEGIN
    DECLARE cam_count INT;
    SELECT numero_cameras INTO cam_count FROM cliente WHERE id = NEW.cliente_id;
    IF cam_count <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'O cliente não pode adicionar mais câmeras.';
    ELSE
        UPDATE cliente SET numero_cameras = numero_cameras - 1 WHERE id = NEW.cliente_id;
    END IF;
END//
DELIMITER ;

-- View para listar clientes com suas câmeras
CREATE VIEW vw_cliente_cameras AS
SELECT c.nome AS cliente_nome, cam.nome AS camera_nome
FROM cliente c
JOIN camera cam ON c.id = cam.cliente_id;

-- Controle de acesso ao banco de dados
CREATE USER 'monitoramento_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON monitoramento.* TO 'monitoramento_user'@'localhost';
FLUSH PRIVILEGES;

ALTER TABLE camera
ADD COLUMN localinstalada VARCHAR(15);

ALTER TABLE camera
CHANGE COLUMN nome registro int;