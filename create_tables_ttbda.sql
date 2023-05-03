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
valor numeric(5,2) constraint c_cuota_valor check (valor > 0),
CONSTRAINT PK_cuota PRIMARY KEY (codcuota));

CREATE TABLE apadriñante(
DNI varchar(9) NOT NULL,
nome varchar(30) NOT NULL,
apelido1 varchar(30) NOT NULL,
apelido2 varchar(30) NOT NULL,
codcuota int NULL,
CONSTRAINT PK_apadriñante PRIMARY KEY (DNI));
