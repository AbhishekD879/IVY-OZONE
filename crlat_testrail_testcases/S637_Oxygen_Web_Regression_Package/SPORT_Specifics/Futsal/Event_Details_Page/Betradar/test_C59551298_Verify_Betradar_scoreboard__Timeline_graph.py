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
class Test_C59551298_Verify_Betradar_scoreboard__Timeline_graph(Common):
    """
    TR_ID: C59551298
    NAME: Verify Betradar scoreboard - Timeline graph
    DESCRIPTION: Verify that Timeline Graph is marked with incidents (Goal and yellow/red cards) occurred during the event.
    PRECONDITIONS: 1. Futsal Event should be In-Play.
    PRECONDITIONS: 2. Inplay Futsal event should be subscribed to betradar scoreboard
    PRECONDITIONS: 3. Betradar scoreboard should configured and enabled in CMS
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: How to configure ?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_urlfor_mobile_app_validation_open_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes URL.
        DESCRIPTION: (For mobile app validation Open the App)
        EXPECTED: URL should be launched.
        """
        pass

    def test_002_click_on_login_and_enter_the_user_credentials_and_click_on_the_login_button(self):
        """
        DESCRIPTION: Click on Login and enter the User credentials and click on the Login button.
        EXPECTED: User should be successfully logged in.
        """
        pass

    def test_003_click_on_futsal_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Futsal sport from A-Z menu
        EXPECTED: User should be able to view the Futsal Event Landing Page.
        """
        pass

    def test_004_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_the_timeline_graph(self):
        """
        DESCRIPTION: Validate the Timeline graph
        EXPECTED: 1: Team names should be mentioned above and below the graph line.
        EXPECTED: 2: Graph intervals should be 0,20,40
        EXPECTED: 2: Timeline Graph should be marked with incidents (Goal and yellow/red cards) occurred during the event
        """
        pass

    def test_006_validate_the_goals_on_graph(self):
        """
        DESCRIPTION: Validate the Goals on graph
        EXPECTED: 1: Futsal ball icon should be displayed for goals
        EXPECTED: 2: Hovering on the icon goal, time and the Team name should be displayed
        """
        pass

    def test_007_validate_the_yellowred_card_incidents(self):
        """
        DESCRIPTION: Validate the Yellow/Red Card incidents
        EXPECTED: On hovering the cards icon YELLOW CARD/ RED CARD, Time and team name should be displayed
        """
        pass
