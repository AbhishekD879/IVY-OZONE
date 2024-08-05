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
class Test_C363745_Launching_a_Stream_when_user_is_not_qualified_to_watch_the_RUK_stream(Common):
    """
    TR_ID: C363745
    NAME: Launching a Stream when user is not qualified to watch the RUK stream
    DESCRIPTION: This test case verifies launching the stream for a user, not qualified to watch the stream.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. There has to be a RUK (Racing UK) stream mapped to the test event.
    PRECONDITIONS: Instruction how to map streams to events can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: 2. SiteServer event should be configured to support RUK/Perform streaming (**'drilldownTagNames'**='EVFLAG_RVA' flag should be set) and should be mapped to RUK/Perform stream event
    PRECONDITIONS: 3. User is logged in with a user that has no restrictions on betting
    PRECONDITIONS: 4. The event should NOT be started so that user can place bets on this event - more than 1 hour left to event start time (isStarted = "false").
    """
    keep_browser_open = True

    def test_001_open_event_details_page_for_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page for any <Race> event which satisfies Preconditions
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
        EXPECTED: **Ladbrokes** and **Coral** Pop up opens with message 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_003_place_a_bet_for_one_selection_with_stake__01(self):
        """
        DESCRIPTION: Place a bet for one selection with stake = 0,1
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_004_refresh_the_event_details_page_and_tapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: Refresh the event details page and tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * [ Coral desktop / Ladbrokes desktop]: A message is displayed: 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_005_place_a_bet_for_selection_from_step_4_with_stake__089(self):
        """
        DESCRIPTION: Place a bet for selection from step #4 with stake = 0,89
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_006_refresh_the_event_details_page_and_tapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: Refresh the event details page and tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * [ Coral desktop / Ladbrokes desktop]: A message is displayed: 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message 'In order to view this event you need to place a bet greater than or equal to £1' (regardless of the user's currency)
        EXPECTED: * User is not able to watch the stream
        """
        pass

    def test_007_place_bet_for_one_selection_with_stake__1(self):
        """
        DESCRIPTION: Place Bet for one selection with stake = 1
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_008_refresh_the_event_details_page_and_tapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: Refresh the event details page and tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * [ Coral desktop / Ladbrokes desktop]: A message is displayed: 'This stream has not yet started. Please try again soon.' error message is shown
        EXPECTED: * [ Ladbrokes and Coral tablet/mobile]: Pop up opens with message 'This stream has not yet started. Please try again soon.'
        EXPECTED: There's an 'Event countdown' to event start time under the message.
        EXPECTED: * User is not able to watch the stream
        """
        pass
