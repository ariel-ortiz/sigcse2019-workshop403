import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('scores')
data = {
    'uuid' : uuid.uuid1().hex,
    'initials': 'JS',
    'score': 99,
    'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
}
table.put_item(Item=data)
print('Item added.')
