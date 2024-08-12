from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == 200
    assert response.json()['user_name'] == 'string'
    assert response.json()['first_name'] == 'string'
    assert response.json()['last_name'] == 'string'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1111111111'
    assert response.json()['email'] == 'usuario@gmail.com'

def test_change_password_success(test_user):
    response = client.put('/user/password', json={'password':'string',
                                              'new_password': 'newstring'})
    assert response.status_code == 204

def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/password', json={'password':'nostring',
                                              'new_password': 'newstring'})
    assert response.status_code == 401
    assert response.json() == {'detail':'Error on password change'}

def test_change_phone_success(test_user):
    response = client.put('/user/phone/2222222222')
    assert response.status_code == 204