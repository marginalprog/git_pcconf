-- Last modification date: 2023-04-26 12:35:39.159

-- tables
-- Table: Body
CREATE TABLE Body (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming boolean  NOT NULL,
    formfactor varchar(255)  NOT NULL,
    formfactorpower varchar(255)  NOT NULL,
    lengthvideo int  NOT NULL,
    lengthcool int  NOT NULL,
    weight decimal(5,2)  NOT NULL,
    color int  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Body_pk PRIMARY KEY (id)
);

-- Table: Configuration
CREATE TABLE Configuration (
    id serial  NOT NULL,
    Power_id serial  NOT NULL,
    Body_id serial  NOT NULL,
    Videocard_id serial  NOT NULL,
    Processor_id serial  NOT NULL,
    Cool_id serial  NOT NULL,
    Motherboard_id serial  NOT NULL,
    Ram_id serial  NOT NULL,
    Disk_id serial  NOT NULL,
    CONSTRAINT Configuration_pk PRIMARY KEY (id)
);

-- Table: Cool
CREATE TABLE Cool (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    lengthcool int  NOT NULL,
    tdp int  NOT NULL,
    socket varchar(255)  NOT NULL,
    connect varchar(15)  NOT NULL,
    airflow decimal(5,2)  NOT NULL,
    weight decimal(5,2)  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Cool_pk PRIMARY KEY (id)
);

-- Table: Disk
CREATE TABLE Disk (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    formfactor varchar(30)  NOT NULL,
    volume int  NOT NULL,
    interface varchar(20)  NOT NULL,
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
    gaming boolean  NOT NULL,
    socket varchar(255)  NOT NULL,
    chipset varchar(20)  NOT NULL,
    formfactor varchar(30)  NOT NULL,
    memorytype varchar(20)  NOT NULL,
    memoryslot int  NOT NULL,
    memorymax int  NOT NULL,
    memoryfreqmin int  NOT NULL,
    memoryfreqmax int  NOT NULL,
    m2 int  NOT NULL,
    sata int  NOT NULL,
    price int  NOT NULL,
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

-- Table: Post_body
CREATE TABLE Post_body (
    id serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT true,
    name varchar(50)  NOT NULL,
    CONSTRAINT Post_body_pk PRIMARY KEY (id)
);

-- Table: Power
CREATE TABLE Power (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    formfactor varchar(255)  NOT NULL,
    power int  NOT NULL,
    certificate varchar(15)  NOT NULL,
    pincpu int  NOT NULL,
    pinpcie int  NOT NULL,
    pinsata int  NOT NULL,
    weight decimal(5,2)  NOT NULL,
    price int  NOT NULL,
    CONSTRAINT Power_pk PRIMARY KEY (id)
);

-- Table: Processor
CREATE TABLE Processor (
    id serial  NOT NULL,
    id_proizv serial  NOT NULL,
    exist boolean  NOT NULL DEFAULT false,
    fullname varchar(50)  NOT NULL,
    gaming boolean  NOT NULL,
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
    gaming boolean  NOT NULL,
    type varchar(20)  NOT NULL,
    volume int  NOT NULL,
    frequency int  NOT NULL,
    throughput int  NOT NULL,
    timing varchar(20)  NOT NULL,
    tdp int  NOT NULL,
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
    gaming boolean  NOT NULL,
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
    CONSTRAINT Videocard_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Body_Post_body (table: Body)
ALTER TABLE Body ADD CONSTRAINT Body_Post_body
    FOREIGN KEY (id_proizv)
    REFERENCES Post_body (id)  
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

-- End of file.

