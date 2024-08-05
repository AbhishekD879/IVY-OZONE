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
class Test_C63770586_CMS_Segment_name_with_only_allowed_chars(Common):
    """
    TR_ID: C63770586
    NAME: CMS Segment name with only allowed chars
    DESCRIPTION: This tc verifies CMS segment name allowed chars
    PRECONDITIONS: User should have access to CMS
    """
    keep_browser_open = True

    def test_001_launch_the_cms_and_navigate_to_super_button(self):
        """
        DESCRIPTION: Launch the CMS and navigate to super button
        EXPECTED: Super button landing page should display
        """
        pass

    def test_002_create_a_super_button_with_valid_data_and_click_on_create_button(self):
        """
        DESCRIPTION: Create a super button with valid data and click on create button
        EXPECTED: Super button details page should open with entered data
        """
        pass

    def test_003_now_in_universal_exclusion_enter_name_other_than_a_za_z0_9__and__(self):
        """
        DESCRIPTION: Now in universal exclusion enter name other than A-Z,a-z,0-9,- and _
        EXPECTED: Valid error message should display
        EXPECTED: universal radio button should be selected
        EXPECTED: text should clear
        """
        pass

    def test_004_click_on_segment_inclusion_and_enter_name_other_than_a_za_z0_9__and__(self):
        """
        DESCRIPTION: Click on segment inclusion and enter name other than A-Z,a-z,0-9,- and _
        EXPECTED: Valid error message should display
        EXPECTED: Segment radio button should be selected
        EXPECTED: text should clear
        EXPECTED: save button should be disabled
        """
        pass

    def test_005_go_back_to_universal_exclusion_and_enter_name_other_than_a_za_z0_9__and__(self):
        """
        DESCRIPTION: Go back to universal exclusion and enter name other than A-Z,a-z,0-9,- and _
        EXPECTED: Valid error message should display
        EXPECTED: universal radio button should be selected
        EXPECTED: text should clear
        """
        pass

    def test_006_click_on_universal_radio_button_enter_segment_name_with_a_z_chars(self):
        """
        DESCRIPTION: Click on universal radio button Enter segment name with A-Z chars
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_007_click_on_revert_changes_and_enter_segment_name_with_a_z_chars(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with a-z chars
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_008_click_on_revert_changes_and_enter_segment_name_with_0_9_chars(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with 0-9 chars
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_009_click_on_revert_changes_and_enter_segment_name_with___and___chars(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with - and - chars
        EXPECTED: TBD
        """
        pass

    def test_010_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_z_and_a_z(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of A-Z and a-z
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_011_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_z_and_0_9(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of A-Z and 0-9
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_012_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_z_and_0_9(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of a-z and 0-9
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_013_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_z_and__and__(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of a-z and -and _
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_014_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_z_and__and__(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of A-Z and -and _
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_015_click_on_revert_changes_and_enter_segment_name_with_combination_of_0_9_and__and__(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of 0-9 and -and _
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_016_click_on_revert_changes_and_enter_segment_name_with_combination_of_a_za_z_0_9_and__and__(self):
        """
        DESCRIPTION: Click on revert changes and Enter segment name with combination of A-z,a-z, 0-9 and -and _
        EXPECTED: No error message should display
        EXPECTED: Segment name should present and save button should enable
        """
        pass

    def test_017_click_on_save_changes_button(self):
        """
        DESCRIPTION: click on save changes button
        EXPECTED: super button should save and navigate to respective segment list
        """
        pass

    def test_018_select_any_super_button_and_click_on_edit_button(self):
        """
        DESCRIPTION: Select any super button and click on edit button
        EXPECTED: Super button should open in edit mode
        """
        pass

    def test_019_select_segment_radio_button_and_repeat_step_6_18(self):
        """
        DESCRIPTION: Select segment radio button and repeat step 6-18
        EXPECTED: Should work as expected
        """
        pass

    def test_020_repeat_above_steps_for_below_modulesfooter_menuhighlights_carouselsurfacebetfeatured_modulefeatured_tab_ribbonquick_links(self):
        """
        DESCRIPTION: repeat above steps for below modules
        DESCRIPTION: Footer menu
        DESCRIPTION: highlights carousel
        DESCRIPTION: Surfacebet
        DESCRIPTION: Featured module
        DESCRIPTION: Featured tab ribbon
        DESCRIPTION: Quick links
        EXPECTED: Should work as expected
        """
        pass
