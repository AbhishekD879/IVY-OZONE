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
class Test_C1274000_Launching_a_Stream_when_user_is_not_qualified_to_watch_the_iGMedia_stream_on_Sport_EDP(Common):
    """
    TR_ID: C1274000
    NAME: Launching a Stream when user is not qualified to watch the iGMedia stream on <Sport> EDP
    DESCRIPTION: This test case verifies launching the stream for a user, not qualified to watch the stream (0 balance and no bets made in last 24 hours)
    DESCRIPTION: Applicable to 'Basketball' events
    DESCRIPTION: Test case is created in order to cover the following ticket: OB Jira ticket: https://jira.openbet.com/browse/LCRCORE-6245
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ( **'drilldownTagNames'** ='EVFLAG_GVM' and **'typeFlagCodes'='GVA'** flags should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. User is logged in and has '0' balance with *NO BETS being placed during the last 24 hours*
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: *   isStarted = "true"
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

    def test_002_for_desktop_only_skip_this_step_if_stream_buttons_are_shownverify_that_warning_message_is_shown_on_edp_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:** (skip this step if stream buttons are shown)
        DESCRIPTION: Verify that warning message is shown on EDP (if no stream buttons are shown)
        EXPECTED: Warning message with following text is shown above the market tabs lane: "In order to view this event you need to place a bet greater than or equal to £1" (regardless of the user's currency)
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * Request to OptIn MS is sent to identify stream provider
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to indetify stream provider, with a following response:
        EXPECTED: ![](index.php?/attachments/get/17832474)
        EXPECTED: * User is not able to watch the stream
        """
        pass
