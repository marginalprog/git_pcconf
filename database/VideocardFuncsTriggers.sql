
---------------------------------------------------Функции и триггеры видеокарты-----------------------------------------------------


-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_videocard(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_videocard(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания видеокарты
CREATE OR REPLACE FUNCTION insert_videocard(
	INT,
	VARCHAR(50),
	BOOL,
	VARCHAR(25),
	VARCHAR(25),
	INT,
	VARCHAR(10),
	INT,
	INT,
	VARCHAR(20),
	INT,
	VARCHAR(25),
	INT,
	INT,
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO videocard(id_proizv,fullname, gaming, chipcreator, chipname, vram, 
						  typevram, frequency, bus, interface, monitor,
					   	  resolution, tdp, length, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о видеокартах
CREATE OR REPLACE FUNCTION get_all_videocard()
RETURNS TABLE(
	kol INT, 
	videocard_exist BOOL,
	videocard_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	chipcreator VARCHAR, 
	chipname VARCHAR, 
	vram INT, 
	typevram VARCHAR, 
	frequency INT, 
	bus INT, 
	interface VARCHAR, 
	monitor INT, 
	resolution VARCHAR, 
	tdp INT, 
	length INT, 
	price INT
) AS $$
	SELECT sklad_videocard.kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price
	FROM videocard, sklad_videocard, proizv_videocard
	WHERE videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_videocard()
RETURNS TABLE(
	kol INT, 
	videocard_exist BOOL,
	videocard_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	chipcreator VARCHAR, 
	chipname VARCHAR, 
	vram INT, 
	typevram VARCHAR, 
	frequency INT, 
	bus INT, 
	interface VARCHAR, 
	monitor INT, 
	resolution VARCHAR, 
	tdp INT, 
	length INT, 
	price INT
) AS $$
	SELECT sklad_videocard.kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price
	FROM videocard, sklad_videocard, proizv_videocard
	WHERE videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id
	AND videocard.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации видеокарт по производителю
CREATE OR REPLACE FUNCTION get_videocard_by_name(name_pr VARCHAR)
RETURNS TABLE(
	kol INT, 
	videocard_exist BOOL,
	videocard_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming BOOL,
	chipcreator VARCHAR, 
	chipname VARCHAR, 
	vram INT, 
	typevram VARCHAR, 
	frequency INT, 
	bus INT, 
	interface VARCHAR, 
	monitor INT, 
	resolution VARCHAR, 
	tdp INT, 
	length INT, 
	price INT
) AS $$
	SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price
	FROM videocard, sklad_videocard, proizv_videocard
	WHERE videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id AND name = name_pr
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех производителей, чьи видеокарты есть в базе (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_videoproizv()
RETURNS TABLE(name VARCHAR) AS $$
	SELECT DISTINCT name FROM proizv_videocard, videocard
	WHERE proizv_videocard.id = videocard.id_proizv
	ORDER BY name ASC
$$ LANGUAGE sql;

-- Функция вывода производителей, чьи видеокарты В НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_videoproizv()
RETURNS TABLE(name VARCHAR) AS $$
	SELECT DISTINCT name FROM proizv_videocard, videocard
	WHERE proizv_videocard.id = videocard.id_proizv
	AND videocard.exist = True
	ORDER BY name ASC
$$ LANGUAGE sql;


-- Триггер создания новой видеокарты (с созданием нового поля на складе
CREATE OR REPLACE FUNCTION insert_skladvideo()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_videocard(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_video_insert_trigger
AFTER INSERT
ON "videocard" -- при добавление НОВОЙ видеокарты создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladvideo();

CREATE OR REPLACE FUNCTION insert_order_videocard(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_videocard(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количество видеокарт на складе
CREATE OR REPLACE FUNCTION update_skladvideo()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_videocard
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_videocard
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_videocard_trigger
AFTER INSERT
ON "order_videocard" -- После создания заказа пересчитать количество видеокарт
FOR EACH ROW
EXECUTE PROCEDURE update_skladvideo();

-- Функция вывода производителей видеокарты
CREATE OR REPLACE FUNCTION get_proizv_videocard()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_videocard ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя видеокарты
CREATE OR REPLACE FUNCTION update_video_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_videocard SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния видеокарты
CREATE OR REPLACE FUNCTION update_videocard_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update videocard set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update videocard set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_videocard_exist_trigger
	AFTER UPDATE ON sklad_videocard FOR EACH ROW
	EXECUTE PROCEDURE update_videocard_exist();
	
	
--------------------------------------------------------------------------------------------------------------------------------------


select  get_proizv_videocard()


SELECT insert_proizv('GIGABYTE')
SELECT insert_videocard(1,'GIGABYTE GeForce RTX 3050 EAGLE OC', 'NVIDIA', 'RTX 3050', 8192, 'GDDR6', 1552, 256, 'PCI-E 4.0', 4, '7680x4320', 130, 28, 29250);
SELECT insert_order_videocard(5, 2, '05.04.2023')

SELECT insert_proizv('MSI')
SELECT insert_videocard(2,'MSI AMD Radeon RX 6600', 'AMD', 'RX 6600', 8192, 'GDDR6', 2044, 128, 'PCI-E 4.0', 4, '7680x4320', 132, 33, 26490);
SELECT insert_order_videocard(6, 2, '05.04.2023')



