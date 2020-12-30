import json
import os
import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Key

conf = Config(
    retries = {
        'max_attempts': 1,
        'mode': 'standard'
    }
)

TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, _):
    ddb = boto3.resource('dynamodb', config = conf)
    table = ddb.Table(TABLE_NAME)

    # Retrieve the latest state data
    response = table.query(
        KeyConditionExpression = Key('PK').eq(event['ID']) & Key('SK').begins_with('2'), 
        # Strongly consistent read
        ConsistentRead = True,
        # Sort items in descending order
        ScanIndexForward = False,
        # Specifies the maximum number of items to evaluate 
        Limit = 1      
    )
    items = response['Items']
    print(json.dumps(items, indent=4))