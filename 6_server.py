from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import grpc
from grpc_reflection.v1alpha import reflection

import rides_pb2 as pb
import rides_pb2_grpc as rpc
from helpers import validate


def new_ride_id():
    return uuid4().hex


class Rides(rpc.RidesServicer):
    """My implementation of the servicer"""

    def Start(self, request, context):
        print("Incoming request", request)
        try:
            validate.start_request(request)
        except validate.Error as err:
            print('Bad Request')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'{err.field} is {err.reason}')
            raise err

        # TODO: Store ride in DB
        ride_id = new_ride_id()
        return pb.StartResponse(id=ride_id)

    def Track(self, request_iterator, context):
        count = 0
        for request in request_iterator:
            # TODO: Store in DB
            print('track:', request)
            count += 1
            
        return pb.TrackResponse(count=count)


if __name__ == '__main__':
    # Start the server and link the Servicer
    server = grpc.server(ThreadPoolExecutor())
    rpc.add_RidesServicer_to_server(Rides(), server)

    # Configure reflection
    names = (
        pb.DESCRIPTOR.services_by_name['Rides'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(names, server)

    addr = '[::]:8888'
    server.add_insecure_port(addr)
    server.start()

    print('SERVER RUNNING ON PORT 8888')

    server.wait_for_termination()
