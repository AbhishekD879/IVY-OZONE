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
class Test_C59551088_Verify_Betradar_Scoreboard_Statistics_tab(Common):
    """
    TR_ID: C59551088
    NAME: Verify Betradar Scoreboard- Statistics tab
    DESCRIPTION: Verify that  Statistics tab contains Match, Sets as separate inner tabs and all tabs consists of Receiver Points, Longest Streak, Total Points Won, Timeouts, Aces , Service Errors for both the teams.
    PRECONDITIONS: 1: Volleyball Event should be In-Play.
    PRECONDITIONS: 2: In Play Volleyball event should be mapped to betradar scoreboard
    PRECONDITIONS: 3: Betradar scoreboard configuration in CMS is enabled.
    PRECONDITIONS: How to configure ?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes__coral_urlfor_mobile_app_validation_open_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral URL.
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

    def test_003_click_on_volleyball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Volleyball sport from A-Z menu
        EXPECTED: User should be able to view the Volleyball Event Landing Page.
        """
        pass

    def test_004_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_click_on_statistics_tab(self):
        """
        DESCRIPTION: Click on Statistics tab
        EXPECTED: User should be able to view the Statistics tab
        """
        pass

    def test_006_validate_the_inner_tabs(self):
        """
        DESCRIPTION: Validate the inner tabs
        EXPECTED: 1: Match, Set 1, Set2, Set3, Se4 should be displayed as inner tabs
        EXPECTED: 2: User should be able to click on the tabs
        EXPECTED: 3: Each tab should contain the below information
        EXPECTED: - Service Points
        EXPECTED: - Aces
        EXPECTED: - Service Errors
        EXPECTED: - Receiver Points
        EXPECTED: - Longest Streak
        EXPECTED: - Total Points Won
        EXPECTED: - Timeouts
        EXPECTED: 4: The values for the above should be on the either side of the line for both the teams
        EXPECTED: 5: The above titles should be at the Centre of the Line
        """
        pass
