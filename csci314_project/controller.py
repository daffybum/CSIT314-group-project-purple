from csci314_project import entity

#User Profile Controller ==============================================================================================
class getRoleListController:
    def __init__(self):
        self.userprofile = entity.UserProfile()
    
    def get_all_role(self):
        return self.userprofile.get_all_role()


class SubmitNewRoleController:
    def __init__(self):
        self.userProfile = entity.UserProfile()
    def submit_new_role(self,role,description):
        return self.userProfile.insert_new_role(role,description)
    
class updatedescriptionController:
    def __init__(self):
        self.userprofile = entity.UserProfile()
    
    def update_description(self, role , new_description):
        return self.userprofile.update_description(role, new_description)  
    
class viewSearcheduserprofileController():
    def __init__(self):
        self.userProfile = entity.UserProfile()
    
    def view_searched_userprofile(self, role):
        return self.userProfile.search_roles(role)

class deleteUserProfile():
    def __init__(self):
        self.userProfile = entity.UserProfile()
    
    def deleteUserProfile(self, role):
        return self.userProfile.delete_profile(role)    
#End ==================================================================================================================
    
  
# User Account Controllers==============================================================================================
class generateuseraccountController:
    def __init__(self):
        self.useraccount = entity.UserAccount()
    def generateUseraccount(self):
        return self.useraccount.generate_users()  

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


class DisplayAccountController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def get_user_info(self, username):
        return self.userAccount.get_user_info(username)

    
class DisplayAgentController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def display_all_agent(self):
        return self.userAccount.displayallagent()
    
class DisplayAgentDetailController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def displayAgentDetail(self, agentname):
        return self.userAccount.get_agent_info(agentname)
    

class DeleteController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def delete_profile(self, username):
        return self.userAccount.delete_account(username, )
    

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
    
    def get_all_users(self):
        return self.userAccount.get_all_users()

    
class EditProfileController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def get_user_info(self,selected_user):
        return self.userAccount.get_user_info(selected_user)
        
    def edit_profile(self,selected_user, name, surname, contact, date_of_birth, email, address ):
        return self.userAccount.edit_profile( selected_user,name, surname,contact,date_of_birth,  email,address)
    
class adminupdatePasswordController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def admin_update_password(self, username, new_password):
        return self.userAccount.admin_update_password(username, new_password )

#End ======================================================================================================================

#property lisitng Controllers ==============================================================================================

class generatepropertiesController:
    def __init__(self):
        self.useraccount = entity.PropertyListing()
    def generateproperties(self):
        return self.useraccount.generate_properties()
    
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
    
    def displayPropertyDetails2(self, property_id):
        return self.propertyListing.get_property_detail2(property_id)
    
class viewSearchedpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_searched_propertyList(self, property_location):
        return self.propertyListing.search_property(property_location)
    
class viewSearchednewpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_searched_newpropertyList(self, property_location):
        return self.propertyListing.search_newproperty(property_location)
    
class viewSearchedoldpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_searched_oldpropertyList(self, property_location):
        return self.propertyListing.search_oldproperty(property_location)

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
    
class viewPersonalpropertyController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()
    
    def view_personal_property(self, posted_by):
        return self.propertyListing.view_personal_property(posted_by)
     
class deletePropertyListingController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()

    def deleteProperty(self,property_id):
        return self.propertyListing.delete_property(property_id)

class updatePropertyListingController():
    def __init__(self):
        self.propertyListing = entity.PropertyListing()

    def updateProperty(self,property_name,property_type,property_location,property_price,property_bedroom,property_bathroom,property_size,property_status,property_id):
        print('123')
        return self.propertyListing.update_property(property_name,property_type,property_location,property_price,property_bedroom,property_bathroom,property_size,property_status,property_id)
    

       
class displaySumDetailController():
    def __init__(self):
        self.detail = entity.detail()
        self.propertyListing = entity.PropertyListing()
    
    def displaySumDetail(self, property_id):
        return self.detail.display_sum_click_detail(property_id)
    
    def displayPropertyDetails2(self, property_id):
        return self.propertyListing.get_property_detail2(property_id)

#End ======================================================================================================================


#favourites Controllers ==============================================================================================
class generatefavouritesController:
    def __init__(self):
        self.useraccount = entity.favourite()
    def generatefavourites(self):
        return self.useraccount.generate_favourites() 

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
    
    
class displaySumFavouritesController:
     def __init__(self):
        self.favourite = entity.favourite()
        self.propertyListing = entity.PropertyListing()
        
     def display_sum_favourites(self, property_id):
        print('234')
        return self.favourite.display_sum_favourites(property_id)
        
     def displayPropertyDetails2(self, property_id):
        return self.propertyListing.get_property_detail2(property_id)
    
 

    
#End ======================================================================================================================

#review Controllers ==============================================================================================
class generatereviewController:
    def __init__(self):
        self.useraccount = entity.Review()
    def generatereview(self):
        return self.useraccount.generate_reviews() 
    
class GiveReviewController():
    def __init__(self):
        self.review = entity.Review()
    def give_review(self,agentname,review,rating,postedby):
        return self.review.givereview(agentname,review,rating,postedby)
    
class DisplayReviewController:
    def __init__(self):
        self.review = entity.Review()
    def displayReview(self, agentname):
        return self.review.displayreview(agentname)

class DisplayOwnReviewController:
    def __init__(self):
        self.review = entity.Review()
    def displayReview(self, agentname):
        return self.review.displayreview(agentname)    

 
    
    
#End ======================================================================================================================    

#detail Controllers ==============================================================================================

    
#End ======================================================================================================================









    
    




      



    

