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
class Test_C2461989_Banach_Verify_bet_placement_error_when_stake_is_too_high(Common):
    """
    TR_ID: C2461989
    NAME: Banach. Verify bet placement error when stake is too high
    DESCRIPTION: Test case verifies error for too high stake during bet placement.
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: **Banach selections are added to dashboard**
    """
    keep_browser_open = True

    def test_001_tap_on_the_place_bet_button_with_odds_and_enter_very_high_stake_eg_2000(self):
        """
        DESCRIPTION: Tap on the place bet button with odds and enter very high stake (e.g. $2000)
        EXPECTED: - Selections are added (in WS client sends message with code 50001 and receives message from quick bet with code 51001)
        EXPECTED: - While placing a bet in WS client sends message with code 50011 and receives message from quick bet with code 51102 containing subErrorCode:"STAKE_HIGH" and description "The maximum stake for this bet is %"
        EXPECTED: - UI error message **Sorry unable to place bet. The maximums stake for this bet is %** appears
        EXPECTED: where % is amount coming from Open Bet
        """
        pass

    def test_002_correct_the_stake_to_match_the_max_stake_value_from_response_and_place_a_bet(self):
        """
        DESCRIPTION: Correct the stake to match the max stake value from response and place a bet
        EXPECTED: - Bet should be placed
        EXPECTED: - User balance is updated
        """
        pass
