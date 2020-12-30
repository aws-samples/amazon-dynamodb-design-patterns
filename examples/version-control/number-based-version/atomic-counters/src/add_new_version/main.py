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

    # Update the item that contains the latest version and content
    response = table.update_item(
        Key={
            'PK': event['ID'],
            'SK': 'v0'
        },
        # Atomic counter is used to increment the latest version
        UpdateExpression='SET #time = :time, #state = :state, Latest = if_not_exists(Latest, :val0) + :val1',
        ExpressionAttributeNames={
            '#time': 'Time',
            '#state': 'State'
        },
        ExpressionAttributeValues={
            ':time': event['Time'],
            ':state': event['State'], 
            ':val0': 0,
            ':val1': 1
        },
        ReturnValues='UPDATED_NEW'  # return the affected attribute after the update
    )

    # Get the updated version
    latest_version = response['Attributes']['Latest']

    # Add the new item with the latest version
    table.put_item(
        Item={
            'PK': event['ID'],
            'SK': 'v' + str(latest_version),
            'Time': event['Time'],
            'State': event['State']
        }
    )