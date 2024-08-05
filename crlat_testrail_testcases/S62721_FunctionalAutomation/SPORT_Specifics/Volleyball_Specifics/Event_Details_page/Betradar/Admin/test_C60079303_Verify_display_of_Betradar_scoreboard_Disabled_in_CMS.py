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
class Test_C60079303_Verify_display_of_Betradar_scoreboard_Disabled_in_CMS(Common):
    """
    TR_ID: C60079303
    NAME: Verify display of Betradar scoreboard- Disabled in CMS
    DESCRIPTION: Verify that Betradar Scoreboard & Visualization is NOT displayed in Event Details Page when Betradar Scoreboard is disabled in CMS
    PRECONDITIONS: 1: User should have access to CMS
    PRECONDITIONS: 2: Betradar component should be mapped to the event
    PRECONDITIONS: 3: Fallback Scoreboard should be enabled in CMS by default
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be able to login as Admin
        """
        pass

    def test_002_navigate_to_bet_radar_section_from_cms___system_configuration___config___bet_radar_scoreboard(self):
        """
        DESCRIPTION: Navigate to bet radar section from CMS - system configuration - config - bet radar scoreboard
        EXPECTED: User should be able to view the Betradar Scoreboard component
        """
        pass

    def test_003_disable_the_betradar_scoreboard_in_cms_and_click_on_save_changes(self):
        """
        DESCRIPTION: Disable the Betradar Scoreboard in CMS and click on Save changes
        EXPECTED: User should be able to save the changes made
        """
        pass

    def test_004_launch_ladbrokes__coral_urlfor_mobile_app_validation_open_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral URL.
        DESCRIPTION: (For mobile app validation Open the App)
        EXPECTED: URL should be launched.
        """
        pass

    def test_005_click_on_login_and_enter_the_user_credentials_and_click_on_the_login_button(self):
        """
        DESCRIPTION: Click on Login and enter the User credentials and click on the Login button.
        EXPECTED: User should be successfully logged in.
        """
        pass

    def test_006_click_on_volleyball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Volleyball sport from A-Z menu
        EXPECTED: User should be able to view the Volleyball Event Landing Page.
        """
        pass

    def test_007_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_008_validate_betradar_scoreboard(self):
        """
        DESCRIPTION: Validate Betradar Scoreboard
        EXPECTED: 1: User should NOT be able to see the Betradar Scoreboard & Visualisation.
        EXPECTED: 2: User should be able to view the Fallback Scoreboard
        """
        pass
