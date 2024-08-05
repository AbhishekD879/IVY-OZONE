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
class Test_C62900281_Verify_Selecting_segments_inclusion_radio_button_will_enable_Segments_inclusion_text_box(Common):
    """
    TR_ID: C62900281
    NAME: Verify Selecting segment(s) inclusion radio button will enable Segment(s) inclusion text box
    DESCRIPTION: This test case verifies segment(s) inclusion radio button functionality
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >Home page > Quick links
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_quick_links_link(self):
        """
        DESCRIPTION: click on Quick links link.
        EXPECTED: User should be able to view existing Quick links should be displayed.
        """
        pass

    def test_004_click_on_quick_links_cta_button(self):
        """
        DESCRIPTION: Click on Quick links CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_button(self):
        """
        DESCRIPTION: Select segment(s) inclusion button
        EXPECTED: Upon selecting segment(s) inclusion radio button ,Segment(s) inclusion text field should be enabled and able to enter text (ex: Football)
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: On successful creation, page should redirect to Quick links module page
        """
        pass

    def test_007_load_oxygen_app_and_verify_quick_links(self):
        """
        DESCRIPTION: Load Oxygen app and verify Quick links
        EXPECTED: For only football segmented user should able to view Quick links (as we have configured segment(s) inclusion as Football)
        """
        pass