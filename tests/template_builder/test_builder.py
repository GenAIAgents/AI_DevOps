import json

from src.template_builder.builder import build


def test_builder():
    desc = {
        'summary': '',
        'provider': 'AWS',
        'lang': 'Python',
        'components': [
            {'type': 'S3Bucket', 'args': {'name': 'myBucket', 'versioned': True}},
            {'type': 'S3Bucket', 'args': {'name': 'myAnotherBucket', 'versioned': True}},
            {'type': 'LambdaFunction', 'args': {
                'name': 'myLambdaFunction',
                'runtime': 'PYTHON_3_6',
                'handler': 'handler.py',
                'code_asset': 'lambda_handlers'
            }},
            {'type': 'EC2Instance', 'args': {
                'name': 'myEC2Instance',
                'vpc_name': 'myVPC',
                'instance_type': 'c7g.xlarge'
            }}
        ],
    }
    desc = json.dumps(desc)

    code = build(desc)
    # assert code
