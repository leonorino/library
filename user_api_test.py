from requests import get, post
from pprint import pprint


pprint(get('http://127.0.0.1:8080/api/users').json())

print(get('http://127.0.0.1:8080/api/users/999').json())  # invalid user id

print(get('http://127.0.0.1:8080/api/users/3').json())

print(post('http://127.0.0.1:8080/api/users', json={
    'name': 'user',
    'hashed_password': '123',
}).json())

print(post('http://127.0.0.1:8080/api/users', json={
    'name': 123,
    'hashed_password': 'name',
}).json())

print(post('http://127.0.0.1:8080/api/users', json={
    'name': 'TIM',
}).json())


pprint(get('http://127.0.0.1:8080/api/users').json())