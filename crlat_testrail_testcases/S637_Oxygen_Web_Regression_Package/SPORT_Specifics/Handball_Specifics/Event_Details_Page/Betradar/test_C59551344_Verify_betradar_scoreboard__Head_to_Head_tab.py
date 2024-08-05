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
class Test_C59551344_Verify_betradar_scoreboard__Head_to_Head_tab(Common):
    """
    TR_ID: C59551344
    NAME: Verify betradar scoreboard - Head to Head tab
    DESCRIPTION: Verify the Head to Head tab contains Previous meetings information like WINS , Draws, Scores, Conceded, League Position and Form
    PRECONDITIONS: 1. Handball Event should be In-Play.
    PRECONDITIONS: 2. Inplay Handball event should be subscribe to betradar scoreboard
    PRECONDITIONS: 3. Betradar scoreboard should configured and enabled in CMS
    PRECONDITIONS: How to configure ?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
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

    def test_003_click_on_handball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Handball sport from A-Z menu
        EXPECTED: User should be able to view the Handball Event Landing Page.
        """
        pass

    def test_004_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_click_on_head_to_head_tab_in_the_betradar_scoreboard_section(self):
        """
        DESCRIPTION: Click on Head to Head tab in the Betradar Scoreboard section
        EXPECTED: User should be able to view the Head to Head tab
        """
        pass

    def test_006_validate_head_to_head_tab(self):
        """
        DESCRIPTION: Validate Head to Head Tab
        EXPECTED: Below Sections should be displayed
        EXPECTED: 1. Previous meetings
        EXPECTED: 2: Scored
        EXPECTED: 3: Conceded
        EXPECTED: 4: League Position
        """
        pass

    def test_007_validate_previous_meetings(self):
        """
        DESCRIPTION: Validate Previous Meetings
        EXPECTED: 1. WINS of both the teams, Draws information should be displayed on a line graph
        EXPECTED: 2. Home Team WINS, DRAW, Away Team WINS differentiated by line color
        """
        pass

    def test_008_validate_scored(self):
        """
        DESCRIPTION: Validate Scored
        EXPECTED: Home and Away team Scored should be displayed on a line graph differentiated by color.
        """
        pass

    def test_009_validate_conceded(self):
        """
        DESCRIPTION: Validate Conceded
        EXPECTED: Home and Away team Conceded should be displayed on a line graph differentiated by color.
        """
        pass

    def test_010_validate_league_position(self):
        """
        DESCRIPTION: Validate League Position
        EXPECTED: 1: League position data should be displayed at the center
        EXPECTED: 2: Form data should be on the either side
        EXPECTED: 3: Last 5 matches win/loss history should display in tiles
        """
        pass
