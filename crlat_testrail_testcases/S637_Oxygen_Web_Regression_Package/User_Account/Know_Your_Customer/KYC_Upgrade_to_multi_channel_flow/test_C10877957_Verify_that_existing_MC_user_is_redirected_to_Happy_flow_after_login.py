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
class Test_C10877957_Verify_that_existing_MC_user_is_redirected_to_Happy_flow_after_login(Common):
    """
    TR_ID: C10877957
    NAME: Verify that existing MC user is redirected to Happy flow after login
    DESCRIPTION: This test case verifies that existent MC user who has 'Age verification result' =  "Under Review" in IMS is redirected to happy flow after login
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. MC User is registered
    PRECONDITIONS: 3. In IMS: 'Age verification result' is set to 'Under Review' for a user
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_log_in_to_an_app(self):
        """
        DESCRIPTION: Log in to an app
        EXPECTED: - User is logged into an app
        EXPECTED: - After login pop-ups are displayed (if any)
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
        EXPECTED: Login pop-up appears
        """
        pass

    def test_004_enter_valid_username__password__tap_login(self):
        """
        DESCRIPTION: Enter valid 'Username' & 'Password' > Tap 'Login'
        EXPECTED: - User is logged into an app
        EXPECTED: - Bet is placed (if user has sufficient balance)
        EXPECTED: OR
        EXPECTED: - 'Quick Deposit' is shown (if user has insufficient balance)
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
        EXPECTED: - 'Quick Deposit' is shown (if user has insufficient balance)
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass
