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
class Test_C9315073_Verify_that_Odds_Boost_token_already_redeemed_error_message_is_shown_in_Bet_slip_Scenario_3(Common):
    """
    TR_ID: C9315073
    NAME: Verify that 'Odds Boost token already redeemed' error message is shown in Bet slip (Scenario 3)
    DESCRIPTION: This test case verifies that 'Odds Boost token already redeemed' error message is shown in Betslip
    PRECONDITIONS: Load application and login with User1 in two windows
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: There is odds boost token for ANY (Token1)
    PRECONDITIONS: Add Token1 for User1 in https://backoffice-tst2.coral.co.uk/office >Adhoc Tokens
    """
    keep_browser_open = True

    def test_001_add_selection_to_betadd_stake_and_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Add selection to Betідшз
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: 'BOOSTED' button is shown
        EXPECTED: Boosted odds is shown
        EXPECTED: Original odd is shown as crossed out
        """
        pass

    def test_002_navigate_to_httpsbackoffice_tst2coralcoukoffice__offerschange_token1_set_bet_type__double(self):
        """
        DESCRIPTION: Navigate to https://backoffice-tst2.coral.co.uk/office > Offers
        DESCRIPTION: Change Token1: Set Bet Type = DOUBLE
        EXPECTED: Bet Type for Token1 is changed from ANY to DOUBLE
        """
        pass

    def test_003_navigate_back_to_applicationtap_place_bet_buttonverify_that_error_message_is_shown(self):
        """
        DESCRIPTION: Navigate back to application
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that error message is shown
        EXPECTED: ''Your Odds Boost has been expired/redeemed.'' error message is shown
        EXPECTED: (error code: TCH_OBW_ERR_5012)
        """
        pass
