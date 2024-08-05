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
class Test_C60088418_Verify_displaying_of_Sign_Posting(Common):
    """
    TR_ID: C60088418
    NAME: Verify displaying of Sign Posting
    DESCRIPTION: This test case verifies displaying of Always On Streaming sign posting icon next to the Greyhound Race event name across all different areas of the app (Next races, EDP etc.)
    PRECONDITIONS: Always On Streaming (Ladbrokes/Coral TV) event(s) are available:
    PRECONDITIONS: typeFlagCodes = 'GVA' AND drilldownTagNames = 'EVFLAG_GAO' + LCGSISSWOGH stream is mapped
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhound_landing_page_and_check_events_within_next_races_available_for_the_always_on_streaming_channelby_defaultcoral___gh_lp__today_tab__next_races_moduleladbrokes___gh_lp__next_races_tab(self):
        """
        DESCRIPTION: Navigate to Greyhound landing page and check events within Next Races available for the Always On Streaming Channel
        DESCRIPTION: By default:
        DESCRIPTION: Coral - GH LP > Today tab > Next Races module
        DESCRIPTION: Ladbrokes - GH LP > Next Races tab
        EXPECTED: Signposting icon is displayed next to event(s) name
        EXPECTED: ![](index.php?/attachments/get/122186912) ![](index.php?/attachments/get/122186913)
        """
        pass

    def test_002_navigate_to_edp_with_always_on_streaming_channel_available(self):
        """
        DESCRIPTION: Navigate to EDP with Always On Streaming Channel available
        EXPECTED: Signposting icon is displayed next to event name
        EXPECTED: ![](index.php?/attachments/get/122186917) ![](index.php?/attachments/get/122186918)
        """
        pass
