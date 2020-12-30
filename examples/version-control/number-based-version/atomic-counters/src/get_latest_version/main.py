import decimal
import json
import os
import boto3
from botocore.config import Config

conf = Config(
    retries = {
        'max_attempts': 1,
        'mode': 'standard'
    }
)

TABLE_NAME = os.environ['TABLE_NAME']

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def handler(event, _):
    ddb = boto3.resource('dynamodb', config = conf)
    table = ddb.Table(TABLE_NAME)

    # Retrieve the latest state data
    response = table.get_item(
        Key={
            'PK': event['ID'],
            'SK': 'v0'
        }
    )
    item = response['Item']
    print(json.dumps(item, indent=4, cls=DecimalEncoder))
