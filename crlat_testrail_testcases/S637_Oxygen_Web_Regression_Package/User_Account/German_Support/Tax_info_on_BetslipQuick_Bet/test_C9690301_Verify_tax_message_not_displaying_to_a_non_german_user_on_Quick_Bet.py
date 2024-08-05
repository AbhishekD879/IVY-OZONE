import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C9690301_Verify_tax_message_not_displaying_to_a_non_german_user_on_Quick_Bet(Common):
    """
    TR_ID: C9690301
    NAME: Verify tax message not displaying to a non german user on 'Quick Bet'
    DESCRIPTION: This test case verifies tax message not displaying to a non german user on 'Quick Bet'
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A non-german user is registered
    PRECONDITIONS: 3. Login as non-german user > get the user balance > logout
    PRECONDITIONS: NOTE:
    PRECONDITIONS: countryCode: "DE" attribute could be found in Application -> Local Storage -> OX.USER (this attribute countryCode: "DE" is cleared after Log Out)
    """
    keep_browser_open = True

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002_add_a_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add a selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_003___enter_stake_that_will_exceed_non_german_user_balance__tap_log_in__place_bet__log_in_with_non_german_user(self):
        """
        DESCRIPTION: - Enter 'Stake' that will exceed non german user balance
        DESCRIPTION: - Tap 'Log in & Place Bet'
        DESCRIPTION: - Log in with non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        EXPECTED: - 'Quick Bet' stays on with an error: "Please deposit a min of £{amount_needed} to continue placing your bet"
        EXPECTED: - Tax message is not displayed
        """
        pass

    def test_004_re_enter_stake_that_is_covered_by_users_balance__tap_place_bet(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Place Bet'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Tax message is not displayed
        """
        pass

    def test_005_close_quick_bet__log_out(self):
        """
        DESCRIPTION: Close 'Quick Bet' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_006___add_a_selection_to_quick_bet__verify_availability_of_tax_message_on_quick_bet(self):
        """
        DESCRIPTION: - Add a selection to 'Quick Bet'
        DESCRIPTION: - Verify availability of tax message on 'Quick Bet'
        EXPECTED: Tax message is not displayed
        """
        pass
