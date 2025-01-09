import requests
import pytest
import random
from requests.auth import HTTPBasicAuth
import time

BASE_URL = 'http://localhost:8080'
TODOS_URL = '/todos'
ADDITIONAL_URL = 'http://localhost:4242'
URL_UPDATES = '/ws'


def generate_random_u64():
    return random.randint(0, 2 ** 64 - 1)


@pytest.mark.parametrize("offset, limit", [(5, -66), (-55, 5), (10, 15), ('b', 'j')])
def test_get_todos(offset, limit):
    params = {
        "offset": offset,
        "limit": limit
    }
    try:
        response = requests.get(BASE_URL + TODOS_URL, params=params)
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        todos = response.json()
        return todos
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TODOs: {e}")
        return []


def test_post():
    num = generate_random_u64()
    payload = {"id": num,
               "text": "Exercise at gym",
               "completed": True}

    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL + TODOS_URL, json=payload, headers=headers)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"


def test_put():
    num = generate_random_u64()
    payload = {
        "id": num,
        "text": "Exercise at gym",
        "completed": True
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL + TODOS_URL, json=payload, headers=headers)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"

    payload_after = {
        "id": id,
        "text": "Exercise at university",
        "completed": False
    }

    response = requests.put(BASE_URL + TODOS_URL + f"/{id}", json=payload_after, headers=headers)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"


def test_delete():
    num = generate_random_u64()
    payload = {
        "id": num,
        "text": "Exercise at gym",
        "completed": True
    }
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth("admin", "admin")
    response = requests.post(BASE_URL + TODOS_URL, json=payload, headers=headers, auth=auth)

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"

    response = requests.delete(BASE_URL + TODOS_URL + f"/{id}", json=payload, headers=headers, auth=auth)

    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"


def test_performance():
    headers = {"Content-Type": "application/json"}
    num_requests = 100
    response_times = []
    successful_requests = 0

    for i in range(num_requests):
        num = generate_random_u64()
        payload = {"id": num, "text": f"Task {i}", "completed": False}
        start_time = time.time()
        response = requests.post(BASE_URL + TODOS_URL, json=payload, headers=headers)
        end_time = time.time()
        response_times.append(end_time - start_time)
        if response.status_code == 201:  # Adjust to the expected success code
            successful_requests += 1
        else:
            print(f"Expected 201 but got {response.status_code}")

    total_requests = len(response_times)
    average_time = sum(response_times) / total_requests if total_requests else 0
    max_time = max(response_times) if response_times else 0

    print(f"Total Requests: {num_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Average Response Time: {average_time:.3f} seconds")
    print(f"Maximum Response Time: {max_time:.3f} seconds")
    print(f"Success Rate: {successful_requests / num_requests * 100:.2f}%")


test_performance()
