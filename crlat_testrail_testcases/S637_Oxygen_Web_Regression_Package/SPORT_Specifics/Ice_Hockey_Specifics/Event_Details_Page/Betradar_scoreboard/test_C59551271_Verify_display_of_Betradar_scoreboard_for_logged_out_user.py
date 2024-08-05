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
class Test_C59551271_Verify_display_of_Betradar_scoreboard_for_logged_out_user(Common):
    """
    TR_ID: C59551271
    NAME: Verify display of Betradar scoreboard for logged out user
    DESCRIPTION: This test case verifies that betradar scoreboard should be displayed even for logged out users in Ice Hockey inplay EDP
    PRECONDITIONS: 1. Ice Hockey Event should be In-Play.
    PRECONDITIONS: 2. Inplay Ice Hockey event should be subscribe to betradar scoreboard
    PRECONDITIONS: 3. Betradar scoreboard should configured and enabled in CMS
    PRECONDITIONS: 4. User is NOT logged in to the applications(Coral and Ladbrokes)
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_ice_hockey_inplay_event_landing_page_from_a_z_menu___ice_hockey___inplay_taborhome___inplay___ice_hockey(self):
        """
        DESCRIPTION: Navigate to Ice Hockey inplay event landing page from A-Z menu - Ice Hockey - inplay tab
        DESCRIPTION: Or
        DESCRIPTION: Home - Inplay - Ice Hockey
        EXPECTED: Ice Hockey event landing page should display with list of inplay events
        EXPECTED: Live now tab(# of inplay events)
        """
        pass

    def test_002_verify_ice_hockey_inplay_landing_page(self):
        """
        DESCRIPTION: verify Ice Hockey inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3. Odds should update as per feed from OB
        EXPECTED: 4. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_click_on_the_event_which_is_subscribed_to_betradar_from_precondition_and_verify_scoreboard__visualization(self):
        """
        DESCRIPTION: Click on the Event which is subscribed to betradar from precondition and verify Scoreboard & Visualization.
        EXPECTED: User should be able to view the Event Details page with Betradar Scoreboard & Visualization.
        """
        pass
