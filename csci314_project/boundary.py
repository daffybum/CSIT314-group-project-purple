from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from csci314_project import controller
from csci314_project import entity
from werkzeug.security import generate_password_hash

boundary = Blueprint('boundary', __name__)  # Blueprints means it has roots inside a bunch of URLs defined
@boundary.route('/', methods=['GET', 'POST'])
def login():                                     
    if request.method == 'POST':
        role =  request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        loginController = controller.LoginController()
        user = loginController.userLogin(username, password, role)
        #print(user.username)
        if (user):
            return redirect(url_for('boundary.home'))
        else:
            flash('Wrong password or username', category='error')

    return render_template("login.html", boolean=True) 

@boundary.route('/logout')
def logout():
    return"<p>Logout</p>"

@boundary.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        surname = request.form.get('surname')
        contact = request.form.get('contact')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            createAccountController = controller.CreateUserAccController()
            password1 = generate_password_hash(password1, method='pbkdf2')
            userAcc = entity.UserAccount(role,username, password1, name, surname, contact, email, date_of_birth, address)
            result = createAccountController.createUserAccount(userAcc)
            if (result):
                flash('Account created!', category='success')
            else:
                flash('Cannot Create Account!', category='error')

    return render_template("sign_up.html")

@boundary.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    return render_template("homepage.html", user_name = username)

@boundary.route('/accountDetail', methods=['GET', 'POST'])
def display_profile():
    username = session.get('username')
    if username:
        display= controller.DisplayController()
        user = display.get_user_info(username)
        if user:
            role,username,name, surname, contact, date_of_birth, email, address = user
            return render_template("accountdetail.html", role=role,username=username,name=name, surname=surname,contact=contact,date_of_birth=date_of_birth, email=email, address=address,user_name = username)
        else:
            flash('User not found', category='error')
            return redirect(url_for('boundary.login'))
    else:
        flash('User not logged in', category='error')
        return redirect(url_for('boundary.login'))
    
@boundary.route('/about-us')
def aboutus():
    username = session.get('username')
    return render_template("AboutUs.html", user_name = username)
