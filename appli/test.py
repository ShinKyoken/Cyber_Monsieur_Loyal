import mysql.connector

mydb = mysql.connector.connect(
  host="servinfo-mariadb",
  user="pandion",
  passwd="pandion",
  database="DBpandion"
)

mycursor = mydb.cursor()

sql = "INSERT INTO ADMIN (idAdmin, nomAdmin, prenomAdmin, dateNaissAdmin, mdpAdmin, mailAdmin)"
