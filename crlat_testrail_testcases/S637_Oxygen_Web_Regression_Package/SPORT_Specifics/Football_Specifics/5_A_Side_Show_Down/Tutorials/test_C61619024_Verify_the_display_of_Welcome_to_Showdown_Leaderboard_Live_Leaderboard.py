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
class Test_C61619024_Verify_the_display_of_Welcome_to_Showdown_Leaderboard_Live_Leaderboard(Common):
    """
    TR_ID: C61619024
    NAME: Verify the display of Welcome to Showdown Leaderboard-Live Leaderboard
    DESCRIPTION: This Test Case Verifies the display of  Welcome to Showdown Leaderboard in Live Leaderboard
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

    def test_002_navigate_to_5_a_side_showdown_lobby_from_homepageedp_pagefb_slpmy_betsbet_receipt(self):
        """
        DESCRIPTION: Navigate to 5-A Side Showdown Lobby from Homepage/EDP page/FB SLP/My bets/Bet receipt.
        EXPECTED: User should be navigated to 5-A-Side showdown lobby.
        """
        pass

    def test_003_click_on_any_card_which_has_live_icon(self):
        """
        DESCRIPTION: Click on any card which has "Live" icon
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
