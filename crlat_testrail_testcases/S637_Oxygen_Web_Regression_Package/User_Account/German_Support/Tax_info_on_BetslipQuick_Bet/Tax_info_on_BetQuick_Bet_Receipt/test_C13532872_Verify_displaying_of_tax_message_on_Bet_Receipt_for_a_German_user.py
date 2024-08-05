import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C13532872_Verify_displaying_of_tax_message_on_Bet_Receipt_for_a_German_user(Common):
    """
    TR_ID: C13532872
    NAME: Verify displaying of tax message on Bet Receipt for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on Bet Receipt for a German user
    DESCRIPTION: AUTOTEST
    DESCRIPTION: Mobile [C16673866]
    DESCRIPTION: Desktop [C16673879]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in with German user (testtest3/qwerty123)
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for single selection
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user). Verify in Application > Local Storage > OX.countryCode. For german user 'DE' value is set.
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_002_verify_availability_of_a_tax_message_on_bet_receipt(self):
        """
        DESCRIPTION: Verify availability of a tax message on Bet Receipt
        EXPECTED: Message: "A fee of 5% is applicable on winnings" is displayed below 'Total Stake' & 'Potential Returns' fields on Bet Receipt
        """
        pass
