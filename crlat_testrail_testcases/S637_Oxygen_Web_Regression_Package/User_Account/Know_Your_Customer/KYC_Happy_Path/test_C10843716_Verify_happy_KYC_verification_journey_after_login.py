import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C10843716_Verify_happy_KYC_verification_journey_after_login(Common):
    """
    TR_ID: C10843716
    NAME: Verify happy KYC verification journey after login
    DESCRIPTION: This test case verifies happy KYC verification journey after a user is logged in
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. Oxygen app is loaded
    PRECONDITIONS: 3. User is registered
    PRECONDITIONS: 4. In IMS: 'Age verification result' is set to 'Under Review' for a user
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_log_into_an_app(self):
        """
        DESCRIPTION: Log into an app
        EXPECTED: - User is logged into an app
        EXPECTED: - After login pop ups are displayed (if any)
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass

    def test_002_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_003_mobile__add_selection_to_quick_bet__enter_stake__tap_login__place_bet(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: - Add selection to 'Quick Bet'
        DESCRIPTION: - Enter Stake
        DESCRIPTION: - Tap 'Login & Place Bet'
        EXPECTED: Login pop up appears
        """
        pass

    def test_004_enter_valid_username__password__tap_login(self):
        """
        DESCRIPTION: Enter valid 'Username' & 'Password' > Tap 'Login'
        EXPECTED: - User is logged into an app
        EXPECTED: - Bet is placed (if user has sufficient balance)
        EXPECTED: OR
        EXPECTED: - 'Quick Deposit' is shown (if user has insufficient balance and cc added)
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_006___add_selection_to_betslip__open_betslip__enter_stake__tap_login__place_bet(self):
        """
        DESCRIPTION: - Add selection to 'Betslip'
        DESCRIPTION: - Open 'Betslip'
        DESCRIPTION: - Enter Stake
        DESCRIPTION: - Tap 'Login & Place Bet'
        EXPECTED: Login pop up appears
        """
        pass

    def test_007_enter_valid_username__password__tap_login(self):
        """
        DESCRIPTION: Enter valid 'Username' & 'Password' > Tap 'Login'
        EXPECTED: - User is logged into an app
        EXPECTED: - Bet is placed (if user has sufficient balance)
        EXPECTED: OR
        EXPECTED: - 'Quick Deposit' is shown (if user has insufficient balance and cc added)
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass
