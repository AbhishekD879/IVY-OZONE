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
class Test_C9315072_Verify_that_Odds_Boost_token_already_redeemed_error_message_is_shown_in_Bet_slip_Scenario_2(Common):
    """
    TR_ID: C9315072
    NAME: Verify that 'Odds Boost token already redeemed' error message is shown in Bet slip (Scenario 2)
    DESCRIPTION: This test case verifies that 'Odds Boost token already redeemed' error message is shown in Betslip
    PRECONDITIONS: Load application and login with User1
    PRECONDITIONS: There is odds boost token for ANY (Token1)
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: Add Token1 with Expiration Date = Now+5min for User1
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslipadd_stake_and_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Add selection to Betslip
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: 'BOOSTED' button is shown
        EXPECTED: Boosted odds is shown
        EXPECTED: Original odd is shown as crossed out
        """
        pass

    def test_002_wait_for_more_than_5_min_so_odds_boost_token_will_be_expiredtap_place_bet_buttonverify_that_error_message_is_shown(self):
        """
        DESCRIPTION: Wait for more than 5 min, so odds boost token will be expired
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that error message is shown
        EXPECTED: ''Your Odds Boost has been expired/redeemed.'' error message is shown
        EXPECTED: (error code: TCH_OBW_ERR_5012
        """
        pass
