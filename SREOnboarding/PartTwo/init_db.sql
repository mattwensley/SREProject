ALTER USER 'root' IDENTIFIED WITH mysql_native_password BY 'password';
create database products;
use products;
create table products1 (
 product varchar(255),
 name varchar(255)
 );

insert into products1 values( "00005","Passionfruit");
insert into products1 values( "00004","Kiwi");
insert into products1 values( "00003","Banana");
