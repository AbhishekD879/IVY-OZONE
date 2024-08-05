import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C60538845_Verify_the_CMS_configurations_for_adding_Contest(Common):
    """
    TR_ID: C60538845
    NAME: Verify the CMS configurations for adding Contest
    DESCRIPTION: This test case verifies all the fields displayed in adding Contest details in 5 A Side showdown tab in CMS
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Menu Item***
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_click_on_5_a_side_showdown_tab(self):
        """
        DESCRIPTION: Click on '5-A Side showdown' tab
        EXPECTED: User should be navigate to Contest page and the below should be displayed
        EXPECTED: ##When no Contests are configured##
        EXPECTED: * Add New Contest
        EXPECTED: ##When at least one Contest is configured##
        EXPECTED: * Add New Contest
        EXPECTED: * Table with below column Headers
        EXPECTED: * Contest Name
        EXPECTED: * Date - Event Start Date
        EXPECTED: * Active
        EXPECTED: * Remove
        EXPECTED: * Edit
        EXPECTED: * Table should include a drag and drop before the Contest name
        EXPECTED: * Search bar should be available
        """
        pass

    def test_004_click_on_add_new_contest_button(self):
        """
        DESCRIPTION: Click on 'Add New Contest' button
        EXPECTED: * User should be displayed a pop-up
        EXPECTED: * Name, Entry Stake, Start Date fields should be displayed
        EXPECTED: * Save button should be displayed
        EXPECTED: * Save button should be disabled
        EXPECTED: **Entry Stake Can be decimal value also**
        """
        pass

    def test_005_validate_that_save_button_is_enabled_only_on_entering_the_mandatory_details_name_start_date_entry_stake(self):
        """
        DESCRIPTION: Validate that Save button is enabled only on entering the mandatory details
        DESCRIPTION: * Name
        DESCRIPTION: * Start Date
        DESCRIPTION: * Entry Stake
        EXPECTED: * User should be able to enter all the details
        EXPECTED: * Save button should be enabled
        """
        pass

    def test_006_click_on_save_button(self):
        """
        DESCRIPTION: Click on Save button
        EXPECTED: * User should be able to click on Save button
        EXPECTED: * User should be redirected to Contest edit details page
        EXPECTED: * ContestID field should be marked mandatory and displayed with an auto generated 25 alphanumeric Unique code
        EXPECTED: * ContestId should be same as the Unique code displayed at the end of CMS URL
        EXPECTED: * Below fields should be displayed
        EXPECTED: * *ContestID
        EXPECTED: * *Name
        EXPECTED: * Description
        EXPECTED: * Game Blurb
        EXPECTED: * Icon --- *allow image upload*
        EXPECTED: * *Start Date
        EXPECTED: * *Event
        EXPECTED: * *Entry Stake
        EXPECTED: * Free Bets Allowed
        EXPECTED: * Prizes --- *Seperate Section*
        EXPECTED: * Sponsor Text
        EXPECTED: * Sponsor Logo ---*Allow upload of image*
        EXPECTED: * Size ---- *Amount of teams that can enter in total*
        EXPECTED: * Teams ---*Number of teams that can be enetered per user*
        EXPECTED: * Entry Confirmation Text
        EXPECTED: * Next Contest
        EXPECTED: * Display
        EXPECTED: * All the * fields should be mandatory
        """
        pass
