import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551289_Verify_display_of_betradar_Scoreboard_Visualization_for_Ice_Hockey_event_when_Betradar_Scoreboard_is_enabled_in_CMS(Common):
    """
    TR_ID: C59551289
    NAME: Verify display of betradar Scoreboard & Visualization for Ice Hockey event when Betradar Scoreboard is enabled in CMS
    DESCRIPTION: Test case verifies the view of Scoreboard & Visualization in EDP when Betradar Scoreboard is enabled in CMS
    PRECONDITIONS: 1. Betradar scoreboard should enable in CMS - system configuration - config - Betradar scoreboard
    PRECONDITIONS: 2. In play Ice Hockey event(s) should present and subscribed to betradar scoreboard
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_ice_hockey_edp_from_home___ice_hockey___inplay(self):
        """
        DESCRIPTION: Launch the application and navigate to Ice Hockey EDP from Home - Ice Hockey - inplay
        EXPECTED: Ice Hockey events should display with player names, live icon, fallback scoreboard default markets odds and link with all other markets
        """
        pass

    def test_002_verify_ice_hockey_inplay_landing_page(self):
        """
        DESCRIPTION: verify Ice Hockey inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3. Pluck indication(Coral beside player name and Lads beside to fallback scoreboard) should display
        EXPECTED: 4. Odds should update as per feed from OB
        EXPECTED: 5. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_click_on_any_inplay_event_and_verify(self):
        """
        DESCRIPTION: click on any inplay event and verify
        EXPECTED: 1. Event name with back icon at top left corner and live icon event time and date should display
        EXPECTED: 2. betradar scoreboard should display
        EXPECTED: 3. Scoreboard should updated as per the feed from betradar
        EXPECTED: 4. Below to the scoreboard all the markets should display with respective odds
        """
        pass

    def test_004_compare_scoreboard_in_both_the_brandslads_and_coral(self):
        """
        DESCRIPTION: Compare scoreboard in both the brands(Lads and Coral)
        EXPECTED: Score should match in both the screens and there should not any delay
        """
        pass
