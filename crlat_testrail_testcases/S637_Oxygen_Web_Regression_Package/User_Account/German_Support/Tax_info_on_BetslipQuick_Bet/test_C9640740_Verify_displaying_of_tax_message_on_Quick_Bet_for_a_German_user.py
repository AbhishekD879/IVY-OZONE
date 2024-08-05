import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C9640740_Verify_displaying_of_tax_message_on_Quick_Bet_for_a_German_user(Common):
    """
    TR_ID: C9640740
    NAME: Verify displaying of tax message on 'Quick Bet' for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Quick Bet' for a German user
    DESCRIPTION: AUTOTESTS : C16706467
    PRECONDITIONS: - A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
    PRECONDITIONS: - A German user is logged out
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: - Please delete cookies and caches before test steps
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add a selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Tax message is NOT displayed
        """
        pass

    def test_002_enter_stake_that_exceeds_german_users_balance__tap_login__place_bet(self):
        """
        DESCRIPTION: Enter 'Stake' that exceeds German user's balance > Tap 'Login & Place Bet'
        EXPECTED: - German user is logged in
        EXPECTED: - Bet is not placed
        EXPECTED: - 'Quick Bet' stays on with an error: "Please deposit a min of £{amount_needed} to continue placing your bet"
        EXPECTED: - Message: "A fee of 5.00% is applicable on winnings" is displayed below 'Total Stake' & 'Potential Returns'
        """
        pass

    def test_003_re_enter_stake_that_is_covered_by_users_balance__tap_place_bet(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Place Bet'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Message: "A fee of 5.00% is applicable on winnings" is displayed below 'Total Stake' & 'Potential Returns' on 'Bet Receipt'
        """
        pass

    def test_004_close_quick_bet__log_out(self):
        """
        DESCRIPTION: Close 'Quick Bet' > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_005___add_a_selection_to_quick_bet__verify_availability_of_tax_message_on_quick_bet(self):
        """
        DESCRIPTION: - Add a selection to 'Quick Bet'
        DESCRIPTION: - Verify availability of tax message on 'Quick Bet'
        EXPECTED: - Message: "A fee of 5.00% is applicable on winnings" remains displayed below 'Stake' & 'Est. Returns' on 'Bet Receipt'
        """
        pass
