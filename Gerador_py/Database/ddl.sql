create database IF NOT EXISTS certificados_db;

use certificados_db;

create table IF NOT EXISTS certificados 
        (
        id int  primary key auto_increment,
        nome varchar(100) not null,
        nacionalidade varchar(100) not null,
        estado varchar(100) not null,
        data_nascimento date not null,
        documento varchar(100) not null,
        data_conclusao datetime not null,
        curso varchar(100) not null,
        carga_horaria varchar(100) not null,
        data_emissao datetime not null,
        nome_assinatura varchar(100) not null,
        cargo varchar(100) not null,
        caminho varchar(100)
        );