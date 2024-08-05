

# OpenAPI
import json

from health_check.checks.sio_client import SioClient
from health_check.checks.utils.exceptions import UnexpectedContent


def check_open_api(env):
    sio = SioClient(environment=env)
    sio.connect()
    response = sio.process_request('ping')
    sio.disconnect()
    if response['ID'] != 18:
        raise UnexpectedContent(
            env,
            sio.endpointOpenAPI,
            'Unexpected response received'.format(json.dumps(response, indent=2))
        )
    else:
        print 'OK'
