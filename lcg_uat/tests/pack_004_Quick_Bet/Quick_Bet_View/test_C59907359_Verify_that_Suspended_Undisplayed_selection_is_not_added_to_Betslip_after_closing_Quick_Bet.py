import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot suspend/undisplay event in prod
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@vtest
class Test_C59907359_Verify_that_Suspended_Undisplayed_selection_is_not_added_to_Betslip_after_closing_Quick_Bet(BaseBetSlipTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C59907359
    NAME: Verify that Suspended/Undisplayed selection is not added to Betslip after closing Quick Bet
    DESCRIPTION: BMA-54870 Quickbet - Add selection if customer taps X
    DESCRIPTION: This Test case verifies that, after customer taps 'X' Button on Quick bet, Quick bet is closed and Selection is not added to Betslip, if selection is already suspended or undisplayed
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in/logged out
    PRECONDITIONS: (Test for logged in and logged out user)
    """
    keep_browser_open = True

    def close_quickbet_verify_betslip(self):
        quick_bet = self.site.quick_bet_panel
        quick_bet.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=0)
        self.site.open_betslip()
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.site.close_betslip()

    def suspend_undisplay_event(self, event_id=None, active=False, displayed=False):
        self.ob_config.change_event_state(event_id=event_id, active=active, displayed=displayed)
        sleep(3)
        self.verify_betslip_counter_change(expected_value=0)
        self.site.open_betslip()
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.site.close_betslip()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params_1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID_1 = event_params_1.event_id
        event_1 = event_params_1.ss_response
        self.__class__.selection_name = event_params_1.team1
        self.__class__.selection_name2 = event_params_1.team2

        market_name = next((market.get('market').get('name') for market in event_1['event']['children']
                            if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        self._logger.info(f'*** Using event "{self.eventID}" with market "{market_name}"')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page. Selection is added Quick Bet
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_002_in_open_bet_find_the_event_added_to_quick_bet_and_suspend_eventmarketselection(self):
        """
        DESCRIPTION: In Open Bet, find the event, added to Quick bet, and suspend Event/Market/Selection
        EXPECTED: Event suspension is reflected on Quick Bet.
        EXPECTED: Message 'Your event has been suspended' is shown. Buttons 'Place bet', 'Add to Betslip' are disabled.
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, active=False, displayed=True)
        sleep(3)
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        self.device.driver.implicitly_wait(0)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_003_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is NOT added to Betslip
        """
        self.close_quickbet_verify_betslip()

    def test_004_in_openbet_make_active_eventmarketselection(self):
        """
        DESCRIPTION: In OpenBet make active Event/Market/Selection
        EXPECTED: * Selection is not highlighted
        EXPECTED: * Betslip counter has not changed
        EXPECTED: * Betslip is empty
        """
        self.suspend_undisplay_event(event_id=self.eventID_1, active=True, displayed=True)

    def test_005_add_another_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add another Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page. Selection is added Quick Bet
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name2)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_006_in_open_bet_find_the_event_added_to_quick_bet_and_undisplay_eventmarketselection(self):
        """
        DESCRIPTION: In Open Bet, find the event, added to Quick bet, and undisplay Event/Market/Selection
        EXPECTED: Event undisplaying is reflected on Quick Bet.
        EXPECTED: Message 'Your event has been suspended' is shown. Buttons 'Place bet', 'Add to Betslip' are disabled.
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=False, active=True)
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        self.device.driver.implicitly_wait(0)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_007_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is NOT added to Betslip
        """
        self.close_quickbet_verify_betslip()

    def test_008_in_openbet_display_eventmarketselection(self):
        """
        DESCRIPTION: In OpenBet display Event/Market/Selection
        EXPECTED: * Selection is not highlighted
        EXPECTED: * Betslip counter has not changed
        EXPECTED: * Betslip is empty
        """
        self.suspend_undisplay_event(event_id=self.eventID_1, displayed=True, active=True)
        self.navigate_to_page("Homepage")
        self.site.login()
        self.test_001_add_selection_to_quick_bet()
        self.test_002_in_open_bet_find_the_event_added_to_quick_bet_and_suspend_eventmarketselection()
        self.test_003_tap_on_x_button()
        self.test_004_in_openbet_make_active_eventmarketselection()
        self.test_005_add_another_selection_to_quick_bet()
        self.test_006_in_open_bet_find_the_event_added_to_quick_bet_and_undisplay_eventmarketselection()
        self.test_007_tap_on_x_button()
        self.suspend_undisplay_event(event_id=self.eventID_1, displayed=True, active=True)
