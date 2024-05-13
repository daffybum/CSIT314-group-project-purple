from csci314_project import entity

# User Account related Controllers
class LoginController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def userLogin(self, username, password, role):
        return self.userAccount.login(username, password, role)
    
class CreateUserAccController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def createUserAccount(self, userAcc):
        return self.userAccount.createUserAcc(userAcc)
        
class DisplayController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def get_user_info(self, username):
        return self.userAccount.get_user_info(username)

class DisplayAccountController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def get_user_account(self, username):
        return self.userAccount.get_user_account(username)
    
class DisplayPasswordController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def get_user_password(self, username):
        return self.userAccount.show_password(username)

class ViewBuyController:
    def __init__(self):
        pass

    def viewProperties(self):
        property_entity = entity.PropertyListing()
        return property_entity.get_property_listing()


class SubmitPropertyListingController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()

    def submit_property_listing(self, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy):
        return self.propertyListing.submit_property_listing(property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy)
    
    
class displayPropertyDetailController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def displayPropertyDetails(self, property_id):
        return self.propertyListing.get_property_detail(property_id)

class saveFavouriteController():
    def __init__(self):
        self.favourite = entity.favourite()
    
    def save_favourites(self,buyer_name,property_id):
        return self.favourite.save_favourite(buyer_name,property_id)

class ViewFavouriteController():
    def __init__(self):
        self.favourite = entity.favourite()
    
    def view_favourites(self,buyer_name):
        return self.favourite.display_favourite(buyer_name)  
    
class viewSearchedpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_searched_propertyList(self, property_location):
        return self.propertyListing.search_property(property_location)

class viewSellingpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_selling_propertyList(self):
        return self.propertyListing.view_selling_property() 
    
class viewSoldpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_sold_propertyList(self):
        return self.propertyListing.view_sold_property()

class DisplayAgentController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def display_all_agent(self):
        return self.userAccount.displayallagent()

class viewPersonalpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_personal_property(self, posted_by):
        return self.propertyListing.view_personal_property(posted_by)
    
class GiveReviewController():
    def __init__(self):
        self.review = entity.Review()
    def give_review(self,username,review,rating,postedby):
        return self.review.givereview(username,review,rating,postedby)

class DisplayAgentDetailController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def displayAgentDetail(self, agentname):
        return self.userAccount.get_agent_info(agentname)
    
class DisplayReviewController:
    def __init__(self):
        self.review = entity.Review()
    def displayReview(self, agentname):
        return self.review.displayreview(agentname)


class DeleteController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def delete_profile(self, username):
        return self.userAccount.delete_account(username, )

#ADMIN
class GetAllUsersController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    
    def get_all_users(self):
        return self.userAccount.get_all_users()

class SearchUserController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def search_user(self,username):
        return self.userAccount.search_user(username)
    
class EditProfileController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def edit_profile(self, role,oldUsername, newUsername, name, surname,contact,date_of_birth, email, address):
        return self.userAccount.edit_profile(role,oldUsername, newUsername, name, surname,contact,date_of_birth, email, address)
    def edit_profile1(self, name, surname, contact,date_of_birth,email, address,oldUsername,):
        print('123')
        return self.userAccount.edit_profile1( name, surname,contact,date_of_birth,  email,address,oldUsername)
        
