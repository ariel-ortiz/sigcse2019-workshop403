import requests

# Remember to change the next line.
URL = 'https://some.end.point.amazonaws.com/default/hello-world'

result = requests.get(URL, params={'name': 'Thanos'})
print(result.status_code)
print(result.headers['X-Powered-By'])
body = result.json()
print(body['message'])
print(body['memory'])
