import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
@pytest.mark.high
@vtest
class Test_C884567_Reflection_on_Sport_Event_suspended_unsuspended_for_live_served_events(BaseSportTest):
    """
    TR_ID: C884567
    VOL_ID: C9697604
    NAME: Reflection on Sport Event suspended/unsuspended for live served events
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event.event_id
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event
        DESCRIPTION: Select one <Sport> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_002_suspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_s(self):
        """
        DESCRIPTION: Suspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"S"**
        """
        self.ob_config.change_event_state(event_id=self.eventID)

    def test_003_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: - Message is shown the event has been suspended
        EXPECTED: 'Your event has been suspended' is shown
        EXPECTED: - Stake box & Price are disabled
        EXPECTED: - 'Bet Now' button and 'Add to Betslip' button are disabled
        """
        self.site.quick_bet_panel.wait_for_quick_bet_info_panel()
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        self.assertEqual(actual_message, expected_message, msg='Actual message "%s" does not match expected "%s"' %
                                                               (actual_message, expected_message))
        self.assertFalse(self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=30, expected_result=False), msg='Amount field is not greyed out')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False), msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False), msg='Add to Betslip button is not disabled')

    def test_004_unsuspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_a(self):
        """
        DESCRIPTION: Unsuspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"A"**
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_005_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: Message is removed
        EXPECTED: Stake box & Price are enabled
        EXPECTED: 'Bet Now' button is enabled
        """
        message = self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=False)
        self.assertFalse(message, msg='Notification Message is not removed')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(timeout=10),
                        msg='Add to Betslip button is disabled')
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=5),
                        msg='Amount field is not enabled')
