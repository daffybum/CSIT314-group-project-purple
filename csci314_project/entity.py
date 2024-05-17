from flask import session
from . import mysql
import random
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from datetime import datetime, timedelta 


class UserProfile:
    def __init__(self, role= None,description=None, status = None):
        self.role = role
        self.description= description
        self.status = status
        
    def get_all_role(self):

        try:
                cur = mysql.connection.cursor()

                query = "SELECT * FROM userprofiles"
                cur.execute(query)
                profile_list = []
                for profile_data in cur.fetchall():
                    profile_item = UserProfile(role=profile_data[0], description=profile_data[1], status=profile_data[2])
                    profile_list.append(profile_item)
                cur.close()
            
                return profile_list
            
        except Exception as e:
            print(f"Error display property: {e}")
            
    def insert_new_role(self, role, description):
        try:
            cur = mysql.connection.cursor()
            insert_query = "INSERT INTO userprofiles (role, description) VALUES (%s, %s)"
            cur.execute(insert_query, (role, description))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error inserting: {str(e)}")
            return False
        

    def update_description(self,role,new_description):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE userprofiles SET description = %s WHERE role = %s;"
            cur.execute(query,(new_description,role))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error updating")
            
#end ==========================================================================================================

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

    def generate_users(self):
        for i in range(5):  # 100 rows
            cur = mysql.connection.cursor()
            role = random.choice(['buyer', 'seller', 'real_estate_agent'])
            username = ''
            vowels = 'aeiou'
            consonants = 'bcdfghjklmnpqrstvwxyz'
            for i in range(5):
                if i % 2 == 0:  # Even position, add a consonant
                    username += random.choice(consonants)
                else:  # Odd position, add a vowel
                    username += random.choice(vowels)
            
            hashed_password=generate_password_hash(username)
            password = hashed_password
            
            name = username
            surname = username
            contact = ''.join(random.choice('0123456789') for _ in range(8))

            start_date = datetime(1900, 1, 1)
            end_date = datetime(2004, 12, 31)
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            random_date = start_date + timedelta(days=random_days)
            date_of_birth = random_date.strftime('%Y-%m-%d')
            email = f"{username}@example.com"
            stations = [
            "Jurong East", "Bukit Batok", "Bukit Gombak", "Choa Chu Kang", "Yew Tee",
            "Kranji", "Marsiling", "Woodlands", "Admiralty", "Sembawang",
            "Canberra", "Yishun", "Khatib", "Yio Chu Kang", "Ang Mo Kio",
            "Bishan", "Braddell", "Toa Payoh", "Novena", "Newton",
            "Orchard", "Somerset", "Dhoby Ghaut", "City Hall", "Raffles Place",
            "Marina Bay", "Marina South Pier", "Pasir Ris", "Tampines", "Simei",
            "Tanah Merah", "Expo", "Changi Airport", "Tanjong Pagar", "Outram Park",
            "Tiong Bahru", "Redhill", "Queenstown", "Commonwealth", "Buona Vista",
            "Dover", "Clementi", "Jurong East", "Chinese Garden", "Lakeside",
            "Boon Lay", "Pioneer", "Joo Koon", "Gul Circle", "Tuas Crescent",
            "Tuas West Road", "Tuas Link"
            ]
            address = random.choice(stations)
            query = "INSERT INTO useraccount (role, username, password, name, surname, contact, date_of_birth, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (role, username, password, name, surname, contact, date_of_birth,email, address)
            cur.execute(query, data)


    
        query = "SELECT username FROM useraccount"
        cur.execute(query)
        
        results = cur.fetchall()
        
        usernames = [row[0] for row in results]
        mysql.connection.commit()
        cur.close()
        
        print("Created users: " , usernames)
        return True


    def login(self, username, password, role):
        session['username'] = username
        session['role'] = role
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
        session['selected_user'] = username # store the username in the session
        cur = mysql.connection.cursor()
        query = "SELECT role,username, name, surname,contact, date_of_birth,email, address FROM useraccount WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return user_data
    
    def get_user_account(self, username):  
        session['selected_user'] = username # store the username in the session
        cur = mysql.connection.cursor()
        query = "SELECT role, username, password FROM useraccount WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        print(user_data)
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

    def edit_profile(self, oldUsername, name, surname, contact, date_of_birth,email, address):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET name = %s, surname = %s, contact = %s, date_of_birth = %s, email = %s,  address = %s WHERE username = %s"
            cur.execute(query, ( name, surname, contact,date_of_birth, email, address, oldUsername))
            mysql.connection.commit()
            return True
        except Exception as e:
            # Log the exception here
            print(f"An error occurred: {e}")
            return False
    
    
    def displayallagent(self):
        try:
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
        except Exception as e:
            print(f"Error displaying agents: {e}")
            return False

    def get_agent_info(self, agentname):  
        try:
            session['agentname'] = agentname 
            cur = mysql.connection.cursor()
            query = "SELECT role,username,contact FROM useraccount WHERE username = %s"
            cur.execute(query, (agentname,))
            agent_data = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            return agent_data
        except Exception as e:
            print(f"Error getting agent info: {e}")
            return False        
    
    def delete_account(self, username):
        try:
            cur = mysql.connection.cursor()
            delete_review_agent_query = "DELETE FROM review WHERE agent_name = %s"
            delete_review_posted_query = "DELETE FROM review WHERE posted_by = %s"
            cur.execute(delete_review_agent_query, (username,))
            cur.execute(delete_review_posted_query, (username,))

            # Delete all entries from favourites where buyer_name is the username
            delete_favourites_query = "DELETE FROM favourites WHERE buyer_name = %s"
            cur.execute(delete_favourites_query, (username,))

            # Delete all properties posted by the user
            delete_properties_query = "DELETE FROM properties WHERE property_postedBy = %s"
            cur.execute(delete_properties_query, (username,))

            # Finally, delete the user account
            delete_user_query = "DELETE FROM useraccount WHERE username = %s"
            cur.execute(delete_user_query, (username,))

            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error deleting account: {e}")
            return False
    
    def update_password(self, username , new_password):
        try:
            new_hashed_password = generate_password_hash(new_password)
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET password = %s WHERE username = %s;"
            data = (new_hashed_password , username)
            cur.execute(query, data)
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating your password: {e}")
            return False   

    def admin_update_password(self, username , new_password):
        try:
            new_hashed_password = generate_password_hash(new_password)
            print(new_password)
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET password = %s WHERE username = %s;"
            data = (new_hashed_password , username)
            cur.execute(query, data)
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating user password: {e}")
            return False           

    def suspendAccount(self, username):
        try:
            cur = mysql.connection.cursor()
            query = "UPDATE useraccount SET password = NULL WHERE username = %s;"
            data = (username)
            cur.execute(query, data)
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating user password: {e}")
            return False         


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
        
    def generate_properties(self):
        
        stations = [
        "Jurong East", "Bukit Batok", "Bukit Gombak", "Choa Chu Kang", "Yew Tee",
        "Kranji", "Marsiling", "Woodlands", "Admiralty", "Sembawang",
        "Canberra", "Yishun", "Khatib", "Yio Chu Kang", "Ang Mo Kio",
        "Bishan", "Braddell", "Toa Payoh", "Novena", "Newton",
        "Orchard", "Somerset", "Dhoby Ghaut", "City Hall", "Raffles Place",
        "Marina Bay", "Marina South Pier", "Pasir Ris", "Tampines", "Simei",
        "Tanah Merah", "Expo", "Changi Airport", "Tanjong Pagar", "Outram Park",
        "Tiong Bahru", "Redhill", "Queenstown", "Commonwealth", "Buona Vista",
        "Dover", "Clementi", "Jurong East", "Chinese Garden", "Lakeside",
        "Boon Lay", "Pioneer", "Joo Koon", "Gul Circle", "Tuas Crescent",
        "Tuas West Road", "Tuas Link"
        ]
        for i in range(5):
            cur = mysql.connection.cursor()
            location = random.choice(stations)
            type = random.choice(['HDB', 'condo', 'landed'])
            property_name = f' A {type} house at {location} MRT station '
            property_type = type
            property_location = location
            random_number = random.uniform(1000, 1000000)
            price = round(random_number, 2)

            property_price = price
            property_bedroom = random.choice(['1,2,3,4,5'])
            property_bathroom = random.choice(['1,2,3,4,5'])
            property_size = random.randint(100, 2000)
            property_status = random.choice(['selling','sold'])
            getusername_query = "SELECT username FROM useraccount WHERE role NOT IN ('buyer', 'admin');"
            cur.execute(getusername_query)
            results = cur.fetchall()
            usernames = [row[0] for row in results]
            property_postedBy = random.choice(usernames)
            query = "INSERT INTO properties (property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy, property_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (property_name,property_type , property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy, property_status)
            cur.execute(query, data)

        query = "SELECT property_name FROM properties"
        cur.execute(query)
        
        results = cur.fetchall()
        
        properties = [row[0] for row in results]
        mysql.connection.commit()
        cur.close()
        
        print("Created properties: " , properties)
        return True

        
        
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
        session['property_id']=property_id
        try:
            cur = mysql.connection.cursor()

            # Fetch property detail
            fetch_query = "SELECT * FROM properties WHERE property_id = %s"
            cur.execute(fetch_query, (property_id,))
            property_data = cur.fetchone()

            # Insert property_id into detail table
            insert_query = "INSERT INTO detail (property_id) VALUES (%s)"
            cur.execute(insert_query, (property_id,))
            
            mysql.connection.commit()  # Commit both the SELECT and INSERT operations

        except Exception as e:
            # Log the exception here
            print(f"An error occurred: {e}")
            mysql.connection.rollback()  # Rollback the transaction in case of error
            property_data = None
        finally:
            if cur is not None:
                cur.close()
        
        return property_data
    
    def get_property_detail2(self,property_id):
        session['property_id']=property_id
        cur = mysql.connection.cursor()

        # Fetch property detail
        fetch_query = "SELECT * FROM properties WHERE property_id = %s"
        cur.execute(fetch_query, (property_id,))
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
            
    def search_newproperty(self, property_location):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_location = %s AND property_status = 'selling'"
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
            
    def search_oldproperty(self, property_location):
        try:
            cur = mysql.connection.cursor()

            query = "SELECT * FROM properties where property_location = %s AND property_status = 'sold'"
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
            property_list = []
            for property_data in cur.fetchall():
                property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                property_list.append(property_item)
            cur.close()
           
            return property_list
         
        except Exception as e:
            print(f"Error searching property: {e}")
            
                
    def delete_property(self,property_id):
        try:
            cur = mysql.connection.cursor()
            delete_query = "DELETE FROM properties where property_id = %s"
            delete_query1 = "DELETE FROM favourites where property_id= %s"
            cur.execute(delete_query, (property_id,))
            cur.execute(delete_query1, (property_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error deleting property: {e}")
            return False
            
    def update_property(self,property_name,property_type,property_location,property_price,property_bedroom,property_bathroom,property_size,property_status,property_id):
        try:
            cur=mysql.connection.cursor()
            query = "UPDATE properties SET property_name=%s,property_type=%s,property_location=%s,property_price=%s,property_bedroom=%s,property_bathroom=%s,property_size=%s,property_status=%s WHERE property_id = %s"
            data = (property_name,property_type,property_location,property_price,property_bedroom,property_bathroom,property_size,property_status,property_id,)
            cur.execute(query, data)
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error update property: {e}")
            return False
                
            

            
class favourite:
    def __init__(self,favourite_id=None,buyer_name=None,property_id=None):
        self.favourite_id = favourite_id
        self.buyer_name = buyer_name
        self.property_id = property_id

    def generate_favourites(self):
        
        for i in range(5):
            try:
                cur = mysql.connection.cursor()
                
                getbuyerid_query = "SELECT username FROM useraccount WHERE role = 'buyer';"
                cur.execute(getbuyerid_query)
                results = cur.fetchall()
                buyers = [row[0] for row in results]
                buyer_name = random.choice(buyers)
                propertyid_query = "SELECT property_id FROM properties;"
                cur.execute(propertyid_query)
                results = cur.fetchall()
                propertyid = [row[0] for row in results]
                property_id = random.choice(propertyid)
                
                query = "INSERT INTO favourites (buyer_name, property_id) VALUES (%s, %s)"
                data = (buyer_name, property_id)
                cur.execute(query, data)
            except Exception as e:

                print(f"An error occurred: {e}")
                pass


        mysql.connection.commit()
        cur.close()
        return True
    
    def save_favourite(self,buyer_name,property_id):
            session['property_id']=property_id
            try:
                cur = mysql.connection.cursor()

                # Fetch property detail
                fetch_query = "SELECT * FROM properties "
                cur.execute(fetch_query)
                property_list = []
                for property_data in cur.fetchall():
                    # Assuming PropertyListing is defined elsewhere and takes the same arguments
                    property_item = PropertyListing(property_id=property_data[0], property_name=property_data[1], property_type=property_data[2], property_location=property_data[3], property_price=property_data[4], property_bedroom=property_data[5], property_bathroom=property_data[6], property_size=property_data[7], property_postedBy=property_data[8], property_status=property_data[9])
                    property_list.append(property_item)

                # Insert property_id into detail table
                insert_query = "INSERT INTO favourites (buyer_name,property_id) VALUES(%s,%s)"
                cur.execute(insert_query, (buyer_name,property_id,))
                
                mysql.connection.commit()  # Commit both the SELECT and INSERT operations

            except Exception as e:
                # Log the exception here
                print(f"An error occurred: {e}")
                mysql.connection.rollback()  # Rollback the transaction in case of error
                return False
            finally:
                if cur is not None:
                    cur.close()
            
            return property_list
    
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

    def display_favourite(self,buyer_name):
            try:
                cur=mysql.connection.cursor()
                query = "SELECT f.favourite_id,f.property_id,p.property_name,p.property_type, p.property_location, p.property_price, p.property_bedroom, p.property_bathroom, p.property_size, p.property_postedBy, p.property_status FROM Properties p INNER JOIN favourites f ON p.property_id = f.property_id WHERE f.buyer_name = %s;"
                data = (buyer_name,)
                cur.execute(query, data)
                favourite_properties = []
                for row in cur.fetchall():
                    favourites = favourite(favourite_id=row[0], property_id=row[1])
                    property = {
                        'property_name': row[2],
                        'property_type': row[3],
                        'property_location': row[4],
                        'property_price': row[5],
                        'property_bedroom': row[6],
                        'property_bathroom': row[7],
                        'property_size': row[8],
                        'property_postedBy': row[9],
                        'property_status': row[10]
                    }
                    favourite_properties.append((favourites, property))
                cur.close()

                return favourite_properties
            except Exception as e:
                print(f"Error viewing favourites: {e}")
                return []

    def display_sum_favourites(self, property_id):
        try:
            cur = mysql.connection.cursor()
            query = "SELECT COUNT(*) AS total_properties FROM favourites WHERE property_id = %s;"
            cur.execute(query, (property_id,))
            total_properties = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            
            #if total_properties:
                #print(f"Total properties for property ID {property_id}: {total_properties[0]}")
            return total_properties
            #else:
                #return False
        except Exception as e:
            print(f"Error displaying properties: {e}")
            return False

            
        
            
class Review:
    def __init__(self,agent_name=None,review_text=None,rating =None,posted_by=None):
        self.agent_name = agent_name
        self.review_text = review_text
        self.rating = rating
        self.posted_by = posted_by

    def generate_reviews(self):
        

        for i in range(5):
            try:
                cur = mysql.connection.cursor()
                getagent_query = "SELECT username FROM useraccount WHERE role = 'real_estate_agent';"
                cur.execute(getagent_query)
                agentresults = cur.fetchall()
                agents = [row[0] for row in agentresults]
                agent_name = random.choice(agents)
                
                review_text = random.choice(['Good','bad','could better','amazing','horrible'])
                rating = random.choice(['1','2','3','4','5'])
                
                getusername_query = "SELECT username FROM useraccount WHERE role NOT IN ('real_estate_agent', 'admin');"
                cur.execute(getusername_query)
                results = cur.fetchall()
                usernames = [row[0] for row in results]
                posted_by = random.choice(usernames)
                
                query = "INSERT INTO review (agent_name,review_text,rating, posted_by ) VALUES (%s, %s, %s, %s)"
                data = (agent_name, review_text, rating, posted_by)
                cur.execute(query, data)
            except Exception as e:

                print(f"An error occurred: {e}")
                pass


        mysql.connection.commit()
        cur.close()
        
        return True
    
    def givereview(self,agentname,review,rating,postedby):
            try:
                cur=mysql.connection.cursor()
                fetch_query = "SELECT role,username,contact FROM useraccount WHERE username = %s"
                cur.execute(fetch_query, (agentname,))
                agent_data = cur.fetchone()
                insert_query = "INSERT INTO review (agent_name,review_text,rating,posted_by) VALUES(%s,%s,%s,%s)"
                cur.execute(insert_query, ((agentname,review,rating,postedby,)))
                mysql.connection.commit()  # Commit both the SELECT and INSERT operations
            except Exception as e:
            # Log the exception here
                print(f"An error occurred: {e}")
                mysql.connection.rollback()  # Rollback the transaction in case of error
                return False
            finally:
                if cur is not None:
                    cur.close()
        
            return agent_data
        
    def displayreview(self,agent_name):
        session['agentname'] = agent_name 
        try:
            cur=mysql.connection.cursor()
            query = "SELECT agent_name,review_text,rating,posted_by from review WHERE agent_name = %s"
            data = (agent_name,)
            cur.execute(query, data)
            review_list = []
            for review_data in cur.fetchall():
                review = Review(agent_name=review_data[0],review_text=review_data[1], rating=review_data[2], posted_by=review_data[3])
                review_list.append(review)
            cur.close()
            return review_list
        
        except Exception as e:
            print(f"Error saving review: {e}")
            return False
        
        
class detail:
    def _init_(self,detail_id=None,property_id=None):
        self.detail_id = detail_id
        self.property_id = property_id

    
    def display_sum_click_detail(self, property_id):
            try:
                cur = mysql.connection.cursor()
                query = "SELECT COUNT(*) AS total_properties_num FROM detail WHERE property_id = %s;"
                cur.execute(query, (property_id,))
                total_properties = cur.fetchone()
                mysql.connection.commit()
                cur.close()
                
                #if total_properties:
                    #print(f"Total properties for property ID {property_id}: {total_properties[0]}")
                return total_properties
                #else:
                    #return False
            except Exception as e:
                print(f"Error displaying properties: {e}")
                return False


