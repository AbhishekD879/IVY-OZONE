from voltron.utils import mixins
from voltron.utils.helpers import do_request


class TimeformClient(mixins.LoggingMixin,):
    def __init__(self, env, *args, **kwargs):
        super(TimeformClient, self).__init__(*args, **kwargs)
        self.site = env

    def get_races(self, count='200', **kwargs):
        response = do_request(url=self.site + '/api/v1/greyhoundracing/races?top={count}'.format(count=count),
                              method='GET')
        race_ids = []
        for item in response:
            race_ids += item.get('openBetIds', [])
        return race_ids

    def get_race_info(self, openbet_id, **kwargs):
        response = do_request(url=self.site + '/api/v1/greyhoundracing/race/{openbet_id}/openbet'.format(openbet_id=openbet_id),
                              method='GET')
        return response
