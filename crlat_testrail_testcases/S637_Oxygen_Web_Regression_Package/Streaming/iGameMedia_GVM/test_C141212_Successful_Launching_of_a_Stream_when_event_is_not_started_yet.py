import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C141212_Successful_Launching_of_a_Stream_when_event_is_not_started_yet(Common):
    """
    TR_ID: C141212
    NAME: Successful Launching of a Stream when event is not started yet
    DESCRIPTION: This test case verifies launching the stream by the user when event is not started, and less than 2 minutes left before event Start Time
    DESCRIPTION: Applies to Greyhounds Racing events
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming (**'drilldownTagNames'** ='EVFLAG_GVM' and **'typeFlagCodes'='GVA'** flags should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: 3. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: for <Race> events:
    PRECONDITIONS: *   isStarted = "false"; it should be less than 2 minutes left before event Start Time.
    PRECONDITIONS: The following parameters should be received in Optin MS response in order play IGMedia stream on mentioned devices/platforms:
    PRECONDITIONS: mobile: ['HLS-LOW'],
    PRECONDITIONS: wrapper: ['HLS-LOW-RAW'] (video URL link is available and native player works as expected, in another case - error that stream is not available is displayed),
    PRECONDITIONS: tablet: ['HLS-HIGH', 'HLS-LOW'],
    PRECONDITIONS: desktop: ['HLS-WEB', 'DASH', 'RTMP-HIGH']
    PRECONDITIONS: Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_eventgreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Greyhounds Racing) which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_place_a_minimum_sum_of_1_15_15_on_1_or_many_selections_within_the_tested_event(self):
        """
        DESCRIPTION: Place a minimum sum of 1£ (1.5$, 1.5Є) on 1 or many selections within the tested event
        EXPECTED: 
        """
        pass

    def test_003_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: - The Video player is shown above market tabs
        EXPECTED: - The Video stream is shown within the player
        EXPECTED: (Ladbrokes)
        EXPECTED: - Stream button changes from 'Watch' to 'Done'
        EXPECTED: (Coral)
        EXPECTED: - Stream button remains 'Live Stream' when clicked on.
        EXPECTED: XHR - optin response contains iGameMedia 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/11918131)
        """
        pass
