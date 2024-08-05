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
class Test_C29232_Launching_Perform_Stream_when_balance_is_not_positive(Common):
    """
    TR_ID: C29232
    NAME: Launching Perform Stream when balance is not positive
    DESCRIPTION: User is trying to launch stream when balance is not positive and bet was not placed during the last 24 hours.
    DESCRIPTION: Applies to <Sport> events and UK Horse Racing since HR UK is under Sport Rules for streaming only.
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true"
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and has '0' balance with **NO BETS** being placed during the last 24 hours
    PRECONDITIONS: 4. Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - In CMS-System Configuration-Structure-performGroup two next properties should be present:
    PRECONDITIONS: 1. CSBIframeEnabled with checkbox checked
    PRECONDITIONS: 2. CSBIframeSportIds with category ID as value (e.g. 21 for Horse Racing)
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

    def test_002_for_desktop_onlyverify_that_warning_message_is_shown_on_edp_if_no_stream_buttons_are_shown(self):
        """
        DESCRIPTION: **For Desktop only:**
        DESCRIPTION: Verify that warning message is shown on EDP (if no stream buttons are shown)
        EXPECTED: Warning message with following text is shown above the market tabs lane: "In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours."
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider
        EXPECTED: User is not able to watch the stream
        EXPECTED: iFrame is not rendered for Horse Racing UK
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * Request to OptIn MS is sent to identify stream provider
        EXPECTED: * **accountHistory** request to bpp is sent to check whether user has any bets placed during the last 24 hours (not applicable for Horse Racing UK)
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours." OR 'In order to view this event you need to place a bet greater than or equal to £1' for race rules streaming.
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours." OR 'In order to view this event you need to place a bet greater than or equal to £1' for race rules streaming.
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to identify stream provider, with a following response:
        EXPECTED: ![](index.php?/attachments/get/17832474)
        EXPECTED: * User is not able to watch the stream
        """
        pass
