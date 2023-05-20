
--Функции и триггеры накопителя


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_disk(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_disk(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания накопителя
CREATE OR REPLACE FUNCTION insert_disk(
	INT,
	VARCHAR(50),
	VARCHAR(30),
	INT,
	VARCHAR(20),
	INT,
	INT,
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO disk(id_proizv, fullname, type, volume, 
					connect, read, write, rpm, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о накопителе
CREATE OR REPLACE FUNCTION get_all_disk()
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_disk()
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name, 
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id
	AND disk.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации накопителя по типу
CREATE OR REPLACE FUNCTION get_disk_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id AND type = type_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


--накопители В НАЛИЧИИ по типу
CREATE OR REPLACE FUNCTION get_having_disk_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id 
	AND type = type_in
	AND disk.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


--ЗАКАЗЫ
CREATE OR REPLACE FUNCTION get_having_order_disk()
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	disk_date DATE,
	disk_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id,
			order_disk.date, order_disk.kol, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk, order_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id 
	AND order_disk.id_izd = disk.id
	AND disk.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_all_order_disk()
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	disk_date DATE,
	disk_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id,
			order_disk.date, order_disk.kol, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk, order_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id 
	AND order_disk.id_izd = disk.id
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция для фильтрации накопителей по типу
CREATE OR REPLACE FUNCTION get_order_disk_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	disk_date DATE,
	disk_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id,
			order_disk.date, order_disk.kol, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk, order_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id
	AND order_disk.id_izd = disk.id
	AND type = type_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_having_order_disk_by_type(type_in VARCHAR)
RETURNS TABLE(
	kol INT,
	disk_exist BOOL,
	disk_id INT,
	disk_date DATE,
	disk_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	type VARCHAR,
	volume INT,
	connect VARCHAR, 
	read INT, 
	write INT, 
	rpm INT,
	price INT
) AS $$
	SELECT sklad_disk.kol, disk.exist, disk.id,
			order_disk.date, order_disk.kol, proizv_disk.name,
			fullname, type, volume, connect, read, write, rpm, price
	FROM disk, sklad_disk, proizv_disk, order_disk
	WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id
	AND order_disk.id_izd = disk.id
	AND type = type_in
	AND disk.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех типов, что есть в базе накопителя (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_disktype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM disk
	ORDER BY type ASC
$$ LANGUAGE sql;

-- Функция вывода накопителей с типами в НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_disktype()
RETURNS TABLE(type VARCHAR) AS $$
	SELECT DISTINCT type FROM disk
	WHERE disk.exist = True
	ORDER BY type ASC
$$ LANGUAGE sql;


-- Триггер создания нового поля диска (с созданием нового поля на складе)
CREATE OR REPLACE FUNCTION insert_skladdisk()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_disk(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_disk_insert_trigger
AFTER INSERT
ON "disk" -- при добавлении НОВОГО накопителя создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladdisk();

CREATE OR REPLACE FUNCTION insert_order_disk(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_disk(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количества накопителей на складе
CREATE OR REPLACE FUNCTION update_skladdisk()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_disk
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_disk
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_disk_trigger
AFTER INSERT
ON "order_disk" -- После создания заказа пересчитать количество 
FOR EACH ROW
EXECUTE PROCEDURE update_skladdisk();

-- Функция вывода производителей накопителей
CREATE OR REPLACE FUNCTION get_proizv_disk()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_disk ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя
CREATE OR REPLACE FUNCTION update_disk_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_disk SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния накопителя
CREATE OR REPLACE FUNCTION update_disk_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update disk set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update disk set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_disk_exist_trigger
	AFTER UPDATE ON sklad_disk FOR EACH ROW
	EXECUTE PROCEDURE update_disk_exist();
	