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
class Test_C59551345_Verify_display_of_Betradar_scoreboard_for_inplay_Handball_event_when_User_is_NOT_logged_in(Common):
    """
    TR_ID: C59551345
    NAME: Verify display of Betradar scoreboard for inplay Handball event when User is NOT logged in
    DESCRIPTION: Test case verifies that even if User is NOT logged in, he should able to view the Betradar Scoreboard & Visualization for the inplay Handball event which is subscribed to betradar component
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

    def test_002_click_on_handball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Handball sport from A-Z menu
        EXPECTED: User should be able to view the Handball Event Landing Page.
        """
        pass

    def test_003_click_on_the_event_betradar_scoreboard_mapped_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard mapped to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_004_validate_betradar_scoreboard__visualisation(self):
        """
        DESCRIPTION: Validate Betradar Scoreboard & Visualisation.
        EXPECTED: User should be able to view the Betradar Scoreboard & Visualisation.
        """
        pass
