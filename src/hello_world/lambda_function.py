import json
from http import HTTPStatus

def name(event):
    q = event.get('queryStringParameters', None)
    if q:
        name = q.get('name', None)
        if name:
            return name
    return 'World'

def lambda_handler(event, context):
    return {
        'statusCode': HTTPStatus.OK.value,
        'body': json.dumps({
            'message': f'Hello, { name(event) }!',
            'answer': 42,
            'happy': True,
            'name': context.function_name,
            'memory': context.memory_limit_in_mb
        }, indent=2),
        'headers': {
            'X-Powered-By': 'AWS Lambda'
        }
    }
