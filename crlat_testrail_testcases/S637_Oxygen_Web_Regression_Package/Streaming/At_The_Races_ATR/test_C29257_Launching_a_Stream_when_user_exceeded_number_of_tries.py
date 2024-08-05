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
class Test_C29257_Launching_a_Stream_when_user_exceeded_number_of_tries(Common):
    """
    TR_ID: C29257
    NAME: Launching a Stream when user exceeded number of tries
    DESCRIPTION: This test case verifies launching the stream by the user when number of tries to launch a stream is exceeded.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. SiteServer event should be configured to support ATR streaming (**'drilldownTagNames'**='EVFLAG_AVA' flag should be set) and should be mapped to ATR stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: * isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: * or
    PRECONDITIONS: * isStarted = "false", but there are less than 2 minutes before the stream 'start time'
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 4. Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    PRECONDITIONS: ** It is also possible to achieve the expected result of step #3 by tapping/clicking 'Watch'/'Live Stream' and 'Live Stream'/'Done' buttons when there are less than 2 minutes before event start.**
    """
    keep_browser_open = True

    def test_001_re_open_event_details_page_of_the_specific_racefor_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: (Re-)Open Event Details page of the specific <Race>for the event which satisfies Preconditions
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
        EXPECTED: priorityProviderCode: "ATR"
        EXPECTED: priorityProviderName: "At The Races"
        EXPECTED: }
        """
        pass

    def test_003_repeat_steps_1_2_10_more_times(self):
        """
        DESCRIPTION: Repeat steps #1-#2 '10' more times
        EXPECTED: Following message/pop up is shown instead of a videoplayer on the 11th execution of step 2:
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "Your limit for streaming has been exceeded. Please try again later."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "Your limit for streaming has been exceeded. Please try again later."
        EXPECTED: * User is not able to watch the stream
        """
        pass
