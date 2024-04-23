from flask import session
from . import mysql
from werkzeug.security import check_password_hash
from datetime import datetime
import pytz
import base64

class UserAccount:
    def __init__(self, username=None, password=None, name=None, surname=None, email=None, date_of_birth=None, address=None, role=None, membership_tier="basic"):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address
        self.membership_tier = membership_tier
        self.role = role

    def login(self, username, password):

        session['username'] = username # store the username in the session

        cur = mysql.connection.cursor()

        query = "SELECT password FROM useraccount WHERE username = %s"
        data = (username,)
        cur.execute(query, data)
        account = cur.fetchone()
        check = check_password_hash(account[0], password)

        return check
    
    
    def changePW(self, username, password):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET password = %s WHERE username = %s"
            data = (password, username)
            cur.execute(query, data)
            mysql.connection.commit()
           
            cur.close()
            return True
        except Exception as e:
            print(f"Error changing Password: {e}")
            return False


    def createUserAcc(self, userAcc):
        try:
            cur = mysql.connection.cursor()

            query = "INSERT INTO useraccount (username, password, name, surname, email, date_of_birth, address, role, membership_tier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            data = (userAcc.username, userAcc.password, userAcc.name, userAcc.surname, userAcc.email, userAcc.date_of_birth, userAcc.address, userAcc.role, userAcc.membership_tier)
            cur.execute(query, data)
           
            mysql.connection.commit()
           
            cur.close()
            return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
        
     
    def get_user_info(self, username):
        cur = mysql.connection.cursor()
        query = "SELECT username, name, surname, email, address FROM useraccount WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return user_data
    
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

class FeedbackForum:
    def __init__(self, feedback_id=None, username=None, content=None, feedback_date=None):
        self.feedback_id = feedback_id
        self.username = username
        self.content = content
        self.feedback_date = feedback_date

    def submitfeedback(self, username, content):
        try:
            cur = mysql.connection.cursor()

            query = "INSERT INTO feedback (username, f_content, feedback_date) VALUES (%s, %s, %s)"
            data = (username, content, datetime.now())
            cur.execute(query, data)

            mysql.connection.commit()

            cur.close()
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False

    def get_all_feedback(self):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM feedback"
            cur.execute(query)
            feedback_list = []
            for feedback_data in cur.fetchall():
                feedback = FeedbackForum(feedback_id=feedback_data[0], username=feedback_data[1], content=feedback_data[2], feedback_date=feedback_data[3])
                feedback_list.append(feedback)

            cur.close()
            return feedback_list
        except Exception as e:
            print(f"Error getting feedback list: {e}")
    
    def time_difference(self, feedback_date):
        #Calculate the time difference between the feedback date and the current time.
        current_time = datetime.now()
        time_diff = current_time - feedback_date
        
        # Extract days, hours, and minutes
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds // 60) % 60
        
        # Format the time difference
        if days == 0:
            if hours == 0:
                if minutes < 2:
                    return "just now"
                else:
                    return f"{minutes} minutes ago"
            elif hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
        elif days == 1:
            return "1 day ago"
        elif days < 30:
            return f"{days} days ago"
        elif days < 365:
            months = days // 30
            return f"{months} months ago"
        else:
            years = days // 365
            return f"{years} years ago"


