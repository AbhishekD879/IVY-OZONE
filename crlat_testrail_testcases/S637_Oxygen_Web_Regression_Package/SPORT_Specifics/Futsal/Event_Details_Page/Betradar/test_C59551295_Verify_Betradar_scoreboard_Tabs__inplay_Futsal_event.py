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
class Test_C59551295_Verify_Betradar_scoreboard_Tabs__inplay_Futsal_event(Common):
    """
    TR_ID: C59551295
    NAME: Verify Betradar scoreboard Tabs - inplay Futsal event
    DESCRIPTION: Test case verifies In-Play Futsal event is displayed the Betradar scoreboard with following tabs
    DESCRIPTION: 1. Pitch
    DESCRIPTION: 2. Statistics
    DESCRIPTION: 3. Head to Head
    DESCRIPTION: 4. Standing
    DESCRIPTION: 5. Timeline
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

    def test_005_validate_tabs_displayed_in_betradar_scoreboard(self):
        """
        DESCRIPTION: Validate tabs displayed in Betradar Scoreboard
        EXPECTED: User should be able to view the following tabs
        EXPECTED: 1: Pitch
        EXPECTED: 2: Statistics
        EXPECTED: 3: Head to Head
        EXPECTED: 4: Standing
        EXPECTED: 5: Timeline
        EXPECTED: Before the tab names logo or sign should be displayed
        """
        pass

    def test_006_verify_default_view_of_tabs(self):
        """
        DESCRIPTION: Verify default view of tabs
        EXPECTED: by default only 4 tabs should display and for the 5th tab should display when click on Hamburger menu
        """
        pass
