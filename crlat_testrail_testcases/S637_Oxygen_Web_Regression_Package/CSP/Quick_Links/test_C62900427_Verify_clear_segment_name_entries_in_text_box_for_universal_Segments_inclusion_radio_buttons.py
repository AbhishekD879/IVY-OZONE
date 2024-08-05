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
class Test_C62900427_Verify_clear_segment_name_entries_in_text_box_for_universal_Segments_inclusion_radio_buttons(Common):
    """
    TR_ID: C62900427
    NAME: Verify clear segment name entries in text box for universal/Segment(s) inclusion radio buttons
    DESCRIPTION: This test case verifies clear segments name entries in text boxes
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

    def test_005_select_universal_radio_button_enter_segment_names_in_text_box(self):
        """
        DESCRIPTION: Select universal Radio button ,enter segment names in text box
        EXPECTED: User should allow to enter segment names
        """
        pass

    def test_006_select_segmentsinclusion_radio_button(self):
        """
        DESCRIPTION: Select segment(s)inclusion radio button
        EXPECTED: a)Segment(s) inclusion test box should enable
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Existing segment names in segment(s) exclusion text box should be cleared
        """
        pass

    def test_008_repeated_56_steps_for_segments_inclusion_radio_button(self):
        """
        DESCRIPTION: Repeated 5&6 steps for Segment(s) inclusion radio button
        EXPECTED: Existing segment names in segment(s) inclusion text box should be cleared
        """
        pass
