import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('duplicate_table')

def lambda_handler(event, context):
    # Get the new data being submitted
    user_id = event.get('user_id')
    name = event.get('name')
    email = event.get('email')
    phone = event.get('phone')

    # Step 1: Check if this email already exists in the table
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email)
    )

    if response['Items']:
        # Step 2: Duplicate found - reject it
        return {
            'statusCode': 200,
            'body': json.dumps('Duplicate found. Entry not added.')
        }
    else:
        # Step 3: No duplicate - add the new record
        table.put_item(
            Item={
                'user_id': user_id,
                'name': name,
                'email': email,
                'phone': phone
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Record added successfully.')
        }
