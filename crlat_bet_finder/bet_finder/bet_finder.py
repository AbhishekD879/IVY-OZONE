import web
import json

with open('resources/odds.json') as infile:
    config = json.load(infile)
urls = (
    '/cypher/.*/0.*', 'get_runner'
)

app = web.application(urls, globals())


class get_runner:
    def GET(self):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'x-requested-with, Content-Type, origin, authorization, accept, client-security-token',
            'Access-Control-Allow-Methods': 'POST, GET',
            'Access-Control-Allow-Origin': 'https://invictus.coral.co.uk',
            'Access-Control-Max-Age': '1000'
        }
        for header_name, header_value in headers.iteritems():
            web.header(header_name, header_value)
        return json.dumps(config)


if __name__ == "__main__":
    app.run()
