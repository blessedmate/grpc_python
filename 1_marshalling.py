import rides_pb2 as pb

request = pb.StartRequest(
    car_id=95,
    driver_id='McQueen',
    passenger_ids=['p1', 'p2', 'p3'],
)

print(request)

# Serialization
data = request.SerializeToString()
print('type', type(data))
print('size', len(data))

# Deserialization
request2 = pb.StartRequest()
request2.ParseFromString(data)
print(request2)
