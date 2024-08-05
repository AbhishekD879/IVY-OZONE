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
class Test_C1108077_Launching_iGame_media_stream_for_an_event_with_several_available_streaming_providers(Common):
    """
    TR_ID: C1108077
    NAME: Launching iGame media stream for an event with several available streaming providers
    DESCRIPTION: This test case verifies successfully launching an iGame Media stream when several streaming providers are mapped to the same event
    DESCRIPTION: Applies to <Race>/<Sport> events
    DESCRIPTION: Note:
    DESCRIPTION: iGame Media stream provider should have the highest priority among other providers mapped to the same event. "iGameMedia stream mapped for this event" flag should NOT be checked on event level in case another stream provider is mapped for this event (e.g. Perform, ATR...)
    DESCRIPTION: ***Jira ticket:***
    DESCRIPTION: BMA-22601: Integrate with iGameMedia
    PRECONDITIONS: 1. In TI:
    PRECONDITIONS: - Flags should be checked on <Type> level: IGameMedia Stream available, Perform Stream available, IMG Stream available, ATR Video Available, Racing UK Video Available
    PRECONDITIONS: - Flags should be checked on <Event> level: IGameMedia Stream mapped for this event, Perform Video Mapped for this event, IMG Video Mapped for this event, At the Races Stream available
    PRECONDITIONS: (In SS response: **'typeFlagCodes'**='PVA , IVA, RVA, RPG... ' AND **'drilldownTagNames'**='EVFLAG_GVM, EVFLAG_PVM, EVFLAG_IVM, EVFLAG_AVA, EVFLAG_RVA, EVFLAG_RPM' flags should be set)
    PRECONDITIONS: 2. IGame Media stream is mapped for an event (or any stream through IGame media)
    PRECONDITIONS: (see instruction: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events)
    PRECONDITIONS: 3. Event should have the following attributes:
    PRECONDITIONS: isStarted = "true"
    PRECONDITIONS: isMarketBetInRun = "true"'
    PRECONDITIONS: 4. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 5. The following parameters should be received in Optin MS response in order play iGameMedia stream on mentioned devices/platforms:
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
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
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
        EXPECTED: priorityProviderCode: "iGameMedia"
        EXPECTED: priorityProviderName: "iGame Media"
        EXPECTED: }
        """
        pass

    def test_003_verify_eventid_response_in_networkdeveloper_tools_in_your_web_browser_(self):
        """
        DESCRIPTION: Verify <eventID> response in Network(Developer Tools in your web browser )
        EXPECTED: - <eventID> response is available
        EXPECTED: - iGame media video iframe is received
        EXPECTED: - priorityProviderCode : "iGameMedia" is received in OPTIN response
        """
        pass

    def test_004_open_event_details_page_of_any_sport_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details Page of any <Sport> event which satisfies Preconditions
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

    def test_005_for_desktop_onlyverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: * The Video player is shown above market tabs
        EXPECTED: * The Video stream is shown within the player
        EXPECTED: No stream buttons appear for the player
        """
        pass

    def test_006_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: Expected Results match those, described in step 2
        """
        pass

    def test_007_repeat_step_3(self):
        """
        DESCRIPTION: Repeat Step #3
        EXPECTED: Expected Results match those, described in step 3
        """
        pass
