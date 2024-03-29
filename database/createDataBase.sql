-- Last modification date: 2023-05-21 15:28:27.738

-- tables
-- Table: Body
CREATE TABLE Body (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming varchar(3)  NOT NULL,
    type varchar(50)  NOT NULL,
    ffmother varchar(255)  NOT NULL,
    ffpower varchar(255)  NOT NULL,
    lengthvideo int  NOT NULL,
    heightcool int  NOT NULL,
    lengthpower int  NOT NULL,
    weight decimal(5,2)  NOT NULL,
    color varchar(50)  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Body_pk PRIMARY KEY (id)
);

-- Table: Client
CREATE TABLE Client (
    id serial  NOT NULL,
    email Varchar(50)  NOT NULL,
    password text  NOT NULL,
    name Varchar(50)  NOT NULL,
    phone Varchar(20)  NOT NULL,
    registration date  NOT NULL,
    CONSTRAINT Client_pk PRIMARY KEY (id)
);

-- Table: Configuration
CREATE TABLE Configuration (
    id serial  NOT NULL,
    Client_id serial  NOT NULL,
    Power_id serial  NOT NULL,
    Body_id serial  NOT NULL,
    Videocard_id serial  NOT NULL,
    Processor_id serial  NOT NULL,
    Cool_id serial  NOT NULL,
    Motherboard_id serial  NOT NULL,
    Ram_id serial  NOT NULL,
    Disk_id serial  NOT NULL,
    price int  NOT NULL,
    date_create date  NOT NULL,
    CONSTRAINT Configuration_pk PRIMARY KEY (id)
);

-- Table: Cool
CREATE TABLE Cool (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    construction Varchar(50)  NOT NULL,
    type varchar(50)  NOT NULL,
    socket varchar(255)  NOT NULL,
    heatpipe int  NOT NULL,
    height int  NOT NULL,
    conncool int  NOT NULL,
    disperse int  NOT NULL,
    voltage int  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Cool_pk PRIMARY KEY (id)
);

-- Table: Disk
CREATE TABLE Disk (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    type varchar(30)  NOT NULL,
    volume int  NOT NULL,
    connect varchar(20)  NOT NULL,
    read int  NOT NULL,
    write int  NOT NULL,
    rpm int  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Disk_pk PRIMARY KEY (id)
);

-- Table: Motherboard
CREATE TABLE Motherboard (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming varchar(3)  NOT NULL,
    socket varchar(20)  NOT NULL,
    chipset varchar(20)  NOT NULL,
    formfactor varchar(30)  NOT NULL,
    pcie varchar(10)  NOT NULL,
    memorytype varchar(20)  NOT NULL,
    memoryslot int  NOT NULL,
    memorymax int  NOT NULL,
    memoryfreqmax int  NOT NULL,
    m2 varchar(20)  NOT NULL,
    sata int  NOT NULL,
    price int  NOT NULL,
    conncool int  NOT NULL,
    connproc int  NOT NULL,
    kolconnproc int  NOT NULL,
    CONSTRAINT Motherboard_pk PRIMARY KEY (id)
);

-- Table: Order_body
CREATE TABLE Order_body (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_body_pk PRIMARY KEY (id)
);

-- Table: Order_cool
CREATE TABLE Order_cool (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_cool_pk PRIMARY KEY (id)
);

-- Table: Order_disk
CREATE TABLE Order_disk (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_disk_pk PRIMARY KEY (id)
);

-- Table: Order_motherboard
CREATE TABLE Order_motherboard (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_motherboard_pk PRIMARY KEY (id)
);

-- Table: Order_power
CREATE TABLE Order_power (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_power_pk PRIMARY KEY (id)
);

-- Table: Order_processor
CREATE TABLE Order_processor (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_processor_pk PRIMARY KEY (id)
);

-- Table: Order_ram
CREATE TABLE Order_ram (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_ram_pk PRIMARY KEY (id)
);

-- Table: Order_videocard
CREATE TABLE Order_videocard (
    id serial  NOT NULL,
    id_izd serial  NOT NULL,
    kol int  NOT NULL CHECK (kol   >= 0),
    date date  NOT NULL,
    CONSTRAINT Order_videocard_pk PRIMARY KEY (id)
);

-- Table: Power
CREATE TABLE Power (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    formfactor varchar(255)  NOT NULL,
    length int  NOT NULL,
    power int  NOT NULL,
    certificate varchar(15)  NOT NULL,
    pinmain varchar(20)  NOT NULL,
    connproc varchar(20)  NOT NULL,
    connvideo varchar(20)  NOT NULL,
    pinsata int  NOT NULL,
    price int  NOT NULL,
    kolconnproc int  NOT NULL,
    kolconnvideo int  NOT NULL,
    CONSTRAINT Power_pk PRIMARY KEY (id)
);

-- Table: Processor
CREATE TABLE Processor (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming varchar(3)  NOT NULL,
    series varchar(50)  NOT NULL,
    socket varchar(20)  NOT NULL,
    core varchar(30)  NOT NULL,
    ncores int  NOT NULL,
    cache int  NOT NULL,
    frequency int  NOT NULL,
    techproc varchar(40)  NOT NULL,
    ramfreq int  NOT NULL,
    graphics varchar(50)  NOT NULL,
    tdp int  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Processor_pk PRIMARY KEY (id)
);

-- Table: Proizv_body
CREATE TABLE Proizv_body (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_body_pk PRIMARY KEY (id)
);

-- Table: Proizv_cool
CREATE TABLE Proizv_cool (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_cool_pk PRIMARY KEY (id)
);

-- Table: Proizv_disk
CREATE TABLE Proizv_disk (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_Disk_pk PRIMARY KEY (id)
);

-- Table: Proizv_motherboard
CREATE TABLE Proizv_motherboard (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_motherboard_pk PRIMARY KEY (id)
);

-- Table: Proizv_power
CREATE TABLE Proizv_power (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_power_pk PRIMARY KEY (id)
);

-- Table: Proizv_processor
CREATE TABLE Proizv_processor (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_processor_pk PRIMARY KEY (id)
);

-- Table: Proizv_ram
CREATE TABLE Proizv_ram (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_ram_pk PRIMARY KEY (id)
);

-- Table: Proizv_videocard
CREATE TABLE Proizv_videocard (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_videocard_pk PRIMARY KEY (id)
);

-- Table: Ram
CREATE TABLE Ram (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming varchar(3)  NOT NULL,
    type varchar(20)  NOT NULL,
    volume int  NOT NULL,
    frequency int  NOT NULL,
    complect int  NOT NULL,
    latency decimal(4,1)  NOT NULL,
    voltage decimal(4,1)  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Ram_pk PRIMARY KEY (id)
);

-- Table: Sklad_body
CREATE TABLE Sklad_body (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_cool
CREATE TABLE Sklad_cool (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_disk
CREATE TABLE Sklad_disk (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_motherboard
CREATE TABLE Sklad_motherboard (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_power
CREATE TABLE Sklad_power (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_processor
CREATE TABLE Sklad_processor (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Sklad_ram
CREATE TABLE Sklad_ram (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol  >= 0)
);

-- Table: Sklad_videocard
CREATE TABLE Sklad_videocard (
    id_izd serial  NOT NULL,
    kol int  NOT NULL DEFAULT 0 CHECK (kol   >= 0)
);

-- Table: Videocard
CREATE TABLE Videocard (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming varchar(3)  NOT NULL,
    chipcreator varchar(25)  NOT NULL,
    chipname varchar(25)  NOT NULL,
    vram int  NOT NULL,
    typevram varchar(10)  NOT NULL,
    frequency int  NOT NULL,
    bus int  NOT NULL,
    interface varchar(20)  NOT NULL,
    monitor int  NOT NULL,
    resolution varchar(25)  NOT NULL,
    tdp int  NOT NULL,
    length int  NOT NULL,
    price int  NOT NULL,
    connvideo int  NOT NULL,
    kolconnvideo int  NOT NULL,
    CONSTRAINT Videocard_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Body_Post_body (table: Body)
ALTER TABLE Body ADD CONSTRAINT Body_Post_body
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_body (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Body (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Body
    FOREIGN KEY (Body_id)
    REFERENCES Body (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Client (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Client
    FOREIGN KEY (Client_id)
    REFERENCES Client (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Cooling (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Cooling
    FOREIGN KEY (Cool_id)
    REFERENCES Cool (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Drive (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Drive
    FOREIGN KEY (Disk_id)
    REFERENCES Disk (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Motherboard (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Motherboard
    FOREIGN KEY (Motherboard_id)
    REFERENCES Motherboard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Power (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Power
    FOREIGN KEY (Power_id)
    REFERENCES Power (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Processor (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Processor
    FOREIGN KEY (Processor_id)
    REFERENCES Processor (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Ram (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Ram
    FOREIGN KEY (Ram_id)
    REFERENCES Ram (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Configuration_Videocard (table: Configuration)
ALTER TABLE Configuration ADD CONSTRAINT Configuration_Videocard
    FOREIGN KEY (Videocard_id)
    REFERENCES Videocard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Cool_Post_cool (table: Cool)
ALTER TABLE Cool ADD CONSTRAINT Cool_Post_cool
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_cool (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Disk_Post_Disk (table: Disk)
ALTER TABLE Disk ADD CONSTRAINT Disk_Post_Disk
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_disk (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Motherboard_Post_motherboard (table: Motherboard)
ALTER TABLE Motherboard ADD CONSTRAINT Motherboard_Post_motherboard
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_motherboard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_body_Body (table: Order_body)
ALTER TABLE Order_body ADD CONSTRAINT Order_body_Body
    FOREIGN KEY (id_izd)
    REFERENCES Body (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_cooling_Cooling (table: Order_cool)
ALTER TABLE Order_cool ADD CONSTRAINT Order_cooling_Cooling
    FOREIGN KEY (id_izd)
    REFERENCES Cool (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_drive_Drive (table: Order_disk)
ALTER TABLE Order_disk ADD CONSTRAINT Order_drive_Drive
    FOREIGN KEY (id_izd)
    REFERENCES Disk (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_motherboard_Motherboard (table: Order_motherboard)
ALTER TABLE Order_motherboard ADD CONSTRAINT Order_motherboard_Motherboard
    FOREIGN KEY (id_izd)
    REFERENCES Motherboard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_processor_Processor (table: Order_processor)
ALTER TABLE Order_processor ADD CONSTRAINT Order_processor_Processor
    FOREIGN KEY (id_izd)
    REFERENCES Processor (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_ram_Ram (table: Order_ram)
ALTER TABLE Order_ram ADD CONSTRAINT Order_ram_Ram
    FOREIGN KEY (id_izd)
    REFERENCES Ram (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Order_videocard_Videocard (table: Order_videocard)
ALTER TABLE Order_videocard ADD CONSTRAINT Order_videocard_Videocard
    FOREIGN KEY (id_izd)
    REFERENCES Videocard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Power_Post_power (table: Power)
ALTER TABLE Power ADD CONSTRAINT Power_Post_power
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_power (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Processor_Post_processor (table: Processor)
ALTER TABLE Processor ADD CONSTRAINT Processor_Post_processor
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_processor (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Ram_Post_ram (table: Ram)
ALTER TABLE Ram ADD CONSTRAINT Ram_Post_ram
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_ram (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_Videocard (table: Sklad_videocard)
ALTER TABLE Sklad_videocard ADD CONSTRAINT Sklad_Videocard
    FOREIGN KEY (id_izd)
    REFERENCES Videocard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_body_Body (table: Sklad_body)
ALTER TABLE Sklad_body ADD CONSTRAINT Sklad_body_Body
    FOREIGN KEY (id_izd)
    REFERENCES Body (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_cooling_Cooling (table: Sklad_cool)
ALTER TABLE Sklad_cool ADD CONSTRAINT Sklad_cooling_Cooling
    FOREIGN KEY (id_izd)
    REFERENCES Cool (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_drive_Drive (table: Sklad_disk)
ALTER TABLE Sklad_disk ADD CONSTRAINT Sklad_drive_Drive
    FOREIGN KEY (id_izd)
    REFERENCES Disk (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_mother_Motherboard (table: Sklad_motherboard)
ALTER TABLE Sklad_motherboard ADD CONSTRAINT Sklad_mother_Motherboard
    FOREIGN KEY (id_izd)
    REFERENCES Motherboard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_power_Power (table: Sklad_power)
ALTER TABLE Sklad_power ADD CONSTRAINT Sklad_power_Power
    FOREIGN KEY (id_izd)
    REFERENCES Power (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_processor_Processor (table: Sklad_processor)
ALTER TABLE Sklad_processor ADD CONSTRAINT Sklad_processor_Processor
    FOREIGN KEY (id_izd)
    REFERENCES Processor (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sklad_ram_Ram (table: Sklad_ram)
ALTER TABLE Sklad_ram ADD CONSTRAINT Sklad_ram_Ram
    FOREIGN KEY (id_izd)
    REFERENCES Ram (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Videocard_Post_videocard (table: Videocard)
ALTER TABLE Videocard ADD CONSTRAINT Videocard_Post_videocard
    FOREIGN KEY (id_proizv)
    REFERENCES Proizv_videocard (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: order_power_Power (table: Order_power)
ALTER TABLE Order_power ADD CONSTRAINT order_power_Power
    FOREIGN KEY (id_izd)
    REFERENCES Power (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Триггер вычитания из всех складов по 1 комплектующему
CREATE OR REPLACE FUNCTION update_all_sklad()
RETURNS trigger
AS $$
DECLARE
	old_video_kol int;
	new_video_kol int;
	
	old_proc_kol int;
	new_proc_kol int;
	
	old_mother_kol int;
	new_mother_kol int;
	
	old_cool_kol int;
	new_cool_kol int;
	
	old_ram_kol int;
	new_ram_kol int;
	
	old_disk_kol int;
	new_disk_kol int;
	
	old_power_kol int;
	new_power_kol int;
	
	old_body_kol int;
	new_body_kol int;
BEGIN
	old_video_kol = (SELECT SUM(kol) FROM sklad_videocard
					WHERE id_izd = NEW.videocard_id);
	new_video_kol = old_video_kol - 1;
	UPDATE sklad_videocard
	SET kol = new_video_kol
    	WHERE id_izd=NEW.videocard_id;
	
	old_proc_kol = (SELECT SUM(kol) FROM sklad_processor
					WHERE id_izd = NEW.processor_id);
	new_proc_kol = old_proc_kol - 1;
	UPDATE sklad_processor
	SET kol = new_proc_kol
    	WHERE id_izd=NEW.processor_id;
		
	old_mother_kol = (SELECT SUM(kol) FROM sklad_motherboard
					WHERE id_izd = NEW.motherboard_id);
	new_mother_kol = old_mother_kol - 1;
	UPDATE sklad_motherboard
	SET kol = new_mother_kol
    	WHERE id_izd=NEW.motherboard_id;	
	
	old_cool_kol = (SELECT SUM(kol) FROM sklad_cool
					WHERE id_izd = NEW.cool_id);
	new_cool_kol = old_cool_kol - 1;
	UPDATE sklad_cool
	SET kol = new_cool_kol
    	WHERE id_izd=NEW.cool_id;
	
	old_ram_kol = (SELECT SUM(kol) FROM sklad_ram
					WHERE id_izd = NEW.ram_id);
	new_ram_kol = old_ram_kol - 1;
	UPDATE sklad_ram
	SET kol = new_ram_kol
    	WHERE id_izd=NEW.ram_id;
	
	old_disk_kol = (SELECT SUM(kol) FROM sklad_disk
					WHERE id_izd = NEW.disk_id);
	new_disk_kol = old_disk_kol - 1;
	UPDATE sklad_disk
	SET kol = new_disk_kol
    	WHERE id_izd=NEW.disk_id;
	
	old_power_kol = (SELECT SUM(kol) FROM sklad_power
					WHERE id_izd = NEW.power_id);
	new_power_kol = old_power_kol - 1;
	UPDATE sklad_power
	SET kol = new_power_kol
    	WHERE id_izd=NEW.power_id;
		
	old_body_kol = (SELECT SUM(kol) FROM sklad_body
					WHERE id_izd = NEW.body_id);
	new_body_kol = old_body_kol - 1;
	UPDATE sklad_body
	SET kol = new_body_kol
    	WHERE id_izd=NEW.body_id;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_all_sklad_trigger
AFTER INSERT
ON "configuration" -- После создания заказа пересчитать количество процессоров
FOR EACH ROW
EXECUTE PROCEDURE update_all_sklad();

-- End of file.

