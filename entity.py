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
        session['username'] = username
        cur = mysql.connection.cursor()

        query = "SELECT password FROM useraccount WHERE username = %s AND role = %s"
        data = (username,role)
        cur.execute(query, data)
        account = cur.fetchone()    
        if account:
        
            check = check_password_hash(account[0], password)
            return check
        else:
            return False
        
        

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
        #session['selected_user'] = username # store the username in the session
        cur = mysql.connection.cursor()
        query = "SELECT role,username, name, surname,contact, date_of_birth,email, address FROM useraccount WHERE username = %s"
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
    
    def displayallagent(self):
        cur = mysql.connection.cursor()
        query = "SELECT username FROM useraccount WHERE role = 'real_estate_agent'"
        cur.execute(query)
        agent_list = []
        for agent_data in cur.fetchall():
            agent_item = UserAccount(username=agent_data[0])
            agent_list.append(agent_item)
        cur.close()
        print(agent_list)
        return agent_list


class PropertyListing:
    def __init__(self,property_id=None,property_name=None,property_type=None,property_location=None,property_price=None, property_bedroom=None,property_bathroom=None,property_size=None,property_status= None,property_postedBy=None):
        self.property_id = property_id
        self.property_name = property_name
        self.property_type =property_type
        self.property_location = property_location
        self.property_price = property_price
        self.property_bedroom = property_bedroom
        self.property_bathroom = property_bathroom
        self.property_size = property_size
        self.property_status = property_status
        self.property_postedBy = property_postedBy
        


    def submit_property_listing(self,property_name,property_type,property_location,property_price, property_bedroom,property_bathroom,property_size, property_postedBy):
        try:
           cur = mysql.connection.cursor()

           query = "INSERT INTO properties (property_name,property_type,property_location,property_price, property_bedroom,property_bathroom,property_size, property_postedBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
           data = (property_name,property_type,property_location,property_price, property_bedroom,property_bathroom,property_size,property_postedBy,)
           cur.execute(query, data)
           
           mysql.connection.commit()
           
           cur.close()
           return True
        except Exception as e:
            print(f"Error creating the property listing: {e}")
            return False
        
    
    def get_property_listing(self):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM properties"
            cur.execute(query)
            property_list = []
            for property_data in cur.fetchall():
                # Assuming PropertyListing is defined elsewhere and takes the same arguments
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
            return property_list
        except Exception as e:
            print(f"Error getting property list: {e}")
            
    def get_property_detail(self,property_id):
        #session['property_id']=property_id
        cur = mysql.connection.cursor()
        query = "SELECT * FROM properties WHERE property_id = %s"
        data = (property_id,)
        cur.execute(query, data)
        property_data = cur.fetchone()
        mysql.connection.commit()
        
        cur.close()
        return property_data
    
    def search_property(self, property_location):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_location = %s"
            data = (property_location,)
            cur.execute(query,data)
            property_list = []
            for property_data in cur.fetchall():
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
           
            return property_list
         
        except Exception as e:
            print(f"Error searching property: {e}")
    
    def view_selling_property(self):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_status = 'selling'"
            cur.execute(query)
            property_list = []
            for property_data in cur.fetchall():
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
            
            return property_list
            
        except Exception as e:
            print(f"Error searching property: {e}")
                
    def view_sold_property(self):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_status = 'sold'"
            cur.execute(query)
            property_list = []
            for property_data in cur.fetchall():
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
            
            return property_list
            
        except Exception as e:
            print(f"Error searching property: {e}")


    def view_personal_property(self, posted_by):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_postedBy = %s"
            data = (posted_by,)
            cur.execute(query,data)
            print(query)
            property_list = []
            for property_data in cur.fetchall():
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
           
            return property_list
         
        except Exception as e:
            print(f"Error searching property: {e}")
            
            
class favourite:
    def __init__(self,favourite_id=None,buyer_name=None,property_id=None):
        self.favourite_id = favourite_id
        self.buyer_id = buyer_name
        self.property_id = property_id

    def save_favourite(self,buyer_name,property_id):
        try:
            #session['selectedpropertys_id']=property_id
            cur=mysql.connection.cursor()
            query = "INSERT INTO favourites (buyer_name,property_id) VALUES(%s,%s)"
            data = (buyer_name, property_id,)
            cur.execute(query, data)
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False
    
    def display_favourite(self,buyer_name):
        try:
            cur=mysql.connection.cursor()
            query = "SELECT p.* FROM Properties p INNER JOIN favourites f ON p.property_id = f.property_id WHERE f.buyer_name = [username];"
            data = (buyer_name,)
            cur.execute(query, data)
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error viewing favourites: {e}")
            return False
        
        
class Review:
    def __init__(self,username=None,review=None,rating =None,postedby=None):
        self.username = username
        self.review = review
        self.rating = rating
        self.posteby = postedby

    def givereview(self,username,review,rating,postedby):
        try:
            cur=mysql.connection.cursor()
            query = "INSERT INTO review (agent_name,review_text,rating,posted_by) VALUES(%s,%s,%s,%s)"
            data = (username,review,rating,postedby)
            cur.execute(query, data)
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error saving review: {e}")
            return False
    
            