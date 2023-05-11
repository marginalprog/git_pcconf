
---------------------------------------------------Функции и триггеры мат. платы-----------------------------------------------------


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_motherboard(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_motherboard(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания материнской платы
CREATE OR REPLACE FUNCTION insert_motherboard(
	INT,
	VARCHAR(50),
	BOOL,
	VARCHAR(20),
	VARCHAR(20),
	VARCHAR(30),
	VARCHAR(30),
	VARCHAR(20),
	INT,
	INT,
	INT,
	INT,
	INT,
	INT,
	INT,
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO motherboard(id_proizv, fullname, gaming, socket, chipset, formfactor, 
						    pcie, memorytype, memoryslot, memorymax, memoryfreqmax,
						    m2, sata, conncool, connproc, kolconnproc, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о материнских платах
CREATE OR REPLACE FUNCTION get_all_motherboard()
RETURNS TABLE(
	kol INT, 
	motherboard_exist BOOL,
	motherboard_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	socket VARCHAR, 
	chipset VARCHAR, 
	formfactor VARCHAR,
	pcie VARCHAR,
	memorytype VARCHAR, 
	memoryslot INT, 
	memorymax INT, 
	memoryfreqmax INT,
	m2 INT,
	sata INT,
	conncool INT,
	connproc INT,
	kolconnproc INT,
	price INT
) AS $$
	SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name,
			fullname, gaming, socket, chipset, formfactor, pcie, 
			memorytype, memoryslot, memorymax, memoryfreqmax,
			m2, sata, conncool, connproc, kolconnproc, price
	FROM motherboard, sklad_motherboard, proizv_motherboard
	WHERE motherboard.id = sklad_motherboard.id_izd AND motherboard.id_proizv = proizv_motherboard.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_motherboard()
RETURNS TABLE(
	kol INT, 
	motherboard_exist BOOL,
	motherboard_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	socket VARCHAR, 
	chipset VARCHAR, 
	formfactor VARCHAR,
	pcie VARCHAR,
	memorytype VARCHAR, 
	memoryslot INT, 
	memorymax INT, 
	memoryfreqmax INT,
	m2 INT,
	sata INT, 
	conncool INT,
	connproc INT,
	kolconnproc INT,
	price INT
) AS $$
	SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name,
			fullname, gaming, socket, chipset, formfactor, pcie, 
			memorytype, memoryslot, memorymax, memoryfreqmax,
			m2, sata, conncool, connproc, kolconnproc, price
	FROM motherboard, sklad_motherboard, proizv_motherboard
	WHERE motherboard.id = sklad_motherboard.id_izd AND motherboard.id_proizv = proizv_motherboard.id
	AND motherboard.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации материнских плат по сокету
CREATE OR REPLACE FUNCTION get_motherboard_by_socket(socket_in VARCHAR)
RETURNS TABLE(
	kol INT, 
	motherboard_exist BOOL,
	motherboard_id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	socket VARCHAR, 
	chipset VARCHAR, 
	formfactor VARCHAR,
	pcie VARCHAR,
	memorytype VARCHAR, 
	memoryslot INT, 
	memorymax INT, 
	memoryfreqmax INT,
	m2 INT,
	sata INT, 
	conncool INT,
	connproc INT,
	kolconnproc INT,
	price INT
) AS $$
	SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name,
			fullname, gaming, socket, chipset, formfactor, pcie, 
			memorytype, memoryslot, memorymax, memoryfreqmax,
			m2, sata, conncool, connproc, kolconnproc, price
	FROM motherboard, sklad_motherboard, proizv_motherboard
	WHERE motherboard.id = sklad_motherboard.id_izd AND motherboard.id_proizv = proizv_motherboard.id AND socket = socket_in
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех сокеты, что есть в базе материнских плат (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_mothersocket()
RETURNS TABLE(socket VARCHAR) AS $$
	SELECT DISTINCT socket FROM motherboard
	ORDER BY socket ASC
$$ LANGUAGE sql;

-- Функция вывода материнских плат, с сокетами в НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_mothersocket()
RETURNS TABLE(socket VARCHAR) AS $$
	SELECT DISTINCT socket FROM motherboard
	WHERE motherboard.exist = True
	ORDER BY socket ASC
$$ LANGUAGE sql;


-- Триггер создания нового материнской платы (с созданием нового поля на складе)
CREATE OR REPLACE FUNCTION insert_skladmother()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_motherboard(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_mother_insert_trigger
AFTER INSERT
ON "motherboard" -- при добавление НОВОЙ материнской платы создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladmother();

CREATE OR REPLACE FUNCTION insert_order_motherboard(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_motherboard(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количество мат.плат на складе
CREATE OR REPLACE FUNCTION update_skladmother()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_motherboard
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_motherboard
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_motherboard_trigger
AFTER INSERT
ON "order_motherboard" -- После создания заказа пересчитать количество материнских плат
FOR EACH ROW
EXECUTE PROCEDURE update_skladmother();

-- Функция вывода производителей материнских плат
CREATE OR REPLACE FUNCTION get_proizv_motherboard()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_motherboard ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя мат.плат
CREATE OR REPLACE FUNCTION update_mother_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_motherboard SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния материнской платы
CREATE OR REPLACE FUNCTION update_motherboard_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update motherboard set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update motherboard set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_motherboard_exist_trigger
	AFTER UPDATE ON sklad_motherboard FOR EACH ROW
	EXECUTE PROCEDURE update_motherboard_exist();
	