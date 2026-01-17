import json
import boto3
import urllib.parse
from datetime import datetime

# Initialize Clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')

# --- CONFIGURATION ---
TABLE_NAME = '/TABLENAME/' 
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:961341543201:CloudLens-Alerts' 

def lambda_handler(event, context):
    # Get the bucket name and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    print(f"Processing file: {key}")

    if not key.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Skipped: {key} is not an image.")
        return {'statusCode': 200, 'body': "Skipped non-image file"}

    try:
        # 1. Get Metadata from S3
        response = s3.head_object(Bucket=bucket, Key=key)
        file_size = response['ContentLength']
        upload_time = str(datetime.now())
        
        # 2. AI Analysis (Amazon Rekognition)
        detected_labels = "Not an image"
        
        # Check if it is an image file
        if key.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("Analyzing image...")
            rek_response = rekognition.detect_labels(
                Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                MaxLabels=5,
                MinConfidence=80
            )
            # Convert the messy AI data into a simple string (e.g., "Car, Wheel, Tire")
            labels = [label['Name'] for label in rek_response['Labels']]
            detected_labels = ", ".join(labels)
            print(f"AI Results: {detected_labels}")

        # 3. Write to DynamoDB (This is what your Dashboard reads!)
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'filename': key,
            'bucket': bucket,
            'size_bytes': file_size,
            'upload_time': upload_time,
            'ai_labels': detected_labels
        })
        
        # 4. (Optional) Send Email Alert
        if SNS_TOPIC_ARN:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"File: {key}\nAI Labels: {detected_labels}",
                Subject='CloudLens Alert'
            )

        return {'statusCode': 200, 'body': json.dumps('Success')}

    except Exception as e:
        print(f"Error: {e}")
        raise e
