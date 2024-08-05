import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C2854684_Verify_Bet_Placement_when_account_is_closed(Common):
    """
    TR_ID: C2854684
    NAME: Verify Bet Placement when account is closed
    DESCRIPTION: This test case verifies Bet Placement when account is closed
    DESCRIPTION: Auto tests:
    DESCRIPTION: Desktop - [C9608470](https://ladbrokescoral.testrail.com/index.php?/cases/view/9608470)
    DESCRIPTION: Mobile - [C9607386](https://ladbrokescoral.testrail.com/index.php?/cases/view/9607386)
    PRECONDITIONS: * Load app and log in with user that has closed his account already (tag **Account_Closed_By_Player=true** is present in 35548 response in WS)
    PRECONDITIONS: * To check request/response open Dev tools -> Network tab -> XHR/WS sorting filter
    """
    keep_browser_open = True

    def test_001_try_to_place_bet_on__sport__race__virtual_sportselection_via_quick_bet(self):
        """
        DESCRIPTION: Try to place bet on
        DESCRIPTION: - Sport
        DESCRIPTION: - Race
        DESCRIPTION: - Virtual Sport
        DESCRIPTION: selection via Quick Bet
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Your account is suspended' error message is displayed
        EXPECTED: * Error with **description=PT_ERR_DISABLE_GAMING** is received in 31012 response from RemoteBetslip MS
        """
        pass

    def test_002_try_to_place_bet__single__multiple__forecaststricasts__tote_poolselection_via_betslip(self):
        """
        DESCRIPTION: Try to place bet
        DESCRIPTION: - Single
        DESCRIPTION: - Multiple
        DESCRIPTION: - Forecasts/Tricasts
        DESCRIPTION: - Tote Pool
        DESCRIPTION: selection via Betslip
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Your account is suspended' error message is displayed
        EXPECTED: * Error with **errorDesc=PT_ERR_DISABLE_GAMING** is received in **placeBet** response from BPP
        """
        pass

    def test_003_try_to_place_bet_on_jackpot_pool(self):
        """
        DESCRIPTION: Try to place bet on Jackpot pool
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'An internal error occurred within the back end system. Contact Coral for more information' error message is displayed
        EXPECTED: * Error with **status=SERVICE_ERROR** is received in **placeBet** response from BPP
        """
        pass

    def test_004_try_to_place_bet_on_lotto(self):
        """
        DESCRIPTION: Try to place bet on Lotto
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Bet error ocurred' error message is displayed
        EXPECTED: * Error with **errorDesc=Playtech Error: Disable Gaming** is received in **placeBet** response from BPP
        """
        pass

    def test_005_try_to_place_bet_on_build_your_bet_selection_via_quick_bet(self):
        """
        DESCRIPTION: Try to place bet on Build Your Bet selection via Quick Bet
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'There was a problem processing your bet, please try again soon'
        EXPECTED: * Error with **betFailureDesc=PT_ERR_DISABLE_GAMING** is received in 51101 response from RemoteBetslip MS
        """
        pass
