
--Функции и триггеры озу


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_ram(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_ram(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания озу
CREATE OR REPLACE FUNCTION insert_ram(
	INT,
	VARCHAR(50),
	BOOL,
	VARCHAR(20),
	INT,
	INT,
	INT,
	INT,
	DECIMAL(4,1),
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO ram(id_proizv, fullname, gaming, type, volume, frequency,
					complect, latency, voltage, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных об озу
CREATE OR REPLACE FUNCTION get_all_ram()
RETURNS TABLE(
	kol INT,
	ram_exist BOOL,
	ram_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	gaming BOOL,
	type VARCHAR,
	volume INT, 
	frequency INT, 
	complect INT, 
	latency INT,
	voltage DECIMAL, 
	price INT
) AS $$
	SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name,
			fullname, gaming, type, volume, frequency,
			complect, latency, voltage, price
	FROM ram, sklad_ram, proizv_ram
	WHERE ram.id = sklad_ram.id_izd AND ram.id_proizv = proizv_ram.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_ram()
RETURNS TABLE(
	kol INT,
	ram_exist BOOL,
	ram_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	gaming BOOL,
	type VARCHAR,
	volume INT, 
	frequency INT, 
	complect INT, 
	latency INT,
	voltage DECIMAL, 
	price INT
) AS $$
	SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, 
			fullname, gaming, type, volume, frequency,
			complect, latency, voltage, price
	FROM ram, sklad_ram, proizv_ram
	WHERE ram.id = sklad_ram.id_izd AND ram.id_proizv = proizv_ram.id
	AND ram.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации охлаждения по типу
CREATE OR REPLACE FUNCTION get_ram_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	ram_exist BOOL,
	ram_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	gaming BOOL,
	type VARCHAR,
	volume INT, 
	frequency INT, 
	complect INT, 
	latency INT,
	voltage DECIMAL, 
	price INT
) AS $$
	SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name,
			fullname, gaming, type, volume, frequency,
			complect, latency, voltage, price
	FROM ram, sklad_ram, proizv_ram
	WHERE ram.id = sklad_ram.id_izd AND ram.id_proizv = proizv_ram.id AND type = type_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех типов, что есть в базе озу (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_ramtype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM ram
	ORDER BY type ASC
$$ LANGUAGE sql;

-- Функция вывода озу, с сокетами в НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_ramtype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM ram
	WHERE ram.exist = True
	ORDER BY type ASC
$$ LANGUAGE sql;


-- Триггер создания нового материнской платы (с созданием нового поля на складе)
CREATE OR REPLACE FUNCTION insert_skladram()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_ram(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER sklad_ram_insert_trigger
AFTER INSERT
ON "ram" -- при добавлении НОВОГО охлаждения создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladram();

CREATE OR REPLACE FUNCTION insert_order_ram(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_ram(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количества озу на складе
CREATE OR REPLACE FUNCTION update_skladram()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_ram
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_ram
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_sklad_ram_trigger
AFTER INSERT
ON "order_ram" -- После создания заказа пересчитать количество 
FOR EACH ROW
EXECUTE PROCEDURE update_skladram();

-- Функция вывода производителей озу
CREATE OR REPLACE FUNCTION get_proizv_ram()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_ram ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя
CREATE OR REPLACE FUNCTION update_ram_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_ram SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния материнской платы
CREATE OR REPLACE FUNCTION update_ram_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update ram set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update ram set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_ram_exist_trigger
	AFTER UPDATE ON sklad_ram FOR EACH ROW
	EXECUTE PROCEDURE update_ram_exist();
