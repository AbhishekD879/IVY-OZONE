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
class Test_C29235_Verify_type_of_the_video(Common):
    """
    TR_ID: C29235
    NAME: Verify type of the video
    DESCRIPTION: This scenario verifies whether type of launched stream corresponds to mapped event type.
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and has a positive balance
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: 5. Endpoints of Optin MS:
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

    def test_003_for_desktoptapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
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

    def test_004_right_click_on_stream_and_select_inspect_element_from_the_right_menu(self):
        """
        DESCRIPTION: Right click on stream and select 'Inspect element' from the right menu
        EXPECTED: 
        """
        pass

    def test_005_find__performeventid_and_copy_it_eg_performeventid1686183indexphpattachmentsget18203635(self):
        """
        DESCRIPTION: Find ** performEventId** and copy it (e.g. performEventId:1686183)
        DESCRIPTION: ![](index.php?/attachments/get/18203635)
        EXPECTED: 
        """
        pass

    def test_006_load_linkhttpwwwmobilecoralperformgroupcomstreamingeventlistdays7version4(self):
        """
        DESCRIPTION: Load link:
        DESCRIPTION: http://www.mobile.coral.performgroup.com/streaming/eventList/?days=7&version=4
        EXPECTED: 
        """
        pass

    def test_007_find_copied_performeventid_through_ctrlplusfcommandplusf_command_and_check_its_event_type(self):
        """
        DESCRIPTION: Find copied 'performEventId' through Ctrl+F/Command+F command and check its 'event type'
        EXPECTED: Event type for this event ("video+data", "data", "video") should correspond to what we see in the launched stream
        EXPECTED: ![](index.php?/attachments/get/18203636)
        """
        pass
