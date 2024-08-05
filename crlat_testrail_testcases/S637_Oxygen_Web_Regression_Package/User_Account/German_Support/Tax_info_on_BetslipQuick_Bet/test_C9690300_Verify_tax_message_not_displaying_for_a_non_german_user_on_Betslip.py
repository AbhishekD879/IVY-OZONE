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
class Test_C9690300_Verify_tax_message_not_displaying_for_a_non_german_user_on_Betslip(Common):
    """
    TR_ID: C9690300
    NAME: Verify tax message not displaying for a non-german user on 'Betslip'
    DESCRIPTION: This test case verifies tax message not displaying to a non german user on 'Betslip'
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A non-german user is registered
    PRECONDITIONS: 3. A German user is logged in
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        pass

    def test_002_add_selections_to_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to 'Betslip' > Open Betslip
        EXPECTED: - Added selections are available within 'Betslip'
        EXPECTED: - Message: "A fee of 5.00 % is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        pass

    def test_003_log_in_as_non_german_user(self):
        """
        DESCRIPTION: Log in as non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_004___open_betslip__verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: - Open Betslip
        DESCRIPTION: - Verify availability of a tax message
        EXPECTED: Message: "A fee of 5.00 % is applicable on winnings" is NOT displayed below 'Stake' & 'Est. Returns' on 'Betslip'
        """
        pass

    def test_005_enter_valid_stake__tap_place_bet(self):
        """
        DESCRIPTION: Enter valid 'Stake' > Tap 'Place Bet'
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - No tax message is displayed
        """
        pass

    def test_006_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'Reuse Selection'
        EXPECTED: Betslip' is displayed with selection(s)
        """
        pass

    def test_007_close_betslip__log_out(self):
        """
        DESCRIPTION: Close 'Betslip' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        pass

    def test_008_open_betslip__verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: Open Betslip > Verify availability of a tax message
        EXPECTED: No tax message is displayed
        """
        pass
