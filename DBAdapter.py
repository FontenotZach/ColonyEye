import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="zfonteno",
    password="f3Fek*bw2&9@d2@!",
    database="ColonyEye"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE mice (label VARCHAR(255), rfid VARCHAR(255))")
