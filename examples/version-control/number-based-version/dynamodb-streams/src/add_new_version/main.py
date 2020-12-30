import os
import boto3
from botocore.config import Config

conf = Config(
    retries={
        'max_attempts': 1,
        'mode': 'standard'
    }
)

TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, _):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE_NAME)

    for record in event['Records']:
        if record['dynamodb']['Keys']['SK']['S'] == 'v0':
            new_image = record['dynamodb']['NewImage']
            latest_id = new_image['PK']['S']
            latest_version = new_image['Latest']['N']
            latest_time = new_image['Time']['S']
            latest_state = new_image['State']['S']

            # Add the new item with the latest version
            table.put_item(
                Item={
                    'PK': latest_id,
                    'SK': 'v' + str(latest_version),
                    'Time': latest_time,
                    'State': latest_state
                }
            )