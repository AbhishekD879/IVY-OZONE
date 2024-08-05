import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C1952947_Banach_Errors_during_bet_placement__Third_parties_assistance(Common):
    """
    TR_ID: C1952947
    NAME: Banach. Errors during bet placement - Third parties assistance
    DESCRIPTION: Test case verifies error flow of adding Banach selection to Quick bet betslip and placing a bet.
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: **Build Your Bet selections are added to Dashboard**
    """
    keep_browser_open = True

    def test_001_verify_error_when_banach_api_responded_with_internal_errors_during_bet_placement_for_the_full_list_of_errors_check_user_story_bma_28361_where_all_error_codes_except_4_are_classified_as_default(self):
        """
        DESCRIPTION: Verify error when Banach api responded with internal errors during bet placement (for the full list of errors check user story BMA-28361, where all error codes except 4 are classified as Default)
        EXPECTED: - In WS client sends message with code 50001 and receives message from quick bet with code 51102 containing "response code":%; SubErrorCode: 'DEFAULT', where % is an error code 0,1,2,3,5,6,7,8
        EXPECTED: - UI error: "There was a problem processing your bet, please try again soon."
        """
        pass

    def test_002_verify_error_when_the_price_has_changed_during_bet_placement(self):
        """
        DESCRIPTION: Verify error when the price has changed during bet placement
        EXPECTED: - In WS client sends message with code 50001 and receives message from quick bet with code 51102 containing "response code":4,  subErrorCode: 'PRICE_CHANGED';
        EXPECTED: - UI error: "Please beware that your selection had a price change"
        """
        pass

    def test_003_verify_error_when_token_expired_during_bet_placement(self):
        """
        DESCRIPTION: Verify error when token expired during bet placement
        EXPECTED: - In WS client sends message with code 50001 and receives message from quick bet with code 51102  containing  error: 'UNAUTHORIZED_ACCESS'
        EXPECTED: - UI error: No message. The request for the new user token has been and bet placed
        """
        pass
