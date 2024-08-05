import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.mobile_only
@pytest.mark.liveserv_updates
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C1044372_Verify_Quick_Bet_when_Selection_becomes_undisplayed(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C1044372
    VOL_ID: C9698127
    NAME: Verify Quick Bet when Selection becomes undisplayed
    DESCRIPTION: This test case verifies Quick Bet when Selection becomes undisplayed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    """
    keep_browser_open = True
    expected_message = vec.quickbet.EVENT_NOT_FOUND

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login
        DESCRIPTION: Open created event
        EXPECTED: User is logged in
        EXPECTED: Event details page is opened
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
        self.__class__.selection_ids = event.selection_ids
        self.__class__.eventID = event.event_id
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_001_add_selection_to_quick_bet_enter_stake_select_ew_option(self):
        """
        DESCRIPTION: Add selection to quick bet
        DESCRIPTION: Enter value in 'Stake' field and select 'E/W' option (if available)
        EXPECTED: 'Stake' field is populated with entered value
        EXPECTED: 'E/W' checkbox is selected
        """
        self.add_selection_to_quick_bet()
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount
        quick_bet.each_way_checkbox.click()
        self.assertEqual(quick_bet.amount_form.input.value, str(self.bet_amount),
                         msg=f'Actual amount: "{quick_bet.amount_form.input.value}" '
                             f'does not match expected: "{self.bet_amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_002_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'BET NOW' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is displayed
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')

    def test_003_trigger_situation_when_event_market_selection_becomes_undisplayed_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger situation when selection becomes undisplayed in Openbet TI tool
        EXPECTED: Selection is undisplayed
        EXPECTED: Bet Receipt stays opened with the same data
        """
        self.ob_config.change_selection_state(selection_id=list(list(self.selection_ids.values()))[0], displayed=False, active=True)
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
