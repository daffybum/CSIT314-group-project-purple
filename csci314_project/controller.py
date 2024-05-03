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
        return self.userAccount.edit_profile1( name, surname,contact,date_of_birth,  email,address,oldUsername)
