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
class Test_C59551347_Verify_Betradar_scoreboard_Tabs__inplay_Handball_event(Common):
    """
    TR_ID: C59551347
    NAME: Verify Betradar scoreboard Tabs - inplay Handball event
    DESCRIPTION: Test case verifies In-Play Handball event is displayed the Betradar scoreboard with following tabs
    DESCRIPTION: 1. Statistics
    DESCRIPTION: 2. Head to Head
    DESCRIPTION: 3. Standing
    DESCRIPTION: 4. Timeline
    DESCRIPTION: 5. Linesups
    PRECONDITIONS: 1. Handball Event should be In-Play.
    PRECONDITIONS: 2. Inplay Handball event should be subscribed to betradar scoreboard
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

    def test_005_validate_tabs_displayed_in_betradar_scoreboard(self):
        """
        DESCRIPTION: Validate tabs displayed in Betradar Scoreboard
        EXPECTED: User should be able to view the following tabs
        EXPECTED: 1. Statistics
        EXPECTED: 2. Head to Head
        EXPECTED: 3. Standing
        EXPECTED: 4. Timeline
        EXPECTED: 5. Linesups
        EXPECTED: Before the tab names logo or sign should be displayed
        """
        pass

    def test_006_verify_default_view_of_tabs(self):
        """
        DESCRIPTION: Verify default view of tabs
        EXPECTED: by default only 4 tabs should display and for the 5th tab should display when click on Hamburger menu
        """
        pass
