def test_database_connection(client):
    try:
        with client.application.app_context():
            mysql = client.application.extensions['mysql']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            assert result[0] == 1  # Assuming the query returns 1
    except Exception as e:
        assert False, f"Database connection failed: {str(e)}"


def test_database_connection(client):
    # Attempt to execute a simple SQL query to check the database connection
    try:
        with client.application.app_context():
            mysql = client.application.extensions['mysql']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            assert result[0] == 1  # Assuming the query returns 1
    except Exception as e:
        # If an exception occurs, the database connection is not successful
        assert False, f"Database connection failed: {str(e)}"





def test_login(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200
    assert b"Logout" in response.data

def test_login_with_valid_credentials(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'seller',
        username='seller',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    
    


def test_login_with_unvalid_username(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'seller',
        username='wrongusername',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    
def test_login_with_unvalid_passwordusername(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'seller',
        username='wrongusername',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_login_with_unvalid_password(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'seller',
        username='seller',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_login_with_unvalid_role(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'wrongseller',
        username='seller',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_login_with_unvalid_rolepassword(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'wrongseller',
        username='seller',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_login_with_unvalid_roleusername(client):
    # Simulate logging in with valid credentials
    response = client.post('/', data=dict(
        role = 'wrongseller',
        username='wrongseller',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200


