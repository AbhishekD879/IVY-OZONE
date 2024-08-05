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
class Test_C62978491_Verify_Edit_option_for_Campaign_after_pot_creation(Common):
    """
    TR_ID: C62978491
    NAME: Verify Edit option for Campaign after pot creation
    DESCRIPTION: This test case verifies Edit option for Campaign after pot creation
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

    def test_002_enter_valid_class_id_select_date_and_click_on_refresh_events_cta_button(self):
        """
        DESCRIPTION: Enter valid Class ID, select date and click on 'Refresh Events' CTA button
        EXPECTED: User should be able to see the races information
        """
        pass

    def test_003_select_individual_race_all_race_check_box_and_click_on_create_pot_cta_button(self):
        """
        DESCRIPTION: Select Individual Race/ All Race check box and click on 'Create Pot' CTA button
        EXPECTED: Confirmation pop up with 'Confirm' and 'Cancel' buttons should be displayed
        """
        pass

    def test_004_click_on_confirm_andnavigate_to_view_pots_tab(self):
        """
        DESCRIPTION: Click on confirm and Navigate to View Pots Tab
        EXPECTED: Below data should be displayed in view Pots Tab
        EXPECTED: * Pots 1-8 should be displayed
        EXPECTED: * Pots Table should consists of pots (1-8), Rating, Weight, Odds
        """
        pass

    def test_005_verify_the_state_of_below_pages_campaign_tab_questions_tab_horse_selection_tab_view_pots_tabs(self):
        """
        DESCRIPTION: Verify the state of below pages
        DESCRIPTION: * Campaign Tab
        DESCRIPTION: * Questions Tab
        DESCRIPTION: * Horse Selection Tab
        DESCRIPTION: * View Pots Tabs
        EXPECTED: Once the pots are created all the below tabs should be freezed and save changes button should be in disabled state
        EXPECTED: * Campaign Tab
        EXPECTED: * Questions Tab
        EXPECTED: * Horse Selection Tab
        EXPECTED: * View Pots Tabs
        """
        pass
