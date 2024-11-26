import pytest
from app import app, db
from models import User, File

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully!"

def test_login(client):
    client.post('/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_file_upload(client):
    client.post('/auth/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    login_response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json['token']
    
    response = client.post('/file/upload', headers={
        "Authorization": f"Bearer {token}"
    }, data={
        'file': (open('test.txt', 'rb'), 'test.txt')
    })
    assert response.status_code == 200
    assert response.json['message'] == "File uploaded successfully!"
