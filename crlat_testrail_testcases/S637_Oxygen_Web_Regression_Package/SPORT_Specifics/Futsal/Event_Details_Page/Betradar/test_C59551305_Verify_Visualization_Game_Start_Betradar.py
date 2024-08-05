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
class Test_C59551305_Verify_Visualization_Game_Start_Betradar(Common):
    """
    TR_ID: C59551305
    NAME: Verify Visualization- Game Start- Betradar
    DESCRIPTION: Verify that when Event comes to In Play Visualization is displayed with Futsal ball and Players positions
    PRECONDITIONS: 1. Futsal Event should be In-Play.
    PRECONDITIONS: 2. Inplay Futsal event should be subscribe to betradar scoreboard
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

    def test_005_validate_visualization(self):
        """
        DESCRIPTION: Validate Visualization
        EXPECTED: 1: Futsal Court should be displayed
        EXPECTED: 2: Player Positions should be displayed
        EXPECTED: 3: Ball Position should be displayed
        """
        pass
