import json
import boto3
import base64
from decimal import Decimal

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


BUCKET_NAME = 'cloudlens-serverless-auditor'  
TABLE_NAME = 'CloudLens-Image-Data'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("----- DEBUG START -----")
    print("Event Received:", json.dumps(event)) 
    
    method = ""
    if 'httpMethod' in event:
        method = event['httpMethod']
    elif 'requestContext' in event and 'http' in event['requestContext']:
        method = event['requestContext']['http']['method']
    
    print(f"DETECTED METHOD: {method}")

    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': ''
        }

    if method == 'POST':
        print("Starting Upload Process...")
        try:
            if event.get('isBase64Encoded', False):
                body = json.loads(base64.b64decode(event['body']))
            else:
                body = json.loads(event['body'])
            
            file_content = base64.b64decode(body['fileContent'])
            file_name = body['filename']
            
            s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)
            print("Upload to S3 Complete!")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*', 
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps("Upload Success")
            }
        except Exception as e:
            print(f"UPLOAD ERROR: {str(e)}")
            return {'statusCode': 500, 'body': str(e)}

    elif method == 'GET':
        print("Scanning DynamoDB...")
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan()
        items = response.get('Items', [])
        
        return {
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps(items, cls=DecimalEncoder)
        }
        
    return {'statusCode': 400, 'body': f"Invalid Method: {method}"}
