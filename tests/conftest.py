import pytest
from csci314_project import MySQL
from csci314_project import create_app
#from . import mysql

#HAVE ERROR
@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = ""
    app.config['MYSQL_DB'] = "csit314_project"
    app.config['MYSQL_HOST'] = "localhost"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    mysql = MySQL()
    mysql.init_app(app)
    # Establish an application context before running the tests
    with app.app_context():
        yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()