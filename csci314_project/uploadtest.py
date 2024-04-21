import mysql.connector 

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="csci314"
)
cursor = conn.cursor()


conn.commit()
conn.close()
