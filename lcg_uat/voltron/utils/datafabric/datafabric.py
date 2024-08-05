import tests
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import do_request


class Datafabric(object):

    def __init__(self):
        """
        Initialization of Datafabric
        """
        pass

    def get_datafabric_data(self, event_id: str, category_id: int = 21, raise_exceptions: bool = False):
        """
        Method to get information from datafabric about race event based on it ID
        BMA-45699 as an information source
        :param event_id: ID of the event
        :param category_id: Category ID of the race (21 - Horse racing, 19 - Greyhounds)
        :param raise_exceptions: If True will raise an exception if resp["Error"] == 'true', otherwise will return empty data dictionary
        :return: data dictionary
        """
        url = f'{tests.settings.datafabric_url}/categories/{category_id}/events/{event_id}/content?locale=en-GB&api-key=' \
              f'{tests.settings.datafabric_api_key}'
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
            resp = do_request(method='GET', url=url, headers=headers)
            if resp['Error'] and raise_exceptions:
                raise ThirdPartyDataException(f'No data available from datafabric for event with {event_id} ID!')
        except Exception as e:
            if raise_exceptions:
                raise e
            else:
                resp = {'Error': 'true'}
        return resp
