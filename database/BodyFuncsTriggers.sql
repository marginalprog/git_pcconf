
--Функции и триггеры корпуса

-- Функция создания нового производителя
CREATE OR REPLACE FUNCTION insert_proizv_body(
	VARCHAR(50))
RETURNS void AS $$
BEGIN
	INSERT INTO proizv_body(name)
	VALUES ($1);
END;
$$ LANGUAGE plpgsql;

-- Функция создания корпуса
CREATE OR REPLACE FUNCTION insert_body(
	INT,
	VARCHAR(50),
	VARCHAR,
	VARCHAR(50),
	VARCHAR(255),
	VARCHAR(255),
	INT,
	INT,
	INT,
	DECIMAL(5,2),
	VARCHAR(50),
	INT)
	RETURNS void AS $$
BEGIN
	INSERT INTO body(id_proizv, fullname, gaming, type, ffmother, ffpower,
					lengthvideo, heightcool, lengthpower, weight, color, price)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12);
END;
$$ LANGUAGE plpgsql;

--- Функция вывода данных о корпусах
CREATE OR REPLACE FUNCTION get_all_body()
RETURNS TABLE(
	kol INT, 
	body_exist BOOL,
	body_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	type VARCHAR,
	ffmother VARCHAR,
	ffpower VARCHAR,
	lengthvideo INT,
	heightcool INT,
	lengthpower INT,
	weight DECIMAL,
	color VARCHAR,
	price INT
) AS $$
	SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, 
			fullname, gaming, type, ffmother, ffpower,
			lengthvideo, heightcool, lengthpower, weight, color, price
	FROM body, sklad_body, proizv_body
	WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id
	ORDER BY exist DESC
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_having_body()
RETURNS TABLE(
	kol INT, 
	body_exist BOOL,
	body_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	type VARCHAR,
	ffmother VARCHAR,
	ffpower VARCHAR,
	lengthvideo INT,
	heightcool INT,
	lengthpower INT,
	weight DECIMAL,
	color VARCHAR,
	price INT
) AS $$
	SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, 
			fullname, gaming, type, ffmother, ffpower,
			lengthvideo, heightcool, lengthpower, weight, color, price
	FROM body, sklad_body, proizv_body
	WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id
	AND body.exist = True
	ORDER BY exist DESC
$$ LANGUAGE sql;

-- Функция для фильтрации корпусов по производителю
CREATE OR REPLACE FUNCTION get_body_by_name(name_pr VARCHAR)
RETURNS TABLE(
	kol INT, 
	body_exist BOOL,
	body_Id INT,   
	proizv_name VARCHAR, 
	fullname VARCHAR,
	gaming VARCHAR,
	type VARCHAR,
	ffmother VARCHAR,
	ffpower VARCHAR,
	lengthvideo INT,
	heightcool INT,
	lengthpower INT,
	weight DECIMAL,
	color VARCHAR,
	price INT
) AS $$
	SELECT kol, body.exist, body.id, proizv_body.name, 
			fullname, gaming, type, ffmother, ffpower,
			lengthvideo, heightcool, lengthpower, weight, color, price
	FROM body, sklad_body, proizv_body
	WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id AND name = name_pr
	ORDER BY exist DESC
$$ LANGUAGE sql;


-- Функция вывода всех производителей, чьи корпуса есть в базе (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_inbase_bodyproizv()
RETURNS TABLE(name VARCHAR) AS $$
	SELECT DISTINCT name FROM proizv_body, body
	WHERE proizv_body.id = body.id_proizv
	ORDER BY name ASC
$$ LANGUAGE sql;

-- Функция вывода производителей, чьи корпуса В НАЛИЧИИ (для заполнения фильтрующих вкладок tabwidget)
CREATE OR REPLACE FUNCTION get_having_bodyproizv()
RETURNS TABLE(name VARCHAR) AS $$
	SELECT DISTINCT name FROM proizv_body, body
	WHERE proizv_body.id = body.id_proizv
	AND body.exist = True
	ORDER BY name ASC
$$ LANGUAGE sql;


-- Триггер создания новой корпуса (с созданием нового поля на складе
CREATE OR REPLACE FUNCTION insert_skladbody()
RETURNS trigger
AS $$
BEGIN
	INSERT INTO sklad_body(id_izd)
	VALUES (NEW.id);
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER sklad_body_insert_trigger
AFTER INSERT
ON "body" -- при добавление НОВОЙ корпуса создаем поле склада
FOR EACH ROW
EXECUTE PROCEDURE insert_skladbody();

CREATE OR REPLACE FUNCTION insert_order_body(
	INT,
	INT,
	DATE)
	RETURNS void AS $$
BEGIN
	INSERT INTO order_body(id_izd, kol, date)
	VALUES ($1, $2, $3);
END;
$$ LANGUAGE plpgsql;


-- Триггер пересчёта количество корпусов на складе
CREATE OR REPLACE FUNCTION update_skladbody()
RETURNS trigger
AS $$
DECLARE
	old_skl_kol int;
	new_skl_kol int;
BEGIN
	old_skl_kol = (SELECT SUM(kol) FROM sklad_body
					WHERE id_izd = NEW.id_izd);
	new_skl_kol = old_skl_kol + NEW.kol;
	UPDATE sklad_body
	SET kol = new_skl_kol
    	WHERE id_izd=NEW.id_izd;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_sklad_body_trigger
AFTER INSERT
ON "order_body" -- После создания заказа пересчитать количество корпусов
FOR EACH ROW
EXECUTE PROCEDURE update_skladbody();

-- Функция вывода производителей корпуса
CREATE OR REPLACE FUNCTION get_proizv_body()
RETURNS TABLE(id INT, exist BOOLEAN, name VARCHAR(50)) AS $$
	SELECT * FROM proizv_body ORDER BY exist DESC, name ASC
$$ LANGUAGE sql;

-- Функция обновления договора производителя корпуса
CREATE OR REPLACE FUNCTION update_body_dogovor(BOOL, VARCHAR) 
RETURNS void AS $$
BEGIN
	UPDATE proizv_body SET exist = $1 WHERE name = $2;
END;
$$ LANGUAGE plpgsql;


-- Триггер на обновление состояния корпуса
CREATE OR REPLACE FUNCTION update_body_exist()
RETURNS TRIGGER AS $$
BEGIN
	IF new.kol>0 
		THEN
			update body set exist = True
        	where id = new.id_izd;
    end if;
	IF new.kol = 0 then
			update body set exist = False
        	where id = new.id_izd;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_body_exist_trigger
	AFTER UPDATE ON sklad_body FOR EACH ROW
	EXECUTE PROCEDURE update_body_exist();
	