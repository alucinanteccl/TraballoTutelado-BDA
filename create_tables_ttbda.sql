 /*CREACIÓN DE LA BASE DE DATOS 'Protectora' */

drop database if exists ttbda;
drop table if exists apadriñante;
drop table if exists cuota;
drop table if exists can;

create database ttbda;

CREATE TABLE can(
codchip bigint NOT NULL,
nome varchar(30) NOT NULL,
observacions varchar(4096) NULL,
DNI_apadriñante varchar(9) NULL,
CONSTRAINT PK_can PRIMARY KEY (codchip));

CREATE TABLE cuota(
codcuota int NOT NULL,
nome varchar(30) NOT NULL,
valor numeric(5,2) constraint c_cuota_valor check (valor > 0) NOT NULL,
CONSTRAINT PK_cuota PRIMARY KEY (codcuota));

CREATE TABLE apadriñante(
DNI varchar(9) NOT NULL,
nome varchar(30) NOT NULL,
apelido1 varchar(30) NOT NULL,
apelido2 varchar(30) NOT NULL,
codcuota int NULL,
CONSTRAINT PK_apadriñante PRIMARY KEY (DNI));


INSERT INTO can(codchip,nome, observacions, DNI_apadriñante)
VALUES (123456789123456,'Cheny','NADA',NULL);
INSERT INTO can(codchip,nome, observacions, DNI_apadriñante)
VALUES (123456789123457,'Cora','HOLA',NULL);
INSERT INTO can(codchip,nome, observacions, DNI_apadriñante)
VALUES (123456789123458,'Pacharán','NADA ESPECIAL',NULL);

INSERT INTO cuota(codcuota,nome, valor)
VALUES (1,'Low',15);
INSERT INTO cuota(codcuota,nome, valor)
VALUES (2,'Standard',30);
INSERT INTO cuota(codcuota,nome, valor)
VALUES (3,'Premium',75);

INSERT INTO apadriñante(DNI,nome,apelido1,apelido2,codcuota)
VALUES('46090621R','Lucía','Conde','Fuentes',NULL);
INSERT INTO apadriñante(DNI,nome,apelido1,apelido2,codcuota)
VALUES('32738040R','Julia','Roade','Conejo',NULL);
INSERT INTO apadriñante(DNI,nome,apelido1,apelido2,codcuota)
VALUES('32725341K','Luis','Bardanca','Rey',NULL);