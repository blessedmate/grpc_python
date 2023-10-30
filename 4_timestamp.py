from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

import rides_pb2 as pb

loc = pb.Location(
    lat=32.5270941,
    long=34.9404309,
)
request = pb.StartRequest(
    car_id=95,
    driver_id='McQueen',
    passenger_ids=['p1', 'p2', 'p3'],
    type=pb.POOL,
    location=loc,
)

time = datetime(2022, 2, 13, 14, 39, 42)
request.time.FromDatetime(time)
print(request)

# toDatetime
time2 = request.time.ToDatetime()
print(type(time2), time2)

# now
now = Timestamp()
now.GetCurrentTime()
print(now)
