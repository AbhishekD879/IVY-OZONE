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
class Test_C64881021_Verify_multiple_segments_inclusion_and_exclusions(Common):
    """
    TR_ID: C64881021
    NAME: Verify multiple segment(s) inclusion and exclusion(s)
    DESCRIPTION: This test case verifies creating a new surface bet with universal for multiple segment inclusion/ exclusion
    PRECONDITIONS: 
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
        DESCRIPTION: Click on super button link.
        EXPECTED: User should be able to view existing super buttons
        """
        pass

    def test_004_click_on_surface_bet_cta_button(self):
        """
        DESCRIPTION: Click on surface bet CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segment(s) inclusion with text boxes
        """
        pass

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting universal radio button Segment(s) exclusion text box should be enabled.
        """
        pass

    def test_006_enter_more_than_one_segments_name_in_segments_exclusion_text_box_with_comma_separated_click_on_save_changes_button(self):
        """
        DESCRIPTION: Enter more than one Segments name in Segment(s) exclusion text box with comma separated, click on save changes button
        EXPECTED: Universal surface bet should be created Successfully with multiple segment(s)exclusion
        """
        pass

    def test_007_load_oxygen_app_and_verify_newly_created_surface_bet(self):
        """
        DESCRIPTION: Load Oxygen app and verify newly created surface bet
        EXPECTED: Newly created surface bet should be shown for
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: 1.Universal(not segmented) users
        """
        pass

    def test_009_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2.Loggedout users
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: 3.Segmented user except segment which is mentioned in Segment(s) exclusions text box
        """
        pass

    def test_011_(self):
        """
        DESCRIPTION: 
        EXPECTED: Note :Setting a configuration with exclusion segment(s) will NOT show that Universal configuration to users of the excluded segment(s) only but will be shown in all other segments.
        """
        pass
