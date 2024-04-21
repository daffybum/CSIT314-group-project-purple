from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import mysql

import stripe

from werkzeug.security import generate_password_hash

from visualex import controller
from visualex import entity

import urllib.request
import os
from werkzeug.utils import secure_filename

boundary = Blueprint('boundary', __name__)  # Blueprints means it has roots inside a bunch of URLs defined

stripe.api_key = "sk_test_51Ou5FZRqVdY5zwenlu9FnQVHaDupGLqxqjC6J6eyBXR09ZccqROeV85QcLOCWb8wFtQYMT4P3FlaIGOOmxJHHFCa00K7pXYYUU"

YOUR_DOMAIN = "http://localhost:5000"

# AUTHENTICATION
@boundary.route('/', methods=['GET', 'POST'])
def login():                                     
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        loginController = controller.LoginController()
        user = loginController.userLogin(username, password)
        #print(user.username)
        if (user):
            return redirect(url_for('boundary.home'))
        else:
            flash('Wrong password or username', category='error')

    return render_template("login.html", boolean=True)

@boundary.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    return render_template("homepage.html", user_name = username)

@boundary.route('/forgotpw', methods=['GET', 'POST'])
def forgotpw():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('newPassword')
        password2 = request.form.get('cfmPassword')

        if password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            changePasswordController = controller.ChangePasswordController()
            password1 = generate_password_hash(password1, method='pbkdf2')
            result = changePasswordController.changePW(username,password1)
            if (result):
                flash('Password Changed!', category='success')
            else:
                flash('Cannot change Password!', category='error')

    return render_template("forgotpw.html")

@boundary.route('/logout')
def logout():
    return"<p>Logout</p>"

@boundary.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        surname = request.form.get('surname')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not role:
            flash('Please select a role.', category='error')
        else:
            createAccountController = controller.CreateUserAccController()
            password1 = generate_password_hash(password1, method='pbkdf2')
            userAcc = entity.UserAccount(username, password1, name, surname, email, date_of_birth, address, role)
            result = createAccountController.createUserAccount(userAcc)
            if (result):
                flash('Account created!', category='success')
            else:
                flash('Cannot Create Account!', category='error')

    return render_template("sign_up.html")

@boundary.route('/about-us')
def aboutus():
    username = session.get('username')
    return render_template("AboutUs.html", user_name = username)

@boundary.route('/membersubscription')
def membersubscription():
    username = session.get('username')
    return render_template('membersubscription.html', user_name = username)


@boundary.route('/paymentSuccess')     # payment page
def handle_payment_success_1():
    username = session.get('username')
    getInvoiceController = controller.GetInvoiceController()
    makePaymentController = controller.MakePaymentController()
    assignMembershipController = controller.AssignMembershipController()
    charges = 20.00
    membership = "gold"
    payment = makePaymentController.makePayment(username, charges)
    display = getInvoiceController.viewDisplay(payment)
    assignMembershipController.assignMembership(username, membership)
    return render_template("paymentSuccess.html", user_name = username, display = display, tier = membership.capitalize())

@boundary.route('/paymentSuccess')
def handle_payment_success_2():
    username = session.get('username')
    getInvoiceController = controller.GetInvoiceController()
    makePaymentController = controller.MakePaymentController()
    assignMembershipController = controller.AssignMembershipController()
    charges = 10.00
    membership = "silver"
    payment = makePaymentController.makePayment(username, charges)
    display = getInvoiceController.viewDisplay(payment)
    assignMembershipController.assignMembership(username, membership)
    return render_template("paymentSuccess.html", user_name = username, display = display, tier = membership.capitalize())

@boundary.route('/create-payment-session', methods=['POST'])  # process payment
def create_checkout_session():
    try:

        username = session.get('username')

        checkMembershipController = controller.CheckMembershipController()

        check_membership = checkMembershipController.checkMembershipExist(username)

        if 'gold-membership' in request.form:

            if(check_membership == 1):
                 flash('Already has gold membership!', category='error')
                 return render_template("membersubscription.html", user_name = username)
            else:
                checkout_session = stripe.checkout.Session.create(
                    line_items = [
                        {
                            'price' : 'price_1Ou8paRqVdY5zwen2Qyhu1Ii',
                            'quantity':1
                        }
                    ],
                    mode="subscription",
                    success_url=url_for('boundary.handle_payment_success_1', _external=True),
                    cancel_url=YOUR_DOMAIN + "/membersubscription"
                )
        
        else:
            if(check_membership == 2):
                flash('Already has silver membership!', category='error')
                return render_template("membersubscription.html", user_name = username)
            else:
                checkout_session = stripe.checkout.Session.create(
                line_items = [
                    {
                        'price' : 'price_1Ou8ovRqVdY5zwenxIfO8AoS',
                        'quantity':1
                    }
                ],
                mode="subscription",
                success_url=url_for('boundary.handle_payment_success_2', _external=True),
                cancel_url=YOUR_DOMAIN + "/membersubscription"
                )
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)


@boundary.route('/userfb', methods=['GET'])
def user_feedback():
    username = session.get('username')
    feedback_controller = controller.ViewFeedbackController()
    feedback_list = feedback_controller.viewFeedback()
    return render_template("feedbackUserPage.html", feedback_list=feedback_list, user_name = username)


@boundary.route('/submitfb', methods=['GET', 'POST'])
def submit_feedback():
    username = session.get('username')
    if request.method == 'POST':
        feedback_content = request.form['feedbackText']
        submitFBController = controller.UploadFeedbackController()
        submitFB = submitFBController.uploadFeedback(username, feedback_content)
        # uploading test
        if submitFB:
            flash('Feedback submitted!', category='success')
            # Redirect back to the user feedback page after submitting feedback
            return redirect(url_for('boundary.user_feedback'))
        else:
            flash('Feedback Submission Invalid!', category='error')
                
    return render_template("feedbackSubmitPage.html", user_name = username)



@boundary.route('/adminfb', methods=['GET'])
def admin_feedback():
    username = session.get('username')
    feedback_controller = controller.ViewFeedbackController()
    feedback_list = feedback_controller.viewFeedback()
    return render_template("feedbackAdminPage.html", feedback_list=feedback_list, user_name=username)



# Upload Image Function
UPLOAD_FOLDER = 'visualex/static/uploads/'
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@boundary.route('/uploadImage')
def upload():
    username = session.get('username')
    return render_template('uploadImage.html', user_name = username)
 
@boundary.route('/uploadImage', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        return render_template('uploadImage.html', filename=filename)
    else:
        flash('Allowed image types are - png and jpeg only')
        return redirect(request.url)
 
@boundary.route('/display/<filename>')  #display image on uploadImage.html
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
@boundary.route('/history', methods=['GET', 'POST'])
def history_logs():
    username = session.get('username')
    history_logs_controller = controller.ViewHistoryController()
    history_logs = history_logs_controller.viewHistory(username)
    return render_template('history.html', history_logs=history_logs, user_name=username)

@boundary.route('/viewmembershiptier')
def view_membership_tier():
    username = session.get('username')
    membership_controller = controller.MembershipController()
    membership_tier = membership_controller.get_membership_tier_info(username)
    return render_template('viewmembershiptier.html', membership_tier=membership_tier, user_name=username)

@boundary.route('/account-detail', methods=['GET', 'POST'])
def display_profile():
    username = session.get('username')
    if username:
        display= controller.DisplayController()
        user = display.get_user_info(username)
        if user:
            username,name, surname, email, address = user
            return render_template("accountdetail.html", username=username,name=name, surname=surname, email=email, address=address, user_name = username)
        else:
            flash('User not found', category='error')
            return redirect(url_for('boundary.login'))
    else:
        flash('User not logged in', category='error')
        return redirect(url_for('boundary.login'))

# Admin View All users details Main page   
@boundary.route('/viewAllUsers')
def viewAllUsers():
    username = session.get('username')
    getAllUserController = controller.GetAllUsersController()
    users_list = getAllUserController.get_all_users()
    return render_template('viewAllUsersAccount.html', user_name = username, users_list = users_list, search_exist = False)

# If admin clicks view button
@boundary.route('/viewUserDetails', methods=['POST'])
def viewUserDetails():
    username = session.get('username')
    selected_user = request.form['selectedUsername']
    display= controller.DisplayController()
    user = display.get_user_info(selected_user)
    if user:
        selected_user,name, surname, email, address = user
        return render_template("accountdetail.html", username=selected_user,name=name, surname=surname, email=email, address=address, user_name = username)


# If admin clicks search
@boundary.route('/viewSearchedUserDetails', methods=['POST'])
def viewSearchedUserDetails():
    username = session.get('username')
    inputUsername = request.form.get('inputUsername')
    searchUserController = controller.SearchUserController()
    searchedUsername = searchUserController.search_user(inputUsername)
    if searchedUsername is None:
        flash('Username does not exist!', category='error')
        getAllUserController = controller.GetAllUsersController()
        users_list = getAllUserController.get_all_users()
        return render_template('viewAllUsersAccount.html', user_name = username, users_list = users_list, search_exist = False)
    else:
        return render_template('viewAllUsersAccount.html', user_name = username, users = searchedUsername ,search_exist = True)
