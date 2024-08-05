import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C62701419_Verify_the_Leaderoard_widget_when_application_is_idle_or_placed_in_background(Common):
    """
    TR_ID: C62701419
    NAME: Verify the Leaderoard widget when application is idle or placed in background
    DESCRIPTION: This test case verifies the display of My entries and Position Summary widget in Leaderboard when the match/event is Live
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
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

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown_lobby_gt_live_leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown Lobby &gt; Live Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_user_should_have_teams_entered_into_the_contestnavigate_to_home_pagefootball_landing_page_and_place_the_appweb_in_backgroundor_in_idle_state_for_few_minutes_and_navigate_back_to_homepagefootball_page(self):
        """
        DESCRIPTION: User should have teams entered into the contest.
        DESCRIPTION: Navigate to Home page/Football landing page and place the app/web in background or in idle state for few minutes  and navigate back to Homepage/Football page
        EXPECTED: When navigate back to Homepage or Football page entry data should be displayed with entry of best position and Progress should be updated dynamically.
        """
        pass
