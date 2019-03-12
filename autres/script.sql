drop table PARTICIPERPARTIE;
drop table CONSTITUER;
drop table PHOTO;
drop table PARTIE;
drop table EQUIPE;
drop table PARTICIPANT;
drop table REGLE;
drop table TOURNOI;
drop table ADMIN;

create table ADMIN (
  idAdmin int primary key,
  nomAdmin varchar(20),
  prenomAdmin varchar(20),
  dateNaissAdmin date,
  mdpAdmin varchar(20),
);

create table TOURNOI (
  idT int primary key,
  idAdmin int,
  regleT varchar(200),
  dateT datetime,
  dureeT varchar(5),
  intituleT varchar(20),
  descT varchar(200),
  typeT varchar(20),
  etatT int,
  nbEquipe int,
  lienT varchar(20),
  nbParticipantsMax int,
  disciplineT varchar(20),
  lieuT varchar(100),
  logoT text,
  foreign key (idAdmin) references ADMIN(idAdmin)
);

create table EQUIPE (
  idE int primary key,
  etatE int,
  nbParticipant int,
  idChefE int unique,
  nomE varchar(20),
  idT int,
  foreign key (idChefE) references PARTICIPANT(idP),
  foreign key (idT) references TOURNOI(idT)
);

create table PARTICIPANT (
  idP int primary key,
  nomP varchar(20),
  prenomP varchar(20),
  mailP varchar(20),
);

create table PHOTO (
  idPhoto int primary key,
  Photo varchar(40),
  descPhoto varchar(20),
  datePhoto date,
  idT int,
  foreign key (idT) references TOURNOI(idT)
);

create table PARTIE (
  idPartie int primary key,
  cartePartie varchar(20)
);

create table PARTICIPERPARTIE (
  idE int,
  idPartie int,
  idT int,
  primary key(idE,idPartie,idT),
  foreign key (idE) references EQUIPE(idE),
  foreign key (idPartie) references PARTIE(idPartie),
  foreign key (idT) references TOURNOI(idT)
);
