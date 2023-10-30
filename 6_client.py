import grpc
from datetime import datetime
from helpers import events

import rides_pb2_grpc as rpc
import rides_pb2 as pb


class ClientError(Exception):
    pass


class Client:
    def __init__(self, addr):
        self.chan = grpc.insecure_channel(addr)
        self.stub = rpc.RidesStub(self.chan)
        print('Connected to', addr)

    def close(self):
        self.chan.close()

    def ride_start(self, car_id, driver_id, passenger_ids, type, lat, long, time):
        request = pb.StartRequest(
            car_id=car_id,
            driver_id=driver_id,
            passenger_ids=passenger_ids,
            type=pb.POOL if type == 'POOL' else pb.REGULAR,
            location=pb.Location(lat=lat, long=long),
        )
        request.time.FromDatetime(time)
        print('ride started:', request)

        try:
            response = self.stub.Start(request)
        except grpc.RpcError as err:
            print("Error:", err)
            raise ClientError(f'{err.code()}: {err.details()}') from err
        return response.id

    def track(self, events):
        self.stub.Track(track_request(event) for event in events)


def track_request(event):
    request = pb.TrackRequest(
        car_id=event.car_id,
        location=pb.Location(lat=event.lat, long=event.long)
    )
    request.time.FromDatetime(event.time)
    return request


if __name__ == '__main__':
    addr = 'localhost:8888'
    client = Client(addr)
    ride_id = client.ride_start(
        car_id=7,
        driver_id='Bond',
        passenger_ids=['M', 'Q'],
        type='POOL',
        lat=51.4871871,
        long=-0.1266743,
        time=datetime(2021, 9, 30, 20, 15),
    )
    print('Ride ID:', ride_id)

    # Streaming
    events = events.rand_events(7)
    try:
        client.track(events)
    except ClientError as err:
        raise SystemExit(f'error: {err}')
