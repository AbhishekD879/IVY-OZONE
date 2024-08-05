import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C60997527_Verify_the_CMS_configurations_for_Leaderboard_widget(Common):
    """
    TR_ID: C60997527
    NAME: Verify the CMS configurations for Leaderboard widget
    DESCRIPTION: This test case verifies the CMS configurations for Leaderboard widget
    PRECONDITIONS: User should have admin access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_fiveasideleaderboardwidget_section_in_cms_system_configuration__structure(self):
        """
        DESCRIPTION: Navigate to FiveASideLeaderBoardWidget section in CMS> System Configuration > Structure
        EXPECTED: * User should be navigated successfully
        EXPECTED: * 3 ON/OFF toggles should appear:
        EXPECTED: 1) Home Page
        EXPECTED: 2) Football Page
        EXPECTED: 3) My Bets
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully
        EXPECTED: * User should be able to enable/ disable the toggles
        """
        pass
