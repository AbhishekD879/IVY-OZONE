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
class Test_C9640741_Verify_displaying_of_tax_message_on_Betslip_for_a_German_user(Common):
    """
    TR_ID: C9640741
    NAME: Verify displaying of tax message on 'Betslip' for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Betslip' for a German user
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A user is logged out
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: - Please delete cookies and caches before test steps
    """
    keep_browser_open = True

    def test_001_add_selections_to_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to 'Betslip' > Open 'Betslip'
        EXPECTED: - 'Betslip' is opened
        EXPECTED: - Added selection(s) is(are) displayed within 'Betslip'
        EXPECTED: - Tax message is NOT displayed
        """
        pass

    def test_002_enter_stake_that_exceeds_german_users_balance__tap_login__place_bet(self):
        """
        DESCRIPTION: Enter 'Stake' that exceeds German user's balance > Tap 'Login & Place Bet'
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        EXPECTED: - Bet is not placed
        EXPECTED: - 'Betslip' stays on with an error: "Please deposit a min..."
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_003_re_enter_stake_that_is_covered_by_users_balance__tap_place_bet(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Place Bet'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns' on 'Bet Receipt'
        """
        pass

    def test_004_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'Reuse Selection'
        EXPECTED: 'Betslip' is displayed with selection(s)
        """
        pass

    def test_005_close_betslip__log_out(self):
        """
        DESCRIPTION: Close 'Betslip' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_006_open_betslip__verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: Open Betslip > Verify availability of a tax message
        EXPECTED: Message: "A fee of 5% is applicable on winnings" remains displayed below 'Stake' & 'Est. Returns' on 'Betslip'
        """
        pass
