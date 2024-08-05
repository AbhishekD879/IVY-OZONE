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
class Test_C59551043_Verify_future_events_Pre_Play_are_not_showing_scoreboard(Common):
    """
    TR_ID: C59551043
    NAME: Verify future events (Pre-Play) are not showing scoreboard
    DESCRIPTION: Test case verifies table tennis future events should not show any scoreboards
    PRECONDITIONS: 1. Betradar scoreboard should enable in CMS - system configuration - config - Betradarscoreboard
    PRECONDITIONS: 2. Fallback scoreboard should enable in CMS - system configuration - config - Fallbackscoreboard
    PRECONDITIONS: 3. Future Table tennis event(s) should present and subscribed to betradar scoreboard
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_a_z_menu___table_tennis___matches_tab(self):
        """
        DESCRIPTION: Launch the application and navigate to A-Z menu - table tennis - matches tab
        EXPECTED: All the matches(Today,tomorrow and future) should display
        """
        pass

    def test_002_click_on_any_event_and_verify(self):
        """
        DESCRIPTION: click on any event and verify
        EXPECTED: Event details with markets and odds should display
        """
        pass

    def test_003_repeat_above_step_for_the_events_from_tomorrow_and_future_tab(self):
        """
        DESCRIPTION: Repeat above step for the events from tomorrow and future tab
        EXPECTED: 
        """
        pass
