import json
import boto3
import uuid
from http import HTTPStatus
from datetime import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('scores')

def make_response(http_status, body):
    return {
        'statusCode': http_status.value,
        'body': json.dumps(body, indent=2),
    }

def sort_items_by_descending_scores_and_ascending_timestamp(items):
    items.sort(key=lambda item: item['timestamp'])
    items.sort(key=lambda item: item['score'], reverse=True)

def make_result_list(items):
    return [
        {
            'uuid': item['uuid'],
            'initials': item['initials'],
            'score': int(item['score']), # Convert Decimal to int
            'timestamp': item['timestamp'],
        }
        for item in items
    ]

def get_scores():
    items = table.scan()['Items']
    sort_items_by_descending_scores_and_ascending_timestamp(items)
    return make_result_list(items)

def handle_get():
    return make_response(HTTPStatus.OK, get_scores())

def parse_body(str):
    try:
        data = json.loads(str)
        if 'initials' in data and 'score' in data:
            return data
        else:
            return None
    except json.decoder.JSONDecodeError:
        return None

def store_item(event):
    data = parse_body(event.get('body', ''))
    if data:
        id = uuid.uuid1().hex
        data['uuid'] = id
        data['timestamp'] = datetime.now().strftime(TIMESTAMP_FORMAT)
        table.put_item(Item=data)
        return id
    else:
        return None

def handle_post(uuid):
    return make_response(
        HTTPStatus.CREATED,
        {'message': f'New resource created with uuid = { uuid }.'})

def handle_bad_request():
    return make_response(
        HTTPStatus.BAD_REQUEST,
        {'message': 'Bad request (invalid input)'})

def handle_bad_method(method):
    return make_response(
        HTTPStatus.METHOD_NOT_ALLOWED,
        {'message': f'Method not supported: { method }'})

def lambda_handler(event, context):
    method = event.get('httpMethod', None)
    if method == 'GET':
        return handle_get()
    elif method == 'POST':
        id = store_item(event)
        if id:
            return handle_post(id)
        else:
            return handle_bad_request()
    else:
        return handle_bad_method(method)
