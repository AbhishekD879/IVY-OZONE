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
class Test_C62764645_Verify_edit_Remove_should_be_enabled_only_for_records_selected_segment_in_the_dropdown(Common):
    """
    TR_ID: C62764645
    NAME: Verify edit/Remove should be enabled only for records selected segment in the dropdown
    DESCRIPTION: This test case verifies edit/remove buttons should be enabled only for the selected segment in the drop down (in details view as well)
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
    PRECONDITIONS: 2) Create a some Segmented and universal Highlights Carousel
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_highlights_carousel_link(self):
        """
        DESCRIPTION: Click on Highlights Carousel link.
        EXPECTED: User should be able to view existing Highlights Carousel should be displayed.
        """
        pass

    def test_004_select_one_of_the_segment_dropdown_and_verify_editremove_button_for_only_selected_segment_on_highlights_carousel_page(self):
        """
        DESCRIPTION: Select one of the segment dropdown, and verify Edit/remove button for only selected segment on Highlights Carousel Page
        EXPECTED: User should able to select from the segment drop down. Edit/Remove button should be enabled for only selected segment on Highlights Carousel Page
        """
        pass

    def test_005_navigate_to_highlights_carousel_detail_page_of_selected_segment(self):
        """
        DESCRIPTION: Navigate to Highlights Carousel detail page of selected segment
        EXPECTED: Edit/Remove button should be enable for only selected segment, should allow to edit/remove in detail view
        """
        pass
