import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59888573_Verify_there_are_no_StatsCenter_API_calls_when_loading_Football_Event_Details_Page(Common):
    """
    TR_ID: C59888573
    NAME: Verify there are no StatsCenter API calls when loading Football Event Details Page
    DESCRIPTION: This test case verified there are no StatsCenter API calls when loading Football EDP
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Open browser Dev Tools -> Network tab
    PRECONDITIONS: 3. Navigate to Football Event Details Page
    """
    keep_browser_open = True

    def test_001_check_browser_network_tab_for_brcompetitionseason_eg_httpsstats_centrecoralcoukapibrcompetitionseason16105500_and_seasons_eg_httpsstats_centrecoralcoukapiseasons13042_requests(self):
        """
        DESCRIPTION: Check browser Network tab for /brcompetitionseason (e.g. https://stats-centre.coral.co.uk/api/brcompetitionseason/16/105/500) and /seasons (e.g. https://stats-centre.coral.co.uk/api/seasons/1/30/42) requests
        EXPECTED: * /brcompetitionseason request is NOT loaded in Network
        EXPECTED: * /seasons request is NOT loaded
        EXPECTED: * All page contents (all markets and selections) loaded and displayed. No errors.
        """
        pass

    def test_002_switch_between_market_tabs(self):
        """
        DESCRIPTION: Switch between market tabs
        EXPECTED: * /brcompetitionseason request is NOT loaded in Network
        EXPECTED: * /seasons request is NOT loaded
        EXPECTED: * All page contents (all markets and selections) loaded and displayed. No errors.
        """
        pass
