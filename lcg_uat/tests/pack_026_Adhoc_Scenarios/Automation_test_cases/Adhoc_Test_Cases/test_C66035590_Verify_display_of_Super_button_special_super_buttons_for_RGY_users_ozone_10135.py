import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035590_Verify_display_of_Super_button_special_super_buttons_for_RGY_users_ozone_10135(Common):
    """
    TR_ID: C66035590
    NAME: Verify display of Super button & special super buttons for RGY users ozone 10135
    DESCRIPTION: This testcase verifies the display of Super button & special super buttons for RGY users
    PRECONDITIONS: 1. Login to CMS as admin user.
    PRECONDITIONS: 2. Super Button & Special super button is created in CMS.
    PRECONDITIONS: 4. Above created QL & SB are added to Bonus suppression List
    PRECONDITIONS: Navigate to Bonus Suppression-->Modules. Give a name for the module. Select above SB & special super button from the alias module names & save.
    PRECONDITIONS: 5. Navigate to configuration and add above module there.
    PRECONDITIONS: Note :
    PRECONDITIONS: Super Button creation in CMS :
    PRECONDITIONS: Navigate to Home page-->Super Button. Click on Create Super Button. Check Active check box, Enter details & Click on Save Button.
    PRECONDITIONS: Super Button creation in CMS :
    PRECONDITIONS: Navigate to Home page-->Special Super Button. Click on Create Special Super Button. Enter details & Click on Save Button.
    """
    keep_browser_open = True

    def test_000_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Application is loaded.
        """
        pass

    def test_000_login_with_a_valid_user(self):
        """
        DESCRIPTION: Login with a valid user.
        EXPECTED: 1. Login is successful.
        EXPECTED: 2. Home page is loaded.
        """
        pass

    def test_000_verify_the_display_of_created_sb_in_homepage_amp_slp_amp_special_sb_in_1_2_free_page(self):
        """
        DESCRIPTION: Verify the display of created SB in homepage &amp; SLP, &amp; Special SB in 1-2 Free page
        EXPECTED: SB &amp; special SB are displayed properly.
        """
        pass

    def test_000_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out successfully.
        """
        pass

    def test_000_login_into_the_application_with_a_rgy_user(self):
        """
        DESCRIPTION: Login into the application with a RGY user.
        EXPECTED: User is logged in successfully.
        """
        pass

    def test_000_verify_the_display_of_created_sb_in_homepage_amp_slp_amp_special_sb_in_1_2_free_page(self):
        """
        DESCRIPTION: Verify the display of created SB in homepage &amp; SLP, &amp; Special SB in 1-2 Free page
        EXPECTED: User is not able to view created SB &amp; special SB.
        """
        pass
