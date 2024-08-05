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
class Test_C59551072_Verify_Fallback_Scoreboard_when_Betradar_is_not_mapped_to_the_event(Common):
    """
    TR_ID: C59551072
    NAME: Verify Fallback Scoreboard when Betradar is not mapped to the event
    DESCRIPTION: Verify Fallback Scoreboard when Betradar is not mapped to the event
    PRECONDITIONS: 1: Volleyball Event should be In-Play.
    PRECONDITIONS: 2: Betradar component is not mapped to event
    PRECONDITIONS: 3: Betradar scoreboard is enabled in CMS
    PRECONDITIONS: 4: Fallback scoreboard should be enabled by default in CMS
    PRECONDITIONS: How to Configure CMS?
    PRECONDITIONS: CMS > System Configuration > Structure > Fallback Scoreboard
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

    def test_004_click_on_the_event_betradar_scoreboard_is_available_but_not_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard is available but NOT mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_fallback_scoreboard(self):
        """
        DESCRIPTION: Validate Fallback Scoreboard
        EXPECTED: User should be able to view the Fallback Scoreboard
        """
        pass
