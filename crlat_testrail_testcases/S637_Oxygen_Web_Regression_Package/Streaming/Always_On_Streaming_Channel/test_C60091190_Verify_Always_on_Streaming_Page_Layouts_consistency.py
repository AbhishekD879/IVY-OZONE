import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60091190_Verify_Always_on_Streaming_Page_Layouts_consistency(Common):
    """
    TR_ID: C60091190
    NAME: Verify Always on Streaming Page Layouts consistency
    DESCRIPTION: This test case verifies behaviour of resulted event(s) at Always On Streaming Page
    PRECONDITIONS: Always On Streaming (Ladbrokes/Coral TV) event(s) are available:
    PRECONDITIONS: typeFlagCodes = 'GVA' AND drilldownTagNames = 'EVFLAG_GAO' + LCGSISSWOGH stream is mapped
    """
    keep_browser_open = True

    def test_001_navigate_to_active_not_started_event_within_always_on_streaming_page_ladbrokescoral_tv_meeting_view(self):
        """
        DESCRIPTION: Navigate to active (not started) event within Always On Streaming Page (Ladbrokes/Coral TV Meeting View)
        EXPECTED: - Active event is displayed as the default view
        EXPECTED: - Only the active events displayed within the top navigation
        """
        pass

    def test_002_stay_on_the_page_and_wait_until_event_is_startedresulted(self):
        """
        DESCRIPTION: Stay on the page and wait until event is started/resulted
        EXPECTED: Page is displayed with suspended selections
        """
        pass

    def test_003_refresh_page_while_event_is_still_startedresulted(self):
        """
        DESCRIPTION: Refresh page (while event is still started/resulted)
        EXPECTED: - User is redirected from Always On Streaming Page (Ladbrokes/Coral TV Meeting View) to event EDP of corresponding meeting
        EXPECTED: - All selections are suspended (if event is started) or event results are displayed (if event is resulted)
        """
        pass

    def test_004_navigate_again_to_active_not_started_event_within_always_on_streaming_page_ladbrokescoral_tv_meeting_view_stay_on_the_page_and_wait_until_event_is_startedresulted_and_select_next_available_not_started_event_within_top_navigation(self):
        """
        DESCRIPTION: Navigate again to active (not started) event within Always On Streaming Page (Ladbrokes/Coral TV Meeting View), stay on the page and wait until event is started/resulted and select next available (not started) event within top navigation
        EXPECTED: - Started/Resulted event is removed from the Meeting view
        EXPECTED: - User is transitioned to the selected event
        EXPECTED: - Only the active events displayed within the top navigation
        """
        pass
