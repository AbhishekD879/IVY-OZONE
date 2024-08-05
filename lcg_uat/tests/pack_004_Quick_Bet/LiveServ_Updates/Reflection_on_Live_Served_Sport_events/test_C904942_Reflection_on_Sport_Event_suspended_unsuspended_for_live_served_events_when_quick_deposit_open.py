import voltron.environments.constants as vec
from time import sleep

import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.quick_deposit
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C904942_Reflection_on_Sport_Event_suspended_unsuspended_for_live_served_events_when_quick_deposit_open(BaseSportTest):
    """
    TR_ID: C904942
    VOL_ID: C9697604
    NAME: Reflection on Sport Event suspended/unsuspended for live served events when quick deposit open
    """
    keep_browser_open = True
    addition = 5

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event.event_id

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event and login
        DESCRIPTION: Select one <Sport> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance
        self.add_selection_from_event_details_to_quick_bet()

    def test_002_enter_amount_greater_than_balance(self):
        """
        DESCRIPTION: Enter amount greater than balance
        EXPECTED: 'Funds needed' message is shown
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.addition + self.user_balance

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition)
        if self.brand != 'ladbrokes':
            message = self.site.quick_bet_panel.info_panels_text[0]
        else:
            message = self.site.quick_bet_panel.deposit_info_message.text
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def test_003_suspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_s(self):
        """
        DESCRIPTION: Suspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"S"**
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        sleep(1)

        self.ob_config.change_event_state(event_id=self.eventID)

    def test_004_check_update_in_quick_deposit(self):
        """
        DESCRIPTION: Check update in Quick deposit
        EXPECTED: 'Your event has been suspended' is shown
        EXPECTED: - Stake box & Price are disabled
        EXPECTED: - 'Make Quick Deposit' button and 'Add to Betslip' button are disabled
        """
        if self.brand != 'ladbrokes':
            message_change = self.site.quick_bet_panel.wait_for_message_to_change(
                previous_message=vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition), timeout=15)
            self.assertTrue(message_change, msg='Old error message is not disappear')

        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

        self.assertFalse(self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=5, expected_result=False),
                         msg='Amount field is not greyed out')
        self.assertFalse(self.site.quick_bet_panel.make_quick_deposit_button.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_005_unsuspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_a(self):
        """
        DESCRIPTION: Unsuspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"A"**
        DESCRIPTION: Message that event has been suspended is removed
        EXPECTED: - * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: - Stake box & Price are enabled
        EXPECTED: - 'Bet Now' button and 'Add to Betslip' button are enabled
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        sleep(1)
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        message_change = self.site.quick_bet_panel.wait_for_message_to_change(
            previous_message=vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended)
        self.assertTrue(message_change, msg='Message that event has been suspended is not removed')

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition)
        if self.brand != 'ladbrokes':
            message = self.site.quick_bet_panel.info_panels_text[0]
        else:
            message = self.site.quick_bet_panel.deposit_info_message.text
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

        self.assertTrue(self.site.quick_bet_panel.make_quick_deposit_button.is_enabled(),
                        msg='LOGIN & PLACE BET button is not disabled')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='Add to Betslip button is disabled')
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=5),
                        msg='Amount field is not enabled')
