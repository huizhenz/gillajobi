import requests

def get_certification_data():
    params = {
        'serviceKey': 'i7C/aq24edYlsN/Zw4CIflOYRYwGhO9HCiNCAXfuNfc7r0grSQHUDHH7ZtAFYfk1oxI0ouqYvqV1I82cHcfqYA==',
        'page': 1,
        'perPage': 100,
    }
    response = requests.get("https://api.odcloud.kr/api/15082998/v1/uddi:24329307-c706-489a-a9a3-a7c43c3508e5", params=params)
    print(response.json())
    return response.json()

get_certification_data()