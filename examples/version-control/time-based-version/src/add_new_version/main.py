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

def handler(event, _):
    ddb = boto3.resource('dynamodb', config = conf)
    table = ddb.Table(TABLE_NAME)

    # Add the new state data item for the equipment
    table.put_item(
        Item = {
            'PK': event['ID'],
            'SK': event['Time'],
            'State': event['State']
        }
    )