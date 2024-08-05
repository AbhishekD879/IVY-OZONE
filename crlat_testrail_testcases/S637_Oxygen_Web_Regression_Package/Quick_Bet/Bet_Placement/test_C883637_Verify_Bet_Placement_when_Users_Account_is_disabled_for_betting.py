import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C883637_Verify_Bet_Placement_when_Users_Account_is_disabled_for_betting(Common):
    """
    TR_ID: C883637
    NAME: Verify Bet Placement when Users Account is disabled for betting
    DESCRIPTION: This test case verifies Bet Placement within Quick Bet when Account is disabled for betting
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings (Quick Bet functionality is available for Mobile ONLY)
    PRECONDITIONS: * in Openbet Ti tool Disable betting for <Sport> for test user [How to disable user's account for bet placement][1]
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Disable+Betting+for+a+User
    """
    keep_browser_open = True

    def test_001_tap_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: * Quick Bet is displayed at the bottom of the page with a message "Sorry, you are not allowed to place bet on this selection."
        EXPECTED: * Add to betslip and PLace bet buttons are disabled
        """
        pass

    def test_002_tap_x_button_on_quick_bet(self):
        """
        DESCRIPTION: Tap 'X' button on Quick Bet
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_003_add_another_selection_from_sport_which_is_not_disabled_for_betting_and_try_to_place_a_bet(self):
        """
        DESCRIPTION: Add another selection from <Sport> which is not disabled for betting and try to place a bet
        EXPECTED: * Bet is placed successfully
        """
        pass

    def test_004_enable_sport_from_step_1_for_betting_openbet_ti_tool(self):
        """
        DESCRIPTION: Enable <Sport> from step #1 for betting Openbet Ti tool
        EXPECTED: <Sport> is enabled for betting
        """
        pass

    def test_005_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps #1-2
        EXPECTED: * Bet is placed successfully
        """
        pass
