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
class Test_C60092371_Verify_the_display_of_Go_To_5_A_Side_button_when_a_5_A_side_bet_is_Voided(Common):
    """
    TR_ID: C60092371
    NAME: Verify the display of 'Go To 5-A Side' button when a 5 A side bet is Voided
    DESCRIPTION: This test case verifies that when a 5-A side bet is voided User is displayed 'Go To 5-A Side" link is displayed in the Settled bets
    PRECONDITIONS: 1: Match should be in Pre-Play
    PRECONDITIONS: 2: Any one of the selection in 5 -A Side should be voided
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_urlapp(self):
        """
        DESCRIPTION: Launch Ladbrokes URL/app
        EXPECTED: User should be able to launch Ladbrokes URL/app
        """
        pass

    def test_002_perform_login(self):
        """
        DESCRIPTION: Perform Login
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_003_navigate_to_settled_bets_under_my_bets(self):
        """
        DESCRIPTION: Navigate to Settled bets under My bets
        EXPECTED: User should be navigated to Settled bet
        """
        pass

    def test_004_scroll_down_to_see_5_a_side_voided_bet(self):
        """
        DESCRIPTION: Scroll down to see 5-A side Voided bet
        EXPECTED: 5 A Side should be displayed
        EXPECTED: Void should be displayed
        EXPECTED: GO TO 5-A SIDE button should be displayed
        """
        pass

    def test_005_click_on_go_to_5_a_side_button(self):
        """
        DESCRIPTION: Click on GO TO 5-A SIDE button
        EXPECTED: User should be navigated to Pitch view
        """
        pass

    def test_006_validate_css_styles_for_go_to_5_a_side_button(self):
        """
        DESCRIPTION: Validate CSS styles for GO TO 5-A SIDE button
        EXPECTED: CSS styles should be as mentioned in Zeplin
        """
        pass

    def test_007_validate_the_ga_tracking_for_cta_button(self):
        """
        DESCRIPTION: Validate the GA tracking for CTA button
        EXPECTED: 
        """
        pass
