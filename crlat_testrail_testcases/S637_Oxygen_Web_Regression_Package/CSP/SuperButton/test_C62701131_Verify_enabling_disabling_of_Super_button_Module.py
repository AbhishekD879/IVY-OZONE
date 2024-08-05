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
class Test_C62701131_Verify_enabling_disabling_of_Super_button_Module(Common):
    """
    TR_ID: C62701131
    NAME: Verify enabling/disabling of 'Super button' Module
    DESCRIPTION: This test case verifies enabling/disabling of "super button" Module on Home page/SLP via CMS, If we disable one super button next available super button should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    PRECONDITIONS: Configure multiple super buttons with different publish dates
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages__gt_super_button_section__gt_open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages -&gt; Super Button section -&gt; open existing Super Button
        EXPECTED: Super Button details page is opened
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully.
        EXPECTED: User should be able to enable/ disable the check box.
        """
        pass

    def test_004_set_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Set 'Active' checkbox and save changes
        EXPECTED: a)Existing Super Button is active
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_005_load_oxygen_app_and_verify_super_button_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button displaying
        EXPECTED: Super Button is displayed on Front End
        """
        pass

    def test_006_go_back_to_the_same_super_button_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Super Button, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Super Button is inactive
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_super_button_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button displaying
        EXPECTED: a) Super Button is NOT displayed on Front End
        EXPECTED: b) If we have other super button with valid date it should display
        """
        pass
