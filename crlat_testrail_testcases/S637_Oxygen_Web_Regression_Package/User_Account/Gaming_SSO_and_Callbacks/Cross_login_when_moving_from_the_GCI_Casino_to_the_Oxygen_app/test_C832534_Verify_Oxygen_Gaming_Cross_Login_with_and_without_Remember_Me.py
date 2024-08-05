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
class Test_C832534_Verify_Oxygen_Gaming_Cross_Login_with_and_without_Remember_Me(Common):
    """
    TR_ID: C832534
    NAME: Verify Oxygen-Gaming Cross Login with and without Remember Me
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby with and without Remember Me
    DESCRIPTION: Gaming Lobby links:
    DESCRIPTION: TST2: http://mcasino-tst2.coral.co.uk/
    DESCRIPTION: STG2: http://mcasino-stg1.coral.co.uk/
    DESCRIPTION: PROD: http://mcasino.coral.co.uk/
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_without_remember_me_option(self):
        """
        DESCRIPTION: Log in without remember me option
        EXPECTED: Login is successful
        """
        pass

    def test_003_navigate_to_gaming_from_sports_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to Gaming from Sports Selector Ribbon
        EXPECTED: Gaming Lobby is opened.
        EXPECTED: The user is automatically logged in to Gaming Lobby.
        """
        pass

    def test_004_log_out_from_gaming_lobby(self):
        """
        DESCRIPTION: Log out from Gaming Lobby
        EXPECTED: 
        """
        pass

    def test_005_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened.
        EXPECTED: User is logged out
        """
        pass

    def test_006_log_in_with_remember_me_option_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Log in with remember me option and repeat steps #3-5
        EXPECTED: 
        """
        pass
