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
class Test_C62701151_Verify_Leaving_Segments_inclusion_text_box_as_empty_should_not_Allowed(Common):
    """
    TR_ID: C62701151
    NAME: Verify Leaving Segment(s) inclusion text box as empty should not Allowed
    DESCRIPTION: This verifies Segment(s) Inclusion text box functionality
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
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

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on super button link.
        EXPECTED: User should be able to view existing super button should be displayed.
        """
        pass

    def test_004_click_on_super_button_cta_button(self):
        """
        DESCRIPTION: Click on super button CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select Segment(s) Inclusion radio button
        EXPECTED: Upon selecting Segment(s) Inclusion radio button ,segment(s) inclusion text box should be enabled.
        """
        pass

    def test_006_leave_segments_inclusion_text_box_as_empty(self):
        """
        DESCRIPTION: Leave segment(s) inclusion text box as empty
        EXPECTED: Leaving Segment(s) Inclusion text field empty – Not allowed
        """
        pass