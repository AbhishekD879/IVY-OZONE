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
class Test_C60079311_Verify_Betradar_Scoreboard_Pitch_Tab(Common):
    """
    TR_ID: C60079311
    NAME: Verify Betradar Scoreboard- Pitch Tab
    DESCRIPTION: Verify that Betradar scoreboard contains the Category, Type & Match Timings as Day, Date Month and Time with (EST/CST/IST) mentioned Match Status, Silks & Team names with scores in one slide and Form Details on the other slide in the Pitch Tab
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

    def test_005_validate_the_match_details_content(self):
        """
        DESCRIPTION: Validate the Match details content
        EXPECTED: 1: Type should be mentioned in the top left corner with Bold font followed by Matchday
        EXPECTED: 2: Type and Matchday should be separated with "|"
        EXPECTED: 3: Date should be mentioned in the next line and the format should be day, date month ( Monday, 3 Feb) followed by Time
        EXPECTED: 4: Time format should be 24 Hrs
        """
        pass

    def test_006_validate_the_match_status_team_names_and_scores(self):
        """
        DESCRIPTION: Validate the Match Status, Team names and Scores
        EXPECTED: 1: Match Status should be in the middle of the Screen.
        EXPECTED: 2: Scores should be displayed  below the Match Status
        EXPECTED: 3: Team names are mentioned below the respective Scores
        """
        pass

    def test_007_validate_the_second_slide_in_pitch_tab(self):
        """
        DESCRIPTION: Validate the second slide in Pitch tab
        EXPECTED: 1: Team form should be the header for the next slide
        EXPECTED: 2: Form details should be on the either side for both the Teams
        """
        pass
