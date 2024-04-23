import mysql.connector 

# Connect to MySQL database
# please change the user/password/db as needed
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="csit314_project"
)
cursor = conn.cursor()


conn.commit()
conn.close()