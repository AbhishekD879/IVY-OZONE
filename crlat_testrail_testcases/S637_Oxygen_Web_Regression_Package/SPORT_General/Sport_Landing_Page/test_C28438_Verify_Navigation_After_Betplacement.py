import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28438_Verify_Navigation_After_Betplacement(Common):
    """
    TR_ID: C28438
    NAME: Verify Navigation After Betplacement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from Sport landing page
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-5233 'Bet Receipt 'Done' Button Navigation Improvement'
    DESCRIPTION: BMA-11096 User is not left on the same page after clicking Done button on slide out Betlsip
    PRECONDITIONS: User should be logged in to place a bet.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap  <Sport>  icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   <Matches> ('Matches'/'Events'/'Races'/'Fights'/'Tournaments') tab is selected by default
        """
        pass

    def test_003_add_selection_to_the_bet_slip___open_bet_slip_slider(self):
        """
        DESCRIPTION: Add selection to the Bet Slip -> open Bet Slip Slider
        EXPECTED: *   Bet Slip Slider open
        EXPECTED: *   Selection is present
        """
        pass

    def test_004_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        pass

    def test_005_tap_go_betting_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Go Betting' button on Bet Receipt page
        EXPECTED: *   Bet Receipt is not shown anymore and betslip slider closes
        EXPECTED: *   User is navigated to last visited page
        """
        pass

    def test_006_tap__back_button_and_select_in_play_tab(self):
        """
        DESCRIPTION: Tap  back button and select 'In-Play' tab
        EXPECTED: **'In-Play'** tab is opened
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: *   Bet Receipt is not shown anymore and betslip slider closes
        EXPECTED: *   User is navigated to last visited page
        """
        pass

    def test_008_tap__back_button_and_select_coupons_tab(self):
        """
        DESCRIPTION: Tap  back button and select 'Coupons' tab
        EXPECTED: **'Coupons'** tab is opened
        """
        pass

    def test_009_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: *   Bet Receipt is not shown anymore and betslip slider closes
        EXPECTED: *   User is navigated to last visited page
        """
        pass
