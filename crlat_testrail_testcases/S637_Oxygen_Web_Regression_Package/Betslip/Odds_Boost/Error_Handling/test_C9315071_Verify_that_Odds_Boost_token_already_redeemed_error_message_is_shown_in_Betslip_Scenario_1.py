import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C9315071_Verify_that_Odds_Boost_token_already_redeemed_error_message_is_shown_in_Betslip_Scenario_1(Common):
    """
    TR_ID: C9315071
    NAME: Verify that 'Odds Boost token already redeemed' error message is shown in Betslip (Scenario 1)
    DESCRIPTION: This test case verifies that 'Odds Boost token already redeemed' error message is shown in Betslip
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: Load application and login with User1 in two windows
    PRECONDITIONS: User1 has only one Odds Boost token (for ANY)
    """
    keep_browser_open = True

    def test_001_add_different_selection_to_the_betslip_in_two_windowsverify_that_odds_boost_button_is_shown_in_both_windows(self):
        """
        DESCRIPTION: Add different selection to the Betslip in two windows
        DESCRIPTION: Verify that odds boost button is shown in both windows
        EXPECTED: 'BOOST' button is shown in both windows
        """
        pass

    def test_002_add_stake_and_tap_boost_button_in_both_windowstap_place_bet_button_in_one_windowverify_that_boosted_bet_is_placed(self):
        """
        DESCRIPTION: Add Stake and tap 'BOOST' button in both windows
        DESCRIPTION: Tap 'Place Bet' button in one window
        DESCRIPTION: Verify that boosted bet is placed
        EXPECTED: Bet receipt with boost title and boosted odds is shown
        """
        pass

    def test_003_tap_boost_button_in_the_second_windowtap_place_bet_buttonverify_that_error_message_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button in the second window
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that error message is shown
        EXPECTED: ''Your Odds Boost has been expired/redeemed.'' error message is shown
        EXPECTED: (error code: TCH_OBW_ERR_5012)
        """
        pass
