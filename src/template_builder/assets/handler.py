import json


def lambda_handler(event, context):
    print('request:', json.dumps(event))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Success!'
    }
