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
class Test_C1493963_Verify_Match_Time_updates_for_Hero_Module(Common):
    """
    TR_ID: C1493963
    NAME: Verify Match Time updates for Hero Module
    DESCRIPTION: This test case verifies Match Time updates for Hero Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * To check data correctness and updates from In Play and Live Serve MS open Dev Tools -> Network tab -> WS -> select '?EIO=3&transport=websocket' request
    PRECONDITIONS: **NOTE** Currently Match Time is implemented for Football ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_hero_module_next_events_module_for_live_events___event_with_match_time_available(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events) -> event with Match Time available
        EXPECTED: Event with Match Time is present within Hero Module
        """
        pass

    def test_004_verify_match_time_displaying(self):
        """
        DESCRIPTION: Verify Match Time displaying
        EXPECTED: Match Time is displayed in the following format:
        EXPECTED: 'MM:SS'
        EXPECTED: where
        EXPECTED: MM - minutes
        EXPECTED: SS - seconds
        """
        pass

    def test_005_verify_match_time_correctness(self):
        """
        DESCRIPTION: Verify Match Time correctness
        EXPECTED: Match Time value corresponds to **[i].initClock.offset_secs** / 60 on the lattest **period_code=FIRST_HALF/SECOND_HALF** in WS response
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass

    def test_006_verify_event_in_half_time(self):
        """
        DESCRIPTION: Verify event in Half Time
        EXPECTED: * **'HT'** label is shown instead of Match Time
        EXPECTED: * Half Time is present when **[i].initClock.state=S** on **period_code="HALF_TIME"** in WS response
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass
