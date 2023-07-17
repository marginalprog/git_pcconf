
--Функции и триггеры блока питания


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_power(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_power(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания блока питания
CREATE OR REPLACE FUNCTION insert_power(
	INT,
	VARCHAR(50),
	VARCHAR(255),
	INT,
	INT,
	VARCHAR(15),
	VARCHAR(20),
	INT,
	INT,
	INT,
	INT,
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO power(id_proizv, fullname, formfactor, length, power,
					certificate, pinmain, connproc, connvideo, pinsata,
					kolconnproc, kolconnvideo, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о блоке питания
CREATE OR REPLACE FUNCTION get_all_power()
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_power()
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id
	AND power.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации блока питания по формфактору
CREATE OR REPLACE FUNCTION get_power_by_factor(factor_in VARCHAR)
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id 
	AND formfactor = factor_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


---------питание В НАЛИЧИИ по фактору
CREATE OR REPLACE FUNCTION get_having_power_by_factor(factor_in VARCHAR)
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id 
	AND formfactor = factor_in
	AND power.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

--ЗАКАЗЫ
CREATE OR REPLACE FUNCTION get_having_order_power()
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	power_date DATE,
	power_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id,
			order_power.date, order_power.kol, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power, order_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id 
	AND order_power.id_izd = power.id
	AND power.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_all_order_power()
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	power_date DATE,
	power_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id,
			order_power.date, order_power.kol, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power, order_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id 
	AND order_power.id_izd = power.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации БП по формфактору
CREATE OR REPLACE FUNCTION get_order_power_by_factor(factor_in VARCHAR)
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	power_date DATE,
	power_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id,
			order_power.date, order_power.kol, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power, order_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id
	AND order_power.id_izd = power.id
	AND formfactor = factor_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_having_order_power_by_factor(factor_in VARCHAR)
RETURNS TABLE(
	kol INT,
	power_exist BOOL,
	power_id INT,
	power_date DATE,
	power_order_kol INT,
	proizv_name VARCHAR,
	fullname VARCHAR,
	formfactor VARCHAR,
	length INT,
	power INT,
	certificate VARCHAR,
	pinmain VARCHAR, 
	pinsata INT,
	connproc INT, 
	kolconnproc INT, 
	connvideo INT, 
	kolconnvideo INT,
	price INT
) AS $$
	SELECT sklad_power.kol, power.exist, power.id,
			order_power.date, order_power.kol, proizv_power.name,
			fullname, formfactor, length, power, certificate, pinmain,
			pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price
	FROM power, sklad_power, proizv_power, order_power
	WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id 
	AND order_power.id_izd = power.id
	AND formfactor = factor_in
	AND power.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех фф, что есть в базе блока питания (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_powerfactor()
RETURNS TABLE(formfactor VARCHAR) AS $$
	SELECT DISTINCT formfactor FROM power
	ORDER BY formfactor ASC
$$ LANGUAGE sql;

-- Функция вывода блоков питания с фф в НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_powerfactor()
RETURNS TABLE(formfactor VARCHAR) AS $$
	SELECT DISTINCT formfactor FROM power
	WHERE power.exist = True
	ORDER BY formfactor ASC
$$ LANGUAGE sql;


-- Триггер создания нового поля БП на складе
CREATE OR REPLACE FUNCTION insert_skladpower()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_power(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_power_insert_trigger
AFTER INSERT
ON "power" -- при добавлении НОВОГО блока питания создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladpower();

CREATE OR REPLACE FUNCTION insert_order_power(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_power(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггерная функция пересчёта количества блоков питания на складе
CREATE OR REPLACE FUNCTION update_skladpower()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_power
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_power
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_power_trigger
AFTER INSERT
ON "order_power" -- После создания заказа пересчитать количество 
FOR EACH ROW
EXECUTE PROCEDURE update_skladpower();

-- Функция вывода производителей блоков питания
CREATE OR REPLACE FUNCTION get_proizv_power()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_power ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя
CREATE OR REPLACE FUNCTION update_power_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_power SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния блока питания
CREATE OR REPLACE FUNCTION update_power_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update power set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update power set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_power_exist_trigger
	AFTER UPDATE ON sklad_power FOR EACH ROW
	EXECUTE PROCEDURE update_power_exist();
	