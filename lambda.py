import json
import boto3

def lambda_handler(event, context):
    try:
        # Handle CORS preflight request
        if event.get("httpMethod") == "OPTIONS":
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                'body': json.dumps({"message": "CORS preflight successful!"})
            }

        # Ensure request is a POST method
        if event.get("httpMethod") != "POST":
            return {
                'statusCode': 400,
                'headers': {"Access-Control-Allow-Origin": "*"},
                'body': json.dumps({"error": "Invalid request method. Use POST."})
            }

        # Convert form data from JSON
        data = json.loads(event['body'])
        
        # Connect to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('contact-form-table')

        # Store data
        table.put_item(Item={
            'email': data['email'],
            'fname': data['fname'],
            'lname': data['lname'],
            'message': data['message']
        })

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({"message": "Data stored successfully!"})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps({'error': str(e)})
        }  
