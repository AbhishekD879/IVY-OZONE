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
class Test_C1493960_Verify_Hero_Module_data_correctness(Common):
    """
    TR_ID: C1493960
    NAME: Verify Hero Module data correctness
    DESCRIPTION: This test case verifies Hero Module data correctness on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * To check data correctness and updates from In Play and Live Serve MS open Dev Tools -> Network tab -> WS -> select '?EIO=3&transport=websocket' request
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

    def test_003_go_to_hero_module_next_events_module_for_live_events(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events)
        EXPECTED: 
        """
        pass

    def test_004_verify_events_filtering_within_hero_module(self):
        """
        DESCRIPTION: Verify events filtering within Hero Module
        EXPECTED: Events are filtered according to:
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * Main market is displayed (available in the response)
        """
        pass

    def test_005_verify_events_ordering_within_hero_module(self):
        """
        DESCRIPTION: Verify events ordering within Hero Module
        EXPECTED: Events are order according to staring time, that corresponds to **[i].startTime** attribute
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass

    def test_006_verify_homedrawaway_prices(self):
        """
        DESCRIPTION: Verify Home/Draw/Away prices
        EXPECTED: Away team name corresponds to **[i].markets.outcomes.prices**
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass

    def test_007_verify_primary_market_correctness(self):
        """
        DESCRIPTION: Verify Primary market correctness
        EXPECTED: Primary market name corresponds to **[i].markets.name**
        EXPECTED: where
        EXPECTED: i - the number of events returned for type
        """
        pass
