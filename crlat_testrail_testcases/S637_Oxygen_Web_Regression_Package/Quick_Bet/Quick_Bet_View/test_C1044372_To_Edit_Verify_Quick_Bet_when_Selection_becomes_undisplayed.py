import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C1044372_To_Edit_Verify_Quick_Bet_when_Selection_becomes_undisplayed(Common):
    """
    TR_ID: C1044372
    NAME: [To Edit] Verify Quick Bet when Selection becomes undisplayed
    DESCRIPTION: This test case verifies Quick Bet when Selection becomes undisplayed
    DESCRIPTION: [To Edit]:
    DESCRIPTION: Step3 - it is impossible to tap selection to add it to QB once it was undisplayed
    DESCRIPTION: Step 11 - there is no "Reuse Selection' button, it was removed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * To check request/response open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_sport__race_landing_page(self):
        """
        DESCRIPTION: Go <Sport> / <Race> landing page
        EXPECTED: <Sport> / <Race> landing page is opened
        """
        pass

    def test_003_trigger_situation_when_event_market_selection_becomes_undisplayed_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger situation when event/ market/ selection becomes undisplayed in Openbet TI tool
        EXPECTED: * Event/ market/ selection is undispalyed
        EXPECTED: * Event/ market/ selection is still displayed on FE
        """
        pass

    def test_004_tap_sportrace_selection_that_belongs_to_eventmarket_from_step_3(self):
        """
        DESCRIPTION: Tap <Sport>/<Race> selection that belongs to event/market from step #3
        EXPECTED: * 30001 request is sent to Remote Betslip micro service with Openbet outcome ID in WS
        EXPECTED: * The next error is received in 30002  response in WS:
        EXPECTED: "ERROR",{"code":"EVENT_NOT_FOUND","description":"Error reading outcome data. Data not found. OutcomeIds - [Openbet outcome ID]"}}
        """
        pass

    def test_005_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * 'Selection is no longer available' message is displayed on grey background
        EXPECTED: * 'ADD TO BETSLIP' and 'PLACE BET' buttons are disabled
        """
        pass

    def test_006_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Quick Bet is not displayed anymore
        """
        pass

    def test_007_add_any_sport__race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add any <Sport> / <Race> selection to Quick bet
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick bet is displayed at the bottom of the page
        """
        pass

    def test_008_enter_value_in_stake_field_and_select_ew_option_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and select 'E/W' option (if available)
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_009_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'BET NOW' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_010_trigger_situation_when_event_market_selection_becomes_undisplayed_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger situation when event/ market/ selection becomes undisplayed in Openbet TI tool
        EXPECTED: * Event/ market/ selection is undispalyed
        EXPECTED: * Bet Receipt stays opened with the same data
        """
        pass

    def test_011_tap_reuse_selection_button(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION' button
        EXPECTED: * Quick bet is opened again
        EXPECTED: * 'Selection is no longer available' message is displayed on grey background
        EXPECTED: * 'ADD TO BETSLIP' and 'PLACE BET' buttons are disabled
        """
        pass

    def test_012_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step #6
        EXPECTED: 
        """
        pass
