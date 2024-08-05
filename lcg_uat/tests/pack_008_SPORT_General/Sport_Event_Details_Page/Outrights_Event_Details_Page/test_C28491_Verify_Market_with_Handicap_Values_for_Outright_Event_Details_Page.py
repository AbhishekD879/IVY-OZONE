import pytest
import tests
import time
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.siteserve_client import SiteServeRequests


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Can not create events and markets through OB
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28491_Verify_Market_with_Handicap_Values_for_Outright_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C28491
    NAME: Verify Market with Handicap Values for Outright Event Details Page
    DESCRIPTION: This test case verifies markets which selections have handicap values available on SS response.
    DESCRIPTION: NOTE, User Story **BMA-5049**
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True
    event_name = f'Outright event {int(time.time())}'
    markets_params = [('handicap_match_result', {'cashout': True})]
    handicap_value = '-1.0'
    event_time = None

    def get_market_outcomes_for_event(self, event_id: (str, int)) -> dict:
        """
        Gets outcomes for all markets for specific event
        :param event_id: int, event id
        :return: dictionary where the key is market name, value is dictionary of outcome names and ids
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=self.ss_query_builder)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []
        markets_outcomes = {}
        for market in markets:
            if 'market' in market and 'children' in market['market']:
                outcomes = {}
                for outcome in market['market']['children']:
                    outcomes.update({outcome['outcome']['name']: outcome['outcome']['id']})
                markets_outcomes[market['market']['name']] = {'id': market['market']['id'], 'outcomes': outcomes}
        return markets_outcomes

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create outright event
        EXPECTED: User should be able to access generated event
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        event = self.ob_config.add_autotest_premier_league_football_outright_event(
            event_name=self.event_name, is_live=True, img_stream=True, markets=self.markets_params)
        self.__class__.eventID, self.__class__.event_time = event.event_id, event.event_date_time
        self.__class__.ss_event_details = ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                               query_builder=self.ss_query_builder)

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        # Covered in Step# 3

    def test_003_tap_event_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        self.__class__.marketID = self.ob_config.market_ids[self.eventID][
            f'handicap_match_result {self.handicap_value}']
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_004_open_market_which_selections_have_handicap_value_available(self):
        """
        DESCRIPTION: Open market which selections have handicap value available
        """
        available_markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(available_markets,
                        msg=f'Handicap markets are not available for outright event "{self.eventID}"')
        available_markets = [x.lower() for x in list(available_markets.keys())]

        market_outcomes = self.get_market_outcomes_for_event(event_id=self.eventID)
        market_outcomes = [x.lower() for x in list(market_outcomes.keys())]
        self.assertListEqual(sorted(available_markets), sorted(market_outcomes),
                             msg=f'Available markets: "{sorted(available_markets)}" '
                                 f'are not the same as expected: "{sorted(market_outcomes)}"')

    def test_005_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        ss_event_markets = self.ss_event_details[0]['event']['children']

        for market in ss_event_markets:
            if market['market']['id'] == self.marketID and market['market'].get('children'):
                ss_market_name = market['market']['name']
                self.__class__.market_outcomes = market['market']['children']
                self.assertTrue(self.market_outcomes, msg=f'"{ss_market_name}" market has no available outcomes')
                break

        for outcome in self.market_outcomes:
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H':
                self.__class__.ss_outcome_handicap_value = \
                    outcome['outcome']['children'][0]['price']['handicapValueDec'].strip(',')
        self.assertEqual(eval(self.handicap_value), eval(self.ss_outcome_handicap_value),
                         msg=f'Handicap value "{eval(self.handicap_value)}" '
                             f'is not the same as expected "{eval(self.ss_outcome_handicap_value)}"')

    def test_006_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed directly to the right of the outcome names
        EXPECTED: Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        # Covered in Step# 5

    def test_007_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        self.assertIn(self.handicap_value[0], self.ss_outcome_handicap_value,
                      msg=f'Handicap value displayed without "{self.handicap_value[0]}" sign')

    def test_008_verify_selections_without_handicap_value_available(self):
        """
        DESCRIPTION: Verify selections without handicap value available
        EXPECTED: Handicap value is NOT shown near the outcome name
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self._logger.info(f'*** Football event with event id "{self.eventID}"')

        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        markets = event_details['children']
        self.assertTrue(markets, msg="Markets not available")

        for market in markets:
            market_details = market['market']
            try:
                outcomes = market_details['children']
            except KeyError:
                self._logger.info('current market' + market_details["templateMarketName"] + ' does not have outcomes')
                continue
            if outcomes:
                for outcome in outcomes:
                    ss_outcome_handicap_value = ((outcome['outcome']['children'][0]['price']).get('handicapValueDec'))
                    self.assertFalse(ss_outcome_handicap_value, msg=f'Handicap value is shown near outcome name')
