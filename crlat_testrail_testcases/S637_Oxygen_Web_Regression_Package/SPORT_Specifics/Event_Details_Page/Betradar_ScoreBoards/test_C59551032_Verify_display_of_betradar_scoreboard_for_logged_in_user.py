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
class Test_C59551032_Verify_display_of_betradar_scoreboard_for_logged_in_user(Common):
    """
    TR_ID: C59551032
    NAME: Verify display of betradar scoreboard for logged in user
    DESCRIPTION: Verify that when Betradar component is available for the table tennis sport and when the event is In Play User is able to view the Scoreboard & Visualization.
    PRECONDITIONS: 1: Table Tennis Event should be In-Play.
    PRECONDITIONS: 2: Inplay table tennis should be subscribed to betradar scoreboard
    PRECONDITIONS: 3: Betradar scoreboard configuration and enabled in CMS
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
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

    def test_003_click_on_table_tennis_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on table tennis sport from A-Z menu
        EXPECTED: User should be able to view the table tennis Event Landing Page.
        """
        pass

    def test_004_click_on_the__event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the  Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_betradar_scoreboard__visualization(self):
        """
        DESCRIPTION: Validate Betradar Scoreboard & Visualization.
        EXPECTED: User should be able to view the Betradar Scoreboard & Visualization.
        """
        pass
