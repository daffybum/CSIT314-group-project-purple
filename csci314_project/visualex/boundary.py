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
