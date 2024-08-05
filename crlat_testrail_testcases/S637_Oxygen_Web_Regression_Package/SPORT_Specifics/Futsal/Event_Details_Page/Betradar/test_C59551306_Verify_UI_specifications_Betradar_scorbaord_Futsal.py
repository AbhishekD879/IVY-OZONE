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
class Test_C59551306_Verify_UI_specifications_Betradar_scorbaord_Futsal(Common):
    """
    TR_ID: C59551306
    NAME: Verify UI specifications- Betradar scorbaord Futsal
    DESCRIPTION: Verify that the Betradar scoreboard is displayed for the In-Play Futsal game in the event display page with the mentioned specifications. (In context to Dimensions, Color and Position)
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
        DESCRIPTION: Launch Ladbrokes URL
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

    def test_005_click_on_header__futsal_league_layout(self):
        """
        DESCRIPTION: click on header : Futsal league layout
        EXPECTED: TBD
        EXPECTED: Following dimensions and CSS should apply
        EXPECTED: width: 375px;
        EXPECTED: height: 42px;
        EXPECTED: background-color: #252835;
        """
        pass

    def test_006_verify_overall_dimension_of_the_screen____click_on_player_name_on_pitch(self):
        """
        DESCRIPTION: verify overall dimension of the screen -  click on player name on pitch
        EXPECTED: Following dimensions and CSS should apply
        EXPECTED: width: 375px;
        EXPECTED: height: 667px;
        """
        pass

    def test_007_verify_font_styles_in_header___click_on_table_tennis_league_text(self):
        """
        DESCRIPTION: Verify font styles in header - click on table tennis league text
        EXPECTED: color: #000000
        EXPECTED: color: rgb(0, 0, 0)
        EXPECTED: background-color: #000000
        EXPECTED: background-color: rgba(0, 0, 0, 0)
        EXPECTED: font-family (stack): Roboto, Helvetica, sans-serif
        EXPECTED: font-size: 16px
        EXPECTED: font-weight: 400
        EXPECTED: font-style: normal
        EXPECTED: text-align: start
        """
        pass
