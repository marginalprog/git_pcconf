
--Функции и триггеры охлаждения


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_cool(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_cool(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания охлаждения
CREATE OR REPLACE FUNCTION insert_cool(
	INT,
	VARCHAR(50),
	VARCHAR(50),
	VARCHAR(50),
	VARCHAR(255),
	INT,
	INT,
	INT,
	INT,
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO cool(id_proizv, fullname, construction, type, socket, heatpipe, 
					 height, disperse, voltage, conncool, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных об охлаждении
CREATE OR REPLACE FUNCTION get_all_cool()
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT, 
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_cool()
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT,
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	AND cool.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации охлаждения по типу
CREATE OR REPLACE FUNCTION get_cool_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT, 
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id AND type = type_in
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_cool_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT, 
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id 
	AND type = type_in
	AND cool.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

--ЗАКАЗЫ
CREATE OR REPLACE FUNCTION get_having_order_cool()
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	cool_date DATE,
	cool_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT,
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, 
			order_cool.date, order_cool.kol, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool, order_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	AND order_cool.id_izd = cool.id
	AND cool.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_all_order_cool()
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	cool_date DATE,
	cool_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT,
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, 
			order_cool.date, order_cool.kol, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool, order_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	AND order_cool.id_izd = cool.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации охлаждения по типу
CREATE OR REPLACE FUNCTION get_order_cool_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	cool_date DATE,
	cool_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT,
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, 
			order_cool.date, order_cool.kol, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool, order_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	AND order_cool.id_izd = cool.id
	AND type = type_in
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_order_cool_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	cool_exist BOOL,
	cool_id INT,
	cool_date DATE,
	cool_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	construction VARCHAR,
	type VARCHAR,
	socket VARCHAR, 
	heatpipe INT, 
	height INT,
	disperse INT,
	voltage INT,
	conncool INT,
	price INT
) AS $$
	SELECT sklad_cool.kol, cool.exist, cool.id, 
			order_cool.date, order_cool.kol, proizv_cool.name,
			fullname, construction, type, socket, heatpipe, 
			height, disperse, voltage, conncool, price
	FROM cool, sklad_cool, proizv_cool, order_cool
	WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id
	AND order_cool.id_izd = cool.id
	AND type = type_in
	AND cool.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех типов, что есть в базе охлаждения (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_cooltype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM cool
	ORDER BY type ASC
$$ LANGUAGE sql;

-- Функция вывода охлаждений с типами в НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_cooltype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM cool
	WHERE cool.exist = True
	ORDER BY type ASC
$$ LANGUAGE sql;


-- Триггер создания нового материнской платы (с созданием нового поля на складе)
CREATE OR REPLACE FUNCTION insert_skladcool()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_cool(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_cool_insert_trigger
AFTER INSERT
ON "cool" -- при добавлении НОВОГО охлаждения создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladcool();

CREATE OR REPLACE FUNCTION insert_order_cool(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_cool(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количество охлаждения на складе
CREATE OR REPLACE FUNCTION update_skladcool()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_cool
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_cool
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_cool_trigger
AFTER INSERT
ON "order_cool" -- После создания заказа пересчитать количество 
FOR EACH ROW
EXECUTE PROCEDURE update_skladcool();

-- Функция вывода производителей охлаждений
CREATE OR REPLACE FUNCTION get_proizv_cool()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_cool ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя
CREATE OR REPLACE FUNCTION update_cool_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_cool SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния охлаждения
CREATE OR REPLACE FUNCTION update_cool_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update cool set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update cool set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_cool_exist_trigger
	AFTER UPDATE ON sklad_cool FOR EACH ROW
	EXECUTE PROCEDURE update_cool_exist();
	