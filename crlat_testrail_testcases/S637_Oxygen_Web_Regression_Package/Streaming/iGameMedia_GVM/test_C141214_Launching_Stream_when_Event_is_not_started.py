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
class Test_C141214_Launching_Stream_when_Event_is_not_started(Common):
    """
    TR_ID: C141214
    NAME: Launching Stream when Event is not started
    DESCRIPTION: User is trying to launch stream when it is more than 15 minutes left to its start time.
    DESCRIPTION: Applies to <Race>/<Sport> events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ( **'drilldownTagNames'** ='EVFLAG_GVM' and **'typeFlagCodes'='GVA'** flags should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. More than 15 min left to event start time. Event should not be started (isStarted = 'false')
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested events(both <Race> and <Sport>)
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
    PRECONDITIONS: **NOTE: If by any circumstances you have no way of verifying this case on <Sport> events, please verify it on <Race> events and leave a corresponding comment as a result of a test case run.**
    PRECONDITIONS: ![](index.php?/attachments/get/65165630)
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_basketball_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any 'Basketball' event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050950) (Coral) / ![](index.php?/attachments/get/3050951) (Ladbrokes) button is shown when scoreboard is absent.
        EXPECTED: -
        EXPECTED: **For Desktop:**
        EXPECTED: 'Watch Live' ![](index.php?/attachments/get/3050948) (Coral) / ![](index.php?/attachments/get/3050949) (Ladbrokes) button is shown in case of scoreboard/visualization being present.
        EXPECTED: * No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_002_for_desktop_only_skip_this_step_if_stream_buttons_are_shownverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:** (skip this step if stream buttons are shown)
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: Warning message with following text is shown above the market tabs lane: "This stream has not yet started. Please try again soon"
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "This stream has not yet started. Please try again soon"
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "This stream has not yet started. Please try again soon". There's an 'Event countdown' to event start time under the message.
        EXPECTED: **User is not able to watch the stream**
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "iGameMedia"
        EXPECTED: priorityProviderName: "iGame Media"
        EXPECTED: }
        """
        pass

    def test_004_open_event_details_page_of_any_race_eventgreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Greyhounds Racing) which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_005_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: Expected Results match those, described in step 3
        """
        pass
