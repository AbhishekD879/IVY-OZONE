import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62700706_Verify_the_behaviour_of_a_contest_when_invitational_contest_toggled_OFF_in_CMS(Common):
    """
    TR_ID: C62700706
    NAME: Verify the behaviour of a contest when invitational contest toggled OFF in CMS
    DESCRIPTION: This test case verifies the behaviour of the contest when disabled invitation toggle
    PRECONDITIONS: """""""1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: Contest Criteria
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: Invitation contest creation :
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: 6. Invitation toggle should be enabled in contest creation page.
    PRECONDITIONS: 7. Standard Leaderboard URL will be generated once the contest is saved.
    PRECONDITIONS: Asset Management
    PRECONDITIONS: 1: Team Flags can be configured in CMS &gt; BYB &gt; ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.""""""
    PRECONDITIONS: "
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
        EXPECTED: User should be displayed a pop-up
        EXPECTED: Name, Entry Stake, Start Date fields should be displayed
        EXPECTED: Save button should be displayed
        EXPECTED: Save button should be disabled
        EXPECTED: Entry Stake Can be decimal value also
        """
        pass

    def test_005_validate_that_save_button_is_enabled_only_on_entering_the_mandatory_details_name_start_date_entry_stake(self):
        """
        DESCRIPTION: Validate that Save button is enabled only on entering the mandatory details
        DESCRIPTION: * Name
        DESCRIPTION: * Start Date
        DESCRIPTION: * Entry Stake
        EXPECTED: User should be able to enter all the details
        EXPECTED: Save button should be enabled
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

    def test_007_enter_the_event_id_and_make_the_enable_toggle_for_invitational_contest_and_check_lobby(self):
        """
        DESCRIPTION: Enter the event ID and make the enable toggle for invitational contest and check lobby.
        EXPECTED: Contest created shouldn't be displayed in lobby for logged in & logged out users until navigated to Standard Leaderboard URL and opted for the user.
        """
        pass

    def test_008_now_navigate_to_the_contest_and_disable_toggle_for_invitational_contest_and_navigate_to_lobby(self):
        """
        DESCRIPTION: Now navigate to the contest and disable toggle for invitational contest and navigate to lobby
        EXPECTED: Contest should be displayed in lobby for logged in or logged out users and should act like a normal contest.
        """
        pass