import json


def test_create_job(client):
    data = {
        'title': 'FastAPI Developer',
        'company': 'CMCG',
        'company_url': 'cmcg.com',
        'location': 'District 7, HCMC',
        'description': 'Senior developer with 5 years experience',
        'date_posted': '2022-10-23',
    }

    response = client.post('/jobs/create-job', json.dumps(data))

    assert response.status_code == 200
    assert response.json()['company'] == 'CMCG'
    assert response.json()['description'] == 'Senior developer with 5 years experience'


def test_read_job(client):
    data = {
        'title': 'FastAPI Developer',
        'company': 'CMCG',
        'company_url': 'cmcg.com',
        'location': 'District 7, HCMC',
        'description': 'Senior developer with 5 years experience',
        'date_posted': '2022-10-23',
    }

    client.post('/jobs/create-job', json.dumps(data))
    response = client.get('/jobs/get/1')

    assert response.status_code == 200
    assert response.json()['title'] == 'FastAPI Developer'


def test_read_not_existed_job(client):
    data = {
        'title': 'FastAPI Developer',
        'company': 'CMCG',
        'company_url': 'cmcg.com',
        'location': 'District 7, HCMC',
        'description': 'Senior developer with 5 years experience',
        'date_posted': '2022-10-23',
    }

    client.post('/jobs/create-job', json.dumps(data))
    response = client.get('/jobs/get/2')

    assert response.status_code == 404
