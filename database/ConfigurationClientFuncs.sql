-- Функция создания клиента
CREATE OR REPLACE FUNCTION create_client(
	VARCHAR(50),
	TEXT,
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
	INT, -- сумма сборки
	DATE) -- дата заказа
	RETURNS void AS $$
BEGIN
	INSERT INTO configuration(client_id, videocard_id, processor_id, motherboard_id,
	cool_id, ram_id, disk_id, power_id, body_id, price, date_create)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
END;
$$ LANGUAGE plpgsql;

-- Функция хеширования пароля
CREATE OR REPLACE FUNCTION get_hash_pass(pass_in VARCHAR)
RETURNS TABLE(
	hash_pass TEXT
) AS $$
	SELECT md5(pass_in)
$$ LANGUAGE sql;

-- функция вывода всех клиентов
CREATE OR REPLACE FUNCTION get_all_client()
RETURNS TABLE(
	client_id int
	email VARCHAR,
	phone VARCHAR,
	password TEXT,
	name VARCHAR,
	registration DATE
) AS $$
	SELECT email, phone, password, name, registration
	FROM client
$$ LANGUAGE sql;

-- Функция получения информации о клиенте по ID
CREATE OR REPLACE FUNCTION get_client_by_id(client_id_in INT)
RETURNS TABLE(
	client_id INT,
	email VARCHAR,
	phone VARCHAR,
	password TEXT,
	name VARCHAR,
	registration DATE
) AS $$
	SELECT id, email, phone, password, name, registration
	FROM client
	WHERE client.id = client_id_in
$$ LANGUAGE sql;

-- Функция вычисления кол-ва сборок по ID клиента (для ЛК)
CREATE OR REPLACE FUNCTION get_kol_configuration(client_id_in INT)
RETURNS TABLE(
	confs INT
) AS $$
	SELECT COUNT(configuration.id)
	FROM configuration
	WHERE configuration.client_id = client_id_in
$$ LANGUAGE sql;

-- Функция вычисления общего кол-ва сборок (для ЛК администратора)
CREATE OR REPLACE FUNCTION get_all_kol_configuration()
RETURNS TABLE(
	confs INT
) AS $$
	SELECT COUNT(configuration.id)
	FROM configuration
$$ LANGUAGE sql;

--функция получения всех конфигураций (на склад)
CREATE OR REPLACE FUNCTION get_all_configuration()
RETURNS TABLE(
	id_conf INT,
	date_order DATE,
	price INT,
	video VARCHAR,
	proc VARCHAR,
	mother VARCHAR,
	cool VARCHAR,
	ram VARCHAR,
	disk VARCHAR,
	power VARCHAR,
	body VARCHAR
) AS $$
	SELECT configuration.id, configuration.date_create, configuration.price, videocard.fullname, processor.fullname, motherboard.fullname, cool.fullname,
		ram.fullname, disk.fullname, power.fullname, body.fullname
	FROM videocard, processor, motherboard, cool, ram, disk, power, body, configuration
	WHERE videocard.id = configuration.videocard_id
	AND processor.id = configuration.processor_id
	AND motherboard.id = configuration.motherboard_id
	AND cool.id = configuration.cool_id
	AND ram.id = configuration.ram_id
	AND disk.id = configuration.disk_id
	AND power.id = configuration.power_id
	AND body.id = configuration.body_id
$$ LANGUAGE sql;


-- Функция для получения конфигураций по клиенту (в ЛК)
CREATE OR REPLACE FUNCTION get_user_configuration(user_id_in INT)
RETURNS TABLE(
	id_conf INT,
	date_order DATE,
	price INT,
	video VARCHAR,
	proc VARCHAR,
	mother VARCHAR,
	cool VARCHAR,
	ram VARCHAR,
	disk VARCHAR,
	power VARCHAR,
	body VARCHAR
) AS $$
	SELECT configuration.id, configuration.date_create, configuration.price, videocard.fullname, processor.fullname, motherboard.fullname, cool.fullname,
		ram.fullname, disk.fullname, power.fullname, body.fullname
	FROM videocard, processor, motherboard, cool, ram, disk, power, body, configuration
	WHERE configuration.client_id = user_id_in
	AND videocard.id = configuration.videocard_id
	AND processor.id = configuration.processor_id
	AND motherboard.id = configuration.motherboard_id
	AND cool.id = configuration.cool_id
	AND ram.id = configuration.ram_id
	AND disk.id = configuration.disk_id
	AND power.id = configuration.power_id
	AND body.id = configuration.body_id
$$ LANGUAGE sql;