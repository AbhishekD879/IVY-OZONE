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
class Test_C64293340_Successfully_Launching_a_IMG_Stream_when_event_is_started(Common):
    """
    TR_ID: C64293340
    NAME: Successfully Launching a IMG Stream when event is started
    DESCRIPTION: This test case verifies launching the stream by user when event is started
    PRECONDITIONS: SiteServer event should be configured to support IMG streaming (**'typeFlagCodes'**='IVA , ... ' AND 'drilldownTagNames'='EVFLAG_IVM' flags should be set) and should be mapped to IMG stream event
    PRECONDITIONS: The event should have the following attributes:
    PRECONDITIONS: isStarted = "true"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: Endpoints of Optin MS:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    """
    keep_browser_open = True

    def test_001_open_event_details_page_for_the_golf_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page for the golf event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: For Mobile/Tablet:
        EXPECTED: 'Watch Live' button is shown when scoreboard is present(for both brands);
        EXPECTED: 'Watch'  (Coral) /  (Ladbrokes) button is shown when scoreboard is absent.
        EXPECTED: -
        EXPECTED: For Desktop:
        EXPECTED: 'Watch Live'  (Coral) /  (Ladbrokes) button is shown in case of scoreboard/visualization being present.
        EXPECTED: No stream buttons are shown if Stream is available WITHOUT mapped Visualization/Scoreboard
        """
        pass

    def test_002_for_desktop_onlyverify_that_streaming_is_started_once_edp_is_opened_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Verify that streaming is started once EDP is opened (if no stream buttons are shown)
        EXPECTED: The Video player is shown above market tabs
        EXPECTED: The Video stream is shown within the player
        EXPECTED: No stream buttons appear for the player
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: All Devices
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: listingUrl attribute is received from https://dge.imggaming.com/api/v2/streaming/events/{eventID}/stream?operatorId=26&auth=de68cd07dd16983b6f6a7eadf0313b85&timestamp=1571814531496&page.page=2&page.size=1 to consume stream [eventID is needed to be inserted in order to view data]
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "IMG"
        EXPECTED: priorityProviderName: "IMG Video Streaming"
        EXPECTED: }
        EXPECTED: Stream is launched
        """
        pass

    def test_004_for_desktop_onlynavigate_to_in_play_and_live_stream_section_on_homepage_and_switch_to_live_stream(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Navigate to 'IN-PLAY AND LIVE STREAM' section on Homepage and switch to 'LIVE STREAM'
        EXPECTED: Stream of 1st event on a list is launched automatically Stream is shown in the player frame below 'In-Play' and 'Live Stream' tabs
        """
        pass

    def test_005_for_desktop_onlymake_the_event_from_step_1_appear_at_the_topas_first_one_of_the_live_stream_events_list_and_refresh_the_page(self):
        """
        DESCRIPTION: For Desktop only:
        DESCRIPTION: Make the event from step 1 appear at the top(as first one) of the Live Stream events list and refresh the page
        EXPECTED: Expected Results match those, described in step 4
        """
        pass
