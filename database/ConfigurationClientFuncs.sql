-- Функция создания клиента
CREATE OR REPLACE FUNCTION create_client(
	VARCHAR(50),
	VARCHAR(50),
	VARCHAR(50),
	VARCHAR(20),
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO client(email, password, name, phone, registration)
	VALUES ($1, $2, $3, $4, $5);
END;
$$ LANGUAGE plpgsql;

-- Функция создания клиента
CREATE OR REPLACE FUNCTION create_configuration(
	INT, -- id клиента
	INT, -- id видеокарты
	INT,
	INT,
	INT,
	INT,
	INT,
	INT,
	INT, -- id корпуса
	DATE) -- дата заказа
	RETURNS void AS $$
BEGIN
	INSERT INTO configuration(client_id, videocard_id, proc_id, motherboard_id,
	cool_id, ram_id, disk_id, power_id, body_id, registration)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
END;
$$ LANGUAGE plpgsql;


select create_client('admin@confpc.ru', 'qwerty', 'admin', '81231231212','01.01.2023')