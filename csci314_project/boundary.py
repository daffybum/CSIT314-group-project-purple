from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from csci314_project import controller
from csci314_project import entity
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

boundary = Blueprint('boundary', __name__)  # Blueprints means it has roots inside a bunch of URLs defined

#User story seller7 Admin11 rea6 Buyer10 
@boundary.route('/', methods=['GET', 'POST'])
def login():                                     
    if request.method == 'POST':
        role =  request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        loginController = controller.LoginController()
        user = loginController.userLogin(username, password, role)

        if (user):
            return redirect(url_for('boundary.home'))
        else:
            flash('Wrong password or username', category='error')

    return render_template("login.html", boolean=True)

#user story seller2 admin12 rea7 buyer11
@boundary.route('/logout')
def logout():
    return"<p>Logout</p>"

#user story admin1
@boundary.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        name = request.form.get('name')
        surname = request.form.get('surname')
        contact = request.form.get('contact')
        date_of_birth = request.form.get('date_of_birth')
        email = request.form.get('email')
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
            userAcc = entity.UserAccount(role,username, password1, name, surname, contact, date_of_birth, email, address)
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


@boundary.route('/profileDetail', methods=['GET', 'POST'])
def display_profile():
    
    username = session.get('username')
    if username:
        display= controller.DisplayController()
        user = display.get_user_info(username)
        if user:
            role, username, name, surname, contact, date_of_birth, email, address = user
            return render_template("profiledetail.html", role = role,username=username, name=name, surname=surname,contact=contact,date_of_birth=date_of_birth, email=email, address=address,user_name = username)
        else:
            flash('User not found', category='error')
            return redirect(url_for('boundary.login'))
    else:
        flash('User not logged in', category='error')
        return redirect(url_for('boundary.login'))

@boundary.route('/accountDetail', methods=['GET', 'POST'])
def display_account():
    
    username = session.get('username')
    if username:
        display= controller.DisplayAccountController()
        user = display.get_user_account(username)
        if user:
            role, username, password = user
            return render_template("accountdetail.html", role = role,username=username, user_name = username)
        else:
            flash('User not found', category='error')
            return redirect(url_for('boundary.login'))
    else:
        flash('User not logged in', category='error')
        return redirect(url_for('boundary.login'))
    
@boundary.route('/showPassword', methods=['GET', 'POST'])
def display_password():
    
    username = session.get('username')
    enteredPassword = request.form.get('password')
    if username:
        display= controller.DisplayPasswordController()
        user = display.get_user_password(username)
        if user:
            role, username, password = user
            if check_password_hash(password, enteredPassword):
                return render_template("accountPassword.html", role = role,username=username, password=enteredPassword, user_name = username)
            else:
                flash('Wrong password please try again', category='error')
                return render_template("accountdetail.html", role = role,username=username, user_name = username)


@boundary.route('/editprofile', methods=['GET', 'POST'])
def editProfile():
    username = session.get('username')
    role = session.get('role')
    selected_user = session.get('selected_user')
    display= controller.DisplayController()

    user = display.get_user_info(selected_user)
    role, selected_user, name, surname, contact, date_of_birth, email, address = user
    if request.method == 'POST':
        name = request.form.get('newname')
        surname = request.form.get('newsurname')
        contact = request.form.get('newcontact')
        date_of_birth = request.form.get('newdate_of_birth')
        email = request.form.get('newemail')
        address = request.form.get('newaddress')
        editProfileController = controller.EditProfileController()
        editProfile = editProfileController.edit_profile(selected_user, name, surname, contact, date_of_birth, email, address)
        if editProfile:
            flash('Profile updated successfully')
            user = display.get_user_info(selected_user)
            role, selected_user, name, surname, contact, email, date_of_birth, address = user
    return render_template("editprofile.html", role=role, username=selected_user, name=name, surname=surname, contact=contact, date_of_birth=date_of_birth, email=email, address=address, user_name=username)

#user story admin2 
@boundary.route('/viewAllUsers')
def viewAllUsers():
    username = session.get('username')
    getAllUserController = controller.GetAllUsersController()
    users_list = getAllUserController.get_all_users()
    return render_template('viewAllUsersAccount.html', user_name = username, users_list = users_list, search_exist = False)

#userstory admin7
@boundary.route('/viewUserDetails', methods=['POST'])
def viewUserDetails():
    username = session.get('username')
    selected_user = request.form['selectedUsername']
    display= controller.DisplayController()
    user = display.get_user_info(selected_user)
    if user:
        role, selected_user, name, surname, contact,date_of_birth, email, address = user
        return render_template("accountdetail.html", role=role, username=selected_user,name=name, surname=surname,contact=contact, date_of_birth=date_of_birth, email=email, address=address, user_name = username)
    
#userstory admin5
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

    
@boundary.route('/about-us')
def aboutus():
    username = session.get('username')
    return render_template("AboutUs.html", user_name = username)

#user story buyer1
@boundary.route('/buy', methods=['GET'])
def buy():
    username = session.get('username')
    property_controller = controller.ViewBuyController()
    property_list = property_controller.viewProperties()
    return render_template("buyPage.html", property_list=property_list, user_name=username)

@boundary.route('/submitPropertyListing', methods=['GET','POST'])
def submitPropertyListing():
    property_postedBy = session.get('username')
    username = session.get('username')
    if request.method == 'POST':
        property_name = request.form.get('property_name')
        property_type = request.form.get('property_type')
        property_location = request.form.get('property_location')
        property_price = request.form.get('property_price')  
        property_bedroom = request.form.get('property_bedroom')
        property_bathroom = request.form.get('property_bathroom')
        property_size = request.form.get('property_size')
        submitPropertyListingController = controller.SubmitPropertyListingController()
        submit_property_list = submitPropertyListingController.submit_property_listing(property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size,property_postedBy)

        if submit_property_list:
            flash('property list Uploaded',category = 'success')
            return redirect(url_for('boundary.submitPropertyListing'))
        else :
            flash('property list fail to upload',category = 'error')
    return render_template('uploadProperty.html', user_name = username)

@boundary.route('/propertyDetails', methods=['GET','POST'])
def propertyDetails():
    username = session.get('username')
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        print(property_id)
    displayPropertyDetails = controller.displayPropertyDetailController()
    propertydetails = displayPropertyDetails.displayPropertyDetails(property_id)
    print(propertydetails)
    if propertydetails:
        print("success")
        property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= propertydetails
        return render_template("viewPropertyDetails.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username)
    else:
        print("if its else")
        return redirect(url_for('boundary.buy')) 

@boundary.route('/saveFavourite', methods=['GET','POST'])
def saveFavourite():
    property_id = session.get('property_id')
    buyer_name = session.get('username')
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        print(property_id)
    saveFavourite = controller.saveFavouriteController()
    favourite = saveFavourite.save_favourites(buyer_name,property_id)
    if favourite:
         flash('Property save successfully',category="success")
         property_controller = controller.ViewBuyController()
         property_list = property_controller.viewProperties()
         return render_template("buyPage.html", property_list=property_list, user_name=buyer_name)
    else:
        print("FAIL")
        flash('property already favourited!', category="error")
        return redirect(url_for('boundary.buy'))
    
@boundary.route('/displayFavourite', methods=['GET','POST'])
def displayFavourite():
    buyer_name = session.get('username')
    displayFavouriteController = controller.ViewFavouriteController()
    favourite = displayFavouriteController.view_favourites(buyer_name)
    print(favourite)
    return render_template("viewfavourites.html", favourites=favourite, user_name=buyer_name)
    
@boundary.route('/viewSearchedProperty', methods=['POST'])
def viewSearchedpropertyDetails():
    username = session.get('username')
    inputproperty = request.form.get('inputProperty')
    searchPropertyController = controller.viewSearchedpropertyController()
    searchedProperty = searchPropertyController.view_searched_propertyList(inputproperty)
    if searchedProperty is None:
        flash(' No properties in that area!', category='error')
        return render_template('buyPage.html', property_list=searchedProperty, user_name=username)
    else:
        return render_template("buyPage.html", property_list=searchedProperty, user_name=username)
#user story 
@boundary.route('/viewSellingProperty', methods=['POST'])
def viewSellingpropertyDetails():
    username = session.get('username')
    sellPropertyController = controller.viewSellingpropertyController()
    sellingProperty = sellPropertyController.view_selling_propertyList()
    if sellingProperty is None:
        flash(' No selling properties at the moment!', category='error')
        return render_template('buyPage.html', property_list=sellingProperty, user_name=username)
    else:
        return render_template("buyPage.html", property_list=sellingProperty, user_name=username)

@boundary.route('/viewSoldProperty', methods=['POST'])
def viewSoldpropertyDetails():
    username = session.get('username')
    soldPropertyController = controller.viewSoldpropertyController()
    soldProperty = soldPropertyController.view_sold_propertyList()
    if soldProperty is None:
        flash(' No sold properties at the moment!', category='error')
        return render_template('buyPage.html', property_list=soldProperty, user_name=username)
    else:
        return render_template("buyPage.html", property_list=soldProperty, user_name=username)
    
@boundary.route('/viewAllAgents')
def viewAllAgent():
    username = session.get('username')
    displayAgentController = controller.DisplayAgentController()
    agentlist = displayAgentController.display_all_agent()
    print(agentlist)
    return render_template('displayagent.html',agentlist = agentlist, user_name = username)

@boundary.route('/sell', methods=['GET'])
def sell():
    username = session.get('username')
    property_controller = controller.viewPersonalpropertyController()
    property_list = property_controller.view_personal_property(username)
    return render_template("sellPage.html", property_list=property_list, user_name=username)

@boundary.route('/giveReview', methods=['GET', 'POST'])
def givereview():

    postedby = session.get('username')
    agentname = session.get('agentname')
    agentDetailController = controller.DisplayAgentDetailController()
    agentDetail = agentDetailController.displayAgentDetail(agentname)
    if agentDetail:
        role,agentname,contact = agentDetail
        if request.method == 'POST':
            review = request.form.get('review_text')
            rating = request.form.get('rating')
        give_review_controller = controller.GiveReviewController()
        reviews = give_review_controller.give_review(agentname,review,rating,postedby)
        if reviews:
            flash(' review and rating submit successfullly!', category='success')
            return render_template("review.html", user_name = postedby,agent_name= agentname,agent_role=role,agent_contact=contact)
        else:
            flash(' you have already reviewed this agent!', category='error')
            return render_template("review.html", user_name = postedby,agent_name= agentname,agent_role=role,agent_contact=contact)


@boundary.route('/displayAgentDetail', methods=['GET', 'POST'])
def displayagentdetail():
    username = session.get('username')
    agentname = request.form.get('agentname')
    print(agentname)
    agentDetailController = controller.DisplayAgentDetailController()
    agentDetail = agentDetailController.displayAgentDetail(agentname)
    if agentDetail:
        role,agentname,contact = agentDetail
        return render_template("review.html", user_name = username,agent_name= agentname,agent_role=role,agent_contact=contact)
    else:
        return render_template("review.html", user_name = username,agent_name= agentname,agent_role=role,agent_contact=contact)
    
@boundary.route('/viewReviewRating', methods=['GET','POST'])
def viewReviewRating():
    username = session.get('username')
    agentname = request.form.get('agentname')
    display_review_controller = controller.DisplayReviewController()
    review_list = display_review_controller.displayReview(agentname)
    if review_list:
        return render_template("viewreview.html", user_name = username,review_list=review_list)
    else:
        return render_template("viewreview.html", user_name = username)
            
@boundary.route('/viewMyOwnReviewRating', methods=['GET'])
def viewMyOwnReviewRating():
    agentname = session.get('username')
    display_review_controller = controller.DisplayReviewController()
    review_list = display_review_controller.displayReview(agentname)
    if review_list:
        return render_template("viewmyownreview.html",  review_list=review_list, user_name=agentname)
    else:
        return render_template("viewmyownreview.html", review_list=review_list, user_name=agentname)
    
@boundary.route('/deleteAccount', methods=['GET', 'POST'])
def delete_account():
        username = session.get('username')
        selected_user = session.get('selected_user')
        if username == "admin":
            userController = controller.DeleteController()
            result = userController.delete_profile(selected_user)
            if result :
                # Account deleted successfully
                # You might want to clear the session and provide a confirmation message
                return redirect(url_for('boundary.login'))
            else:
                # Account deletion failed (username not found, database error, etc.)
                flash('Failed to delete this account.', category='error')
                return redirect(url_for('boundary.viewAllUsers'))
        else:
            userController = controller.DeleteController()
            print(username)
            result = userController.delete_profile(username)
            if result :
                # Account deleted successfully
                # You might want to clear the session and provide a confirmation message
                return redirect(url_for('boundary.login'))
            else:
                # Account deletion failed (username not found, database error, etc.)
                flash('Failed to delete your account. Please try again later.', category='error')
        return redirect(url_for('boundary.home'))

    
@boundary.route('/updatePassword', methods=['GET', 'POST'])
def update_password():
    username = session.get('username')
    new_password = request.form.get('new_password')
    print(new_password)
    updatePassword = controller.updatePasswordController()
    result = updatePassword.update_password(username, new_password)
    if result:
        flash('Updated password, please login again.', category='success')
        return redirect(url_for('boundary.login'))
    else:
        flash('Failed update your password, please try again', category='error')
        return redirect(url_for('boundary.home'))
        
@boundary.route('/adminUpdatePassword', methods=['GET','POST'])
def adminupdate_password():
    username = session.get('username')
    selected_username = request.form.get('selectedusername')
    new_password = request.form.get('new_password')
    updatePassword = controller.adminupdatePasswordController()
    result = updatePassword.admin_update_password(selected_username, new_password)
    print(username)
    print(selected_username)
    print(new_password)
    print(result)
    if result:
        flash('Updated user password', category='success')
        return redirect(url_for('boundary.viewAllUsers'))
    else:
        flash('Failed update your password, please try again', category='error')
        return redirect(url_for('boundary.viewAllUsers'))
                        

        
@boundary.route('/deleteProperty', methods=['POST'])
def delete_property():
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        print(property_id)
    propertyController = controller.deletePropertyListingController()
    result = propertyController.deleteProperty(property_id)
    print(result)
    if result :
        flash('delete property successfully',category='success')
        return redirect(url_for('boundary.sell') )
    else:
        flash('Failed to delete property', category='error')
    return redirect(url_for('boundary.sell'))

@boundary.route('/updateProperty', methods=['POST','GET'])
def update_property():
    username = session.get('username')
    property_id = session.get('property_id')
    print(property_id)
    if request.method == 'POST':
        property_name = request.form.get('property_name')
        property_type = request.form.get('property_type')
        property_location = request.form.get('property_location')
        property_price = request.form.get('property_price')  
        property_bedroom = request.form.get('property_bedroom')
        property_bathroom = request.form.get('property_bathroom')
        property_size = request.form.get('property_size')
        property_status = request.form.get('property_status')
        propertyController = controller.updatePropertyListingController()
        result = propertyController.updateProperty(property_name,property_type,property_location,property_price,property_bedroom,property_bathroom,property_size,property_status,property_id)
        if result:
            flash('Property updatede successfully',category='success')
            return redirect(url_for('boundary.sell') )
        else:
            flash('Property updatede unsuccessfully',category='error')
            return redirect(url_for('boundary.sell') )
    return render_template("updateProperty.html",user_name= username)

@boundary.route('/sellPropertyDetails', methods=['GET','POST'])
def sellpropertyDetails():
    username = session.get('username')
    property_id = request.form.get('property_id')
    print(property_id)
    displayPropertyDetails = controller.displayPropertyDetailController()
    propertydetails = displayPropertyDetails.displayPropertyDetails(property_id)
    print(propertydetails)
    if propertydetails:
        property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= propertydetails
        return render_template("updateProperty.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username)
    else:
        return redirect(url_for('boundary.sell'))

@boundary.route('/sellPropertyDetails2', methods=['GET','POST'])
def sellpropertyDetails2():
    username = session.get('username')
    property_id = request.form.get('property_id')
    print(property_id)
    displayPropertyDetails = controller.displayPropertyDetailController()
    propertydetails = displayPropertyDetails.displayPropertyDetails(property_id)
    print(propertydetails)
    if propertydetails:
        property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= propertydetails
        return render_template("SellerPropertyDetails.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username)
    else:
        return redirect(url_for('boundary.sell'))
    
@boundary.route('/displaySumFavourites', methods=['GET', 'POST'])
def display_sum_favourites():
    username = session.get('username')
    property_id = session.get('property_id')
    
    calculateController= controller.calculateSumFavouritesController()
    result = calculateController.calculate_sum_favourites(property_id)
    
    if result:
        print("HI")
        displayController = controller.displaySumFavouritesController()
        displayresult = displayController.display_sum_favourites(property_id)
        print(displayresult)
        if displayresult:
             
            flash('display the sum successfully', category='success')
            return redirect(url_for('boundary.login'))
        else:
            flash('Failed display the sum , please try again', category='error')
    return render_template("SellerPropertyDetails.html",user_name= username)