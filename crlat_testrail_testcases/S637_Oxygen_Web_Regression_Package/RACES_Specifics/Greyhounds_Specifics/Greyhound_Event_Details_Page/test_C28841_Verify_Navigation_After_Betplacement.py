import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28841_Verify_Navigation_After_Betplacement(Common):
    """
    TR_ID: C28841
    NAME: Verify Navigation After Betplacement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from Greyhound event details page
    DESCRIPTION: **Jira ticket: BMA-5233, BMA-11096**
    PRECONDITIONS: User should be  logged in to place a bet.
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: *   'Greyhounds'  landing page is opened
        EXPECTED: *   'Today' tab is opened by default
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_add_selection_to_the_bet_slip__open_bet_slip_slider(self):
        """
        DESCRIPTION: Add selection to the Bet Slip ->open Bet Slip Slider
        EXPECTED: *   Bet Slip Slider opens
        EXPECTED: *   Selection is present
        """
        pass

    def test_005_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        pass

    def test_006_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on same page
        """
        pass

    def test_007_tap_back_button_and_select_tomorrow_tab(self):
        """
        DESCRIPTION: Tap back button and select 'Tomorrow' tab
        EXPECTED: 'Tomorrow' tab is opened
        """
        pass

    def test_008_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on same page ( 'Tomorrow' tab is selected)
        """
        pass

    def test_009_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        """
        pass

    def test_010_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps 2-6
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on same page
        """
        pass
