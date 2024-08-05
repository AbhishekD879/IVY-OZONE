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
class Test_C61619027_Verify_the_display_of_Welcome_to_5_A_Side_Showdown_User_Team_already_entered_Pre_Leaderboard(Common):
    """
    TR_ID: C61619027
    NAME: Verify the display of Welcome to 5-A Side Showdown_User Team already entered_Pre Leaderboard
    DESCRIPTION: This test case verifies the display of Welcome to 5-A Side Showdown when User Team already entered to Pre Leaderboard
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: Item Label:Showdown Overlay
    PRECONDITIONS: Path: /five-a-side-showdown/welcome-overlay
    PRECONDITIONS: **Tutorial should be enabled in CMS**
    PRECONDITIONS: **To Qualify for Showdown**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be able log in successfully
        """
        pass

    def test_002_navigate_to_pre_event_leaderboard_for_the_first_time(self):
        """
        DESCRIPTION: Navigate to Pre-Event Leaderboard for the first time
        EXPECTED: * User should be navigated to Pre-Event Leaderboard and Welcome Overlay(Get Started) should be displayed
        EXPECTED: ![](index.php?/attachments/get/161000053)
        """
        pass

    def test_003_click_on_get_started_and_check_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Click on "Get Started" and check GA tracking for CTA button.
        EXPECTED: * "Get Started" CTA button should be GA Tracked
        EXPECTED: **Example:**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "Get Started"
        EXPECTED: eventCategory: "Showdown lobby"
        EXPECTED: eventLabel: "5-A-Side Leaderboard Welcome Overlay"
        EXPECTED: * Close icon should not be displayed in Get Started Screen
        """
        pass

    def test_004_verify_the_pre_event_leaderboard_tutorialwelcome_to_5_a_side_showdownclick_on_next__check_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Verify the Pre-Event Leaderboard tutorial(Welcome to 5-A Side Showdown)
        DESCRIPTION: Click on Next & Check GA tracking for CTA button.
        EXPECTED: * Pre-Event Leaderboard tutorial should be displayed
        EXPECTED: ![](index.php?/attachments/get/151652266)
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available to close the tutorial
        EXPECTED: * Next Button should be GA Tracked
        """
        pass
