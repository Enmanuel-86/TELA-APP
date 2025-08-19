BEGIN TRANSACTION;
CREATE TABLE tb_alumnos (

	alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,

	representante_id INTEGER NOT NULL,

	cedula VARCHAR(10) UNIQUE,

	primer_nombre VARCHAR(15) NOT NULL,

	segundo_nombre VARCHAR(15),

	apellido_paterno VARCHAR(15) NOT NULL,

	apellido_materno VARCHAR(15),

	fecha_nacimiento DATE NOT NULL,

	lugar_nacimiento VARCHAR(15) NOT NULL,

	sexo CHAR(1) DEFAULT 'M',

	cma BOOLEAN DEFAULT 1,

	imt BOOLEAN DEFAULT 1,

	relacion_con_rep VARCHAR(15) NOT NULL,

	escolaridad VARCHAR(20) DEFAULT 'No posee',

	procedencia VARCHAR(35) DEFAULT 'Foraneo/a',

	situacion VARCHAR(10) DEFAULT 'Ingresado',

	CHECK(LENGTH(cedula) <= 10),

	CHECK(LENGTH(primer_nombre) <= 15),

	CHECK(LENGTH(segundo_nombre) <= 15),

	CHECK(LENGTH(apellido_paterno) <= 15),

	CHECK(LENGTH(apellido_materno) <= 15),

	CHECK(LENGTH(lugar_nacimiento) <= 15),

	CHECK(situacion IN ('Ingresado', 'Inicial', 'Egresado', 'Rotado', 'Inactivo')),

	CHECK(LENGTH(relacion_con_rep) <= 15),

	CHECK(LENGTH(escolaridad) <= 20),

	CHECK(LENGTH(procedencia) <= 35),

	FOREIGN KEY(representante_id)

		REFERENCES tb_representantes(representante_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_alumnos" VALUES(1,1,'30466351','Ariana','G','Mijares','G','2000-08-21','Barcelona','F',1,1,'Padre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(2,1,'31466351','Ana','G','Mijares','G','2001-08-21','Barcelona','F',1,1,'Padre','6to grado aprobado','UE 29 De Marzo','Ingresado');
INSERT INTO "tb_alumnos" VALUES(3,1,'32466351','Alejandra','G','Mijares','G','2002-08-21','Barcelona','F',1,1,'Padre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(4,1,'33466351','Alison','G','Mijares','G','2003-08-21','Barcelona','F',1,1,'Padre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(5,1,'34466351','Alana','G','Mijares','G','2004-08-21','Barcelona','F',1,1,'Padre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(6,2,'35342903','Andony',NULL,'Amundaray',NULL,'2005-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(7,2,'36342903','Antonio',NULL,'Amundaray',NULL,'2006-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(8,2,'37342903','Anderson',NULL,'Amundaray',NULL,'2007-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(9,2,'38342903','Angel',NULL,'Amundaray',NULL,'2008-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(10,2,'39342903','Andres',NULL,'Amundaray',NULL,'2009-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(11,2,'40342903','Alonso',NULL,'Amundaray',NULL,'2010-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(12,2,'41342903','Armando',NULL,'Amundaray',NULL,'2011-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(13,2,'42342903','Alvaro',NULL,'Amundaray',NULL,'2012-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(14,2,'43342903','Alejandro',NULL,'Amundaray',NULL,'2013-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(15,2,'44342903','Alejo',NULL,'Amundaray',NULL,'2014-09-26','Barcelona','M',1,1,'Madre','6to grado aprobado','IEE Brisas del Mar','Ingresado');
INSERT INTO "tb_alumnos" VALUES(16,1,'31485909','Miguel',NULL,'Infante',NULL,'2004-01-26','Barcelona','M',0,0,'Padre','6to grado aprobado','Escuela tal','Inicial');
INSERT INTO "tb_alumnos" VALUES(17,12,'40751989','Luis','Manuel','Garcia','Lopez','2010-03-02','barcelona','M',0,0,'Hijo','Ninguna','U E Escuela de arte','Inicial');
INSERT INTO "tb_alumnos" VALUES(18,13,'407519891','Marco','Manuel','Garcia','Lopez','2010-03-02','barcelona','M',0,0,'Hijo','Ninguna','U E Escuela de arte','Inicial');
INSERT INTO "tb_alumnos" VALUES(19,1,'40751912','Luis','Manuel','Garcia','Lopez','2010-03-02','barcelona','M',0,0,'Hijo','Ninguna','U E Escuela de arte','Inicial');
INSERT INTO "tb_alumnos" VALUES(20,14,'40123989','Jose','Manolo','Merida','Lopez','2010-03-02','barcelona','M',0,1,'Hijo','Ninguna','U E Escuela de arte','Inicial');
INSERT INTO "tb_alumnos" VALUES(21,2,'40199989','Francisco','Jose','Merida','Lopez','2010-03-02','barcelona','M',0,1,'Hijo','Ninguna','U E Escuela de arte','Inicial');
INSERT INTO "tb_alumnos" VALUES(22,15,'446576','Daniel','','Farias','','2025-07-11','asasdsad','M',0,1,'Sobrino','asdasd','sadasda','Inicial');
CREATE TABLE tb_alumnos_egresados(

	alumno_egresado_id INTEGER PRIMARY KEY AUTOINCREMENT,

	alumno_id INTEGER UNIQUE NOT NULL,

	fecha_emision DATE DEFAULT (DATE('NOW', 'LOCALTIME')),

	razon_egreso VARCHAR(50) NOT NULL,

	CHECK(LENGTH(razon_egreso) <= 50),

	FOREIGN KEY(alumno_id)

		REFERENCES tb_alumnos(alumno_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
CREATE TABLE tb_asistencia_alumnos (

	asist_alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,

	inscripcion_id INTEGER NOT NULL,

	fecha_asistencia DATE NOT NULL,

	estado_asistencia BOOLEAN DEFAULT NULL,

	dia_no_laborable VARCHAR(100) DEFAULT NULL,

	CHECK(LENGTH(dia_no_laborable) <= 100),

	FOREIGN KEY(inscripcion_id)

		REFERENCES tb_inscripciones(inscripcion_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_asistencia_alumnos" VALUES(1,6,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(2,7,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(3,8,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(4,9,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(5,10,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(6,11,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(7,12,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(8,13,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(9,14,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(10,15,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(11,1,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(12,2,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(13,3,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(14,4,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(15,5,'2024-05-01',NULL,'Dia del trabajador');
INSERT INTO "tb_asistencia_alumnos" VALUES(16,6,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(17,7,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(18,8,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(19,9,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(20,10,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(21,11,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(22,1,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(23,2,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(24,3,'2024-05-02',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(25,12,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(26,13,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(27,14,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(28,15,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(29,4,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(30,5,'2024-05-02',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(31,6,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(32,7,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(33,8,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(34,9,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(35,10,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(36,1,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(37,2,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(38,3,'2024-05-03',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(39,11,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(40,12,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(41,13,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(42,14,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(43,15,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(44,4,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(45,5,'2024-05-03',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(46,6,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(47,7,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(48,8,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(49,9,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(50,10,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(51,1,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(52,2,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(53,3,'2024-05-06',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(54,11,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(55,12,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(56,13,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(57,14,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(58,15,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(59,4,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(60,5,'2024-05-06',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(61,6,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(62,7,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(63,8,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(64,9,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(65,1,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(66,2,'2024-05-07',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(67,10,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(68,11,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(69,12,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(70,13,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(71,14,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(72,15,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(73,3,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(74,4,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(75,5,'2024-05-07',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(76,6,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(77,7,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(78,8,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(79,9,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(80,10,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(81,11,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(82,12,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(83,13,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(84,14,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(85,15,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(86,1,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(87,2,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(88,3,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(89,4,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(90,5,'2024-05-08',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(91,6,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(92,7,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(93,8,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(94,9,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(95,10,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(96,1,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(97,2,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(98,3,'2024-05-09',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(99,11,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(100,12,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(101,13,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(102,14,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(103,15,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(104,4,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(105,5,'2024-05-09',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(106,6,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(107,7,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(108,8,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(109,9,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(110,1,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(111,2,'2024-05-10',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(112,10,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(113,11,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(114,12,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(115,13,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(116,14,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(117,15,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(118,3,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(119,4,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(120,5,'2024-05-10',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(121,6,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(122,7,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(123,8,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(124,9,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(125,1,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(126,2,'2024-05-13',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(127,10,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(128,11,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(129,12,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(130,13,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(131,14,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(132,15,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(133,3,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(134,4,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(135,5,'2024-05-13',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(136,6,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(137,7,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(138,8,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(139,9,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(140,1,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(141,2,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(142,3,'2024-05-14',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(143,10,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(144,11,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(145,12,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(146,13,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(147,14,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(148,15,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(149,4,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(150,5,'2024-05-14',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(151,6,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(152,7,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(153,8,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(154,9,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(155,1,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(156,2,'2024-05-15',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(157,10,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(158,11,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(159,12,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(160,13,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(161,14,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(162,15,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(163,3,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(164,4,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(165,5,'2024-05-15',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(166,6,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(167,7,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(168,8,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(169,9,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(170,10,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(171,11,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(172,1,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(173,2,'2024-05-16',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(174,12,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(175,13,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(176,14,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(177,15,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(178,3,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(179,4,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(180,5,'2024-05-16',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(181,6,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(182,7,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(183,8,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(184,9,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(185,1,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(186,2,'2024-05-17',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(187,10,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(188,11,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(189,12,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(190,13,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(191,14,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(192,15,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(193,3,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(194,4,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(195,5,'2024-05-17',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(196,6,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(197,7,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(198,8,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(199,9,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(200,10,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(201,11,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(202,12,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(203,13,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(204,1,'2024-05-20',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(205,14,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(206,15,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(207,2,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(208,3,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(209,4,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(210,5,'2024-05-20',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(211,6,'2024-05-21',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(212,7,'2024-05-21',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(213,8,'2024-05-21',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(214,1,'2024-05-21',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(215,2,'2024-05-21',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(216,9,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(217,10,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(218,11,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(219,12,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(220,13,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(221,14,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(222,15,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(223,3,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(224,4,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(225,5,'2024-05-21',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(226,6,'2024-05-22',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(227,7,'2024-05-22',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(228,1,'2024-05-22',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(229,8,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(230,9,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(231,10,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(232,11,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(233,12,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(234,13,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(235,14,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(236,15,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(237,2,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(238,3,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(239,4,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(240,5,'2024-05-22',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(241,6,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(242,7,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(243,8,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(244,9,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(245,10,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(246,1,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(247,2,'2024-05-23',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(248,11,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(249,12,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(250,13,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(251,14,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(252,15,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(253,3,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(254,4,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(255,5,'2024-05-23',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(256,6,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(257,7,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(258,8,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(259,9,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(260,1,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(261,2,'2024-05-24',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(262,10,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(263,11,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(264,12,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(265,13,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(266,14,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(267,15,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(268,3,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(269,4,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(270,5,'2024-05-24',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(271,6,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(272,7,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(273,8,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(274,9,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(275,1,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(276,2,'2024-05-27',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(277,10,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(278,11,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(279,12,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(280,13,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(281,14,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(282,15,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(283,3,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(284,4,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(285,5,'2024-05-27',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(286,6,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(287,7,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(288,8,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(289,9,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(290,1,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(291,2,'2024-05-28',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(292,10,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(293,11,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(294,12,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(295,13,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(296,14,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(297,15,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(298,3,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(299,4,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(300,5,'2024-05-28',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(301,6,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(302,7,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(303,8,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(304,9,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(305,10,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(306,11,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(307,12,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(308,13,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(309,14,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(310,15,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(311,1,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(312,2,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(313,3,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(314,4,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(315,5,'2024-05-29',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(316,6,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(317,7,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(318,8,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(319,9,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(320,10,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(321,1,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(322,2,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(323,3,'2024-05-30',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(324,11,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(325,12,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(326,13,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(327,14,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(328,15,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(329,4,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(330,5,'2024-05-30',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(331,6,'2024-05-31',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(332,7,'2024-05-31',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(333,8,'2024-05-31',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(334,1,'2024-05-31',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(335,2,'2024-05-31',1,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(336,9,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(337,10,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(338,11,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(339,12,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(340,13,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(341,14,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(342,15,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(343,3,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(344,4,'2024-05-31',0,NULL);
INSERT INTO "tb_asistencia_alumnos" VALUES(345,5,'2024-05-31',0,NULL);
CREATE TABLE tb_asistencia_empleados (

	asist_empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER NOT NULL,

	fecha_asistencia DATE DEFAULT (DATE('NOW', 'LOCALTIME')),

	hora_entrada TIME DEFAULT NULL,

	hora_salida TIME DEFAULT NULL,

	estado_asistencia VARCHAR(15) NOT NULL,

	motivo_retraso VARCHAR(100) DEFAULT NULL,

	motivo_inasistencia VARCHAR(100) DEFAULT NULL,

	CHECK(LENGTH(estado_asistencia) <= 15),

	CHECK(LENGTH(motivo_retraso) <= 100),

	CHECK(LENGTH(motivo_inasistencia) <= 100),

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_asistencia_empleados" VALUES(1,1,'2024-09-24','07:00:00','12:30:00','PRESENTE',NULL,NULL);
INSERT INTO "tb_asistencia_empleados" VALUES(2,2,'2024-09-24','09:30:00','12:30:00','PRESENTE','Mucho trafico',NULL);
INSERT INTO "tb_asistencia_empleados" VALUES(3,3,'2024-09-24',NULL,NULL,'IJ',NULL,'Accidente automovilistico');
INSERT INTO "tb_asistencia_empleados" VALUES(4,1,'2024-09-25',NULL,NULL,'II',NULL,'Estar enfermo');
INSERT INTO "tb_asistencia_empleados" VALUES(5,2,'2024-09-25',NULL,NULL,'IJ',NULL,'Operacion');
INSERT INTO "tb_asistencia_empleados" VALUES(6,3,'2024-09-25','11:30:00','12:30:00','PRESENTE','Mucho trafico',NULL);
INSERT INTO "tb_asistencia_empleados" VALUES(7,1,'2024-09-26','10:30:00','12:30:00','PRESENTE','Mucho trafico',NULL);
INSERT INTO "tb_asistencia_empleados" VALUES(8,2,'2024-09-26',NULL,NULL,'IJ',NULL,'Operacion');
CREATE TABLE tb_auditorias (

	auditoria_id INTEGER PRIMARY KEY AUTOINCREMENT,

	usuario_id INTEGER NOT NULL,

	entidad_afectada VARCHAR(35) NOT NULL,

	accion VARCHAR(250) NOT NULL,

	fecha_accion DATE DEFAULT(DATE('NOW', 'LOCALTIME')),

	CHECK(LENGTH(entidad_afectada) <= 35),

	CHECK(LENGTH(accion) <= 250),

	FOREIGN KEY(usuario_id)

		REFERENCES tb_usuarios(usuario_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_auditorias" VALUES(1,2,'EMPLEADOS','REGISTRÓ A Ligia Garcia. CÉDULA: 24345231','2025-06-13');
INSERT INTO "tb_auditorias" VALUES(2,2,'EMPLEADOS','REGISTRÓ A Mario Castañeda. CÉDULA: 40989586','2025-06-14');
INSERT INTO "tb_auditorias" VALUES(3,2,'REPRESENTANTES','REGISTRÓ A Pedro Lopez. CÉDULA: Buscar','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(4,2,'ALUMNOS','REGISTRÓ A Miguel Infante A LA ESPECIALIDAD Artesanía. MATRICULA: MAT-11daac8','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(5,2,'REPRESENTANTES','REGISTRÓ A Jose Maito. CÉDULA: 6456456','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(6,2,'REPRESENTANTES','REGISTRÓ A Socrates Romeo. CÉDULA: 8398291','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(7,2,'REPRESENTANTES','REGISTRÓ A Enmanuel Gorcea. CÉDULA: 09809800','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(8,2,'ALUMNOS','REGISTRÓ A Marco Garcia A LA ESPECIALIDAD Ceramica. MATRICULA: MAT-a5799e6','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(9,2,'ALUMNOS','REGISTRÓ A Luis Garcia A LA ESPECIALIDAD Artesanía. MATRICULA: MAT-785d99d','2025-07-04');
INSERT INTO "tb_auditorias" VALUES(10,2,'REPRESENTANTES','REGISTRÓ A Jairo Ramos. CÉDULA: 9872738','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(11,2,'ALUMNOS','REGISTRÓ A Jose Merida A LA ESPECIALIDAD Ceramica. MATRICULA: MAT-1901b87','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(12,2,'EMPLEADOS','REGISTRÓ A Jose Medina. CÉDULA: 09456323','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(13,2,'EMPLEADOS','REGISTRÓ A Martin Gomez. CÉDULA: 454223','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(14,2,'EMPLEADOS','REGISTRÓ A Maria de las nieves. CÉDULA: 4352345','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(15,2,'ALUMNOS','REGISTRÓ A Francisco Merida A LA ESPECIALIDAD Hoteleria. MATRICULA: MAT-39c3380','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(16,2,'REPRESENTANTES','REGISTRÓ A Manuel Lopez. CÉDULA: 4532211','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(17,2,'ALUMNOS','REGISTRÓ A Daniel Farias A LA ESPECIALIDAD Artesanía. MATRICULA: MAT-664bf08','2025-07-07');
INSERT INTO "tb_auditorias" VALUES(18,1,'EMPLEADOS','REGISTRÓ A Juan Guerra. CÉDULA: 1038021983','2025-07-17');
CREATE TABLE tb_cargos_empleados (

	cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,

	codigo_cargo VARCHAR(15) UNIQUE NOT NULL,

	cargo VARCHAR(35) NOT NULL,

	CHECK(LENGTH(codigo_cargo) <= 15),

	CHECK(LENGTH(cargo) <= 35)

);
INSERT INTO "tb_cargos_empleados" VALUES(1,'100000C','BACHILLER CONTRATADO');
INSERT INTO "tb_cargos_empleados" VALUES(2,'100000','BACHILLER I');
CREATE TABLE tb_detalles_cargo (

	detalle_cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER UNIQUE NOT NULL,

	cargo_id INTEGER NOT NULL,

	funcion_cargo_id INTEGER NOT NULL,

	especialidad_id INTEGER,

	tipo_cargo_id INTEGER NOT NULL,

	titulo_cargo VARCHAR(100) NOT NULL,

	labores_cargo VARCHAR(50),

	CHECK(LENGTH(titulo_cargo) <= 100),

	CHECK(LENGTH(labores_cargo) <= 50),

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(cargo_id)

		REFERENCES tb_cargos_empleados(cargo_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE,

	FOREIGN KEY(funcion_cargo_id)

		REFERENCES tb_funciones_cargo(funcion_cargo_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE,

	FOREIGN KEY(especialidad_id)

		REFERENCES tb_especialidades(especialidad_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE,

	FOREIGN KEY(tipo_cargo_id)

		REFERENCES tb_tipos_cargo(tipo_cargo_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_detalles_cargo" VALUES(1,1,1,1,NULL,1,'BACHILLER','AUTONOMIA E INDEPENDENCIA SOCIO FAMILIAR');
INSERT INTO "tb_detalles_cargo" VALUES(2,2,1,1,NULL,1,'BACHILLER','Hacer tal cosa');
INSERT INTO "tb_detalles_cargo" VALUES(3,3,1,1,1,2,'BACHILLER',NULL);
INSERT INTO "tb_detalles_cargo" VALUES(4,4,1,1,1,2,'BACHILLER',NULL);
INSERT INTO "tb_detalles_cargo" VALUES(5,5,1,1,1,2,'TSU en administracion','');
INSERT INTO "tb_detalles_cargo" VALUES(6,6,1,1,2,2,'TSU','');
INSERT INTO "tb_detalles_cargo" VALUES(7,7,1,1,3,2,'TSU','nada');
INSERT INTO "tb_detalles_cargo" VALUES(8,8,1,1,NULL,1,'assadsad','assa');
INSERT INTO "tb_detalles_cargo" VALUES(9,9,1,1,NULL,1,'assa','saddsad');
INSERT INTO "tb_detalles_cargo" VALUES(10,10,1,1,NULL,1,'slakdjsaklj','lsakjdlkasjd');
CREATE TABLE tb_diagnosticos (

	diagnostico_id INTEGER PRIMARY KEY AUTOINCREMENT,

	diagnostico VARCHAR(30) NOT NULL,

	CHECK(LENGTH(diagnostico) <= 30)

);
INSERT INTO "tb_diagnosticos" VALUES(1,'Sindrome de down');
INSERT INTO "tb_diagnosticos" VALUES(2,'Espectro Autista leve');
INSERT INTO "tb_diagnosticos" VALUES(3,'Deficit de atencion');
INSERT INTO "tb_diagnosticos" VALUES(11,'retraso IV');
INSERT INTO "tb_diagnosticos" VALUES(12,'zapata4d');
CREATE TABLE tb_empleados (

	empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,

	cedula VARCHAR(10) UNIQUE NOT NULL,

	primer_nombre VARCHAR(15) NOT NULL,

	segundo_nombre VARCHAR(15),

	apellido_paterno VARCHAR(15) NOT NULL,

	apellido_materno VARCHAR(15),

	fecha_nacimiento DATE NOT NULL,

	sexo CHARACTER(1) DEFAULT 'M',

	tiene_hijos_menores BOOLEAN DEFAULT 0,

	fecha_ingreso_institucion DATE DEFAULT (DATE('NOW', 'LOCALTIME')),

	fecha_ingreso_ministerio DATE NOT NULL,

	talla_camisa VARCHAR(3) NOT NULL,

	talla_pantalon INTEGER NOT NULL,

	talla_zapatos INTEGER NOT NULL,

	num_telefono VARCHAR(15) DEFAULT 'No tiene',

	correo_electronico VARCHAR(50) UNIQUE NOT NULL,

	estado_reside VARCHAR(20) NOT NULL,

	municipio VARCHAR(20) NOT NULL,

	direccion_residencia VARCHAR(100) NOT NULL,

	situacion VARCHAR(10) DEFAULT 'Activo',

	CHECK(LENGTH(primer_nombre) <= 15),

	CHECK(LENGTH(segundo_nombre) <= 15),

	CHECK(LENGTH(apellido_paterno) <= 15),

	CHECK(LENGTH(apellido_materno) <= 15),

	CHECK(LENGTH(talla_camisa) <= 3),

	CHECK(talla_pantalon > 0),

	CHECK(talla_zapatos > 0), 

	CHECK(LENGTH(num_telefono) <= 15),

	CHECK(LENGTH(correo_electronico) <= 50),

	CHECK(LENGTH(estado_reside) <= 20),

	CHECK(LENGTH(municipio) <= 20),

	CHECK(LENGTH(direccion_residencia) <= 100),

	CHECK(situacion IN ('Activo', 'Inactivo', 'Eliminado'))

);
INSERT INTO "tb_empleados" VALUES(1,'17536256','DOUGLAS','JOSE','MARQUEZ','BETANCOURT','1983-05-17','M',1,'2025-06-10','2005-10-12','S',34,43,'04160839587','lazarinadedios@hotmail.com','Anzoategui','Simon Bolivar','Las Casitas, Sector 4, Calle 12, Casa N° 14, Barcelona','Activo');
INSERT INTO "tb_empleados" VALUES(2,'5017497','ENMANUEL','JESÚS','GARCIA','RAMOS','1956-10-10','M',1,'2025-06-10','2007-07-19','M',35,41,'04147947961','enmanuel212@hotmail.com','Anzoategui','Simon Bolivar','Urbanizacion La Villa olimpica, calle 16, casa N° 10, Barcelona','Activo');
INSERT INTO "tb_empleados" VALUES(3,'18128319','ROSMARY','DEL VALLE','SALAS','JIMENEZ','1986-10-28','F',0,'2025-06-10','2010-09-12','XXL',32,46,'0412345235','rosmarysalas1700gmail.com','Anzoategui','Simon Bolivar','CALLE LAS MERCEDES,SECTOR N° 2, LA PONDEROSA, BARCELONA','Activo');
INSERT INTO "tb_empleados" VALUES(4,'16788123','JOSE','ALEJANDRO','SALAS','JIMENEZ','1985-10-28','F',0,'2025-06-10','2012-09-12','M',32,44,'04247684587','joseale@gmail.com','Anzoategui','Simon Bolivar','VIA EL RINCON,SECTOR N° 2, BARCELONA','Activo');
INSERT INTO "tb_empleados" VALUES(5,'24345231','Ligia','','Garcia','','2000-03-02','F',1,'2025-06-13','2025-06-18','S',23,25,'04120293022','lgii@gmail.com','Anzoategui','Bolivar','Calle 19','Activo');
INSERT INTO "tb_empleados" VALUES(6,'40989586','Mario','','Castañeda','','1980-03-18','M',1,'2025-06-14','1980-03-21','M',11,12,'041201202','mariocastaneda@gmail.com','Anzoategui','Bolivar','Calle nuevo mexico','Activo');
INSERT INTO "tb_empleados" VALUES(7,'09456323','Jose','Juarez','Medina','','2025-07-15','M',0,'2025-07-07','2014-07-17','S',2,2,'12321312','juanjose@gmail.com','Anzoategui','Bolivar','Calle 3134','Activo');
INSERT INTO "tb_empleados" VALUES(8,'454223','Martin','','Gomez','','2025-07-23','M',0,'2025-07-07','2025-07-31','S',1,2,'123123123','aasdas@gmail.com','asdsad','sadasdsa','asdasdsa','Activo');
INSERT INTO "tb_empleados" VALUES(9,'4352345','Maria','','de las nieves','','2025-07-23','F',0,'2025-07-07','2025-08-07','S',2,2,'213213','ss@gmail.com','sa','sad','sad','Activo');
INSERT INTO "tb_empleados" VALUES(10,'1038021983','Juan','Luis','Guerra','','2025-07-29','M',0,'2025-07-17','2025-07-22','M',1,1,'213123','jsalkdj@gmail.coom','kjhk','kjh','kh','Activo');
CREATE TABLE tb_enfermedades_cronicas(

	enferm_cronica_id INTEGER PRIMARY KEY AUTOINCREMENT,

	enfermedad_cronica VARCHAR(35) NOT NULL,

	CHECK(LENGTH(enfermedad_cronica) <= 35)

);
INSERT INTO "tb_enfermedades_cronicas" VALUES(1,'Artritis');
INSERT INTO "tb_enfermedades_cronicas" VALUES(2,'Diabetes');
CREATE TABLE tb_especialidades (

	especialidad_id INTEGER PRIMARY KEY AUTOINCREMENT,

	especialidad VARCHAR(40) NOT NULL,

	CHECK(LENGTH(especialidad) <= 40)

);
INSERT INTO "tb_especialidades" VALUES(1,'Artesanía');
INSERT INTO "tb_especialidades" VALUES(2,'Ceramica');
INSERT INTO "tb_especialidades" VALUES(3,'Hoteleria');
CREATE TABLE tb_funciones_cargo (

	funcion_cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,

	funcion_cargo VARCHAR(45) NOT NULL,

	CHECK(LENGTH(funcion_cargo) <= 45)

);
INSERT INTO "tb_funciones_cargo" VALUES(1,'Auxiliar');
CREATE TABLE tb_historial_enferm_cronicas(

	hist_enferm_cronica_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER,

	enferm_cronica_id INTEGER NOT NULL,

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(enferm_cronica_id)

		REFERENCES tb_enfermedades_cronicas(enferm_cronica_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_historial_enferm_cronicas" VALUES(1,1,1);
INSERT INTO "tb_historial_enferm_cronicas" VALUES(2,1,2);
INSERT INTO "tb_historial_enferm_cronicas" VALUES(3,2,1);
CREATE TABLE tb_info_bancaria_alumnos(

	info_banc_alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,

	alumno_id INTEGER NOT NULL,

	tipo_cuenta VARCHAR(40) NOT NULL,

	num_cuenta VARCHAR(20) UNIQUE NOT NULL,

	CHECK(LENGTH(tipo_cuenta) <= 40),

	CHECK(LENGTH(num_cuenta) <= 20),

	FOREIGN KEY(alumno_id)

		REFERENCES tb_alumnos(alumno_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_info_bancaria_alumnos" VALUES(1,1,'Ahorro','1234567890');
INSERT INTO "tb_info_bancaria_alumnos" VALUES(2,16,'CORRIENTE','086203045067');
INSERT INTO "tb_info_bancaria_alumnos" VALUES(3,20,'corriente','8474733922');
INSERT INTO "tb_info_bancaria_alumnos" VALUES(4,20,'ahorro','83746748');
CREATE TABLE tb_info_clinica_alumnos (

	info_clin_alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,

	alumno_id INTEGER NOT NULL,

	diagnostico_id INTEGER NOT NULL,

	fecha_diagnostico DATE NOT NULL,

	medico_tratante VARCHAR(35) NOT NULL,

	certificacion_discap VARCHAR(15) UNIQUE NOT NULL,

	fecha_vencimiento_certif DATE NOT NULL,

	medicacion VARCHAR(30) DEFAULT 'No tiene',

	CHECK(LENGTH(medico_tratante) <= 35),

	CHECK(LENGTH(certificacion_discap) <= 15),

	CHECK(LENGTH(medicacion) <= 30),

	FOREIGN KEY(alumno_id)

		REFERENCES tb_alumnos(alumno_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(diagnostico_id)

		REFERENCES tb_diagnosticos(diagnostico_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_info_clinica_alumnos" VALUES(1,1,1,'2012-10-11','Dr Alejandro','D-0321121','2015-08-14','No tiene');
INSERT INTO "tb_info_clinica_alumnos" VALUES(2,2,2,'2013-05-14','Dr Jose','D-365515','2016-11-15','Carbamazepina');
INSERT INTO "tb_info_clinica_alumnos" VALUES(3,2,3,'2019-03-15','Dr Angel','D-365516','2022-05-15','Carbamazepina');
INSERT INTO "tb_info_clinica_alumnos" VALUES(4,16,1,'2006-05-13','DR. ALEJANDRO','D-234796','2010-05-15','No tiene');
INSERT INTO "tb_info_clinica_alumnos" VALUES(5,18,2,'2025-07-23','kaka','d03083','2025-07-23','cete');
INSERT INTO "tb_info_clinica_alumnos" VALUES(6,19,2,'2025-07-08','jajas','d-129389','2025-07-15','alskdj');
INSERT INTO "tb_info_clinica_alumnos" VALUES(7,20,3,'2025-07-09','Dr Marco Aurelio','D-737484584','2029-06-24','Acetaminofen Forte');
INSERT INTO "tb_info_clinica_alumnos" VALUES(8,20,2,'2029-05-27','Dr Mario Silva','D-21039823','2029-05-17','Hibuprofeno');
INSERT INTO "tb_info_clinica_alumnos" VALUES(9,21,1,'2025-07-14','Jose','ssss','2025-07-16','sss');
INSERT INTO "tb_info_clinica_alumnos" VALUES(10,22,1,'2025-07-08','assad','dadas','2025-07-15','dasdas');
CREATE TABLE tb_info_clinica_empleados(

	info_clin_empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER NOT NULL,

	diagnostico_id INTEGER NOT NULL,

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(diagnostico_id)

		REFERENCES tb_diagnosticos(diagnostico_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_info_clinica_empleados" VALUES(1,1,1);
CREATE TABLE tb_info_laboral (

	info_lab_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER UNIQUE NOT NULL,

	cod_depend_cobra CHAR(9) NOT NULL,

	institucion_labora VARCHAR(25) NOT NULL,

	CHECK(LENGTH(cod_depend_cobra) <= 9),

	CHECK(LENGTH(institucion_labora) <= 25),

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_info_laboral" VALUES(1,1,'006505188','TEV TRONCONAL III');
INSERT INTO "tb_info_laboral" VALUES(2,2,'006505188','TEV TRONCONAL III');
INSERT INTO "tb_info_laboral" VALUES(3,3,'006505199','TEV TRONCONAL I');
INSERT INTO "tb_info_laboral" VALUES(4,5,'123123123','Escuela de tal');
INSERT INTO "tb_info_laboral" VALUES(5,6,'123123123','Escuela de doblaje');
INSERT INTO "tb_info_laboral" VALUES(6,7,'123123123','Jose Mario');
INSERT INTO "tb_info_laboral" VALUES(7,8,'123123123','asdsadsad');
INSERT INTO "tb_info_laboral" VALUES(8,9,'123123123','sasdasd');
INSERT INTO "tb_info_laboral" VALUES(9,10,'123123123','jaksdhajskd');
CREATE TABLE tb_inscripciones (

	inscripcion_id INTEGER PRIMARY KEY AUTOINCREMENT,

	num_matricula CHAR(11) UNIQUE NOT NULL,

	alumno_id INTEGER UNIQUE NOT NULL,

	especialidad_id INTEGER NOT NULL,

	fecha_inscripcion DATE DEFAULT (DATE('NOW', 'LOCALTIME')),

	periodo_escolar CHARACTER(9) NOT NULL,

	CHECK(LENGTH(num_matricula) <= 11),

	FOREIGN KEY(alumno_id)

		REFERENCES tb_alumnos(alumno_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(especialidad_id)

		REFERENCES tb_especialidades(especialidad_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_inscripciones" VALUES(1,'MAT-1234567',1,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(2,'MAT-1341345',2,2,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(3,'MAT-1222145',3,2,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(4,'MAT-1782315',4,2,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(5,'MAT-125t341',5,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(6,'MAT-22ft341',6,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(7,'MAT-12ju241',7,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(8,'MAT-123fn21',8,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(9,'MAT-1238942',9,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(10,'MAT-323dw41',10,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(11,'MAT-42sf341',11,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(12,'MAT-34hy341',12,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(13,'MAT-3kl2344',13,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(14,'MAT-5qa2341',14,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(15,'MAT-52jm346',15,1,'2025-06-10','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(16,'MAT-11daac8',16,1,'2025-07-04','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(17,'MAT-a5799e6',18,2,'2025-07-04','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(18,'MAT-785d99d',19,1,'2025-07-04','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(19,'MAT-1901b87',20,2,'2025-07-07','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(20,'MAT-39c3380',21,3,'2025-07-07','2025-2026');
INSERT INTO "tb_inscripciones" VALUES(21,'MAT-664bf08',22,1,'2025-07-07','2025-2026');
CREATE TABLE tb_medidas_alumnos (

	medid_alumno_id INTEGER PRIMARY KEY AUTOINCREMENT,

	alumno_id INTEGER NOT NULL,

	estatura REAL NOT NULL,

	peso REAL NOT NULL,

	talla_camisa VARCHAR(3) NOT NULL,

	talla_pantalon INTEGER NOT NULL,

	talla_zapatos INTEGER NOT NULL,

	CHECK(LENGTH(talla_camisa) <= 3),

	CHECK(talla_pantalon > 0),

	CHECK(talla_zapatos > 0),

	FOREIGN KEY(alumno_id)

		REFERENCES tb_alumnos(alumno_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_medidas_alumnos" VALUES(1,1,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(2,2,1.69,50.0,'S',29,41);
INSERT INTO "tb_medidas_alumnos" VALUES(3,3,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(4,4,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(5,5,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(6,6,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(7,7,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(8,8,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(9,9,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(10,10,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(11,11,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(12,12,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(13,13,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(14,14,1.42,56.9,'M',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(15,15,1.43,54.9,'S',30,36);
INSERT INTO "tb_medidas_alumnos" VALUES(16,16,1.87,49.5,'M',30,46);
INSERT INTO "tb_medidas_alumnos" VALUES(17,18,170.0,60.0,'M',32,32);
INSERT INTO "tb_medidas_alumnos" VALUES(18,19,170.0,60.0,'M',32,32);
INSERT INTO "tb_medidas_alumnos" VALUES(19,20,170.0,60.0,'M',32,32);
INSERT INTO "tb_medidas_alumnos" VALUES(20,21,170.0,60.0,'M',32,32);
INSERT INTO "tb_medidas_alumnos" VALUES(21,22,44.0,34.0,'S',2,2);
CREATE TABLE tb_permisos (

	permiso_id INTEGER PRIMARY KEY AUTOINCREMENT,

	tipo_permiso VARCHAR(70) NOT NULL,

	CHECK(LENGTH(tipo_permiso) <= 70)

);
INSERT INTO "tb_permisos" VALUES(1,'GESTIONAR USUARIOS');
INSERT INTO "tb_permisos" VALUES(2,'GESTIONAR CARGOS');
INSERT INTO "tb_permisos" VALUES(3,'CREAR EMPLEADOS');
INSERT INTO "tb_permisos" VALUES(4,'ACTUALIZAR EMPLEADOS');
INSERT INTO "tb_permisos" VALUES(5,'ELIMINAR EMPLEADOS');
INSERT INTO "tb_permisos" VALUES(6,'CONSULTAR EMPLEADOS');
INSERT INTO "tb_permisos" VALUES(7,'CREAR ESPECIALIDADES');
INSERT INTO "tb_permisos" VALUES(8,'ACTUALIZAR ESPECIALIDADES');
INSERT INTO "tb_permisos" VALUES(9,'ELIMINAR ESPECIALIDADES');
INSERT INTO "tb_permisos" VALUES(10,'CONSULTAR ESPECIALIDADES');
INSERT INTO "tb_permisos" VALUES(11,'CREAR ALUMNOS');
INSERT INTO "tb_permisos" VALUES(12,'ACTUALIZAR ALUMNOS');
INSERT INTO "tb_permisos" VALUES(13,'ELIMINAR ALUMNOS');
INSERT INTO "tb_permisos" VALUES(14,'CONSULTAR ALUMNOS');
INSERT INTO "tb_permisos" VALUES(15,'CREAR REPRESENTANTES');
INSERT INTO "tb_permisos" VALUES(16,'ACTUALIZAR REPRESENTANTES');
INSERT INTO "tb_permisos" VALUES(17,'ELIMINAR REPRESENTANTES');
INSERT INTO "tb_permisos" VALUES(18,'CONSULTAR REPRESENTANTES');
CREATE TABLE tb_permisos_x_rol (

	perm_x_rol_id INTEGER PRIMARY KEY AUTOINCREMENT,

	rol_id INTEGER NOT NULL,

	permiso_id INTEGER NOT NULL,

	FOREIGN KEY(rol_id)

		REFERENCES tb_roles(rol_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE,

	FOREIGN KEY(permiso_id)

		REFERENCES tb_permisos(permiso_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
INSERT INTO "tb_permisos_x_rol" VALUES(1,1,1);
INSERT INTO "tb_permisos_x_rol" VALUES(2,1,2);
INSERT INTO "tb_permisos_x_rol" VALUES(3,1,3);
INSERT INTO "tb_permisos_x_rol" VALUES(4,1,4);
INSERT INTO "tb_permisos_x_rol" VALUES(5,1,5);
INSERT INTO "tb_permisos_x_rol" VALUES(6,1,6);
INSERT INTO "tb_permisos_x_rol" VALUES(7,1,7);
INSERT INTO "tb_permisos_x_rol" VALUES(8,1,8);
INSERT INTO "tb_permisos_x_rol" VALUES(9,1,9);
INSERT INTO "tb_permisos_x_rol" VALUES(10,1,10);
INSERT INTO "tb_permisos_x_rol" VALUES(11,1,11);
INSERT INTO "tb_permisos_x_rol" VALUES(12,1,12);
INSERT INTO "tb_permisos_x_rol" VALUES(13,1,13);
INSERT INTO "tb_permisos_x_rol" VALUES(14,1,14);
INSERT INTO "tb_permisos_x_rol" VALUES(15,1,15);
INSERT INTO "tb_permisos_x_rol" VALUES(16,1,16);
INSERT INTO "tb_permisos_x_rol" VALUES(17,1,17);
INSERT INTO "tb_permisos_x_rol" VALUES(18,1,18);
INSERT INTO "tb_permisos_x_rol" VALUES(19,2,3);
INSERT INTO "tb_permisos_x_rol" VALUES(20,2,4);
INSERT INTO "tb_permisos_x_rol" VALUES(21,2,6);
INSERT INTO "tb_permisos_x_rol" VALUES(22,2,7);
INSERT INTO "tb_permisos_x_rol" VALUES(23,2,8);
INSERT INTO "tb_permisos_x_rol" VALUES(24,2,10);
INSERT INTO "tb_permisos_x_rol" VALUES(25,2,11);
INSERT INTO "tb_permisos_x_rol" VALUES(26,2,12);
INSERT INTO "tb_permisos_x_rol" VALUES(27,2,14);
INSERT INTO "tb_permisos_x_rol" VALUES(28,2,15);
INSERT INTO "tb_permisos_x_rol" VALUES(29,2,16);
INSERT INTO "tb_permisos_x_rol" VALUES(30,2,18);
INSERT INTO "tb_permisos_x_rol" VALUES(31,3,3);
INSERT INTO "tb_permisos_x_rol" VALUES(32,3,6);
INSERT INTO "tb_permisos_x_rol" VALUES(33,3,10);
INSERT INTO "tb_permisos_x_rol" VALUES(34,3,11);
INSERT INTO "tb_permisos_x_rol" VALUES(35,3,14);
INSERT INTO "tb_permisos_x_rol" VALUES(36,3,15);
INSERT INTO "tb_permisos_x_rol" VALUES(37,3,18);
CREATE TABLE tb_reposos_empleados (

	reposo_empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER NOT NULL,

	motivo_reposo VARCHAR(100) NOT NULL,

	fecha_emision DATE DEFAULT (DATE('NOW', 'LOCALTIME')),

	fecha_reingreso DATE NOT NULL,

	CHECK(LENGTH(motivo_reposo) <= 100),

	CHECK(fecha_reingreso > fecha_emision),

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE CASCADE

		ON UPDATE CASCADE

);
CREATE TABLE tb_representantes (

	representante_id INTEGER PRIMARY KEY AUTOINCREMENT,

	cedula VARCHAR(10) UNIQUE NOT NULL,

	nombre VARCHAR(15) NOT NULL,

	apellido VARCHAR(15) NOT NULL,

	direccion_residencia VARCHAR(100) NOT NULL,

	num_telefono VARCHAR(15) DEFAULT 'No tiene',

	carga_familiar INTEGER NOT NULL,

	estado_civil VARCHAR(15) DEFAULT 'Soltero/a',

	CHECK(LENGTH(cedula) <= 10),

	CHECK(LENGTH(nombre) <= 15),

	CHECK(LENGTH(apellido) <= 15),

	CHECK(LENGTH(direccion_residencia) <= 100),

	CHECK(LENGTH(num_telefono) <= 15),

	CHECK(carga_familiar >= 0),

	CHECK(LENGTH(estado_civil) <= 15)

);
INSERT INTO "tb_representantes" VALUES(1,'12345','Juan','Mijares','Av. Juan de Urpín , C/ Rocal nº 21-18, Barcelona','04142878970',4,'Casado/a');
INSERT INTO "tb_representantes" VALUES(2,'123456','Doris','Yanez','BNA, Urb. Brisas del Mar, C/ sal José , nº 04','04248098766',6,'Soltero/a');
INSERT INTO "tb_representantes" VALUES(3,'Buscar','Pedro','Lopez','calle 2','04132341234',4,'soltero');
INSERT INTO "tb_representantes" VALUES(4,'9876','Manuel','Silva','calle 3','04122344321',2,'Casado');
INSERT INTO "tb_representantes" VALUES(5,'1234567','Mario','Castañeda','calle 21','02939499',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(6,'098098098','Juan','Perez','calle 231','0403010120',1,'Soltero');
INSERT INTO "tb_representantes" VALUES(7,'8768594','Jose','Marino','calles','980989098',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(8,'76876678','Jose','Maria','sjsjsj','29299',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(9,'4565465','Mario','Kajsd','sdjalksdj','123123',2,'Lkasjd');
INSERT INTO "tb_representantes" VALUES(10,'109238092','Jose','Slskjd','askldj','10923',88,'Askldj');
INSERT INTO "tb_representantes" VALUES(11,'6456456','Jose','Maito','callee','1023809',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(12,'8398291','Socrates','Romeo','jsladk','09380948',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(13,'09809800','Enmanuel','Gorcea','saldkj','09384098',2,'Soltero');
INSERT INTO "tb_representantes" VALUES(14,'9872738','Jairo','Ramos','Calle 3423','0431238828',2,'Casado');
INSERT INTO "tb_representantes" VALUES(15,'4532211','Manuel','Lopez','dasdsa','12312312',2,'Casado');
CREATE TABLE tb_roles (

	rol_id INTEGER PRIMARY KEY AUTOINCREMENT,

	tipo_rol VARCHAR(25) NOT NULL,

	CHECK(LENGTH(tipo_rol) <= 25)

);
INSERT INTO "tb_roles" VALUES(1,'DIRECTOR');
INSERT INTO "tb_roles" VALUES(2,'SUB-DIRECTOR');
INSERT INTO "tb_roles" VALUES(3,'SECRETARIO');
CREATE TABLE tb_tipos_cargo (

	tipo_cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,

	tipo_cargo VARCHAR(25) NOT NULL,

	horario_llegada TIME NOT NULL,

	CHECK(LENGTH(tipo_cargo) <= 25)

);
INSERT INTO "tb_tipos_cargo" VALUES(1,'ADMINISTRATIVO','07:00:00');
INSERT INTO "tb_tipos_cargo" VALUES(2,'DOCENTE','09:00:00');
CREATE TABLE tb_usuarios (

	usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,

	empleado_id INTEGER UNIQUE NOT NULL,

	rol_id INTEGER NOT NULL,

	nombre_usuario VARCHAR(10) UNIQUE NOT NULL,

	clave_usuario VARCHAR(12) NOT NULL,

	CHECK(LENGTH(nombre_usuario) <= 10),

	CHECK(nombre_usuario NOT LIKE '% %'),

	CHECK(LENGTH(clave_usuario) <= 12),

	CHECK(clave_usuario NOT LIKE '% %'),

	FOREIGN KEY(empleado_id)

		REFERENCES tb_empleados(empleado_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE,

	FOREIGN KEY(rol_id)

		REFERENCES tb_roles(rol_id)

		ON DELETE RESTRICT

		ON UPDATE CASCADE

);
INSERT INTO "tb_usuarios" VALUES(1,1,1,'douglas345','1234');
INSERT INTO "tb_usuarios" VALUES(2,2,3,'Enmanuel86','1212');
CREATE VIEW vw_alumnos_egresados_x_especialidad AS

	SELECT 

		especialidades.especialidad_id,

		especialidades.especialidad,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'M' THEN 1 ELSE 0 END), 0) AS total_varones_egresados,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'F' THEN 1 ELSE 0 END), 0) AS total_hembras_egresadas

	FROM tb_especialidades AS especialidades

	LEFT JOIN tb_inscripciones AS inscripciones 

		ON inscripciones.especialidad_id = especialidades.especialidad_id

	LEFT JOIN tb_alumnos AS alumnos 

		ON inscripciones.alumno_id = alumnos.alumno_id AND alumnos.situacion = 'Egresado'

	GROUP BY especialidades.especialidad;
CREATE VIEW vw_alumnos_rotados_x_especialidad AS 

	SELECT 

		especialidades.especialidad_id,

		especialidades.especialidad,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'M' THEN 1 ELSE 0 END), 0) AS total_varones_rotados,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'F' THEN 1 ELSE 0 END), 0) AS total_hembras_rotadas

	FROM tb_especialidades AS especialidades

	LEFT JOIN tb_inscripciones AS inscripciones 

		ON inscripciones.especialidad_id = especialidades.especialidad_id

	LEFT JOIN tb_alumnos AS alumnos 

		ON inscripciones.alumno_id = alumnos.alumno_id AND alumnos.situacion = 'Rotado'

	GROUP BY especialidades.especialidad;
CREATE VIEW vw_alumnos_ingresados_x_especialidad AS

	SELECT 

		especialidades.especialidad_id,

		especialidades.especialidad,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'M' THEN 1 ELSE 0 END), 0) AS total_varones_ingresados,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'F' THEN 1 ELSE 0 END), 0) AS total_hembras_ingresadas

	FROM tb_especialidades AS especialidades

	LEFT JOIN tb_inscripciones AS inscripciones 

		ON inscripciones.especialidad_id = especialidades.especialidad_id 

	LEFT JOIN tb_alumnos AS alumnos 

		ON inscripciones.alumno_id = alumnos.alumno_id AND alumnos.situacion = 'Ingresado'

	INNER JOIN vw_alumnos_egresados_x_especialidad AS alumnos_egresados

		ON alumnos_egresados.especialidad_id = especialidades.especialidad_id

	INNER JOIN vw_alumnos_rotados_x_especialidad AS alumnos_rotados

		ON alumnos_rotados.especialidad_id = especialidades.especialidad_id

	GROUP BY especialidades.especialidad;
CREATE VIEW vw_alumnos_iniciales_x_especialidad AS

	SELECT 

		especialidades.especialidad_id,

		especialidades.especialidad,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'M' THEN 1 ELSE 0 END), 0) AS total_varones_iniciales,

		COALESCE(SUM(CASE WHEN alumnos.sexo = 'F' THEN 1 ELSE 0 END), 0) AS total_hembras_iniciales

	FROM tb_especialidades AS especialidades

	LEFT JOIN tb_inscripciones AS inscripciones 

		ON inscripciones.especialidad_id = especialidades.especialidad_id 

	LEFT JOIN tb_alumnos AS alumnos 

		ON inscripciones.alumno_id = alumnos.alumno_id AND alumnos.situacion = 'Inicial'

	GROUP BY especialidades.especialidad;
CREATE VIEW vw_matricula_completa_alumnos AS

	SELECT

		especialidades.especialidad_id,

		especialidades.especialidad,

		alumnos_iniciales.total_varones_iniciales,

		alumnos_ingresados.total_varones_ingresados,

		alumnos_egresados.total_varones_egresados,

		alumnos_rotados.total_varones_rotados,

		(alumnos_iniciales.total_varones_iniciales + 

		alumnos_ingresados.total_varones_ingresados) AS matricula_total_varones,

		alumnos_iniciales.total_hembras_iniciales,

		alumnos_ingresados.total_hembras_ingresadas,

		alumnos_egresados.total_hembras_egresadas,

		alumnos_rotados.total_hembras_rotadas,

		(alumnos_iniciales.total_hembras_iniciales + 

		alumnos_ingresados.total_hembras_ingresadas) AS matricula_total_hembras

	FROM tb_especialidades AS especialidades

	INNER JOIN vw_alumnos_iniciales_x_especialidad AS alumnos_iniciales

		ON alumnos_iniciales.especialidad_id = especialidades.especialidad_id

	INNER JOIN vw_alumnos_ingresados_x_especialidad AS alumnos_ingresados

		ON alumnos_ingresados.especialidad_id = especialidades.especialidad_id

	INNER JOIN vw_alumnos_egresados_x_especialidad AS alumnos_egresados

		ON alumnos_egresados.especialidad_id = especialidades.especialidad_id

	INNER JOIN vw_alumnos_rotados_x_especialidad AS alumnos_rotados

		ON alumnos_rotados.especialidad_id = especialidades.especialidad_id;
CREATE VIEW vw_registro_asistencia_alumnos AS

	SELECT

		especialidades.especialidad_id,

		especialidades.especialidad,

		STRFTIME('%Y-%m', asistencia_alumnos.fecha_asistencia) AS anio_mes,

		asistencia_alumnos.fecha_asistencia,

		asistencia_alumnos.dia_no_laborable,

		SUM(CASE WHEN alumnos.sexo = 'M' AND asistencia_alumnos.estado_asistencia = 1 THEN 1 ELSE 0 END) AS varones_presentes,

		SUM(CASE WHEN alumnos.sexo = 'F' AND asistencia_alumnos.estado_asistencia = 1 THEN 1 ELSE 0 END) AS hembras_presentes,

		SUM(CASE WHEN alumnos.sexo = 'M' AND asistencia_alumnos.estado_asistencia = 0 THEN 1 ELSE 0 END) AS varones_ausentes,

		SUM(CASE WHEN alumnos.sexo = 'F' AND asistencia_alumnos.estado_asistencia = 0 THEN 1 ELSE 0 END) AS hembras_ausentes

	FROM tb_asistencia_alumnos AS asistencia_alumnos

	INNER JOIN tb_inscripciones AS inscripciones

		ON asistencia_alumnos.inscripcion_id = inscripciones.inscripcion_id

	INNER JOIN tb_especialidades AS especialidades

		ON inscripciones.especialidad_id = especialidades.especialidad_id

	INNER JOIN tb_alumnos AS alumnos

		ON inscripciones.alumno_id = alumnos.alumno_id

	GROUP BY asistencia_alumnos.fecha_asistencia

	ORDER BY asistencia_alumnos.fecha_asistencia;
CREATE VIEW vw_sumatorias_asistencias_inasistencias AS

	SELECT

		especialidad_id,

		especialidad,

		anio_mes,

		CAST(SUM(varones_presentes) AS REAL) AS sumatoria_varones_presentes,

		CAST(SUM(hembras_presentes) AS REAL) AS sumatoria_hembras_presentes,

		CAST((SUM(varones_presentes)+SUM(hembras_presentes)) AS REAL) AS sumatoria_general_presentes,

		CAST(SUM(varones_ausentes) AS REAL) AS sumatoria_varones_ausentes,

		CAST(SUM(hembras_ausentes) AS REAL) AS sumatoria_hembras_ausentes,

		CAST((SUM(varones_ausentes)+SUM(hembras_ausentes)) AS REAL) AS sumatoria_general_ausentes

	FROM vw_registro_asistencia_alumnos;
CREATE VIEW vw_porcentajes_asistencias_inasistencias AS

	SELECT

		especialidad_id,

		especialidad,

		ROUND((sumatoria_varones_presentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100) AS porcentaje_varones_presentes,

		ROUND((sumatoria_hembras_presentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100) AS porcentaje_hembras_presentes,

		((ROUND((sumatoria_varones_presentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100)) + 

		(ROUND((sumatoria_hembras_presentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100))) AS porcentaje_general_presentes,

		ROUND((sumatoria_varones_ausentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100) AS porcentaje_varones_ausentes,

		ROUND((sumatoria_hembras_ausentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100) AS porcentaje_hembras_ausentes,

		((ROUND((sumatoria_varones_ausentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100)) + 

		(ROUND((sumatoria_hembras_ausentes / (sumatoria_general_presentes + sumatoria_general_ausentes)) * 100))) AS porcentaje_general_ausentes

	FROM vw_sumatorias_asistencias_inasistencias;
CREATE VIEW vw_asistencia_empleados AS

	SELECT 

		asistencia_empleados.asist_empleado_id,

		empleados.cedula,

		empleados.primer_nombre,

		empleados.apellido_paterno,

		asistencia_empleados.fecha_asistencia,

		asistencia_empleados.estado_asistencia,

		STRFTIME('%H:%M', asistencia_empleados.hora_entrada) AS hora_entrada,

		STRFTIME('%H:%M', asistencia_empleados.hora_salida) AS hora_salida,

		asistencia_empleados.motivo_retraso,

		asistencia_empleados.motivo_inasistencia,

		CASE

			WHEN hora_entrada IS NOT NULL AND hora_entrada > tipos_cargo.horario_llegada THEN

				(CAST(STRFTIME('%H', hora_entrada) AS INTEGER) - CAST(STRFTIME('%H', tipos_cargo.horario_llegada) AS INTEGER)) +

				(CAST(STRFTIME('%M', hora_entrada) AS INTEGER) - CAST(STRFTIME('%M', tipos_cargo.horario_llegada) AS INTEGER)) / 60.0

			WHEN estado_asistencia = 'II' THEN 5.5

			ELSE 0

		END AS horas_retraso

		FROM tb_empleados AS empleados

		INNER JOIN tb_detalles_cargo AS detalles_cargo 

			ON detalles_cargo.empleado_id = empleados.empleado_id

		INNER JOIN tb_funciones_cargo AS funciones_cargo 

			ON detalles_cargo.funcion_cargo_id = funciones_cargo.funcion_cargo_id

		INNER JOIN tb_tipos_cargo AS tipos_cargo

			ON detalles_cargo.tipo_cargo_id = tipoS_cargo.tipo_cargo_id

		INNER JOIN tb_asistencia_empleados AS asistencia_empleados

			ON asistencia_empleados.empleado_id = empleados.empleado_id;
CREATE TRIGGER tg_egresar_alumno

AFTER INSERT ON tb_alumnos_egresados

BEGIN

	UPDATE tb_alumnos SET situacion = 'Egresado'

	WHERE alumno_id = NEW.alumno_id;

END;
CREATE TRIGGER tg_eliminar_egreso_alumno

AFTER UPDATE ON tb_alumnos

WHEN NEW.situacion != 'Egresado' AND OLD.situacion = 'Egresado'

BEGIN

	DELETE FROM tb_alumnos_egresados

	WHERE alumno_id = NEW.alumno_id;

END;
CREATE TRIGGER tg_reposo_empleado

AFTER INSERT ON tb_reposos_empleados

BEGIN

	UPDATE tb_empleados SET situacion = 'Inactivo'

	WHERE empleado_id = NEW.empleado_id;

END;
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('tb_roles',3);
INSERT INTO "sqlite_sequence" VALUES('tb_permisos',18);
INSERT INTO "sqlite_sequence" VALUES('tb_permisos_x_rol',37);
INSERT INTO "sqlite_sequence" VALUES('tb_representantes',15);
INSERT INTO "sqlite_sequence" VALUES('tb_alumnos',22);
INSERT INTO "sqlite_sequence" VALUES('tb_info_bancaria_alumnos',4);
INSERT INTO "sqlite_sequence" VALUES('tb_medidas_alumnos',21);
INSERT INTO "sqlite_sequence" VALUES('tb_diagnosticos',12);
INSERT INTO "sqlite_sequence" VALUES('tb_info_clinica_alumnos',10);
INSERT INTO "sqlite_sequence" VALUES('tb_especialidades',3);
INSERT INTO "sqlite_sequence" VALUES('tb_inscripciones',21);
INSERT INTO "sqlite_sequence" VALUES('tb_asistencia_alumnos',345);
INSERT INTO "sqlite_sequence" VALUES('tb_empleados',10);
INSERT INTO "sqlite_sequence" VALUES('tb_usuarios',2);
INSERT INTO "sqlite_sequence" VALUES('tb_enfermedades_cronicas',2);
INSERT INTO "sqlite_sequence" VALUES('tb_historial_enferm_cronicas',3);
INSERT INTO "sqlite_sequence" VALUES('tb_info_clinica_empleados',1);
INSERT INTO "sqlite_sequence" VALUES('tb_info_laboral',9);
INSERT INTO "sqlite_sequence" VALUES('tb_cargos_empleados',2);
INSERT INTO "sqlite_sequence" VALUES('tb_funciones_cargo',1);
INSERT INTO "sqlite_sequence" VALUES('tb_tipos_cargo',2);
INSERT INTO "sqlite_sequence" VALUES('tb_detalles_cargo',10);
INSERT INTO "sqlite_sequence" VALUES('tb_asistencia_empleados',8);
INSERT INTO "sqlite_sequence" VALUES('tb_auditorias',18);
COMMIT;
