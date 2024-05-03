from flask import session
from . import mysql
from werkzeug.security import check_password_hash

class UserAccount:
    def __init__(self, role= None,username=None, password=None, name=None, surname=None, contact=None, email=None, date_of_birth=None, address=None):
        self.role = role
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.contact = contact
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address

    def login(self, username, password, role):

        session['username'] = username # store the username in the session

        cur = mysql.connection.cursor()

        query = "SELECT password FROM useraccount WHERE username=%s AND role= %s"
        cur.execute(query, (username,role))
        account = cur.fetchone()
        check = check_password_hash(account[0], password)

        return check
    
    def createUserAcc(self, userAcc):
        try:
           cur = mysql.connection.cursor()

           query = "INSERT INTO useraccount (role,username, password, name, surname, contact, email, date_of_birth, address) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)" 
           data = (userAcc.role,userAcc.username, userAcc.password, userAcc.name, userAcc.surname, userAcc.contact, userAcc.email, userAcc.date_of_birth, userAcc.address)
           cur.execute(query, data)
           
           mysql.connection.commit()
           
           cur.close()
           return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
    
    def get_user_info(self, username):  # to edit membership_tier for admin
        session['selected_user'] = username # store the username in the session
        cur = mysql.connection.cursor()
        query = "SELECT role, username, name, surname, contact, email, date_of_birth, address FROM useraccount WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return user_data
