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
class Test_C61033857_Verify_tutorial_for_Pre_Event_Leaderboard_when_customer_has_entered_team_into_the_Contest(Common):
    """
    TR_ID: C61033857
    NAME: Verify tutorial for Pre-Event Leaderboard when customer has entered team into the Contest.
    DESCRIPTION: This Test case verifies the tutorial for Pre-Event Leaderboard when customer has entered team into the Contest.
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side contests should be configured in CMS  & one event should be in Live.
    PRECONDITIONS: *CMS Configuration:*
    PRECONDITIONS: Tutorial toggle should be turned ON in CMS.
    PRECONDITIONS: User should be navigating through showdown for the first time & should have placed at least one qualifying bet on 5-A-Side.
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
        EXPECTED: ![](index.php?/attachments/get/161019229)
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

    def test_005_verify_prize_pool_screenclick_on_next__check_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Verify Prize Pool Screen
        DESCRIPTION: Click on Next & Check GA tracking for CTA button.
        EXPECTED: * Prize Pool screen should be displayed as per design
        EXPECTED: *Top 3 Prizes are highlighted on the prize pool as per design
        EXPECTED: ![](index.php?/attachments/get/151652262)
        EXPECTED: * Text should be driven from CMS
        EXPECTED: * Close button is available to close the tutorial
        EXPECTED: * Next Button should be GA Tracked
        """
        pass

    def test_006_verify_rules_screenclick_on_next___check_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Verify Rules Screen
        DESCRIPTION: Click on Next &  Check GA tracking for CTA button.
        EXPECTED: * Rules screen should be displayed as per design
        EXPECTED: * Rules Button should be highlighted as per the design
        EXPECTED: ![](index.php?/attachments/get/161000138)
        EXPECTED: * Text should be driven from CMS
        EXPECTED: * Close button is available to close the tutorial
        EXPECTED: * Next Button should be GA Tracked
        """
        pass

    def test_007_verify_build_another_team_screenclick_on_finish___check_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Verify Build Another Team Screen
        DESCRIPTION: Click on Finish &  Check GA tracking for CTA button.
        EXPECTED: * Build Another Team screen should be displayed as per design
        EXPECTED: * Build Another Team button should be highlighted as per
        EXPECTED: design
        EXPECTED: ![](index.php?/attachments/get/151652268)
        EXPECTED: * Text should be driven from CMS
        EXPECTED: * Close button is available to close the tutorial
        EXPECTED: * Finish button is available to close the tutorial
        EXPECTED: * Finish Button should be GA Tracked
        """
        pass

    def test_008_verify_from_step_3__with_the_same_user_for_the_second_time(self):
        """
        DESCRIPTION: Verify from step 3  with the same user for the second time.
        EXPECTED: No tutorial should be displayed in FE.
        """
        pass
