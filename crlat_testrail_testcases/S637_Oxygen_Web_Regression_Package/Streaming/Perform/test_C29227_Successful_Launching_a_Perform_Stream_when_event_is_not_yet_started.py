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
class Test_C29227_Successful_Launching_a_Perform_Stream_when_event_is_not_yet_started(Common):
    """
    TR_ID: C29227
    NAME: Successful Launching a Perform Stream when event is not yet started
    DESCRIPTION: This test case verifies launching the stream by the user when event is not started, and less than 2 minutes left before event Start Time
    DESCRIPTION: Applies to <Sport> events
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: 5. It should be less than 2 minutes left before event Start Time, event should not be started
    PRECONDITIONS: 6. Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_sport_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which satisfies Preconditions
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

    def test_002_for_desktop_onlyverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: * The Video player is shown above market tabs
        EXPECTED: * The Video stream is shown within the player
        EXPECTED: No stream buttons appear for the player
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: * **listingUrl** attribute is received from OptIn MS to consume streaming
        EXPECTED: * Stream is launched
        EXPECTED: * The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass

    def test_004_for_desktop_onlynavigate_to_in_play_and_live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Navigate to 'IN-PLAY AND LIVE STREAM ' section on Homepage and switch to 'LIVE STREAM'
        EXPECTED: Stream of 1st event on a list is launched automatically
        EXPECTED: Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_005_for_desktop_onlymake_the_event_from_step_1_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Make the event from step 1 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Expected Results match those, described in step 4
        """
        pass