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
class Test_C59551342_Verify_betradar_scoreboard__lineups_tab__Hamburger_menu(Common):
    """
    TR_ID: C59551342
    NAME: Verify betradar scoreboard - lineups tab  - Hamburger menu
    DESCRIPTION: Verify that Betradar scoreboard contains lineups
    PRECONDITIONS: 1. Handball Event should be In-Play.
    PRECONDITIONS: 2. Inplay Handball  event should be subscribed to betradar scoreboard
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

    def test_005_validate_the_screen_displayed_in_lineups_tab(self):
        """
        DESCRIPTION: Validate the Screen displayed in lineups tab.
        EXPECTED: Lineups tab - Hamburger menu will display only when the tabs are not fitting in default view of scoreboard
        EXPECTED: for eg : in mobile or desktop view if we have 8 tabs and only 5 tabs are fitting in default view then remaining 3 tabs should display in  Hamburger menu.
        EXPECTED: User should able to click and view data in respective tabs
        """
        pass
