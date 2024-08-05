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
class Test_C59551335_Verify_Betradar_scoreboard__Timeline(Common):
    """
    TR_ID: C59551335
    NAME: Verify Betradar scoreboard - Timeline
    DESCRIPTION: Verify that the occurrence of all incidents like Goal, Corner Kick, Free Kick, Kick in and Match status are displayed in Timeline tab with Time, Silk, and the sign representing the incident under First Half or Second Half.
    PRECONDITIONS: 1.  Handball Event should be In-Play.
    PRECONDITIONS: 2. Inplay Handball  event should be subscribe to betradar scoreboard
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

    def test_003_click_on_handball__sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Handball  sport from A-Z menu
        EXPECTED: User should be able to view the Handball  Event Landing Page.
        """
        pass

    def test_004_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_click_on_the_hamburger_menu_beside_the_tabs_in_betradar_scoreboard(self):
        """
        DESCRIPTION: Click on the hamburger menu beside the tabs in betradar scoreboard
        EXPECTED: User should be able to view Timeline title
        """
        pass

    def test_006_click_on_the_timeline(self):
        """
        DESCRIPTION: Click on the Timeline
        EXPECTED: User should be able to view the Timeline tab
        """
        pass

    def test_007_validate_the_incidents_data_in_timeline_tab(self):
        """
        DESCRIPTION: Validate the Incidents data in Timeline tab
        EXPECTED: 1: Timeline tab should be categorized as two - 2nd Half, 1st Half
        EXPECTED: 2: By Default 1st half should be expanded
        EXPECTED: 3: 2nd Half is collapsed
        EXPECTED: 4: At the 1st and 2nd Half header sections Goal scores should be mentioned (0-4)
        EXPECTED: 5: Inside the  1st Half header a sub header should be there '<icon>' '1st Half'
        EXPECTED: 6: The incidents occurred in the First Half of the game should be mentioned sorted by Time
        EXPECTED: 7: Time | Shirt icon| Incident icon and the Incident name in the Next line
        EXPECTED: 8: If the Incident is a goal at the other end Score should be mentioned (0-3)
        EXPECTED: 9: Inside the  2nd Half header a sub header should be there '<icon>' 'End of game'
        """
        pass

    def test_008_validate_expandcollapse_of_the_sections(self):
        """
        DESCRIPTION: Validate Expand/Collapse of the sections
        EXPECTED: User should be able to Expand & Collapse 1st Half and 2nd Half sections
        """
        pass
