create database  if not exists pttdb ;
use pttdb ;

create table if not exists ptt_Stock (id int not null Primary key, date date ,post_tag text ,post_title text , 
post_author text ,tag text,push int,good int,bad int,url text ) ;

create table if not exists ptt_Gossiping (id int not null Primary key, date date ,post_tag text ,post_title text , 
post_author text ,tag text,push int,good int,bad int,url text ) ;

