mport boto3
import json

dynamodb = boto3.resource('dynamodb')
routes_table = dynamodb.Table('bus_routes')
bookings_table = dynamodb.Table('bus_bookings')

def lambda_handler(event, context):
    route_id = event.get('route_id')
    seat_number = event.get('seat_number')
    passenger_name = event.get('passenger_name')
    booking_id = event.get('booking_id')

    # Step 1: Check if this seat is already booked for this route
    response = bookings_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('route_id').eq(route_id) &
                          boto3.dynamodb.conditions.Attr('seat_number').eq(seat_number)
    )

    if response['Items']:
        # Seat already taken
        return {
            'statusCode': 200,
            'body': json.dumps('This seat is already booked. Please choose another seat.')
        }

    # Step 2: Get the route to check available seats
    route_response = routes_table.get_item(Key={'route_id': route_id})
    if 'Item' not in route_response:
        return {
            'statusCode': 404,
            'body': json.dumps('Route not found.')
        }

    route = route_response['Item']
    available_seats = int(route.get('available_seats', 0))

    if available_seats <= 0:
        return {
            'statusCode': 200,
            'body': json.dumps('No seats available on this route.')
        }

    # Step 3: Save the booking
    bookings_table.put_item(
        Item={
            'booking_id': booking_id,
            'route_id': route_id,
            'seat_number': seat_number,
            'passenger_name': passenger_name
        }
    )

    # Step 4: Reduce available seats by 1
    routes_table.update_item(
        Key={'route_id': route_id},
        UpdateExpression='SET available_seats = available_seats - :val',
        ExpressionAttributeValues={':val': 1}
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Booking confirmed for seat ' + str(seat_number))
    }
