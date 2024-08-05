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
class Test_C141288_Launching_a_Stream_when_user_is_not_qualified_to_watch_the_iGMedia_stream_on_Race_EDP(Common):
    """
    TR_ID: C141288
    NAME: Launching a Stream when user is not qualified to watch the iGMedia stream on <Race> EDP
    DESCRIPTION: This test case verifies launching the stream for a user, not qualified to watch the stream (when Racing Rule is applied)
    DESCRIPTION: Applicable to <Greyhound Racing> events; Applicable for users with 'GBP' currency setting.
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. SiteServer event should be configured to support GVM streaming ( **'drilldownTagNames'** ='EVFLAG_GVM' and **'typeFlagCodes'='GVA'** flags should be set) and should be mapped to GVM stream event
    PRECONDITIONS: 2. User is logged into the Oxygen app, has a positive balance and wallet currency is set to 'GBP'.
    PRECONDITIONS: 3. The event should NOT be started so that user can place bets on this event - more than 1 hour left to event start time (isStarted = "false").
    PRECONDITIONS: The following parameters should be received in Optin MS response in order play IGMedia stream on mentioned devices/platforms:
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
    PRECONDITIONS: ![](index.php?/attachments/get/65165630)
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_eventgreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Greyhounds Racing) which satisfies Preconditions
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
        EXPECTED: * Request to OptIn MS is sent to identify stream provider
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * Request to OptIn MS is sent (see preconditions) to indetify stream provider, with a following response:
        EXPECTED: ![](index.php?/attachments/get/118215248)
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_003_place_a_bet_for_one_selection_with_stake__01_gbp(self):
        """
        DESCRIPTION: Place a bet for one selection with stake = '0,1' GBP
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Expected Results match those, described in step 2
        """
        pass

    def test_005_place_a_bet_for_one_selection_with_stake__089_gbp(self):
        """
        DESCRIPTION: Place a bet for one selection with stake = '0,89' GBP
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Expected Results match those, described in step 2
        """
        pass

    def test_007_place_bet_for_one_selection_with_stake__001_gbp(self):
        """
        DESCRIPTION: Place Bet for one selection with stake = '0.01' GBP
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_008_refresh_the_event_details_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Refresh the event details page and repeat step 2
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
