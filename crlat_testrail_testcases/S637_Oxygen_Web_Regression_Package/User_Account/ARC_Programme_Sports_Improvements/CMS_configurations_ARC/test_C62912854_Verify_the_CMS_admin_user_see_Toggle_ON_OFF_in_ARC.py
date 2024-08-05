import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62912854_Verify_the_CMS_admin_user_see_Toggle_ON_OFF_in_ARC(Common):
    """
    TR_ID: C62912854
    NAME: Verify the CMS admin user see Toggle ON/OFF  in ARC
    DESCRIPTION: This test case verifies the CMS configurations for
    PRECONDITIONS: User have CMS admin access
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in to CMS
        """
        pass

    def test_002_navigate_to_arc_creation_screen(self):
        """
        DESCRIPTION: Navigate to ARC creation screen
        EXPECTED: ARC creation screen should be available
        """
        pass

    def test_003_a_toggle_switch_should_be_available_for_profile(self):
        """
        DESCRIPTION: A toggle switch should be available for profile
        EXPECTED: User to switch on and off the the Profile
        """
        pass
