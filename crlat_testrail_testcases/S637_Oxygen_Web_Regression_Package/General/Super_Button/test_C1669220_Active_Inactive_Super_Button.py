import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1669220_Active_Inactive_Super_Button(Common):
    """
    TR_ID: C1669220
    NAME: Active/Inactive Super Button
    DESCRIPTION: This test case verifies Active/Inactive Super Button displaying
    PRECONDITIONS: * Super Button should be added and configured in CMS:
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * Content manager is logged in
        """
        pass

    def test_002_go_to_sports_pages___super_button_section_____open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages -> Super Button section ->   open existing Super Button
        EXPECTED: Super Button details page is opened
        """
        pass

    def test_003_set_active_checkbox_and_save_changesnote_date_range_should_be_valid(self):
        """
        DESCRIPTION: Set 'Active' checkbox and save changes
        DESCRIPTION: Note: date range should be valid
        EXPECTED: * Existing Super Button is active
        EXPECTED: * Changes is saved successfully
        """
        pass

    def test_004_load_oxygen_app_and_verify_super_button_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button displaying
        EXPECTED: Super Button is displayed on Front End
        """
        pass

    def test_005_go_back_to_the_same_super_button_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Super Button, unselect 'Active' checkbox and save changes
        EXPECTED: * Existing Super Button is inactive
        EXPECTED: * Changes is saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_super_button_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button displaying
        EXPECTED: Super Button is NOT displayed on Front End
        """
        pass
