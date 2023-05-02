 /*CREACIÓN DE LA BASE DE DATOS 'PEDIDOS' */

drop database if exists ttbda;
drop table if exists apadriñante;
drop table if exists gato;
drop table if exists can;

create database ttbda;

CREATE TABLE can(
codchip bigint NOT NULL,
nome varchar(30) NOT NULL,
observacions varchar(4096) NULL,
CONSTRAINT PK_can PRIMARY KEY (codchip));

CREATE TABLE gato(
codchip bigint NOT NULL,
nome varchar(30) NOT NULL,
observacions varchar(4096) NULL,
CONSTRAINT PK_gato PRIMARY KEY (codchip));

CREATE TABLE apadriñante(
DNI bigint NOT NULL,
nome varchar(30) NOT NULL,
apelido1 varchar(30) NOT NULL,
apelido2 varchar(30) NOT NULL,
cuota numeric(5,2) constraint c_apadriñante_cuota check (cuota > 0),
codchip bigint NOT NULL,
CONSTRAINT PK_apadriñante PRIMARY KEY (DNI));
