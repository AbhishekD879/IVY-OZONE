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
class Test_C62764769_Create_new_surface_bet_with_Segments_Inclusion_single_segment_and_verify_in_FE(Common):
    """
    TR_ID: C62764769
    NAME: Create new surface bet with Segment(s) Inclusion (single segment) and verify in FE
    DESCRIPTION: This test case verifies creating a new surface bet with Segment(s) Inclusion (single segment)
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;
    PRECONDITIONS: CMS &gt; sports pages &gt;home page&gt; surface bet
    PRECONDITIONS: 2) Segment should be created in Optimove and user should mapped to respective segment
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
        EXPECTED: User should be able to view existing surface bets should be displayed.
        """
        pass

    def test_004_click_on_surface_bet_cta_button(self):
        """
        DESCRIPTION: Click on surface bet CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segment(s) inclusion with text boxes
        """
        pass

    def test_005_select_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Select segment(s) inclusion radio button
        EXPECTED: Upon selecting segment(s) inclusion radio button Segment(s) inclusion text box should be enabled.
        """
        pass

    def test_006_enter_segment_name_in_segments_inclusion_text_box_click_on_save_changes_button(self):
        """
        DESCRIPTION: Enter segment name in Segment(s) inclusion text box click on save changes button
        EXPECTED: Segmented surface bet should be created Successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_newly_created_surface_bet_for_segmented_user(self):
        """
        DESCRIPTION: Load Oxygen app and verify newly created surface bet for segmented user
        EXPECTED: Specific segmented user only should able view newly created Surface bet.
        EXPECTED: (Not visible in Universal view and other segmented view)
        """
        pass
