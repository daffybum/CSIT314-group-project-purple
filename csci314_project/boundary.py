from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from csci314_project import controller
from csci314_project import entity
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

boundary = Blueprint('boundary', __name__)  # Blueprints means it has roots inside a bunch of URLs defined


#This one for create the 100 user , 100 propertylist, 100 review and 100 favourites==========================================================
boundary.route('/generateuser', methods=['GET', 'POST'])
def createuser():

    generateusercontroller = controller.generateuseraccountController()
    generateuser = generateusercontroller.generateUseraccount()
    if generateuser:
        flash('Generated 100 users', category='success')
        return render_template("login.html")
    else:
        flash('failed to generate 100 users', category='fail')

@boundary.route('/generateproperties', methods=['GET', 'POST'])
def createproperties():

    generatepropertycontroller = controller.generatepropertiesController()
    generateproperty = generatepropertycontroller.generateproperties()
    if generateproperty:
        flash('Generated 100 propertyies', category='success')
        return render_template("login.html")
    else:
        flash('failed to generate 100 users', category='fail')

@boundary.route('/generatefavourites', methods=['GET', 'POST'])
def createfavourites():

    generatefav = controller.generatefavouritesController()
    generatefavourites = generatefav.generatefavourites()
    if generatefavourites:
        flash('Generated favourites', category='success')
        return render_template("login.html")
    else:
        flash('failed to generate 100 users', category='fail')

@boundary.route('/generatereview', methods=['GET', 'POST'])
def createreviews():

    generaterev = controller.generatereviewController()
    generatereview = generaterev.generatereview()
    if generatereview:
        flash('Generated reviews', category='success')
        return render_template("login.html")
    else:
        flash('failed to generate reviews', category='fail')
#End ====================================================================================================================================

#Boundary of User Profile ================================================================================================================
@boundary.route('/viewAllrole', methods=['GET', 'POST'])
def viewAllRole():
    user_role = session.get('role')
    username = session.get('username')
    getAllRoleController = controller.getRoleListController()
    role_list = getAllRoleController.get_all_role()
    return render_template('viewAllUserProfiles.html', user_name = username, role_list = role_list, user_role = user_role)

@boundary.route('/viewSearcheduserProfile', methods=['POST','GET'])
def viewSearcheduserProfile():
    user_role = session.get('role')
    username = session.get('username')
    inputroles = request.form.get('inputroles')
    print(inputroles)
    searchRolesController = controller.viewSearcheduserprofileController()
    searchedRoles = searchRolesController.view_searched_userprofile(inputroles)
    print(searchedRoles)
    if searchedRoles is None:
        flash(' No properties in that area!', category='error')
        return render_template('viewAllUserProfiles.html', role_list=searchedRoles, user_name=username, user_role = user_role)
    else:
        return render_template("viewAllUserProfiles.html", role_list=searchedRoles, user_name=username, user_role = user_role)

@boundary.route('/submitNewRole', methods=['GET', 'POST'])
def submitNewRole():
    user_role = session.get('role')
    username = session.get('username')
    if request.method == 'POST':
        role = request.form.get('role')
        description = request.form.get('description')
        print(role)
        print(description)
        submitNewRoleController = controller.SubmitNewRoleController()
        newRole = submitNewRoleController.submit_new_role(role,description)
        if newRole:
            flash('Successfully Insert New Role', category='success')
            return redirect(url_for('boundary.viewAllRole'))
        else:
            flash('Failed Insert New Role', category='error')
            return redirect(url_for('boundary.viewAllRole'))
      

@boundary.route('/updateDescription', methods=['GET', 'POST'])
def update_description():
    user_role = session.get('role')
    username = session.get('username')
    if request.method == 'POST':
        selected_role= request.form.get('selected_role')
        print(selected_role)
        new_description= request.form.get('new_description')
        updatedesciption = controller.updatedescriptionController()
        update = updatedesciption.update_description(selected_role, new_description)
        if update:
            flash('Successfully updated description', category='success')
            return redirect(url_for('boundary.viewAllRole'))
        else:
            flash('Failed updated description', category='error')
            return redirect(url_for('boundary.viewAllRole'))
        
        
@boundary.route('/adminDeleteProfile', methods=['GET','POST'])
def delete_profile():
    user_role = session.get('role')
    username = session.get('username')
    selected_role = request.form.get('deleteselected_role')
    deleteController = controller.deleteUserProfile()
    delete = deleteController.deleteUserProfile(selected_role)
    if delete:
        flash('Successfully deleted role', category='success')
        return redirect(url_for('boundary.viewAllRole'))
    else:
        flash('Failed delete role', category='error')
        return redirect(url_for('boundary.viewAllRole'))
    
        
#End =====================================================================================================================================
        
#User Account=============================================================================================================================

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
    username = session.get('username')
    user_role = session.get('role') 
    if username == 'admin':
        return render_template("admincreateuser.html", user_name = username, user_role= user_role)
    else:
        return render_template("sign_up.html")


@boundary.route('/home', methods=['GET', 'POST'])
def home():
    user_role = session.get('role')
    username = session.get('username')

    return render_template("homepage.html", user_name = username, user_role= user_role)




@boundary.route('/accountDetail', methods=['GET', 'POST'])
def display_account():
    user_role = session.get('role')
    username = session.get('username')
    if username:
        display= controller.DisplayAccountController()
        user = display.get_user_account(username)
        if user:
            role, username, password = user
            return render_template("accountdetail.html", role = role,username=username, user_name = username, user_role = user_role)
        else:
            flash('User not found', category='error')
            return redirect(url_for('boundary.login'))
    else:
        flash('User not logged in', category='error')
        return redirect(url_for('boundary.login'))
    
@boundary.route('/editprofile', methods=['GET', 'POST'])
def editProfile():
    user_role = session.get('role')
    username = session.get('username')
    selected_user = session.get('selected_user')

    # Instantiate the controller
    editProfileController = controller.EditProfileController()

    if request.method == 'POST':
        name = request.form.get('newname')
        surname = request.form.get('newsurname')
        contact = request.form.get('newcontact')
        date_of_birth = request.form.get('newdate_of_birth')
        email = request.form.get('newemail')
        address = request.form.get('newaddress')

        editProfile = editProfileController.edit_profile(selected_user, name, surname, contact, date_of_birth, email, address)
        if editProfile:
            user_details = editProfileController.get_user_info(selected_user)
            role, selected_user, name, surname, contact, date_of_birth, email, address = user_details
            flash('Profile updated successfully', category="success")
            return render_template("edituseraccount.html", role=role, username=selected_user, name=name, surname=surname, contact=contact, date_of_birth=date_of_birth, email=email, address=address, user_name=username, user_role=user_role)
        else:
            flash('Profile update failed', category="error")
            return redirect(url_for('boundary.viewAllUsers'))
    else:
        # Handling the GET request to pre-fill the form with existing details
        user_details = editProfileController.get_user_info(selected_user)
        if user_details:
            role, selected_user, name, surname, contact, date_of_birth, email, address = user_details
            return render_template("edituseraccount.html", role=role, username=selected_user, name=name, surname=surname, contact=contact, date_of_birth=date_of_birth, email=email, address=address, user_name=username, user_role=user_role)
        else:
            flash('User not found', category="error")
            return redirect(url_for('boundary.viewAllUsers'))

#user story admin2 
@boundary.route('/viewAllUsers')
def viewAllUsers():
    user_role = session.get('role')
    username = session.get('username')
    getAllUserController = controller.GetAllUsersController()
    users_list = getAllUserController.get_all_users()
    return render_template('viewAllUsersAccount.html', user_name = username, users_list = users_list, search_exist = False, user_role = user_role)

#userstory admin7
@boundary.route('/viewUserDetails', methods=['POST'])
def viewUserDetails():
    user_role = session.get('role')
    username = session.get('username')
    selected_user = request.form['selectedUsername']
    display= controller.DisplayController()
    user = display.get_user_info(selected_user)
    if user:
        role, selected_user, name, surname, contact,date_of_birth, email, address = user
        return render_template("accountdetail.html", role=role, username=selected_user,name=name, surname=surname,contact=contact, date_of_birth=date_of_birth, email=email, address=address, user_name = username, user_role = user_role)
    
#userstory admin5
@boundary.route('/viewSearchedUserDetails', methods=['POST'])
def viewSearchedUserDetails():
    user_role = session.get('role')
    username = session.get('username')
    inputUsername = request.form.get('inputUsername')
    searchUserController = controller.SearchUserController()
    searchedUsername = searchUserController.search_user(inputUsername)
    if searchedUsername is None:
        flash('Username does not exist!', category='error')
        getAllUserController = controller.GetAllUsersController()
        users_list = getAllUserController.get_all_users()
        return render_template('viewAllUsersAccount.html', user_name = username, users_list = users_list, search_exist = False, user_role = user_role)
    else:
        return render_template('viewAllUsersAccount.html', user_name = username, users = searchedUsername ,search_exist = True, user_role = user_role)
    

@boundary.route('/deleteAccount', methods=['GET', 'POST'])
def delete_account():
    user_role = session.get('role')
    username = session.get('username')
    selected_user = session.get('selected_user')

    userController = controller.DeleteController()
    result = userController.delete_profile(selected_user)
    if result :

        return redirect(url_for('boundary.viewAllUsers'))
    else:

        flash('Failed to delete this account.', category='error')
        return redirect(url_for('boundary.viewAllUsers'))
    

@boundary.route('/adminUpdatePassword', methods=['GET','POST'])
def adminupdate_password():
    user_role = session.get('role')
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
        

#Buyer =================================================================================================================
 

#user story buyer1
@boundary.route('/buy', methods=['GET'])
def buy():
    user_role = session.get('role')
    username = session.get('username')
    property_controller = controller.ViewBuyController()
    property_list = property_controller.viewProperties()
    return render_template("buyPage.html", property_list=property_list, user_name=username, user_role = user_role)

#Calculate the mortgage
@boundary.route('/propertyDetails', methods=['GET','POST'])
def propertyDetails():
    user_role = session.get('role')
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
        return render_template("viewPropertyDetails.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username , user_role = user_role)
    else:
        print("if its else")
        return redirect(url_for('boundary.buy')) 
    

@boundary.route('/viewAllAgents')
def viewAllAgent():
    user_role = session.get('role')
    username = session.get('username')
    displayAgentController = controller.DisplayAgentController()
    agentlist = displayAgentController.display_all_agent()
    print(agentlist)
    return render_template('displayagent.html',agentlist = agentlist, user_name = username, user_role = user_role)



#Search for all property    
@boundary.route('/viewSearchedProperty', methods=['POST','GET'])
def viewSearchedpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    inputproperty = request.form.get('inputProperty')
    searchPropertyController = controller.viewSearchedpropertyController()
    searchedProperty = searchPropertyController.view_searched_propertyList(inputproperty)
    if searchedProperty is None:
        flash(' No properties in that area!', category='error')
        return render_template('buyPage.html', property_list=searchedProperty, user_name=username, user_role = user_role)
    else:
        return render_template("buyPage.html", property_list=searchedProperty, user_name=username, user_role = user_role)

#Search the new property    
@boundary.route('/viewSearchedNewProperty', methods=['POST','GET'])
def viewSearchednewpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    inputproperty = request.form.get('inputProperty')
    searchPropertyController = controller.viewSearchednewpropertyController()
    searchedProperty = searchPropertyController.view_searched_newpropertyList(inputproperty)
    if searchedProperty is None:
        flash(' No properties in that area!', category='error')
        return render_template('buyPage.html', property_list=searchedProperty, user_name=username, user_role = user_role)
    else:
        return render_template("buyPage.html", property_list=searchedProperty, user_name=username, user_role = user_role)
  
#Search the Old property    
@boundary.route('/viewSearchedOldProperty', methods=['POST','GET'])
def viewSearchedoldpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    inputproperty = request.form.get('inputProperty')
    searchPropertyController = controller.viewSearchedoldpropertyController()
    searchedProperty = searchPropertyController.view_searched_oldpropertyList(inputproperty)
    if searchedProperty is None:
        flash(' No properties in that area!', category='error')
        return render_template('buyPage.html', property_list=searchedProperty, user_name=username, user_role = user_role)
    else:
        return render_template("buyPage.html", property_list=searchedProperty, user_name=username, user_role = user_role)
    

#user story 
@boundary.route('/viewSellingProperty', methods=['POST'])
def viewSellingpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    sellPropertyController = controller.viewSellingpropertyController()
    sellingProperty = sellPropertyController.view_selling_propertyList()
    if sellingProperty is None:
        flash(' No selling properties at the moment!', category='error')
        return render_template('buyPage.html', property_list=sellingProperty, user_name=username, user_role = user_role)
    else:
        return render_template("buyPage.html", property_list=sellingProperty, user_name=username, user_role = user_role)

@boundary.route('/viewSoldProperty', methods=['POST'])
def viewSoldpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    soldPropertyController = controller.viewSoldpropertyController()
    soldProperty = soldPropertyController.view_sold_propertyList()
    if soldProperty is None:
        flash(' No sold properties at the moment!', category='error')
        return render_template('buyPage.html', property_list=soldProperty, user_name=username, user_role = user_role)
    else:
        return render_template("buyPage.html", property_list=soldProperty, user_name=username, user_role = user_role)
    

                        

 #Seller And Real Estate Agent ============================================================================================================================
        
@boundary.route('/sell', methods=['GET'])
def sell():
    user_role = session.get('role')
    username = session.get('username')
    property_controller = controller.viewPersonalpropertyController()
    property_list = property_controller.view_personal_property(username)
    return render_template("sellPage.html", property_list=property_list, user_name=username, user_role = user_role)


@boundary.route('/submitPropertyListing', methods=['GET','POST'])
def submitPropertyListing():
    user_role = session.get('role')
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
    return render_template('uploadProperty.html', user_name = username , user_role = user_role)


@boundary.route('/deleteProperty', methods=['POST'])
def delete_property():
    user_role = session.get('role')
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
    user_role = session.get('role')
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
    return render_template("updateProperty.html",user_name= username, user_role = user_role)

#Ignore this first , this one is doing about the the sum of the detail
@boundary.route('/sellPropertyDetails', methods=['GET','POST'])
def sellpropertyDetails():
    user_role = session.get('role')
    username = session.get('username')
    property_id = request.form.get('property_id')
    print(property_id)
    displayPropertyDetails = controller.displayPropertyDetailController()
    propertydetails = displayPropertyDetails.displayPropertyDetails2(property_id)
    print(propertydetails)
    if propertydetails:
        property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= propertydetails
        return render_template("updateProperty.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username, user_role = user_role)
    else:
        return redirect(url_for('boundary.sell'))

@boundary.route('/sellPropertyDetails2', methods=['GET','POST'])
def sellpropertyDetails2():
    user_role = session.get('role')
    username = session.get('username')
    property_id = request.form.get('property_id')
    print(property_id)
    displayPropertyDetails = controller.displayPropertyDetailController()
    propertydetails = displayPropertyDetails.displayPropertyDetails2(property_id)
    print(propertydetails)
    if propertydetails:
        property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= propertydetails
        return render_template("SellerPropertyDetails.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username, user_role = user_role)
    else:
        return redirect(url_for('boundary.sell'))
    

# Ignore This first , Still got error
@boundary.route('/displaySumDetail2', methods=['GET', 'POST'])
def display_sum_detail():
    username = session.get('username')
    property_id = session.get('property_id')
    user_role = session.get('role')
    displayController = controller.displaySumDetailController()
    displayresult2 = displayController.displaySumDetail(property_id)
    if displayresult2:
         displayresult = displayController.displayPropertyDetails2(property_id)
         property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= displayresult
         total_properties_num= displayresult2
         flash('display the sum successfully', category='success')
         return render_template("SellerPropertyDetails.html",user_name= username, property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, total_properties_num= total_properties_num, user_role = user_role)
    else:
        flash('Failed display the sum , please try again', category='error')
    return render_template("SellerPropertyDetails.html",user_name= username, user_role = user_role)

#Review =================================================================================================================================
@boundary.route('/displayAgentDetail', methods=['GET', 'POST'])
def displayagentdetail():
    user_role = session.get('role')
    username = session.get('username')
    agentname = request.form.get('agentname')
    print(agentname)
    agentDetailController = controller.DisplayAgentDetailController()
    agentDetail = agentDetailController.displayAgentDetail(agentname)
    if agentDetail:
        role,agentname,contact = agentDetail
        return render_template("review.html", user_name = username,agent_name= agentname,agent_role=role,agent_contact=contact, user_role = user_role)
    else:
        return render_template("review.html", user_name = username,agent_name= agentname,agent_role=role,agent_contact=contact, user_role = user_role)
    
    
@boundary.route('/giveReview', methods=['GET', 'POST'])
def givereview():
    user_role = session.get('role')
    postedby = session.get('username')
    agentname = session.get('agentname')
    if request.method == 'POST':
        review = request.form.get('review_text')
        rating = request.form.get('rating')
    give_review_controller = controller.GiveReviewController()
    reviews = give_review_controller.give_review(agentname, review, rating, postedby)
    if reviews:
        agentname, role, contact = reviews
        flash('Review and rating submitted successfully!', category='success')
        return render_template("review.html", user_name=postedby, agent_name=agentname, agent_role=role, agent_contact=contact, user_role=user_role)
    else:
        # Handle the case when reviews is None
        flash('You have already reviewed this agent!', category='error')
        # Assuming role and contact are not relevant if reviews is None
        return redirect(url_for('boundary.viewAllAgent'))

@boundary.route('/viewReviewRating', methods=['GET','POST'])
def viewReviewRating():
    user_role = session.get('role')
    username = session.get('username')
    agentname = request.form.get('agentname')
    display_review_controller = controller.DisplayReviewController()
    review_list = display_review_controller.displayReview(agentname)
    if review_list:
        return render_template("viewreview.html", user_name = username,review_list=review_list, user_role = user_role)
    else:
        return render_template("viewreview.html", user_name = username, user_role = user_role)
            
@boundary.route('/viewMyOwnReviewRating', methods=['GET'])
def viewMyOwnReviewRating():
    user_role = session.get('role')
    agentname = session.get('username')
    display_review_controller = controller.DisplayOwnReviewController()
    review_list = display_review_controller.displayReview(agentname)
    if review_list:
        return render_template("viewmyownreview.html",  review_list=review_list, user_name=agentname, user_role = user_role)
    else:
        return render_template("viewmyownreview.html", review_list=review_list, user_name=agentname, user_role = user_role)

#===================================================================================================================================
    
    
#Favourites    
@boundary.route('/saveFavourite', methods=['GET','POST'])
def saveFavourite():
    user_role = session.get('role')
    property_id = session.get('property_id')
    buyer_name = session.get('username')
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        print(property_id)
    saveFavourite = controller.saveFavouriteController()
    favourite = saveFavourite.save_favourites(buyer_name,property_id)
    if favourite:
        flash('property favourited',category = 'success')
        return render_template("buyPage.html", property_list = favourite, user_name=buyer_name, user_role = user_role)
    else:
        print("FAIL")
        flash('property already favourited!', category="error")
        return redirect(url_for('boundary.buy'))
    
@boundary.route('/displayFavourite', methods=['GET','POST'])
def displayFavourite():
    user_role = session.get('role')
    role = session.get('role')
    buyer_name = session.get('username')
    displayFavouriteController = controller.ViewFavouriteController()
    favourite = displayFavouriteController.view_favourites(buyer_name)
    print(favourite)
    return render_template("viewfavourites.html", favourites=favourite, user_name=buyer_name, role = role, user_role = user_role)



#Still working on it
@boundary.route('/displaySumFavourites', methods=['GET', 'POST'])
def display_sum_favourites():
    username = session.get('username')
    property_id = session.get('property_id')
    user_role = session.get('role')
    displayController = controller.displaySumFavouritesController()
    displayresult = displayController.display_sum_favourites(property_id)
    print(displayresult)
    if displayresult:
         result = displayController.displayPropertyDetails2(property_id)
         property_id, property_name, property_type, property_location, property_price, property_bedroom, property_bathroom, property_size, property_postedBy ,property_status= result
         total_properties = displayresult 
         flash('display the sum successfully', category='success')
         return render_template("SellerPropertyDetails.html", property_id=property_id, property_name=property_name, property_type=property_type, property_location=property_location, property_price=property_price, property_bedroom=property_bedroom, property_bathroom=property_bathroom, property_size=property_size, property_postedBy=property_postedBy, property_status=property_status, user_name=username, total_properties= total_properties, user_role = user_role)
    else:
        flash('Failed display the sum , please try again', category='error')
    return render_template("SellerPropertyDetails.html",user_name= username, user_role = user_role)