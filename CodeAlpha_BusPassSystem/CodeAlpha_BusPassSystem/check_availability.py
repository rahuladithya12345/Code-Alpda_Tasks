import boto3
import json

dynamodb = boto3.resource('dynamodb')
routes_table = dynamodb.Table('bus_routes')

def lambda_handler(event, context):
    route_id = event.get('route_id')

    response = routes_table.get_item(Key={'route_id': route_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('Route not found.')
        }

    route = response['Item']
    available_seats = route.get('available_seats', 0)

    return {
        'statusCode': 200,
        'body': json.dumps('Available seats on this route: ' + str(available_seats))
    }
