import json

from fastapi import status


def test_create_job(client, normal_user_token_headers):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    response = client.post(
        "/jobs/create-job", data=json.dumps(data), headers=normal_user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["company"] == "CMCG"
    assert response.json()["description"] == "Senior developer with 5 years experience"


def test_read_job(client):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    client.post("/jobs/create-job", data=json.dumps(data))
    response = client.get("/jobs/get/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "FastAPI Developer"


def test_read_not_existed_job(client):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    client.post("/jobs/create-job", data=json.dumps(data))
    response = client.get("/jobs/get/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_all_jobs(client, normal_user_token_headers):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    client.post(
        "/jobs/create-job", data=json.dumps(data), headers=normal_user_token_headers
    )
    client.post(
        "/jobs/create-job", data=json.dumps(data), headers=normal_user_token_headers
    )
    response = client.get("/jobs/all")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]
    assert response.json()[1]


def test_update_job(client, normal_user_token_headers):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    client.post(
        "/jobs/create-job", data=json.dumps(data), headers=normal_user_token_headers
    )
    data["title"] = "FastAPI Developer - Test"
    response = client.put(
        "/jobs/update/1", data=json.dumps(data), headers=normal_user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] == "Successfully updated."


def test_delete_job(client, normal_user_token_headers):
    data = {
        "title": "FastAPI Developer",
        "company": "CMCG",
        "company_url": "cmcg.com",
        "location": "District 7, HCMC",
        "description": "Senior developer with 5 years experience",
        "date_posted": "2022-10-23",
    }

    client.post(
        "/jobs/create-job", data=json.dumps(data), headers=normal_user_token_headers
    )
    response = client.delete("/jobs/delete/1", headers=normal_user_token_headers)
    deleted_job = client.get("/jobs/get/1/")

    assert deleted_job.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["msg"] == "Successfully deleted."
