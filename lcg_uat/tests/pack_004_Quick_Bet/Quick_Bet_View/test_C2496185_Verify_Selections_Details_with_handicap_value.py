import re

import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import generate_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.quick_bet
@pytest.mark.handicap
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.mobile_only
@vtest
class Test_C2496185_Verify_Selections_Details_with_handicap_value(BaseSportTest):
    """
    TR_ID: C2496185
    VOL_ID: C11049257
    NAME: Verify Selection's Details with handicap value
    DESCRIPTION: This test case verifies selections details with handicap value within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. To get event's details open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section
    PRECONDITIONS: See attributes:
    PRECONDITIONS: 'name' on event level to see event name and local time
    PRECONDITIONS: 'name' on market level to see market name
    PRECONDITIONS: 'name' on outcome level to see selection name
    PRECONDITIONS: 'priceNum' and 'priceDen' to see current odds in fractional format
    PRECONDITIONS: 'priceDec' to see current odds in decimal format
    """
    keep_browser_open = True
    team1 = generate_name()
    team2 = generate_name()
    ss_event_details = None
    ss_market_name = None
    ss_outcome_name = ss_home_outcome = None
    ss_outcome_handicap_value = None
    handicap_negative, handicap_positive = '-1.0', '+3.0'
    selection_name = market_name = event_name = selection_odds = None
    handicap_value = None
    market_outcomes = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        event = self.ob_config.add_autotest_premier_league_football_event(team1=self.team1, team2=self.team2,
                                                                          markets=[('handicap_match_result',
                                                                                    {'cashout': True})])
        self.__class__.eventID = event.event_id
        self.__class__.ss_event_details = ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                               query_builder=self.ss_query_builder)

    def test_001_add_one_selection_to_quick_bet_where_handicap_is_available(self, handicap=handicap_negative):
        """
        DESCRIPTION: Add one selection to Quick Bet where handicap is available
        EXPECTED: Quick Bet is displayed at the bottom of page
        """
        self.__class__.marketID = self.ob_config.market_ids[self.eventID][f'handicap_match_result {handicap}']
        self.navigate_to_edp(event_id=self.eventID)

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        handicap_results = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(handicap_results, msg=f'"{self.expected_market_sections.handicap_results}" market not available')

        outcome_groups = handicap_results.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg=f'"{self.expected_market_sections.handicap_results}" market has no outcomes')
        self.assertIn(handicap.split('.')[0], outcome_groups.keys(),
                      msg='"%s" outcome group not available among "%s" groups' %
                          (handicap.split('.')[0], outcome_groups.keys()))

        outcome_group = outcome_groups.get(handicap.split('.')[0])
        outcomes = outcome_group.items_as_ordered_dict
        outcome = outcomes.get(vec.sb.HOME.title())
        outcome.click()

        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not displayed at the bottom of page')

    def test_002_verify_selections_details(self):
        """
        DESCRIPTION: Verify selection's details
        EXPECTED: The following information is displayed within Quick Bet:
        EXPECTED: * selection name and handicap value (e.g <Selection name> (handicap value))
        EXPECTED: * market name
        EXPECTED: * event name
        EXPECTED: * selection's odds
        """
        quick_bet_panel = self.site.quick_bet_panel

        # selection_name_with_handicap_value example 'Jonesland (-1.0)'
        selection_name_with_handicap_value = quick_bet_panel.selection.content.outcome_name
        selection_name_with_handicap_value_re = re.search(r'(.*)\((.*)\)', selection_name_with_handicap_value)

        self.__class__.selection_name = selection_name_with_handicap_value_re.group(1).strip()
        self.__class__.handicap_value = selection_name_with_handicap_value_re.group(2)
        self.assertTrue(self.selection_name, msg='Selection name not available')
        self.assertTrue(self.handicap_value, msg='Handicap value not available')

        self.__class__.market_name = quick_bet_panel.selection.content.market_name
        self.assertTrue(self.market_name, msg='Market name is not available')

        self.__class__.event_name = quick_bet_panel.selection.content.event_name
        self.assertTrue(self.event_name, msg='Event name is not available')

        self.__class__.selection_odds = quick_bet_panel.selection.content.odds
        self.assertTrue(self.selection_odds, msg='Selection odds are not available')

        quick_bet_panel.close()

    def test_003_verify_selection_name_and_handicap_value(self):
        """
        DESCRIPTION: Verify selection name and handicap value
        EXPECTED: * Selection name corresponds to **'name'** attribute on the outcome level
        EXPECTED: * Handicap value corresponds to **'handicapValueDec'** from the Site Server response
        """
        ss_event_markets = self.ss_event_details[0]['event']['children']

        for market in ss_event_markets:
            if market['market']['id'] == self.marketID and market['market'].get('children'):
                self.__class__.ss_market_name = market['market']['name']
                self.__class__.market_outcomes = market['market']['children']

        self.assertTrue(self.market_outcomes, msg=f'"{self.ss_market_name}" market has no available outcomes')

        ss_outcome_name = None
        for outcome in self.market_outcomes:
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H':
                self.__class__.ss_home_outcome = outcome
                ss_outcome_name = outcome['outcome']['name']
                self.__class__.ss_outcome_handicap_value = \
                    outcome['outcome']['children'][0]['price']['handicapValueDec'].strip(',')

        self.assertEqual(self.selection_name, ss_outcome_name,
                         msg=f'Selection name "{self.selection_name}" is not the same as expected "{ss_outcome_name}"')

        self.assertEqual(eval(self.handicap_value), eval(self.ss_outcome_handicap_value),
                         msg=f'Handicap value "{eval(self.handicap_value)}" '
                             f'is not the same as expected "{eval(self.ss_outcome_handicap_value)}"')

    def test_004_verify_sign_for_handicap_value(self, value_sign=handicap_negative[0]):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: * handicap value is displayed with **'-'** sign if **'handicapValueDec'**contains negative value
        EXPECTED: * handicap value is displayed with **'+'** sign if **'handicapValueDec'**contains positive value
        EXPECTED: * handicap value is displayed with **'+'** sign if **'handicapValueDec'** has no sign
        """
        self.assertIn(value_sign, self.handicap_value,
                      msg=f'Handicap value displayed without "{value_sign}" sign')

    def test_005_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Market name corresponds to **'name'** attribute on the market level in SiteServer response
        """
        self.assertEqual(self.market_name, self.ss_market_name,
                         msg=f'Market name "{self.market_name}" is not the same as expected "{self.ss_market_name}"')

    def test_006_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to **'name'** attribute on the event level in SiteServer response
        """
        ss_event_name = self.ss_event_details[0]['event']['name']
        self.assertEqual(self.event_name, ss_event_name,
                         msg=f'Event name "{self.event_name}" is not  the same as expected "{ss_event_name}"')

    def test_007_verify_selections_odds(self):
        """
        DESCRIPTION: Verify selection`s odds
        EXPECTED: * Selection`s odds correspond to **'data.selectionPrice.priceNum'** and **'data.selectionPrice.priceDen'** attributes in fraction format
        EXPECTED: * Selection`s odds correspond **'data.selectionPrice.priceDec'** attribute in decimal format
        EXPECTED: *  Selection`s odds is equal to SP when **'data.selectionPrice.priceType=SP'** attribute is received in WS response
        """
        ss_odds = '%s/%s' % (self.ss_home_outcome['outcome']['children'][0]['price']['priceNum'],
                             self.ss_home_outcome['outcome']['children'][0]['price']['priceDen'])
        self.assertEqual(self.selection_odds, ss_odds,
                         msg=f'Selection odds "{self.selection_odds}" are not the same as expected "{ss_odds}"')

    def test_008_verify_selections_details_with_positive_handicap_value(self, handicap=handicap_positive):
        """
        DESCRIPTION: Repeat steps 1-7 with positive handicap
        """
        self.test_001_add_one_selection_to_quick_bet_where_handicap_is_available(handicap=handicap)
        self.test_002_verify_selections_details()
        self.test_003_verify_selection_name_and_handicap_value()
        self.test_004_verify_sign_for_handicap_value(value_sign=handicap[0])
        self.test_005_verify_market_name()
        self.test_006_verify_event_name()
        self.test_007_verify_selections_odds()
