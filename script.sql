drop table PARTICIPERPARTIE;
drop table INSCRIRE;
drop table CONSTITUER;
drop table APPARTENIR;
drop table PARTIE;
drop table PHOTO;
drop table ADMIN;
drop table TOURNOI;
drop table EQUIPE;
drop table PARTICIPANT;

create table ADMIN (
  idAdmin int primary key,
  nomAdmin varchar(20),
  prenomAdmin varchar(20),
  dateNaissAdmin date,
  mdpAdmin varchar(20),
  mailAdmin varchar(100),
  dateInsc date
);


create table TOURNOI (
  idT int primary key,
  regleT varchar(200),
  dateT date,
  dureeT varchar(5),
  intituleT varchar(20),
  descT varchar(200),
  typeT varchar(20),
  etatT int,
  nbEquipe int,
  lienT varchar(20),
  nbParticipantsMax int,
  disciplineT varchar(20),
  lieuT varchar(100)
);

create table PARTICIPANT (
  idP int primary key,
  nomP varchar(20),
  prenomP varchar(20),
  mailP varchar(20)
);

create table EQUIPE (
  idE int primary key,
  etatE int,
  nbParticipant int,
  idChefE int unique,
  nomE varchar(20),
  foreign key (idChefE) references PARTICIPANT(idP)
);

create table PHOTO (
  idPhoto int primary key,
  Photo varchar(40),
  descPhoto varchar(20),
  datePhoto date
);

create table CONSTITUER (
  idP int,
  idE int,
  primary key(idP,idE),
  foreign key (idE) references EQUIPE(idE),
  foreign key (idP) references PARTICIPANT(idP)
);

create table APPARTENIR (
  idPhoto int,
  idT int,
  primary key(idPhoto,idT),
  foreign key (idT) references TOURNOI(idT),
  foreign key (idPhoto) references PHOTO(idPhoto)
);

create table INSCRIRE (
  idT int,
  idE int,
  primary key(idT,idE),
  foreign key (idE) references EQUIPE(idE),
  foreign key (idT) references TOURNOI(idT)
);


create table PARTIE (
  idPartie int primary key,
  cartePartie varchar(20)
);

create table PARTICIPERPARTIE (
  idE int,
  idPartie int,
  primary key(idE,idPartie),
  foreign key (idE) references EQUIPE(idE),
  foreign key (idPartie) references PARTIE(idPartie)
);
