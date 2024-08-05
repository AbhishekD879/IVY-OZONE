import json
import os

import web
from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = "server.cert"
CherryPyWSGIServer.ssl_private_key = "server.key"


urls = (
    '/(.*)', 'prematch',
    '/api/match/byobid/.*/pre', 'prematch'
)
app = web.application(urls, globals())


class prematch(web.application):
    with open(os.path.join('resources/stats.json')) as prematch_stats_file:
            prematch_stats_dict = json.load(prematch_stats_file)
            prematch_stats_string = json.dumps(prematch_stats_dict)

    def GET(self, name):
        headers = [
        {
          "name": "Date",
          "value": "Mon, 01 Aug 2016 08:11:57 GMT"
        },
        {
          "name": "Server",
          "value": "nginx/1.9.9"
        },
        {
          "name": "X-Powered-By",
          "value": "Express"
        },
        {
          "name": "ETag",
          "value": "W/\"c00b-Nwg4CgN1mk+1iitM2yFx0g\""
        },
        {
          "name": "Access-Control-Allow-Methods",
          "value": "GET, OPTIONS, POST, PUT, DELETE"
        },
        {
          "name": "Access-Control-Allow-Origin",
          "value": "https://vis-static-tst2.coral.co.uk"
        },
        {
          "name": "Access-Control-Allow-Credentials",
          "value": "true"
        },
        {
          "name": "Connection",
          "value": "keep-alive"
        },
        {
          "name": "Access-Control-Allow-Headers",
          "value": "Content-Type"
        },
        {
          "name": "Content-Type",
          "value": "application/json; charset=utf-8"
        }
        ]
        for item in headers:
            web.header(item['name'], item['value'])
        return self.prematch_stats_string

    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


if __name__ == "__main__":
    app.run()