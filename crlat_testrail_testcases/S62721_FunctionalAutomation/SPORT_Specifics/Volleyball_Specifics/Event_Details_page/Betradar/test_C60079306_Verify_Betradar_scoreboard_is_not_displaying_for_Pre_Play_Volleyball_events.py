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
class Test_C60079306_Verify_Betradar_scoreboard_is_not_displaying_for_Pre_Play_Volleyball_events(Common):
    """
    TR_ID: C60079306
    NAME: Verify Betradar scoreboard is not displaying for Pre-Play Volleyball events
    DESCRIPTION: Verify that for Pre-play event the Event Details Page is not showing any scoreboard
    PRECONDITIONS: 1: Volleyball Event should be Pre-Play.
    PRECONDITIONS: 2: Betradar scoreboard configuration in CMS is enabled.
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

    def test_004_click_on_the_pre__play_event_betradar_scoreboard_mapped_to_the_event(self):
        """
        DESCRIPTION: Click on the Pre- Play Event (Betradar Scoreboard Mapped to the event)
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_betradar_scoreboard(self):
        """
        DESCRIPTION: Validate Betradar Scoreboard.
        EXPECTED: For Pre-play event the Event Details Page should be same as now in Production.(No Scoreboard widget)
        """
        pass
