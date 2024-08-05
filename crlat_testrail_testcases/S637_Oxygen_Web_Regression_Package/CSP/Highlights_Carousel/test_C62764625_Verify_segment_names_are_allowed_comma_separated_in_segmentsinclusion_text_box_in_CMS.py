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
class Test_C62764625_Verify_segment_names_are_allowed_comma_separated_in_segmentsinclusion_text_box_in_CMS(Common):
    """
    TR_ID: C62764625
    NAME: Verify segment name(s) are allowed comma separated in segment(s)inclusion text box in CMS
    DESCRIPTION: This test case verifies CMS configuration for segment(S) inclusion text box
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
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

    def test_003_click_on_highlights_carousel_link(self):
        """
        DESCRIPTION: click on Highlights Carousel link.
        EXPECTED: User should be able to view existing Highlights Carousel should be displayed.
        """
        pass

    def test_004_click_on_highlights_carousel_cta_button(self):
        """
        DESCRIPTION: Click on Highlights Carousel CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select segment(s) inclusion radio button
        EXPECTED: Upon selecting segment(s) inclusion radio button ,Segment(s) inclusion text box should be enabled.
        """
        pass

    def test_006_verify_user_able_to_enter_more_than_one_segment_name_in_segments_inclusion_text_box(self):
        """
        DESCRIPTION: Verify user able to enter more than one segment name in segment(s) inclusion text box.
        EXPECTED: User should be able to enter more than one segment name with comma (,) separated
        """
        pass
