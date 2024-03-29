
---------------------------------------------------Функции и триггеры процессора-----------------------------------------------------


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_processor(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_processor(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания процессора
CREATE OR REPLACE FUNCTION insert_processor(
	INT,
	VARCHAR(50),
	VARCHAR,
	VARCHAR(50),
	VARCHAR(20),
	VARCHAR(30),
	INT,
	INT,
	INT,
	VARCHAR(40),
	INT,
	VARCHAR(50),
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO processor(id_proizv, fullname, gaming, series, socket, core, ncores, 
						  cache, frequency, techproc, ramfreq, graphics, tdp, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о процессорах
CREATE OR REPLACE FUNCTION get_all_processor()
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_processor()
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,	
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	AND processor.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция для фильтрации процессоров по серии
CREATE OR REPLACE FUNCTION get_processor_by_series(series_in VARCHAR)
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, graphics, tdp, price	
	FROM processor, sklad_processor, proizv_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id AND series = series_in
	ORDER BY exist DESC
$$ LANGUAGE sql;

---------процессоры В НАЛИЧИИ по серии
CREATE OR REPLACE FUNCTION get_having_processor_by_series(series_in VARCHAR)
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, graphics, tdp, price	
	FROM processor, sklad_processor, proizv_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id AND series = series_in
	AND processor.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

--ЗАКАЗЫ
CREATE OR REPLACE FUNCTION get_having_order_processor()
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,  
	processor_date DATE,
	processor_order_kol INT,
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,	
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, order_processor.date, order_processor.kol,
	proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, 
	frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor, order_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	AND order_processor.id_izd = processor.id
	AND processor.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_all_order_processor()
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,  
	processor_date DATE,
	processor_order_kol INT,
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,	
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, order_processor.date, order_processor.kol,
	proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, 
	frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor, order_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	AND order_processor.id_izd = processor.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации процессоров по серии
CREATE OR REPLACE FUNCTION get_order_processor_by_series(series_in VARCHAR)
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,  
	processor_date DATE,
	processor_order_kol INT,
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,	
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, order_processor.date, order_processor.kol,
	proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, 
	frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor, order_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	AND order_processor.id_izd = processor.id 
	AND series = series_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_having_order_processor_by_series(series_in VARCHAR)
RETURNS TABLE(
	kol INT, 
	processor_exist BOOL,
	processor_id INT,  
	processor_date DATE,
	processor_order_kol INT,
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	series VARCHAR,
	socket VARCHAR, 
	core VARCHAR, 
	ncores INT, 
	cache INT, 
	frequency INT, 
	techproc VARCHAR, 
	ramfreq INT,
	graphics VARCHAR,	
	tdp INT, 
	price INT
) AS $$
	SELECT sklad_processor.kol, processor.exist, processor.id, order_processor.date, order_processor.kol,
	proizv_processor.name, fullname, gaming, series, socket, core, ncores, cache, 
	frequency, techproc, ramfreq, graphics, tdp, price
	FROM processor, sklad_processor, proizv_processor, order_processor
	WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id
	AND order_processor.id_izd = processor.id 
	AND series = series_in
	AND processor.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция вывода всех серий процессоров что есть базе (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_procseries()
RETURNS TABLE(series VARCHAR) AS $$
	SELECT DISTINCT series FROM processor
	ORDER BY series ASC
$$ LANGUAGE sql;

-- Функция вывода серий процессоров которые В НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_procseries()
RETURNS TABLE(series VARCHAR) AS $$
	SELECT DISTINCT series FROM processor
	WHERE processor.exist = True
	ORDER BY series ASC
$$ LANGUAGE sql;


-- Триггер создания нового процессора (с созданием нового поля на складе)
CREATE OR REPLACE FUNCTION insert_skladproc()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_processor(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_proc_insert_trigger
AFTER INSERT
ON "processor" -- при добавление НОВОГО процессора создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladproc();

CREATE OR REPLACE FUNCTION insert_order_processor(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_processor(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количества процессоров на складе
CREATE OR REPLACE FUNCTION update_skladproc()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_processor
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_processor
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_processor_trigger
AFTER INSERT
ON "order_processor" -- После создания заказа пересчитать количество процессоров
FOR EACH ROW
EXECUTE PROCEDURE update_skladproc();

-- Функция вывода производителей процессоров
CREATE OR REPLACE FUNCTION get_proizv_processor()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_processor ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя процессора
CREATE OR REPLACE FUNCTION update_proc_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_processor SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния процессора
CREATE OR REPLACE FUNCTION update_processor_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update processor set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update processor set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_processor_exist_trigger
	AFTER UPDATE ON sklad_processor FOR EACH ROW
	EXECUTE PROCEDURE update_processor_exist();
	