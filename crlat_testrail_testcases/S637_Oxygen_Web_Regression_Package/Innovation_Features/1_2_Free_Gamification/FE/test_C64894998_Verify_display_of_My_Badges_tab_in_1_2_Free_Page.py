import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C64894998_Verify_display_of_My_Badges_tab_in_1_2_Free_Page(Common):
    """
    TR_ID: C64894998
    NAME: Verify display of 'My Badges' tab in 1-2 Free Page
    DESCRIPTION: This test case verifies display of 'My Badges' tab in 1-2 Free Page
    PRECONDITIONS: My Badges and Season should be configured in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_application(self):
        """
        DESCRIPTION: Launch Ladbrokes application
        EXPECTED: Ladbrokes application should be launched successfully
        """
        pass

    def test_002_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_003_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        pass

    def test_004_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: User should be able to view 'My Badges' tab
        """
        pass

    def test_005_logout_from_the_ladbrokes_application(self):
        """
        DESCRIPTION: Logout from the Ladbrokes application
        EXPECTED: User should be able to logout successfully
        """
        pass

    def test_006_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        pass

    def test_007_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: 'My Badges' tab should not be displayed to the user
        """
        pass
