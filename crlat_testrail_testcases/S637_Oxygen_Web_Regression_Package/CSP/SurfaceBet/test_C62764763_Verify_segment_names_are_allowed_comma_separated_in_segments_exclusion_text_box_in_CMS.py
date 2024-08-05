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
class Test_C62764763_Verify_segment_names_are_allowed_comma_separated_in_segments_exclusion_text_box_in_CMS(Common):
    """
    TR_ID: C62764763
    NAME: Verify segment name(s) are allowed comma separated in segment(s) exclusion text box in CMS
    DESCRIPTION: This test case verifies CMS configuration for segment(S) exclusion text box
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
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

    def test_003_click_on_surface_bet_link(self):
        """
        DESCRIPTION: click on surface bet link.
        EXPECTED: User should be able to view existing surface bet should be displayed.
        """
        pass

    def test_004_click_on_surface_bet_cta_button(self):
        """
        DESCRIPTION: Click on surface bet CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        pass

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select universal radio button
        EXPECTED: Upon selecting universal radio button ,Segment(s) Exclusion text box should be enabled.
        """
        pass

    def test_006_verify_user_able_to_enter_more_than_one_segment_name_in_segments_exclusion_text_box(self):
        """
        DESCRIPTION: Verify user able to enter more than one segment name in segment(s) Exclusion text box.
        EXPECTED: User should be able to enter more than one segment name with comma (,) separated
        """
        pass