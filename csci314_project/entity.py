from flask import session
from . import mysql
from werkzeug.security import check_password_hash

class UserAccount:
    def __init__(self, role= None,username=None, password=None, name=None, surname=None, contact = None, date_of_birth=None,email=None, address=None):
        self.role = role
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.contact = contact
        self.date_of_birth = date_of_birth
        self.email = email
        self.address = address

    def login(self, username, password, role):

        session['username'] = username # store the username in the session

        cur = mysql.connection.cursor()

        query = "SELECT password FROM useraccount WHERE username = %s"
        data = (username,)
        cur.execute(query, data)
        account = cur.fetchone()
        check = check_password_hash(account[0], password)

        return check

    def createUserAcc(self, userAcc):
        try:
           cur = mysql.connection.cursor()

           query = "INSERT INTO useraccount (role,username, password, name, surname, contact,date_of_birth, email, address) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s)" 
           data = (userAcc.role,userAcc.username, userAcc.password,userAcc.name, userAcc.surname, userAcc.contact,userAcc.date_of_birth,userAcc.email,  userAcc.address)
           cur.execute(query, data)
           
           mysql.connection.commit()
           
           cur.close()
           return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
        
    def get_user_info(self, username):  
        session['selected_user'] = username # store the username in the session
        cur = mysql.connection.cursor()
        query = "SELECT role,username, name, surname,contact, date_of_birth,email, address FROM useraccount WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return user_data

#ADMIN
    def get_all_users(self):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT username FROM useraccount"
            cur.execute(query)
            users_list = []
            for user_name in cur.fetchall():
                username = user_name[0]
                users_list.append(username)

            cur.close()
            return users_list
        except Exception as e:
            print(f"Error getting username list: {e}")

    def search_user(self, username):
            try:
                cur = mysql.connection.cursor()

                query = "SELECT username FROM useraccount where username = %s"
                data = (username,)
                cur.execute(query,data)
            
                result =  cur.fetchone()

                cur.close()
                if result:
                    return result[0]
                else:
                    return None 
            except Exception as e:
                print(f"Error searching user: {e}")

    def edit_profile(self, role,oldUsername, newUsername, name, surname, contact, date_of_birth, email,address):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET role = %s, username = %s, name = %s, surname = %s, contact = %s, date_of_birth = %s,email = %s, address = %s  WHERE username = %s"
            data = (role, newUsername, name, surname, contact,date_of_birth,email, address, oldUsername)
            cur.execute(query, data)
            mysql.connection.commit()
           
            cur.close()
            return True
        except Exception as e:
            print(f"Error changing profile: {e}")
            return False
        
    def edit_profile1(self, oldUsername, name, surname, contact, date_of_birth,email, address):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET name = %s, surname = %s, contact = %s, date_of_birth = %s, email = %s,  address = %s WHERE username = %s"
            data = ( name, surname, contact,date_of_birth, email, address, oldUsername)
            cur.execute(query, data)
            mysql.connection.commit()
           
            cur.close()
            return True
        except Exception as e:
            print(f"Error changing profile: {e}")
            return False
