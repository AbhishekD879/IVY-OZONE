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
class Test_C62701201_Verify_Selecting_Universal_radio_button_should_disable_Segments_Inclusion_radio_button_and_Segment_inclusion_text_box(Common):
    """
    TR_ID: C62701201
    NAME: Verify Selecting Universal radio button should disable Segment(s) Inclusion radio button and Segment inclusion text box
    DESCRIPTION: This test case verifies Universal radio button functionality
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Menus > Footer menu.
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

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus.
        """
        pass

    def test_004_click_on_footer_menu_cta_button(self):
        """
        DESCRIPTION: Click on Footer Menu CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting Universal radio button ,Segment(s) inclusion radio button and segment(s) inclusion text box should disabled.
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: On successful creation, page should redirect to footer menu module page
        """
        pass
