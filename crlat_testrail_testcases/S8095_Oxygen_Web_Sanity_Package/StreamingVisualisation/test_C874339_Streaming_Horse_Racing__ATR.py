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
class Test_C874339_Streaming_Horse_Racing__ATR(Common):
    """
    TR_ID: C874339
    NAME: Streaming Horse Racing - ATR
    DESCRIPTION: Video Streaming - Verify that the customer can see an ATR Sport video stream for the Live <Race> event
    PRECONDITIONS: Following Races are applicable for ATR streaming: Horse Racing, Greyhounds Racing
    PRECONDITIONS: Mapping guide form:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 1. Navigate to Backoffice > Admin > Media Content > Map ATR Streams
    PRECONDITIONS: 2. Search for streams by clicking on "Show events"
    PRECONDITIONS: 3. Check that an ATR stream is available and mapped to a <Race> event (**'drilldownTagNames'**='EVFLAG_AVA' flag should be set)
    PRECONDITIONS: 4. User is logged in into Oxygen app
    PRECONDITIONS: 5. Event should have the following attributes:
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: *   isStarted = "false"; it should be less than 2 minutes left before event Start Time.
    PRECONDITIONS: __Notice:__
    PRECONDITIONS: How to find requests in dev tools? Take the event id from the address bar > open dev tools > Network > in Search enter event ID > find in searched results request that is started with "Optin"
    PRECONDITIONS: ![](index.php?/attachments/get/65165634)
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_eventhorsegreyhounds_racing_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event(Horse/Greyhounds Racing) which satisfies Preconditions
        EXPECTED: The event details page(EDP) is loaded
        EXPECTED: Desktop:
        EXPECTED: 'Live Stream' (Coral) / 'Watch' (Ladbrokes) button is shown below the event name line
        EXPECTED: Mobile/Tablet:
        EXPECTED: 'Live Stream' (Coral) / 'Watch' (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_clicktap_on_the_live_streamwatch_button(self):
        """
        DESCRIPTION: Click/Tap on the "Live Stream"/"Watch" button
        EXPECTED: "In order to view this event you need to place a bet greater than or equal to £1" message is displayed
        EXPECTED: User is not able to watch the stream
        """
        pass

    def test_003_add_a_selection_from_this_event_to_bet_slip_and_place_a_bet_with_an_amount_equal_to_1_15_15(self):
        """
        DESCRIPTION: Add a selection from this event to bet slip and place a bet with an amount equal to 1£ (1.5$, 1.5Є)
        EXPECTED: The bet is successfully placed
        """
        pass

    def test_004_clicktap_on_the_live_streamwatch_button_again(self):
        """
        DESCRIPTION: Click/Tap on the "Live Stream"/"Watch" button again
        EXPECTED: If the Video is available(current time is 2 minutes before start time or even less, or start time is due)  - the video player is opened with a video stream being shown within it
        EXPECTED: If the Video is not yet available(start time has not yet come - more than 2 minutes before start time) - **"This stream has not yet started. Please try again soon."** message is displayed
        EXPECTED: If the Video is not yet available(start time is due but stream provider has not provided stream for any reason) - **"The Stream for this event is currently not available."** message is displayed
        EXPECTED: XHR - optin response contains ATR 'priorityProviderCode'
        EXPECTED: ![](index.php?/attachments/get/11918130)
        """
        pass
