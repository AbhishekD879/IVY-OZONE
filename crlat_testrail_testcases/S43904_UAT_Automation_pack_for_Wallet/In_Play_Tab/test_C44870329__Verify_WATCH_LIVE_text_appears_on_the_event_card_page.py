import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870329__Verify_WATCH_LIVE_text_appears_on_the_event_card_page(Common):
    """
    TR_ID: C44870329
    NAME: "-Verify WATCH LIVE' text appears on the event card page"
    DESCRIPTION: "-Verify Watching now' text appears on the event card when 'In-Play' switcher is selected for active streame
    DESCRIPTION: - Verify only stream applicable events are available on Watch page"
    DESCRIPTION: -This test case verifies "Watch live" page in In-Play sports ribbon
    PRECONDITIONS: Login to site or app and navigate to "In-Play" tab
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_watch_live_icon_in_play_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify displaying of "Watch Live" icon In-Play Sports Ribbon tab
        EXPECTED: "Watch Live" icon is displayed as the FIRST icon in the ribbon
        """
        pass

    def test_002_verify_default_users_navigation_after_in_play_tab_opening(self):
        """
        DESCRIPTION: Verify default user's navigation after In-Play tab opening
        EXPECTED: The user is landed on the FIRST sport in the ribbon by default (not the Watch Live tab)
        """
        pass

    def test_003_click_on_watch_live_iconverify_displaying_of_events_with_mapped_streams_in_inplay_and_upcoming_sections(self):
        """
        DESCRIPTION: Click on "Watch Live" icon
        DESCRIPTION: Verify displaying of events with mapped streams in Inplay and upcoming sections
        EXPECTED: "Watch Live" page is opened
        EXPECTED: Inplay and upcoming sections are displayed
        EXPECTED: Events which are not started are displayed in "Upcoming" section
        EXPECTED: Events without available stream are not displayed in "Watch live" page
        """
        pass

    def test_004_for_desktopgo_to_hp__in_play_and_live_stream_module_is_displayedverify_displaying_of_watch_live_icon_in_in_play_and_live_stream_ribbon(self):
        """
        DESCRIPTION: For Desktop:
        DESCRIPTION: Go to HP > "In-Play and Live Stream" module is displayed
        DESCRIPTION: Verify displaying of "Watch Live" icon in "In-Play and Live Stream" Ribbon
        EXPECTED: "Watch Live" icon is not displayed in "In-Play and Live Stream" Ribbon
        """
        pass
