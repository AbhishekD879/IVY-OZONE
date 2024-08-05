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
class Test_C36377806_Verify_Gaming_Cross_Login(Common):
    """
    TR_ID: C36377806
    NAME: Verify Gaming Cross Login
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby
    DESCRIPTION: The following options should be checked in CMS:
    DESCRIPTION: Make sure all below items are equal to "GAMING_URL" from buildInfo.json:
    DESCRIPTION: systemConfiguration>GamingEnabled>gamingURL
    DESCRIPTION: Menus>Footer Menus>Gaming>Target Uri
    DESCRIPTION: Sports Pages>Sport Categories>Gaming>General Sport Configuration>Target Uri
    DESCRIPTION: System config > GamingEnabled
    DESCRIPTION: System config > NativeGaming
    DESCRIPTION: ![](index.php?/attachments/get/118214372)
    DESCRIPTION: ![](index.php?/attachments/get/118214368)
    DESCRIPTION: ![](index.php?/attachments/get/118214369)
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

    def test_004_navigate_back_to_oxygen_using_sports_icon_from_gaming_footer_mobiletablet__sports_from_sports_selector_ribbon_desktop(self):
        """
        DESCRIPTION: Navigate back to Oxygen using Sports icon from Gaming Footer (Mobile/Tablet) / Sports from Sports Selector Ribbon (Desktop)
        EXPECTED: * Oxygen app is loaded
        EXPECTED: * User is still logged in
        """
        pass

    def test_005_tap_gaming_icon_from_footer_menu_mobiletablet__from_sports_selector_ribbon_desktop(self):
        """
        DESCRIPTION: Tap Gaming icon from Footer menu (Mobile/Tablet) / from Sports Selector Ribbon (Desktop)
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
