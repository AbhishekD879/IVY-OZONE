import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.portal_dependant
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C34705559_Cash_Out_bet_with_Each_Way_terms_available(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C34705559
    NAME: Cash Out bet with Each Way terms available
    DESCRIPTION: This test case verifies Cash Out bet with Each Way terms available
    PRECONDITIONS: 1. Load app and log in
    PRECONDITIONS: 2. Place single and multiple HR bets with E/W option set and Cashout option available
    PRECONDITIONS: 3. Place single and multiple bets on Outright events with E/W option set and Cashout option available
    PRECONDITIONS: 4. Open DevTools and check the next request to SS to get Each-way data
    PRECONDITIONS: https://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForOutcome/{outcomeIDs}?simpleFilter=event.suspendAtTime:greaterThan:2020-01-13T12:44:00.000Z&racingForm=outcome&includeUndisplayed=true&translationLang=en&includeRestricted=true&prune=event&prune=market
    PRECONDITIONS: where,
    PRECONDITIONS: *   outcomeIDs - valid ID(s) of outcome that bet was placed on
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   domain - resource domain
    PRECONDITIONS: e.g. ss-aka-ori.coral.co.uk - Prod
    PRECONDITIONS: ![](index.php?/attachments/get/52704924)
    """
    keep_browser_open = True
    ew_my_bet_format = vec.bet_history.EXPECTED_MY_BETS_EACH_WAY_FORMAT
    number_of_events = 2

    def get_market_from_ss(self, event_id: str) -> dict:
        """
        Gets market for given event from SS response
        :param event_id: specifies event id
        :return: dict with market attributes and their values
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []

        self.assertTrue(markets, msg=f'Markets are not present for the event')
        return markets[0]['market']

    def eachway_factor_check(self, market):
        self.assertIn('isEachWayAvailable', market.keys(),
                      msg=f'There\'s no property "isEachWayAvailable" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['isEachWayAvailable'], 'true',
                          msg='Incorrect value for "isEachWayAvailable" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['isEachWayAvailable'], 'true'))

        self.assertIn('eachWayFactorNum', market.keys(),
                      msg=f'There\'s no property "eachWayFactorNum" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num']),
                          msg='Incorrect value for "eachWayFactorNum" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num'])))

        self.assertIn('eachWayFactorDen', market.keys(),
                      msg=f'There\'s no property "eachWayFactorDen" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den']),
                          msg='Incorrect value for "eachWayFactorDen" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den'])))

        self.assertIn('eachWayPlaces', market.keys(),
                      msg=f'There\'s no property "eachWayPlaces" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayPlaces'], str(self.ew_terms['ew_places']),
                          msg='Incorrect value for "eachWayPlaces" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayPlaces'], str(self.ew_terms['ew_places'])))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CashOut tab configuration in CMS
        DESCRIPTION: Load Oxygen application and login as user with no bets available for cash out
        """
        if self.brand == 'bma':
            system_config = self.get_initial_data_system_configuration()
            cashout_cms = system_config.get('CashOut')
            if not cashout_cms:
                cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
            if not cashout_cms:
                raise CmsClientException('CashOut section not found in System Configuration')
            self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
            if not self.is_cashout_tab_enabled:
                raise CmsClientException('CashOut tab is not enabled in CMS')

        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            event = events[0]
            self.__class__.racing_event_name1 = event['event']['name']
            self.__class__.eventID1 = event['event']['id']
            outcomes = next((market['market'] for market in event['event']['children']
                             if market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            if not outcomes:
                raise SiteServeException(f'Event {self.eventID1} does not have Each way market')
            sleep(2)
            self.__class__.ew_terms = {'ew_places': int(outcomes['eachWayPlaces']),
                                       'ew_fac_num': int(outcomes['eachWayFactorNum']),
                                       'ew_fac_den': int(outcomes['eachWayFactorDen'])}
            for i in outcomes['children']:
                if not str(i['outcome']['name']).__contains__('Unnamed'):
                    self.__class__.selection_id1 = i['outcome']['id']
                    break
            event2 = events[1]
            self.__class__.racing_event_name2 = event2['event']['name']
            eventID2 = event['event']['id']
            self.__class__.outcomes2 = next((market['market'] for market in event2['event']['children']
                                             if market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            if not self.outcomes2:
                raise SiteServeException(f'Event {eventID2} does not have Each way market')
            for i in self.outcomes2['children']:
                if not str(i['outcome']['name']).__contains__('Unnamed'):
                    self.__class__.selection_id2 = i['outcome']['id']
                    break

            # outright
            class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)

            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       class_id=class_ids,
                                       brand=self.brand)
            events_filter = self.ss_query_builder \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                            vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))

            found_events = []
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            for event in resp:
                if event.get('event') and event['event'].get('children'):
                    markets = event['event']['children']
                    for market in markets:
                        if market['market']['templateMarketName'] == 'Outright' and \
                                market['market']['name'] == 'Outright':
                            found_events.append(event)

            if len(found_events) < 2:
                raise SiteServeException(
                    f'No outright events with each way market found for category id "{self.ob_config.football_config.category_id}"')
            event = found_events[0]
            self.__class__.event_name1 = event['event']['name']
            self.__class__.eventID3 = event['event']['id']
            self.__class__.outcomes3 = next((market['market'] for market in event['event']['children']
                                             if market.get('market').get('templateMarketName') == 'Outright'), None)
            if not self.outcomes3:
                raise SiteServeException(f'Event {self.eventID3} does not have Each way market')

            for i in self.outcomes3['children']:
                if not str(i['outcome']['name']).__contains__('Unnamed'):
                    self.__class__.selection_id3 = i['outcome']['id']
                    break
            event2 = found_events[1]
            self.__class__.event_name2 = event2['event']['name']
            self.__class__.outcomes4 = next((market['market'] for market in event2['event']['children']
                                             if market.get('market').get('templateMarketName') == 'Outright'),
                                            None)
            if not self.outcomes4:
                raise SiteServeException('Event does not have Each way market')
            for i in self.outcomes4['children']:
                if not str(i['outcome']['name']).__contains__('Unnamed'):
                    self.__class__.selection_id4 = i['outcome']['id']
                    break

        else:
            event1 = self.ob_config.add_UK_racing_event(cashout=True, ew_terms=self.ew_terms)
            self.__class__.racing_event_name1 = event1[6]['event']['name']
            self.__class__.selection_id1 = list(event1.selection_ids.values())[0]
            self.__class__.eventID1 = event1.event_id
            event2 = self.ob_config.add_UK_racing_event(cashout=True, ew_terms=self.ew_terms)
            self.__class__.racing_event_name2 = event2[6]['event']['name']
            self.__class__.selection_id2 = list(event2.selection_ids.values())[0]
            self.__class__.eventID2 = event2.event_id

            # outright
            ew_event1 = self.ob_config.add_autotest_premier_league_football_outright_event(cashout=True,
                                                                                           ew_terms=self.ew_terms)
            self.__class__.eventID3 = ew_event1.event_id
            self.__class__.selection_id3 = list(ew_event1.selection_ids.values())[0]
            self.__class__.event_name1 = ew_event1[7]['event']['name']

            ew_event2 = self.ob_config.add_england_premier_league_football_outright_event(cashout=True,
                                                                                          ew_terms=self.ew_terms)
            self.__class__.eventID4 = ew_event2.event_id
            self.__class__.selection_id4 = list(ew_event2.selection_ids.values())[0]
            self.__class__.event_name2 = ew_event2[7]['event']['name']

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        self.place_single_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
        else:
            self.site.open_my_bets_open_bets()

    def test_002_verify_single_hr_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Verify **single** HR Cash Out bet with each-way terms
        EXPECTED: * 'Each Way' text is shown in brackets next to bet type
        EXPECTED: * Each way terms are displayed next to the market name in the next format:
        EXPECTED: 'x/y odds - places z,j,k'
        EXPECTED: e.g. 1/4 odds - places 1,2,4
        EXPECTED: ![](index.php?/attachments/get/53285767)
        """
        each_way = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms['ew_fac_num'], ew_fac_den=self.ew_terms['ew_fac_den'],
                                                ew_places=','.join(
                                                str(place) for place in range(1, self.ew_terms['ew_places'] + 1)))
        if self.brand == 'bma':
            bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type='SINGLE (EACH WAY)', event_names=self.racing_event_name1)
        else:
            sleep(3)  # New bet on OpenBets tab takes few secs to load
            bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type='SINGLE (EACH WAY)', event_names=self.racing_event_name1)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        for betleg_name, betleg in bet_legs.items():
            self.assertIn(each_way, betleg.market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{betleg.market_name}"')

    def test_003_verify_each_way_terms_availability(self):
        """
        DESCRIPTION: Verify each-way terms availability
        EXPECTED: Each-way terms are displayed if 'isEachWayAvailable' = 'true' attribute is present in the SS response on market level for a particular event
        EXPECTED: ![](index.php?/attachments/get/53285768)
        """
        self.__class__.market = self.get_market_from_ss(self.eventID1)
        self.eachway_factor_check(market=self.market)

    def test_004_verify_each_way_terms_correctness(self):
        """
        DESCRIPTION: Verify each-way terms correctness
        EXPECTED: Terms correspond to the 'eachWayFactorNum', 'eachWayFactorDen' and 'eachWayPlaces' attributes from SS response for particular event
        EXPECTED: ![](index.php?/attachments/get/53285769)
        """
        # covered in above step

    def test_005_repeat_steps_2_4_for_multiple_hr_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **multiple** HR Cash Out bet with each-way terms
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])
        self.place_multiple_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand()
        if tests.settings.backend_env == 'prod':
            self.__class__.ew_terms2 = {'ew_places': int(self.outcomes2['eachWayPlaces']),
                                        'ew_fac_num': int(self.outcomes2['eachWayFactorNum']),
                                        'ew_fac_den': int(self.outcomes2['eachWayFactorDen'])}
            each_way2 = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms2['ew_fac_num'],
                                                     ew_fac_den=self.ew_terms2['ew_fac_den'],
                                                     ew_places=','.join(
                                                         str(place) for place in
                                                         range(1, self.ew_terms2['ew_places'] + 1)))
        each_way = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms['ew_fac_num'],
                                                ew_fac_den=self.ew_terms['ew_fac_den'],
                                                ew_places=','.join(
                                                    str(place) for place in range(1, self.ew_terms['ew_places'] + 1)))
        if self.brand == 'bma':
            bet_name, double_bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type='DOUBLE (EACH WAY)', event_names=self.racing_event_name2)
        else:
            sleep(3)  # New bet on OpenBets tab takes few secs to load
            bet_name, double_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type='DOUBLE (EACH WAY)', event_names=self.racing_event_name2)
        bet_legs = list(double_bet.items_as_ordered_dict.values())
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        if tests.settings.backend_env == 'prod':
            self.assertIn(each_way, bet_legs[0].market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{bet_legs[0].market_name}"')
            self.assertIn(each_way2, bet_legs[1].market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{bet_legs[1].market_name}"')
        else:
            for betleg_name, betleg in double_bet.items_as_ordered_dict.items():
                self.assertIn(each_way, betleg.market_name,
                              msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{betleg.market_name}"')
        self.__class__.market = self.get_market_from_ss(self.eventID1)
        self.eachway_factor_check(market=self.market)

    def test_006_repeat_steps_2_4_for_single_outright_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **single** Outright Cash Out bet with each-way terms
        """
        self.__class__.expected_betslip_counter_value = 0
        if tests.settings.backend_env == 'prod':
            self.__class__.ew_terms = {'ew_places': int(self.outcomes3['eachWayPlaces']),
                                       'ew_fac_num': int(self.outcomes3['eachWayFactorNum']),
                                       'ew_fac_den': int(self.outcomes3['eachWayFactorDen'])}
        self.open_betslip_with_selections(selection_ids=self.selection_id3)
        self.place_single_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        each_way = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms['ew_fac_num'],
                                                ew_fac_den=self.ew_terms['ew_fac_den'],
                                                ew_places=','.join(
                                                    str(place) for place in range(1, self.ew_terms['ew_places'] + 1)))
        sleep(3)  # New bet on OpenBets tab takes few secs to load
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE (EACH WAY)', event_names=self.event_name1)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        for betleg_name, betleg in bet_legs.items():
            self.assertIn(each_way, betleg.market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{betleg.market_name}"')
        self.__class__.market = self.get_market_from_ss(self.eventID3)
        self.eachway_factor_check(market=self.market)

    def test_007_repeat_steps_2_4_for_multiple_outright_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **multiple** Outright Cash Out bet with each-way terms
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id3, self.selection_id4])
        self.place_multiple_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        if tests.settings.backend_env == 'prod':
            self.__class__.ew_terms2 = {'ew_places': int(self.outcomes4['eachWayPlaces']),
                                        'ew_fac_num': int(self.outcomes4['eachWayFactorNum']),
                                        'ew_fac_den': int(self.outcomes4['eachWayFactorDen'])}
            each_way2 = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms2['ew_fac_num'],
                                                     ew_fac_den=self.ew_terms2['ew_fac_den'],
                                                     ew_places=','.join(
                                                         str(place) for place in
                                                         range(1, self.ew_terms2['ew_places'] + 1)))
        each_way = self.ew_my_bet_format.format(ew_fac_num=self.ew_terms['ew_fac_num'],
                                                ew_fac_den=self.ew_terms['ew_fac_den'],
                                                ew_places=','.join(
                                                    str(place) for place in range(1, self.ew_terms['ew_places'] + 1)))
        sleep(3)  # Bets on OpenBets tab takes few secs to load
        bet_name, double_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE (EACH WAY)', event_names=self.event_name2)
        bet_legs = list(double_bet.items_as_ordered_dict.values())
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        if tests.settings.backend_env == 'prod':
            self.assertIn(each_way, bet_legs[0].market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{bet_legs[0].market_name}"')
            self.assertIn(each_way2, bet_legs[1].market_name,
                          msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{bet_legs[1].market_name}"')
        else:
            for betleg_name, betleg in double_bet.items_as_ordered_dict.items():
                self.assertIn(each_way, betleg.market_name,
                              msg=f'Each way "{each_way}" is not present or not '
                              f'match required format in "{betleg.market_name}"')
        self.__class__.market = self.get_market_from_ss(self.eventID3)
        self.eachway_factor_check(market=self.market)
