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
class Test_C60034281_Verify_absence_of_accountHistory_request_for_Perform_sport_streams(Common):
    """
    TR_ID: C60034281
    NAME: Verify absence of accountHistory request for Perform sport streams
    DESCRIPTION: This test case verifies absence of BPP accountHistory request when starting Perform sport stream
    PRECONDITIONS: 1.1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 1.2. The event should have the following attributes:
    PRECONDITIONS: * isStarted = "true"
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 1.3. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: Endpoints of Opt-In MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_the_sport_event_with_mapped_perform_stream(self):
        """
        DESCRIPTION: Navigate to EDP of the sport event with mapped Perform stream
        EXPECTED: * EDP is loaded
        EXPECTED: * 'Watch live' or 'Watch' button is present
        """
        pass

    def test_002__press_watch_live_or_watch_button_check_requests_in_devtools_network_tab(self):
        """
        DESCRIPTION: * Press 'Watch live' or 'Watch' button
        DESCRIPTION: * Check requests in devtools Network tab
        EXPECTED: There is NO request to BPP /Proxy/accountHistory?
        """
        pass
