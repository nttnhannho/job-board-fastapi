import json


def test_create_user(client):
    data = {
        'username': 'test_user',
        'email': 'test_email@test.com',
        'password': 'test_password',
    }
    response = client.post('/users/', json.dumps(data))

    assert response.status_code == 200
    assert response.json()['email'] == 'test_email@test.com'
    assert response.json()['is_active'] == True
