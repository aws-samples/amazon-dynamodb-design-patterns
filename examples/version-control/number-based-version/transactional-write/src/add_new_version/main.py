import os
import boto3
from botocore.config import Config

conf = Config(
    retries={
        'max_attempts': 1, # Find more information about retries here: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html
        'mode': 'standard'
    }
)

ddb = boto3.client('dynamodb', config=conf)
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, _):

    # Retrieve the latest version
    response_latest_version = ddb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {'S': event['ID']},
            'SK': {'S': 'v0'}
        }
    )

    latest_version = 0
    higher_version = 1

    # Extract 'Latest' from response
    if 'Item' in response_latest_version:
        latest_version = response_latest_version['Item']['Latest']['N']
        higher_version = int(latest_version) + 1

    # Transactional write where Update and Put are grouped together
    ddb.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'TableName': TABLE_NAME,
                    'Key': {
                        'PK': {
                            'S': event['ID']
                        },
                        'SK': {
                            'S': 'v0'
                        }
                    },
                    # Conditional write makes the update idempotent here since the conditional check is on the same attribute that is being updated.
                    'ConditionExpression': 'attribute_not_exists(#latest) OR #latest = :latest',
                    'UpdateExpression': 'SET #time = :time, #state = :state, #latest = :higher_version',
                    'ExpressionAttributeNames': {
                        '#latest': 'Latest',
                        '#time': 'Time',
                        '#state': 'State'
                    },
                    'ExpressionAttributeValues': {
                        ':latest': {
                            'N': str(latest_version)
                        },
                        ':higher_version': {
                            'N': str(higher_version)
                        },
                        ':time': {
                            'S': event['Time']
                        },
                        ':state': {
                            'S': event['State']
                        }
                    }
                }
            },
            {
                'Put': {
                    'TableName': TABLE_NAME,
                    'Item': {
                        'PK': {
                            'S': event['ID']
                        },
                        'SK': {
                            'S': 'v' + str(higher_version)
                        },
                        'Time': {
                            'S': event['Time']
                        },
                        'State': {
                            'S': event['State']
                        }
                    }
                }
            }
        ]
    )