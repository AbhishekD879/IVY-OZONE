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
class Test_C29263_Launching_Stream_when_Event_is_finished(Common):
    """
    TR_ID: C29263
    NAME: Launching Stream when Event is finished
    DESCRIPTION: User is trying to launch the stream when event is finished.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. SiteServer event should be configured to support RUK/Perform streaming (**'typeFlagCodes'**='RVA) and should be mapped to RUK/Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: * isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: * or
    PRECONDITIONS: * isStarted = "false", but there are less than 2 minutes before the stream 'start time'
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 4. Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditionsduring_the_period_of_stream_from_start_time___2_min_to_start_time_plus_1_min(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
        DESCRIPTION: (During the period of Stream from 'Start Time' **- 2 Min** to 'Start Time **+ 1 Min**')
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * Stream is launched
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: * **listingUrl** attribute is received from OptIn MS to consume streaming
        EXPECTED: * The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass

    def test_003_refresh_the_event_details_page_and_tapclick_watch__live_stream_button_when_stream_is_not_activestart_time_plus_3_min___stream_start_time_can_be_taken_from_admin_in_ti(self):
        """
        DESCRIPTION: Refresh the event details page and Tap/Click 'Watch' / 'Live Stream' button when stream is not active
        DESCRIPTION: ('Start Time **+ 3 Min**' <-> Stream 'Start Time' can be taken from /admin in TI)
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "This event is over."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "This event is over."
        EXPECTED: **User is not able to watch the stream**
        """
        pass
