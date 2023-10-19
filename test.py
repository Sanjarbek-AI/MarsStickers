import requests


def login(modme_id, parol):
    url = "https://api.marsit.uz/api/v1/auth/signin"
    payload = {"student": {'external_id': modme_id, 'code': parol, 'role': "student"}}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(data.get('access_token'))
        return data.get('access_token')
    return False


def get_products():
    url = "https://api.marsit.uz/api/v1/shop/transaction"
    params = {"company_id": 2}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3aG8iOjEsInN1YiI6IjEzMDQiLCJleHAiOjE2OTY0MjE3MDB9.o4lYZhIbG7WpjTamRThIwZbsCoyA2RQTKCYA7RH7UxM",
        "Host": "api.marsit.uz",
        "Origin": "https://space.marsit.uz",
        "Referer": "https://space.marsit.uz/",
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        print("Request was successful")
        print("Response JSON:", response.json())
    else:
        # Handle errors
        print(f"Request failed with status code {response.status_code}")
        print("Response content:", response.text)


def buy_product():
    url = "https://api.marsit.uz/api/v1/shop/buy/105"

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3aG8iOjEsInN1YiI6IjE3MzgiLCJleHAiOjE2OTY0MjMyMjN9.3njr7dyUxgSgqeMVFZYL2VCHmzgN1W5ev2VKTXelRxU"

    payload = {"product_id": 105}

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("POST request was successful")
        print("Response content:")
        print(response.json())
    else:
        print(f"POST request failed with status code {response.status_code}")
        print("Response content:")
        print(response.text)
