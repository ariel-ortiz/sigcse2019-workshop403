import json
import yaml
from http import HTTPStatus

YAML_FILE_NAME = 'pugnacious_orc.yaml'

def read_yaml_file():
    global ADVENTURE
    with open(YAML_FILE_NAME) as f:
        ADVENTURE = yaml.load(f)
    for key in ADVENTURE:
        ADVENTURE[key]['place'] = key

def make_response(http_status, body):
    return {
        'statusCode': http_status.value,
        'body': json.dumps(body, indent=2),
    }

def make_place_response(query_string_params):
    if 'place' in query_string_params:
        place = query_string_params['place']
        if place in ADVENTURE:
            return make_response(HTTPStatus.OK,ADVENTURE[place])
    return make_response(
        HTTPStatus.NOT_FOUND,
        {'message': "Incorrect or missing 'place' parameter."})

def make_url(host, path, place):
    return (f'https://{ host }/default{ path }/'
            f'?place={ place }')

def make_places_list_response(event):
    path = event.get('path', None)
    headers = event.get('headers', None)
    host = headers.get('Host', None)
    places = [
        {
            'place': place,
            'url': make_url(host, path, place),
        }
        for place in sorted(ADVENTURE.keys())
    ]
    return make_response(HTTPStatus.OK, places)

def handle_get(event):
    query_string_params = event.get('queryStringParameters', None)
    if query_string_params:
        return make_place_response(query_string_params)
    else:
        return make_places_list_response(event)

def handle_bad_method(method):
    return make_response(
        HTTPStatus.METHOD_NOT_ALLOWED,
        {'message': f'Method not supported: { method }'})

def lambda_handler(event, context):
    method = event.get('httpMethod', None)
    if method == 'GET':
        return handle_get(event)
    else:
        return handle_bad_method(method)

read_yaml_file()
