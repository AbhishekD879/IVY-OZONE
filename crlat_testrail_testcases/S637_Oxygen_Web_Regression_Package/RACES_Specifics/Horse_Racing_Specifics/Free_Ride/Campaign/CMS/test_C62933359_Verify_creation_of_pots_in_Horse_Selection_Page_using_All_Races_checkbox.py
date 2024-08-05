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
class Test_C62933359_Verify_creation_of_pots_in_Horse_Selection_Page_using_All_Races_checkbox(Common):
    """
    TR_ID: C62933359
    NAME: Verify creation of pots in Horse Selection Page using All Races checkbox
    DESCRIPTION: This test case verifies creation of pots from Horse Selection Page using All Races checkbox
    PRECONDITIONS: 1: User should be logged into oxygen CMS with admin access
    PRECONDITIONS: 2: Campaign should be created successfully
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

    def test_002_enter_valid_class_id_and_select_date(self):
        """
        DESCRIPTION: Enter valid Class ID and select date
        EXPECTED: User should able see the entered Class ID and selected date
        """
        pass

    def test_003_click_on_refresh_events_cta_button(self):
        """
        DESCRIPTION: Click on 'Refresh Events' CTA button
        EXPECTED: User should be able to see the races information
        """
        pass

    def test_004_select_all_races_check_box(self):
        """
        DESCRIPTION: Select All Races check box
        EXPECTED: All races should be selected for the respective meeting
        """
        pass

    def test_005_click_on_create_pot_cta_button(self):
        """
        DESCRIPTION: Click on 'Create Pot' CTA button
        EXPECTED: * 'Create Pot' CTA button should be enabled
        EXPECTED: * confirmation pop up 'Confirm' and 'Cancel' buttons should be displayed
        """
        pass

    def test_006_click_on_cancel_button(self):
        """
        DESCRIPTION: Click on Cancel Button
        EXPECTED: Confirmation pop up should be closed
        """
        pass

    def test_007_navigate_to_view_pots_tab(self):
        """
        DESCRIPTION: Navigate to View Pots Tab
        EXPECTED: Below data should not be displayed in View Pots tab
        EXPECTED: * Pots 1-8 should not be displayed
        EXPECTED: * Pots Table should not consists of pots (1-8), Rating, Weight, Odds
        """
        pass

    def test_008_repeat_steps_2_5_and_click_on_confirm_button(self):
        """
        DESCRIPTION: Repeat steps 2-5 and Click on Confirm Button
        EXPECTED: Confirmation pop up should be closed
        """
        pass

    def test_009_navigate_to_view_pots_tab(self):
        """
        DESCRIPTION: Navigate to View Pots Tab
        EXPECTED: Below data should be displayed in view Pots Tab
        EXPECTED: * Pots 1-8 should be displayed
        EXPECTED: * Pots Table should consists of pots (1-8), Rating, Weight, Odds
        """
        pass
