version = '0.3'

import json
import os
import requests
from socketIO_client import SocketIO, LoggingNamespace, ConnectionError, TimeoutError, PacketError, TRANSPORTS
from requests.exceptions import ReadTimeout
from time import time, sleep
import logging
requests.packages.urllib3.disable_warnings()
logging.getLogger('requests').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

class MyNamespace(LoggingNamespace):
    def __init__(self, _transport, path):
        super(MyNamespace, self).__init__(_transport, path)
        self.data = []

    def get_response(self):
        if len(self.data) != 0:
            return self.data.pop()
        else:
            return None

    def on_connect(self):
        pass

    def on_message(self, data):
        jsondata = json.loads(data)
        self.data.append(json.loads(data))
        # Sio_client.on_msg(jsondata)

class SioClient:
    def __init__(self, environment='tst2', host=None):
        self.data = {}
        self.message = ''
        self.environment = environment
        self.wtime = 0.05
        self.socketIO = None
        self.namespace = None
        self.headers={}
        with open(os.path.join(os.path.split(__file__)[0],'resources/{0}/requests.json'.format(self.environment))) as data_file,\
        open(os.path.join(os.path.split(__file__)[0], 'resources/{0}/headers.json'.format(environment))) as headers_file:
            self.requests_dict = json.load(data_file)
            self.headers_dict = json.load(headers_file)
        if host is None:
            with open(os.path.join(os.path.split(__file__)[0],'resources/{0}/endpoints.json'.format(self.environment))) as endpoints_file:
                self.endpointOpenAPI = json.load(endpoints_file)['OpenApi'][0]['url']
        else:
            self.endpointOpenAPI = 'https://{0}'.format(host)
        print ''

    def connect(self):
        time_param = int(round(time() * 1000))
        # print time_param

        for header in self.headers_dict['SIOconnect']:
            self.headers[header['name']] = header['value']
            self.headers['queryString'] = str(time_param)

        self.socketIO = SocketIO(
            self.endpointOpenAPI,
            Namespace=MyNamespace,
            headers=self.headers,
            verify=False,
            params={'t': str(time_param)}
        )
        self.namespace = self.socketIO.get_namespace()


    def disconnect(self):
        self.socketIO.disconnect()

    def send(self, msg):
        self.socketIO.message(json.dumps(msg))
        self.socketIO.wait_for_callbacks()
        # self.socketIO.message(json.dumps(msg))

    def send_wait(self, msg):
        self.send(msg)
        # self.waiter()
        response = {}
        for i in range(1, 600):
            response = self.namespace.get_response()
            if response is not None:
                break
            else:
                self.socketIO.wait(self.wtime)
        return response

    def process_request(self, request, **kwarg):
        request_data = self.requests_dict[request]['request']
        if request_data and kwarg is not None:
            for param in kwarg.keys():
                request_data[param] = kwarg[param]
            return self.send_wait(request_data)
        else:
            print 'Request %s not found' % request
            return None