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
class Test_C832533_Verify_Oxygen_Gaming_Cross_Login(Common):
    """
    TR_ID: C832533
    NAME: Verify Oxygen-Gaming Cross Login
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby
    DESCRIPTION: Gaming Lobby links:
    DESCRIPTION: TST2: http://mcasino-tst2.coral.co.uk/
    DESCRIPTION: STG2: http://mcasino-stg1.coral.co.uk/
    DESCRIPTION: PROD: http://mcasino.coral.co.uk/
    DESCRIPTION: AUTOTEST: [C9698691]
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
        DESCRIPTION: Log in (without remember me option)
        EXPECTED: Login is successful
        """
        pass

    def test_003_select_gaming_from_sports_selector_ribbon(self):
        """
        DESCRIPTION: Select Gaming from Sports Selector Ribbon
        EXPECTED: * Gaming Lobby is opened .
        EXPECTED: * User is automatically logged in to Gaming Lobby.
        """
        pass

    def test_004_navigate_back_to_oxygen_using_sports_icon_from_gaming_footer(self):
        """
        DESCRIPTION: Navigate back to Oxygen using Sports icon from Gaming Footer
        EXPECTED: *Oxygen app is loaded
        EXPECTED: * User is still logged in
        """
        pass

    def test_005_tap_gaming_icon_from_footer(self):
        """
        DESCRIPTION: Tap Gaming icon from Footer
        EXPECTED: * Gaming Lobby is opened
        EXPECTED: * User is logged in to Gaming Lobby
        """
        pass

    def test_006_log_out_from_gaming_lobby(self):
        """
        DESCRIPTION: Log out from Gaming Lobby
        EXPECTED: 
        """
        pass

    def test_007_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: * Homepage is opened.
        EXPECTED: * User is logged out.
        """
        pass
