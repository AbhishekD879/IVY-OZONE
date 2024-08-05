import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.streaming
@vtest
class Test_C141211_Successful_Launch_of_Stream_when_event_is_started(Common):
    """
    TR_ID: C141211
    NAME: Successful Launch of Stream when event is started
    DESCRIPTION: This test case verifies launching the stream by user when event is started
    DESCRIPTION: Applies to <Race>/<Sport> events
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ( **'drilldownTagNames'** ='EVFLAG_GVM' and **'typeFlagCodes'='GVA'** flags should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: for <Race> events:
    PRECONDITIONS: *   isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: for <Sport> events:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: 3. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: The following parameters should be received in Optin MS response in order play IGameMedia stream on mentioned devices/platforms:
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

    def test_002_place_a_minimum_sum_of_1_15_15_on_1_or_many_selections_within_the_tested_event(self):
        """
        DESCRIPTION: Place a minimum sum of 1£ (1.5$, 1.5Є) on 1 or many selections within the tested event
        EXPECTED: 
        """
        pass

    def test_003_for_desktop_only_skip_this_step_if_stream_buttons_are_shownverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:** (skip this step if stream buttons are shown)
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: * The Video player is shown above market tabs
        EXPECTED: * The Video stream is shown within the player
        EXPECTED: No stream buttons appear for the player
        """
        pass

    def test_004_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
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

    def test_005_for_desktop_onlynavigate_to_in_play_and_live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Navigate to 'IN-PLAY AND LIVE STREAM ' section on Homepage and switch to 'LIVE STREAM'
        EXPECTED: Stream of 1st event on a list is launched automatically
        EXPECTED: Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_006_for_desktop_onlymake_the_event_from_step_1_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Make the event from step 1 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Expected Results match those, described in step 5
        """
        pass

    def test_007_open_event_details_page_of_any_race_eventgreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Greyhounds Racing) which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_009_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: Expected Results match those, described in step 4
        """
        pass
