import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event creation/suspension invlove
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28536_Half_Time_Full_Time_market_section_in_case_suspensions_occurrence(BaseSportTest):
    """
    TR_ID: C28536
    NAME: Half Time/Full Time market section in case suspensions occurrence
    DESCRIPTION: This test case verifies Half Time/Full Time market section behavior on suspensions occurrence
    DESCRIPTION: **Jira ticket:** BMA-3863
    DESCRIPTION: [TO EDIT] Looks like the following is not up to date relating to this market
    DESCRIPTION: - market sections
    DESCRIPTION: - 'Show All' section
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def verify_suspended_event_market_selection(self, verification_type='event'):
        """
           This method will verify suspended event/market & selection, button name and button disable functionality
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')

        if self.brand == 'ladbrokes':
            self.__class__.expected_market_name = 'Half time/ Full Time Result Market'
        else:
            self.__class__.expected_market_name = 'HALF TIME/ FULL TIME RESULT MARKET' if self.device_type == 'mobile' else 'Half Time/ Full Time Result Market'

        half_time_full_time = markets_list.get(self.expected_market_name)
        self.assertTrue(half_time_full_time,
                        msg=f'"{self.expected_market_name}" section is not found in "{markets_list.keys()}"')

        outcomes = markets_list[self.expected_market_name].outcomes.items_as_ordered_dict

        if verification_type in ['event', 'market']:
            for outcome_name, outcome in outcomes.items():
                self.assertEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                                 msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=5, poll_interval=1),
                                 msg='Bet button is not disabled, but was expected to be disabled')
                try:
                    outcome.bet_button.click()
                    self.assertFalse(outcome.bet_button.is_enabled(expected_result=True, timeout=5, poll_interval=1),
                                     msg='Bet button is not disabled, but was expected to be disabled')
                except Exception:
                    continue
        else:
            for outcome_name, outcome in outcomes.items():
                if outcome_name == self.selection_name:
                    self.assertEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                                     msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
                    self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=5, poll_interval=1),
                                     msg='Bet button is not disabled, but was expected to be disabled')
                else:
                    self.assertNotEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                                        msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text"')
                    self.assertTrue(outcome.bet_button.is_enabled(expected_result=True, timeout=5, poll_interval=1),
                                    msg='Bet button is disabled, but was expected to be enabled')

    def navigate_to_football_edp(self, event_id):
        """
        This method used to navigate to football edp page
        """
        self.navigate_to_edp(event_id, timeout=20)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails', timeout=20)

        result = wait_for_result(
            lambda: self.site.contents.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Event details page is not loaded completely')

    def test_000_pre_conditions(self):
        """
            PRECONDITIONS: Create a mutliple events
        """
        self.__class__.market_name = 'Half-Time/Full-Time'

        markets_params = [('half_time_full_time', {'cashout': True})]
        event_1 = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID_1 = event_1.event_id

        event_2 = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID_2 = event_2.event_id

        for market in event_2.ss_response['event']['children']:
            if market['market']['templateMarketName'] == self.market_name:
                self.__class__.marketid = market['market']['id']
                break

        event_3 = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID_3 = event_3.event_id

        for market in event_3.ss_response['event']['children']:
            if market['market']['templateMarketName'] == self.market_name:
                self.__class__.selection_id = market['market']['children'][0]['outcome']['id']
                self.__class__.selection_name = market['market']['children'][0]['outcome']['name']
                break

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Football>' icon on the Sports Menu Ribbon
        EXPECTED: *   <Football> Landing Page is opened
        EXPECTED: *   'Leagues & Competitions' sorting type is selected by default
        """
        self.site.open_sport(name='FOOTBALL', timeout=5)
        self.site.wait_content_state('FOOTBALL')

    def test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(self):
        """
        DESCRIPTION: Go to Football Event Details page of suspended event
        DESCRIPTION: (with attribute **eventStatusCode="S")**
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   'Main Markets' collection is selected by default
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=False)
        self.navigate_to_football_edp(self.eventID_1)

    def test_004_verify_half_timefull_time_marketof_suspended_event(self):
        """
        DESCRIPTION: Verify Half Time/Full Time market of suspended event
        EXPECTED: *   [TO EDIT] Half Time/Full Time market sections are all greyed out
        EXPECTED: *   [TO EDIT] Disabled odds/price buttons are displayed on outcomes on 'Show All' section
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        self.verify_suspended_event_market_selection(verification_type='event')

    def test_005_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED:
        """
        self.ob_config.change_market_state(self.eventID_2, self.marketid, displayed=True)
        self.navigate_to_football_edp(self.eventID_2)

    def test_006_verify_half_timefull_time_market_section_in_case_of_suspension(self):
        """
        DESCRIPTION: Verify 'Half Time/Full Time market section in case of suspension
        EXPECTED: *   If** **'Half Time/Full Time market** **are with attribute **marketStatusCode="S",  **Market is disabled and it's imposible to make a bet
        EXPECTED: *   [TO EDIT] Half Time/Full Time market sections are all greyed out
        EXPECTED: *   [TO EDIT] Disabled odds/price buttons are displayed on 'Show All' section
        """
        self.verify_suspended_event_market_selection(verification_type='market')

    def test_007_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.navigate_to_football_edp(self.eventID_3)

    def test_008_verify_outcome_of_half_timefull_time_market_section_with_attribute_outcomestatuscodes(self):
        """
        DESCRIPTION: Verify outcome of Half Time/Full Time market section with attribute **outcomeStatusCode="S" **
        EXPECTED: *   Selection odds/price button is disabled
        EXPECTED: *   It's impossible to place a bet for this selection
        EXPECTED: *   The rest event's selections are enabled with prices
        """
        self.verify_suspended_event_market_selection(verification_type='selection')
