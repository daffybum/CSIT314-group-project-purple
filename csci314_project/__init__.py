from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

# please change the user/password/db as needed
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'HelloWorld'
    app.config['MYSQL_USER'] = "def"
    app.config['MYSQL_PASSWORD'] = "password"
    app.config['MYSQL_DB'] = "csit314_project"

    app.config['UPLOAD_FOLDER'] = 'csit314_project/static/uploads/'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    mysql = MySQL(app)

    #from .views import views
    from .boundary import boundary

    #app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(boundary, url_prefix='/')

    return app

