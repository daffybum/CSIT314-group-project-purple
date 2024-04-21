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

           query = "INSERT INTO useraccount (username, password, name, surname, email, date_of_birth, address, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
           data = (userAcc.username, userAcc.password, userAcc.name, userAcc.surname, userAcc.email, userAcc.date_of_birth, userAcc.address, userAcc.role)
           cur.execute(query, data)
           
           mysql.connection.commit()
           
           cur.close()
           return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
        
    def assignMembership(self, username, membership):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET membership_tier = %s WHERE username = %s"
            data = (membership, username)
            cur.execute(query, data)
            mysql.connection.commit()
           
            cur.close()
            return True
        except Exception as e:
            print(f"Error changing Membership_tier: {e}")
            return False
        
    def checkMembershipExist(self, username):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT membership_tier FROM useraccount WHERE username = %s"
            data = (username,)
            cur.execute(query, data)
            membership_data = cur.fetchone()

            cur.close()

            if membership_data[0] == 'gold':
                return 1
            elif membership_data[0] == 'silver':
                return 2
            else:
                return 0
        except Exception as e:
            print(f"Error Checking Membership: {e}")
            return None
        
    def get_membership_tier_info(self, username):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT membership_tier FROM useraccount WHERE username = %s"
            cur.execute(query, (username,))
            membership_tier = cur.fetchone()[0]
            cur.close()

            if membership_tier == 'basic':
                return {'membership_tier': 'basic', 'monthly_fee': 'Free', 'description': [
                    '1. Generate Descriptive Text', 
                    '2. Text to Speech feature to read text as audio message']}
            elif membership_tier == 'silver':
                return {'membership_tier': 'Silver', 'monthly_fee': '$10.00', 'description': [
                    '1. Generate Descriptive Text',
                    '2. Text to Speech feature to read text as audio message',
                    '3. Selective analysis feature to circle image',
                    '4. Generate descriptive text on the selected part of the image']}
            elif membership_tier == 'gold':
                return {'membership_tier': 'Gold', 'monthly_fee': '$20.00', 'description': [
                    '1. Generate Descriptive Text',
                    '2. Text to Speech feature to read text as audio message',
                    '3. Selective analysis feature to circle image',
                    '4. Generate descriptive text on the selected part of the image',
                    '5. Generate a story for the image instead of just descriptive text.']}
            else:
                return None
        except Exception as e:
            print(f"Error Retrieving Membership Tier Info: {e}")
            return None
        
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

class Transactions:
    def __init__(self, transaction_id=None, username=None, payment_timestamp=None, charges=None):
        self.transaction_id = transaction_id
        self.username = username
        self.payment_timestamp = payment_timestamp
        self.charges = charges

    def make_payment(self, username, charges):
        try:

            current_timestamp = datetime.utcnow()

            # Define the timezone GMT+8
            gmt8_timezone = pytz.timezone('Asia/Singapore')

            # Localize the current timestamp to GMT+8 timezone
            payment_timestamp = pytz.utc.localize(current_timestamp).astimezone(gmt8_timezone)

            cur = mysql.connection.cursor()

            query = "INSERT INTO transaction (username, payment_timestamp, charges) VALUES (%s, %s, %s)"
            data = (username, payment_timestamp, charges)
            cur.execute(query, data)

            mysql.connection.commit()

            cur.close()
            payment_timestamp = str(payment_timestamp)
            parts = payment_timestamp.split(".")
            fisrt_part = parts[0]
            return fisrt_part
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return False
        
    def get_invoice(self, payment_timestamp):
        try:

            cur = mysql.connection.cursor()

            query = "SELECT * FROM transaction WHERE payment_timestamp = %s"
            data = (payment_timestamp,)
            cur.execute(query, data)

            display = cur.fetchone()

            cur.close()
            return display
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return False
        
class HistoryLogs:
    def __init__(self, history_id=None, username=None, h_date=None, result_id=None):
        self.history_id = history_id
        self.username = username
        self.h_date = h_date
        self.result_id = result_id
    
    def get_history_logs_with_predictions(self, username):
        try:
            cur = mysql.connection.cursor()

            query = """
            SELECT h.*, p.image_id, p.predicted_label, p.confidence_score, i.image_data
            FROM history h
            JOIN prediction_results p ON h.result_id = p.result_id
            JOIN image_metadata i ON p.image_id = i.image_id
            WHERE h.username = %s
            """
            cur.execute(query, (username,))
            history_logs_with_predictions_and_images = []
            for row in cur.fetchall():
                history_log = HistoryLogs(history_id=row[0], username=row[1], h_date=row[2], result_id=row[3])
                image_blob = row[7]  # Assuming image_blob is the column storing BLOB data
                # Convert the binary image data to Base64
                image_data_base64 = base64.b64encode(image_blob).decode('utf-8')
                prediction_info = {
                    'image_id': row[4],
                    'predicted_label': row[5],
                    'confidence_score': row[6],
                    'image_data': image_data_base64
                }
                history_logs_with_predictions_and_images.append((history_log, prediction_info))

            cur.close()
            return history_logs_with_predictions_and_images
        except Exception as e:
            print(f"Error getting history logs with predictions and images: {e}")
            return []
