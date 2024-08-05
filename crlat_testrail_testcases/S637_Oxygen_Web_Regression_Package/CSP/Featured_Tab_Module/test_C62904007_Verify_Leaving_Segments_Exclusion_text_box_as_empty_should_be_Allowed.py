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
class Test_C62904007_Verify_Leaving_Segments_Exclusion_text_box_as_empty_should_be_Allowed(Common):
    """
    TR_ID: C62904007
    NAME: Verify Leaving Segment(s) Exclusion text box as empty should be Allowed
    DESCRIPTION: This verifies Segment(s) Exclusion text box functionality
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured tab module
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

    def test_003_click_on_featured_tab_module_link(self):
        """
        DESCRIPTION: click on Featured tab module link.
        EXPECTED: User should be able to view existing Featured tab module should be displayed.
        """
        pass

    def test_004_click_on_featured_tab_module_cta_button(self):
        """
        DESCRIPTION: Click on Featured tab module CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select universal radio button
        EXPECTED: Upon selecting universal radio button ,Segment(s) Exclusion text box should be enabled.
        """
        pass

    def test_006_leave_segments_inclusion_text_box_as_empty(self):
        """
        DESCRIPTION: Leave segment(s) inclusion text box as empty
        EXPECTED: Leaving Segment(s) Exclusion text field empty – Allowed
        """
        pass
