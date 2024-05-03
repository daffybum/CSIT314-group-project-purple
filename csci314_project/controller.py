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
    
