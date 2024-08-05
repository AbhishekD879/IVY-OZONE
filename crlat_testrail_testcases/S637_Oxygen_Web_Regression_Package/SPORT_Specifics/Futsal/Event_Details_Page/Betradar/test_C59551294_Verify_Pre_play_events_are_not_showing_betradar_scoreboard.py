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
class Test_C59551294_Verify_Pre_play_events_are_not_showing_betradar_scoreboard(Common):
    """
    TR_ID: C59551294
    NAME: Verify Pre-play events are not showing betradar scoreboard
    DESCRIPTION: Verify that for Pre-play event the Event Details Page is not showing any scoreboard
    PRECONDITIONS: 1. Futsal Event should be In-Play.
    PRECONDITIONS: 2. Betradar scoreboard should be configured and enabled in CMS
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

    def test_002_click_on_futsal_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Futsal sport from A-Z menu
        EXPECTED: User should be able to view the Futsal Event Landing Page.
        """
        pass

    def test_003_click_on_pre__play_event__betradar_scoreboard_mapped_to_the_event(self):
        """
        DESCRIPTION: Click on Pre- Play Event ( Betradar scoreboard mapped to the Event)
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_004_validate_betradar_scoreboard(self):
        """
        DESCRIPTION: Validate Betradar Scoreboard.
        EXPECTED: For Pre-play event the Event Details Page should be same as now in Production.(No Scoreboard widget)
        """
        pass
