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
class Test_C61619018_Verify_the_display_of_Tutorial_button_Live_Leaderboard_when_customer_has_entered_single_team(Common):
    """
    TR_ID: C61619018
    NAME: Verify the display of Tutorial button -Live Leaderboard when customer has entered single team
    DESCRIPTION: This Test Case Verifies the display of Tutorial button in Live Leaderboard when customer has entered single team
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

    def test_002_verify_tutorial_button_in_live_event_leaderboard(self):
        """
        DESCRIPTION: Verify Tutorial button in Live event leaderboard
        EXPECTED: Tutorial button should be displayed as per the design
        """
        pass

    def test_003_click_on_the_tutorial_button(self):
        """
        DESCRIPTION: Click on the Tutorial Button
        EXPECTED: Welcome Overlay(Get started) CTA button is displayed as below
        EXPECTED: ![](index.php?/attachments/get/161000053)
        EXPECTED: Close icon is *not* present
        """
        pass

    def test_004_click_on_get_started_cta_and_verify_the_welcome_to_showdown_leaderboard_screenverify_ga_tracking_for_get_started_cta(self):
        """
        DESCRIPTION: Click on Get Started CTA and verify the Welcome to Showdown Leaderboard Screen
        DESCRIPTION: Verify GA Tracking for Get Started CTA
        EXPECTED: Welcome to Showdown Leaderboard screen should be displayed as per design
        EXPECTED: Text is driven from CMS
        EXPECTED: Close icon is present for the customer to exit the tutorial.
        EXPECTED: ![](index.php?/attachments/get/151652812)
        EXPECTED: Get Started CTA is GA Tracked
        """
        pass

    def test_005_click_on_next_and_verify_your_team_screenverify_ga_tracking_for_next_button(self):
        """
        DESCRIPTION: Click on NEXT and verify Your Team Screen
        DESCRIPTION: Verify GA Tracking for NEXT Button
        EXPECTED: Your Team screen should be as per the design
        EXPECTED: 'My Entry' should be displayed  as per the design
        EXPECTED: Text is driven from CMS
        EXPECTED: Close button is available to close the tutorial
        EXPECTED: Next button is displayed to navigate to another screen and the button is GA Tracked
        EXPECTED: ![](index.php?/attachments/get/151652813)
        """
        pass

    def test_006_click_on_next_and_verify_your_team_details_screenverify_ga_tracking_for_next_button(self):
        """
        DESCRIPTION: Click on NEXT and verify Your Team Details Screen
        DESCRIPTION: Verify GA Tracking for NEXT Button
        EXPECTED: Your Team Details screen should be as per the design
        EXPECTED: second player in the team should be highlighted as per the design
        EXPECTED: Text is driven from CMS
        EXPECTED: Close button is available to close the Tutorial
        EXPECTED: Next button is displayed to navigate to another screen and the button is GA Tracked
        EXPECTED: ![](index.php?/attachments/get/161000059)
        """
        pass

    def test_007_click_on_next_button_and_verify_position_summary_bar_customer_only_has_one_teamverify_ga_tracking_for_next_button(self):
        """
        DESCRIPTION: Click on NEXT Button and verify POSITION SUMMARY BAR (Customer only has one team)
        DESCRIPTION: Verify GA Tracking for NEXT Button
        EXPECTED: Position Summary Bar screen should be as per the designs
        EXPECTED: Bar is highlighted as per the design
        EXPECTED: Text about 'Tapping on the bar' is NOT present
        EXPECTED: Text is driven from CMS
        EXPECTED: Close button is available to close the tutorial
        EXPECTED: Next button is displayed to navigate to another screen and the button is GA Tracked
        EXPECTED: ![](index.php?/attachments/get/161000110)
        """
        pass

    def test_008_click_on_next_button_and_verify_leaderboard_screenverify_ga_tracking_for_finish_button(self):
        """
        DESCRIPTION: Click on NEXT Button and verify Leaderboard screen
        DESCRIPTION: Verify GA Tracking for Finish Button
        EXPECTED: Leaderboard screen should be as per design
        EXPECTED: Top 3 positions should be highlighted per the design
        EXPECTED: Text is driven from CMS
        EXPECTED: Close button is available to close the tutorial
        EXPECTED: Finish' button is available to close the tutorial and the button is GA Tracked
        """
        pass

    def test_009_repeat_step2_with_the_same_user(self):
        """
        DESCRIPTION: Repeat step2 with the same user
        EXPECTED: No tutorial should be displayed
        """
        pass
