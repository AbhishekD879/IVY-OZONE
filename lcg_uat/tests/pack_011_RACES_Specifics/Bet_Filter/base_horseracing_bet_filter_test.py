import tests
from tests.Common import Common
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import do_request


class BaseHorseRacingBetFilterTest(Common):
    FILTERS = {'COURSE AND DISTANCE WINNER': 'courseDistanceWinner',
               'COURSE WINNER': 'courseWinner',
               'DISTANCE WINNER': 'distanceWinner',
               'WINNER LAST TIME': 'winnerLastTime',
               'WINNER WITHIN LAST 3': 'winnerLast3Starts',
               'PLACED LAST TIME': 'placedLastTime',
               'PLACED WITHIN LAST 3': 'placedLast3Starts',
               'PROVEN': 'provenGoing'}

    @property
    def site(self):
        return self._site

    @classmethod
    def openBetFilterPage(cls):
        cls.hostname = tests.HOSTNAME
        cls.setUpSite()
        cls._device.open_url(url='%s%s' % (cls.hostname, '/bet-finder'))
        cls._site.wait_splash_to_hide()
        cls._site.wait_content_state(state_name='HorseRacingBetFilterPage')

    @staticmethod
    def get_bets():
        response = do_request(method='GET', url=tests.settings.hr_bet_filter_url)
        cypher = response.get('cypher')
        if not cypher:
            raise ThirdPartyDataException('No available data for bet finder')
        runners = cypher.get('runners')
        if not runners:
            raise ThirdPartyDataException('No available runners data for bet finder')
        return runners

    def get_number_of_bets(self, **kwargs):
        bets = self.get_bets()
        filtered_bets = []
        if 'course' in kwargs.keys() and kwargs['course'] != 'All Meetings':
            bets = list(filter(lambda bet: bet['course'] == kwargs['course'], bets))
        if 'digital_tipster_filter' in kwargs.keys():
            bets = list(filter(lambda bet: bet['supercomputerSelection'] == kwargs['digital_tipster_filter'][0][0], bets))
        if 'star' in kwargs.keys():
            bets = list(filter(lambda bet: bet['starRating'] == kwargs['star'], bets))
        if 'filters' in kwargs.keys():
            for value in kwargs['filters']:
                try:
                    bets = list(filter(lambda bet: bet[self.FILTERS[value]] == 'Y', bets))
                except Exception:
                    bets = list(filter(lambda bet: bet[self.FILTERS[value.upper()]] == 'Y', bets))
        if 'odds' in kwargs.keys():
            for value in kwargs['odds']:
                start, end = self.get_interval(odds=value)
                for bet in bets:
                    odds = bet['odds']
                    if odds:
                        num, denom = odds.split('/')
                        odds = float(num) / float(denom)
                        if (odds >= start) and (odds <= end):
                            filtered_bets.append(bet)
                    if value == '33/1 OR BIGGER' and odds == '':
                        filtered_bets.append(bet)
        else:
            filtered_bets = list(bets)
        return len(filtered_bets)

    def get_interval(self, odds):
        first_symbol = odds.split(' ')[0]
        if first_symbol in ['ODDS', 'Odds']:
            return 0.0, 1.0
        elif first_symbol in ['EVENS', 'Evens']:
            return 1.00001, 3.5
        elif first_symbol == '4/1':
            return 4.0, 7.5
        elif first_symbol == '8/1':
            return 8.0, 14.0
        elif first_symbol == '16/1':
            return 16.0, 28.0
        else:
            return 33.0, 1000000.0

    def get_formstring_value(self, horse_name):
        for bet in self.get_bets():
            if bet['horseName'] == horse_name:
                return bet['formString']

    def verify_number_of_bets(self, expected_number_of_bets):
        self.site.horseracing_bet_filter.find_bets_button.click()
        self.site.wait_content_state_changed()
        actual_number_of_results = self.site.racing_bet_filter_results_page.number_of_results
        delta = 1
        self.assertAlmostEqual(actual_number_of_results, expected_number_of_bets, delta=delta,
                               msg=f'Incorrect number of bets displayed on Bets Filter Results page. '
                                   f'AR: [{actual_number_of_results}] ER: [{expected_number_of_bets}] with delta "{delta}"')
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HorseRacingBetFilterPage')

    def verify_filters(self, filters, type='filters', unselect=True):
        filter_items_ui = self.site.horseracing_bet_filter.items_as_ordered_dict
        self.assertTrue(filter_items_ui, msg='No filters found')
        for filter in list(dict.fromkeys(filters)):
            filter_element = filter_items_ui.get(filter if self.brand == 'bma' else filter.upper())
            self.assertTrue(filter_element, f'No filter "{filter}" found among filters "{filter_items_ui.keys()}"')
            filter_element.click()
            self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=filter if self.brand == 'bma' else filter.upper(), timeout=15),
                            msg=f'Filter [{filter}] is not selected which is wrong.')
        filter = {type: filters}
        expected_number_of_bets = self.get_number_of_bets(**filter)
        actual_number_of_bets = self.site.horseracing_bet_filter.read_number_of_bets()
        delta = 1
        self.assertAlmostEqual(int(actual_number_of_bets), int(expected_number_of_bets), delta=delta,
                               msg=f'Filters [{filters}] works incorrectly. '
                                   f'AR: [{actual_number_of_bets}] '
                                   f'ER: [{expected_number_of_bets}] with delta "{delta}"')
        if expected_number_of_bets != 0:
            self.verify_number_of_bets(self.get_number_of_bets(**filter))
        if unselect:
            for filter in filters:
                filter_element = self.site.horseracing_bet_filter.items_as_ordered_dict.get(filter)
                self.assertTrue(filter_element, f'No filter "{filter}" found among filters "{filter_items_ui}"')
                filter_element.click()
