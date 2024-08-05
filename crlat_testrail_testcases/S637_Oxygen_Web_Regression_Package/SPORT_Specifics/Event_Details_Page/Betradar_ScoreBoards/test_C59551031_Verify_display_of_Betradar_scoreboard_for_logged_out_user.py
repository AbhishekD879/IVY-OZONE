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
class Test_C59551031_Verify_display_of_Betradar_scoreboard_for_logged_out_user(Common):
    """
    TR_ID: C59551031
    NAME: Verify display of Betradar scoreboard for logged out user
    DESCRIPTION: This test case verifies that betradar scoreboard should be displayed even for logged out users in table tennis inplay EDP
    PRECONDITIONS: 1. Table tennis Event should be In-Play.
    PRECONDITIONS: 2. Inplay Table tennis event should be subscribe to betradar scoreboard
    PRECONDITIONS: 3. Betradar scoreboard should configured and enabled in CMS
    PRECONDITIONS: 4. User is NOT logged in to the applications(Coral and Ladbrokes)
    PRECONDITIONS: To map betradar scoreboard for any event follow steps-TBD
    PRECONDITIONS: XXXX
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_table_tennis_inplay_event_landing_page_from_a_z_menu___table_tennis___inplay_taborhome___inplay___table_tennis(self):
        """
        DESCRIPTION: Navigate to table tennis inplay event landing page from A-Z menu - table tennis - inplay tab
        DESCRIPTION: Or
        DESCRIPTION: Home - Inplay - table tennis
        EXPECTED: table tennis event landing page should display with list of inplay events
        EXPECTED: Live now tab(# of inplay events)
        """
        pass

    def test_002_verify_table_tennis_inplay_landing_page(self):
        """
        DESCRIPTION: verify table tennis inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3. Ball indication(Coral beside player name and Lads beside to fallback scoreboard) should display
        EXPECTED: 4. Odds should update as per feed from OB
        EXPECTED: 5. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_click_on_the_event_which_is_subscribed_to_betradar_from_precondition_and_verify_scoreboard__visualization(self):
        """
        DESCRIPTION: Click on the Event which is subscribed to betradar from precondition and verify Scoreboard & Visualization.
        EXPECTED: User should be able to view the Event Details page with Betradar Scoreboard & Visualization.
        EXPECTED: refer attached screenshot
        EXPECTED: ![](index.php?/attachments/get/105776035)
        """
        pass
