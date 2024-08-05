import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62933362_Verify_the_meetings_Races_info_displayed_and_behavior_of_All_Races_Individual_Races_checkboxes_in_Horse_Selection_Page(Common):
    """
    TR_ID: C62933362
    NAME: Verify the meetings/Races info displayed and behavior of All Races/Individual Races checkboxes in Horse Selection Page
    DESCRIPTION: This test case verifies meetings/Races info displayed and behavior of All Races/Individual Races checkboxes in Horse Selection Page
    PRECONDITIONS: 1. User should be logged into oxygen CMS with admin access
    PRECONDITIONS: 2. Campaign should be created successfully
    """
    keep_browser_open = True

    def test_001_click_on_horse_selection_tab(self):
        """
        DESCRIPTION: Click on Horse selection Tab
        EXPECTED: Below fields should be displayed under Horse Selection Tab
        EXPECTED: * Fetch for classIds
        EXPECTED: * Fetch from
        EXPECTED: * HH MM SS
        EXPECTED: * Restrict to UK And IRE
        EXPECTED: * 'Refresh Events' CTA button
        """
        pass

    def test_002__single_class_identer_valid_class_ids_multiple_class_idsenter_valid_class_ids_separated_by_commas(self):
        """
        DESCRIPTION: * Single Class ID
        DESCRIPTION: Enter valid Class Ids
        DESCRIPTION: * Multiple Class Id's
        DESCRIPTION: Enter valid Class Id's separated by commas
        EXPECTED: User should able to see the entered data
        """
        pass

    def test_003_select_the_valid_date(self):
        """
        DESCRIPTION: Select the valid date
        EXPECTED: User should able to select the date
        """
        pass

    def test_004_click_on_refresh_events_cta_button(self):
        """
        DESCRIPTION: Click on 'Refresh Events' CTA button
        EXPECTED: User should be able to see the races information
        """
        pass

    def test_005_verify_the_display_of_fields_on_horse_selection_page(self):
        """
        DESCRIPTION: Verify the display of fields on Horse selection page
        EXPECTED: Below fields should be displayed
        EXPECTED: * Meetings information
        EXPECTED: * Races Information
        EXPECTED: * All Races selection checkbox
        EXPECTED: * Individual Race selection checkbox
        EXPECTED: * Create pots to campaign CTA button
        """
        pass

    def test_006_select_all_races_selection_checkbox_for_specific_meeting(self):
        """
        DESCRIPTION: Select 'All Races' selection checkbox for specific meeting
        EXPECTED: All races should be selected for the respective meeting
        """
        pass

    def test_007_deselect_all_races_selection_checkbox_for_specific_meeting(self):
        """
        DESCRIPTION: Deselect 'All Races' selection checkbox for specific meeting
        EXPECTED: All races should be deselected for the respective meeting
        """
        pass

    def test_008_select_one_or_more_individual_race_selection_checkbox(self):
        """
        DESCRIPTION: Select one or more 'Individual Race' selection checkbox
        EXPECTED: User should be able to select one or more than one using 'Individual Race' checkbox
        """
        pass

    def test_009_deselect_one_or_more_individual_race_selection_checkbox(self):
        """
        DESCRIPTION: Deselect one or more 'Individual Race' selection checkbox
        EXPECTED: User should be able to deselect one or more than one using 'Individual Race' checkbox
        """
        pass

    def test_010_repeat_step1_and_enter_invalid_class_id(self):
        """
        DESCRIPTION: Repeat step1 and enter invalid class ID
        EXPECTED: 'No events found message' should be displayed
        """
        pass
