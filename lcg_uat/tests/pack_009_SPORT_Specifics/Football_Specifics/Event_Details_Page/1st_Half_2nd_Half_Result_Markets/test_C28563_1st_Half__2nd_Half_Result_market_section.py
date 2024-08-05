import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event can not be created in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28563_1st_Half__2nd_Half_Result_market_section(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28563
    NAME: 1st Half / 2nd Half Result market section
    DESCRIPTION: This test case verifies '1st Half / 2nd Half Result' market section on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    """
    keep_browser_open = True
    EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS = ['1ST HALF', '2ND HALF']

    def verify_selections_displaying_for_market(self, market=None):
        home_team = market[0]['outcome']['outcomeMeaningMinorCode']
        self.assertEqual(home_team, 'H', msg=f'Actual outcomeMeaningMinorCode: "{home_team}" is not same as'
                                             f'Expected outcomeMeaningMinorCode: "H"')
        draw = market[1]['outcome']['outcomeMeaningMinorCode']
        self.assertEqual(draw, 'D', msg=f'Actual outcomeMeaningMinorCode: "{draw}" is not same as'
                                        f'Expected outcomeMeaningMinorCode: "D"')
        away_team = market[2]['outcome']['outcomeMeaningMinorCode']
        self.assertEqual(away_team, 'A', msg=f'Actual outcomeMeaningMinorCode: "{away_team}" is not same as'
                                             f'Expected outcomeMeaningMinorCode: "A"')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create a event
        """
        self.__class__.market_name = '1st Half / 2nd Half Result'
        markets_params = [('first_half_result', {'cashout': True}),
                          ('second_half_result', {'cashout': True})]
        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        for market in event.ss_response['event']['children']:
            if market['market']['templateMarketName'] == 'First-Half Result':
                self.__class__.first_half_market = market['market']['children']
            elif market['market']['templateMarketName'] == 'Second-Half Result':
                self.__class__.second_half_market = market['market']['children']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        wait_for_result(lambda: self.site.wait_content_state(state_name='EventDetails'), timeout=120)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_1st_half__2nd_half_result_market_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘1st Half / 2nd Half Result’
        EXPECTED: *   It is possible to collapse/expand section
        """
        if self.brand == 'bma' and self.device_type == 'mobile':
            expected_market_name = self.market_name.upper()
        else:
            expected_market_name = self.market_name

        self.assertIn(expected_market_name, self.markets_list,
                      msg=f'"{expected_market_name}" section is not present')

        self.__class__.first_half_second_half = self.markets_list.get(expected_market_name)
        self.assertTrue(self.first_half_second_half,
                        msg=f'"{expected_market_name}" section is not found in "{self.markets_list.keys()}"')

        if not self.first_half_second_half.is_expanded():
            sleep(2)
            self.first_half_second_half.expand()
        self.assertTrue(self.first_half_second_half.is_expanded(),
                        msg=f'"{self.first_half_second_half}" section is not expanded')

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (First-Half Result, Second-Half Result) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.first_half_second_half.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.first_half_second_half}" has no cashout label')

    def test_005_expand_1st_half__2nd_half_result_market_section(self):
        """
        DESCRIPTION: Expand '1st Half / 2nd Half Result' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two filters: '1st Half Result' (selected by default), '2nd Half Result'
        EXPECTED: *   <Home Team>, <Draw>, <Away Team> selections with corresponding price/odds buttons
        """
        first_half_second_half = self.first_half_second_half.grouping_buttons.items_names
        self.assertEqual(first_half_second_half, self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS,
                         msg=f'Actual market headers "{first_half_second_half}" '
                             f'are not same as expected headers: "{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS}"')
        btn_1st_half = self.first_half_second_half.grouping_buttons.items_as_ordered_dict.get(
            vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_1st_half.is_selected(),
                        msg=f'"{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[0]}" button is not selected by default')
        switchers = self.first_half_second_half.grouping_buttons.items_as_ordered_dict
        for name, switcher in switchers.items():
            switcher.click()
            selections_list = self.first_half_second_half.outcomes.items
            self.assertEqual(len(selections_list), 3,
                             msg=f'Actual outcomes length: "{len(selections_list)}" is not same as '
                                 f'Expected length: "3"')
            for selection in range(len(selections_list)):
                self.assertTrue(selections_list[selection].bet_button.is_displayed(),
                                msg=f'selection name: "{selection}" is not displayed')

    def test_006_verify_market_shown_for_1st_half_result(self):
        """
        DESCRIPTION: Verify market shown for '1st Half Result'
        EXPECTED: *   Only market with attribute **name="First-Half Result" **is present
        """
        market = self.first_half_second_half.grouping_buttons.items_as_ordered_dict.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        market.click()
        sleep(1)
        market_name = market.name
        self.assertEqual(market_name, self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[0],
                         msg=f'Actual market name: "{market_name}" is not same as'
                             f'Expected market name: "{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[0]}"')

    def test_007_verify_market_shown_for_2nd_half_result(self):
        """
        DESCRIPTION: Verify market shown for '2nd Half Result'
        EXPECTED: *   Only market with attribute **name="Second-Half Result" **is present
        """
        market = self.first_half_second_half.grouping_buttons.items_as_ordered_dict.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        market.click()
        sleep(1)
        market_name = market.name
        self.assertEqual(market_name, self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[1],
                         msg=f'Actual market name: "{market_name}" is not same as'
                             f'Expected market name: "{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS[1]}"')

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   <Home team> selection is shown first (on the left side) - outcome with attribute **outcomeMeaningMinorCode="H"**
        EXPECTED: *   <Draw> selection is shown second (in the middle) - outcome with attribute **outcomeMeaningMinorCode="D"**
        EXPECTED: *   <Away team> selection is shown third (on the right side) - outcome with attribute **outcomeMeaningMinorCode="A"**
        """
        self.verify_selections_displaying_for_market(market=self.first_half_market)
        self.verify_selections_displaying_for_market(market=self.second_half_market)
