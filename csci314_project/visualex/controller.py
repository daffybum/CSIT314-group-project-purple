from visualex import entity

# User Account related Controllers
class LoginController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def userLogin(self, username, password):
        return self.userAccount.login(username, password)

class CreateUserAccController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def createUserAccount(self, userAcc):
        return self.userAccount.createUserAcc(userAcc)
    
class ChangePasswordController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def changePW(self, username, password):
        return self.userAccount.changePW(username, password)
    

class UploadFeedbackController:
    def __init__(self):
        self.feedback_forum = entity.FeedbackForum()
    def uploadFeedback(self, username, feedback):
        return self.feedback_forum.submitfeedback(username, feedback)
    
class ViewFeedbackController:
    def __init__(self):
        self.feedback_list = entity.FeedbackForum()
    def viewFeedback(self):
        return self.feedback_list.get_all_feedback()
    
class AssignMembershipController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def assignMembership(self, username, membership):
        return self.userAccount.assignMembership(username, membership)
    
class CheckMembershipController:
    def __init__(self):
        self.userAccount = entity.UserAccount()
    def checkMembershipExist(self, username):
        return self.userAccount.checkMembershipExist(username)
    
# Transaction Related Controller
class MakePaymentController:
    def __init__(self):
        self.transactions = entity.Transactions()
    def makePayment(self, username, charges):
        return self.transactions.make_payment(username, charges)
    
class GetInvoiceController:
    def __init__(self):
        self.display = entity.Transactions()
    def viewDisplay(self,payment_timestamp):
        return self.display.get_invoice(payment_timestamp)
    
class ViewHistoryController:
    def __init__(self):
        self.history_log = entity.HistoryLogs()
    def viewHistory(self, username):
        return self.history_log.get_history_logs_with_predictions(username)
    
class MembershipController:
    def __init__(self):
        self.view_membership_tier = entity.UserAccount()

    def get_membership_tier_info(self, username):
        return self.view_membership_tier.get_membership_tier_info(username)
    

class DisplayController:
    def __init__(self):
        self.userAccount = entity.UserAccount()

    def get_user_info(self, username):
        return self.userAccount.get_user_info(username)
    
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
