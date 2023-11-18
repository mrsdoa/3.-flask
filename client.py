import requests

# response = requests.get('http://127.0.0.1:5000/advertisement/1',)
# print(response.status_code)
# print(response.text)

response = requests.post('http://127.0.0.1:5000/advertisement', json={'title':'advertisement_1', 'description': 'text', 'owner': 'name'}, headers={'Authorization':'some_token'})
print(response.status_code)
print(response.text)

# response = requests.patch('hhttp://127.0.0.1:5000/advertisement/1', json={'title':'advertisement_1', 'description': 'text'},)
# print(response.status_code)
# print(response.text)
#
# response = requests.get('http://127.0.0.1:5000/advertisement/1',)
# print(response.status_code)
# print(response.text)
#
# response = requests.delete('http://127.0.0.1:5000/advertisement/1',)
# print(response.status_code)
# print(response.text)
