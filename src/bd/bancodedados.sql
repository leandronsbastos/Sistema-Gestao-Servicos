Create Database Sistema_Solicit_Serv;

use Sistema_Solicit_Serv; 

Create table user(
    id_user int not null primary key auto_increment,
    nome_user varchar(55),
    email_user varchar(70),
    pass_user varchar(255),
    type_user varchar(15),
    constraint ck_type_user Check(type_user in ('admin','user','exec'))
); 
Create table solicitacao(
    id_sol int not null primary key auto_increment,
    title_sol varchar(55) not null,
    desc_sol varchar(155) not null,
    status_sol varchar(55) not null,
    type_problem varchar(20),
    comentario varchar(155),
    id_user int,
    constraint ck_type_problem Check (type_problem in ('Problemas de Hardware','Problemas de Software','Duvidas ou Esclarecimentos'))
);

ALTER TABLE solicitacao ADD FOREIGN KEY (id_user) REFERENCES user(id_user);