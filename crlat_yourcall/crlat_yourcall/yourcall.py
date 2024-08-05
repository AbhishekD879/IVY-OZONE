# -*- coding: utf-8 -*-
import json
import os
from collections import namedtuple
import time
import web
from web.wsgiserver import CherryPyWSGIServer
from crlat_ob_client.openbet_config import OBConfig

CherryPyWSGIServer.ssl_certificate = 'api-proxy.digitalsportstech.com.crt'
CherryPyWSGIServer.ssl_private_key = 'api-proxy.digitalsportstech.com.key'
hostname = 'https://invictus.coral.co.uk'


def get_games_filtered(source_data_dict, league_ids=None):
    data = source_data_dict['data']

    if league_ids:
        data = [league for league in data if str(league['leagueId']) in league_ids]
        data.sort(key=lambda x: time.mktime(time.strptime(x['date'], '%Y-%m-%d %H:%M:%S')))
    response_data = {
        'errors': None,
        'data': data,
        'options': {
            'totalPagesCount': 1,
            'currentPage': 1,
            'totalItemsCount': len(data),
        },
        'version': '4.24.3'
    }
    return response_data

urls = (
    # Landing page
    '/ob/leagues.json', 'leagues',  # https://api-proxy.digitalsportstech.com/ob/leagues.json?apiKey=coralob2&isActive=1&v=4
    '/ob/games.json', 'games',  # '/ob/games.json?apiKey=coralob2&leagueId=153,146,150,151,149,123,142&order=asc&sort=date&status=1&v=4'
                                # /ob/games.json?apiKey=coralob2prod&obEventId=9194238&status=1&v=4
    # Event details page
    '/gfm/feed.json', 'feed',  # /gfm/feed.json?apiKey=coralob2prod&gameId=83226&v=4 in games_event.json[data][id] == gameID
    '/dfm/feed.json', 'feed_market', # /dfm/feed.json?apiKey=coralob2prod&gameId=83422&playerId=158086&v=4 or /dfm/feed.json?apiKey=coralob2&gameId=83226&statisticId=30&v=4
    '/ob/players.json', 'players',  # /ob/players.json?apiKey=coralob2prod&isActive=1&obEventId=9194238&status=1&v=4
    '/statistics.json', 'statistics',  # /statistics.json?apiKey=coralob2prod&betType=1&leagueId=146&sportId=1&v=4
    '/odds/stat-value-range.json', 'odds_stats', # /odds/stat-value-range.json?apiKey=coralob2prod&playerId=158086&statisticId=30&v=4
    '/odds/accumulator-calculate.json', 'odds_calc', #/odds/accumulator-calculate.json?apiKey=coralob2prod&events%5B0%5D%5BconditionType%5D=3&events%5B0%5D%5BconditionValue%5D=2&events%5B0%5D%5Bgame1Id%5D=83422&events%5B0%5D%5Bplayer1Id%5D=158086&events%5B0%5D%5BstatisticId%5D=30&events%5B0%5D%5Btype%5D=1&v=4
    '/bets/max-exposure.json', 'max_expose', #/bets/max-exposure.json?apiKey=coralob2&events%5B0%5D%5BconditionType%5D=3&events%5B0%5D%5BconditionValue%5D=75&events%5B0%5D%5Bgame1Id%5D=84586&events%5B0%5D%5Bplayer1Id%5D=141124&events%5B0%5D%5BstatisticId%5D=1617&events%5B0%5D%5Btype%5D=1&odds=17%2F20&sportbookUser=at_user_has_card&v=4

    # helpers
    '/crlat/crlat_get_config', 'crlat_get_config',

)
event_id = None
games_event_dict = None
games_all_dict = None

headers = {
            'origin': hostname,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'uk,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Mobile Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'referer': hostname,
            ':authority': 'api-proxy.digitalsportstech.com',
            'if-none-match': 'W/\'0R6VJvzcfnGqBTyfIpxU6Q==\'',
            ':scheme': 'https',
            ':method': 'GET',
            'Access-Control-Allow-Origin': hostname
        }


def file_to_response(filename):
    with open(os.path.join('resources/%s' % filename)) as infile:
        # print infile.name
        res_dict = json.load(infile)
        res_string = json.dumps(res_dict)
        Params = namedtuple("response_types", ["as_string", "as_dict"])
        response_params = Params(res_string, res_dict)
        return response_params


def get_statistic_ids():
    statistics = file_to_response(filename='statistics.json').as_dict['data']
    statistic_ids = {}
    for statistic in statistics:
        statistic_ids[statistic['title']] = statistic['id']
    return statistic_ids


class base(web.application):
    def __init__(self):
        games_for_event = file_to_response(filename='games_event.json')
        global games_event_dict
        games_event_dict = games_for_event.as_dict
        games_all = file_to_response(filename='games.json')
        global games_all_dict
        games_all_dict = games_all.as_dict
        # self.leagues_str = file_to_response(filename='leagues.json').as_string
        global event_id
        if not event_id:
            # if 'obEventId' in web.input().keys():
            print '______ creating event'
            ob_conf = OBConfig(env='tst2')
            event_params = ob_conf.add_football_event_to_england_premier_league(team1='Leicester City', team2='Stoke City')
            event_id = event_params.event_id
            print '______ event id %s' % event_id


class leagues(base):

    def GET(self):
        user_data = '&'.join(['%s=%s' % (key, value) for key, value in web.input().items()])
        print user_data
        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value
        web.header(':path', '/ob/{resource}?{query_params}'.format(resource='leagues.json', query_params=user_data))
        print web.ctx.headers
        self.leagues_str = file_to_response(filename='leagues.json').as_string
        return self.leagues_str


class games(base):

    def GET(self):
        user_data = '&'.join(['%s=%s' % (key, value) for key, value in web.input().items()])
        print user_data

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value
        web.header(':path', '/ob/{resource}?{query_params}'.format(resource='games.json', query_params=user_data))
        print web.ctx.headers

        # replacing event id in all games response
        for number, game in enumerate(games_all_dict['data']):
            if game['id'] == 83298:  # TODO need to generate game id?? or just use hardcoded one
                games_all_dict['data'][number]['obEventId'] = event_id
                break
                # TODO
                # games_all_dict['data'][number]['title'] - generate today's date
                # games_all_dict['data'][number]['date'] - generate today's date

        # replacing event id in games for event response
        games_event_dict['data'][0]['obEventId'] = event_id
        # print 'BASE: all games dict: ', games_all_dict
        # print 'games for event dict: ', games_event_dict
        # TODO need to update game id?? (but we are searching for game based on its id) and generate actual date
        # games_event_dict['data'][0]['id'] = game_id random number, also need to update in all responces
        # games_event_dict['data][0]['title'] - generate today's date
        # games_event_dict['data][0]['date'] - generate today's date

        if 'leagueId' in web.input().keys():  # returns all events/games in all available leagues
            # print 'GAMES all games dict: ', self.games_all_dict
            league_ids = web.input()['leagueId'].strip(',').split(',')
            return json.dumps(get_games_filtered(games_all_dict, league_ids=league_ids))
        elif 'obEventId' in web.input().keys():  # returns specific event/game
            return json.dumps(games_event_dict)


class feed(base):

    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='feed.json').as_string


class feed_market(base):

    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        file_name = None
        if 'statisticId' in web.input():
            statistic_id = web.input()['statisticId']
            if str(get_statistic_ids()['Cards']) in statistic_id:
                file_name = 'feed_player.json'
            elif str(get_statistic_ids()['Goals']) in statistic_id:
                file_name = 'feed_game.json'
        elif 'playerId' in web.input():
            file_name = 'feed_select_player.json'

        if file_name:
            return file_to_response(filename=file_name).as_string
        else:
            return 'Couldn\'t mock market selections with unknown statistic id: %s' % statistic_id


class players(base):

    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='players.json').as_string


class statistics(base):
    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='statistics.json').as_string


class odds_stats(base):
    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='odds_stats.json').as_string


class odds_calc(base):
    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='odds_calc.json').as_string


class max_expose(base):
    def GET(self):

        for name, value in headers.items():
            web.header(name, value)
            print name, '___', value

        return file_to_response(filename='max-exposure.json').as_string


class crlat_get_config(web.application):

    def GET(self):
        global event_id
        return json.dumps(
            {
                'event_id': event_id
            },
            indent=2
        )

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
    app.wsgifunc()
