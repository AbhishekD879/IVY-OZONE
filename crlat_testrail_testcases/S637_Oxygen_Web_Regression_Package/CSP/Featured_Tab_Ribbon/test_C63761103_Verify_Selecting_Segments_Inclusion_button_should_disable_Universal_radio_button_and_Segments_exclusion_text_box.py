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
class Test_C63761103_Verify_Selecting_Segments_Inclusion_button_should_disable_Universal_radio_button_and_Segments_exclusion_text_box(Common):
    """
    TR_ID: C63761103
    NAME: Verify Selecting Segment(s) Inclusion  button should disable Universal radio  button and Segment(s) exclusion text box
    DESCRIPTION: This test case verifies Segment(s) Inclusion radio button functionality
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
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

    def test_003_click_on_module_ribbon_tab_link(self):
        """
        DESCRIPTION: click on Module ribbon tab link.
        EXPECTED: User should be able to view existing Module ribbon tab should be displayed.
        """
        pass

    def test_004_click_on_module_ribbon_tab_cta_button(self):
        """
        DESCRIPTION: Click on Module ribbon tab CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select Segment(s) Inclusion radio button
        EXPECTED: Upon selecting Segment(s) Inclusion radio button ,Universal radio button and segment(s) exclusion text box should disabled.
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: On successful creation, page should redirect to Module ribbon tab module page
        """
        pass
