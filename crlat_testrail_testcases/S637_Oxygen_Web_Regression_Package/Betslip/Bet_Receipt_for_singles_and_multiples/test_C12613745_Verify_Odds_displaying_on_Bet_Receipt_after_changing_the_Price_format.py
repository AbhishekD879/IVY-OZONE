import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C12613745_Verify_Odds_displaying_on_Bet_Receipt_after_changing_the_Price_format(Common):
    """
    TR_ID: C12613745
    NAME: Verify Odds displaying on Bet Receipt after changing the Price format
    DESCRIPTION: This test case verifies Odds displaying on Bet Receipt after changing the Price format
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Odds format is Fractional
    PRECONDITIONS: 5. Make bet placement for selection
    PRECONDITIONS: 6. Make sure Bet is placed successfully
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        EXPECTED: * Odds are shown in Fractional format
        """
        pass

    def test_002_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_bet_receipt_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Bet Receipt page
        EXPECTED: Odds are shown in Decimal format
        """
        pass
