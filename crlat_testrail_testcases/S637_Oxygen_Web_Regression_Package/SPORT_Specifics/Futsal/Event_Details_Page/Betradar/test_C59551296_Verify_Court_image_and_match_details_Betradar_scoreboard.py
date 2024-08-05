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
class Test_C59551296_Verify_Court_image_and_match_details_Betradar_scoreboard(Common):
    """
    TR_ID: C59551296
    NAME: Verify Court image and match details- Betradar scoreboard
    DESCRIPTION: Verify that Futsal court is displayed as the background image and the Type, Day followed by Date & Month , Time, score are displayed on the black screen.
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

    def test_005_validate_the_screen_displayed_in_pitch_tab(self):
        """
        DESCRIPTION: Validate the Screen displayed in Pitch tab.
        EXPECTED: Futsal Court should be displayed as the background image and all the match details inside a black rectangular screen
        """
        pass

    def test_006_validate_the_match_details_content(self):
        """
        DESCRIPTION: Validate the Match details content
        EXPECTED: 1: Type should be mentioned in the top left corner with Bold font followed by Matchday
        EXPECTED: 2: Type and Matchday should be separated with "|"
        EXPECTED: 3: Date should be mentioned in the next line and the format should be day, date month ( Monday, 3 Feb) followed by Time
        EXPECTED: 4: Time format should be 24 Hrs
        """
        pass

    def test_007_validate_the_match_status_team_names_and_scores(self):
        """
        DESCRIPTION: Validate the Match Status, Team names and Scores
        EXPECTED: 1: Match Status should be in the middle of the Screen.
        EXPECTED: 2: Scores should be separated with Colon and are mentioned below the Match Status
        EXPECTED: 3: Team names are mentioned below the respective Scores
        """
        pass

    def test_008_validate_betradar_branding(self):
        """
        DESCRIPTION: Validate Betradar branding
        EXPECTED: "data by Betradar driven by facts" text should be displayed
        """
        pass
