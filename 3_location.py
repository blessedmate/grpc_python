import rides_pb2 as pb

loc = pb.Location(
    lat=32.5270941,
    long=34.9404309,
)
print(loc)

request = pb.StartRequest(
    car_id=95,
    driver_id='McQueen',
    passenger_ids=['p1', 'p2', 'p3'],
    type=pb.POOL,
    location=loc,
)

print(request)
print('lat:', request.location.lat)
