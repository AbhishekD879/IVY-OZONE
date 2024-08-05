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
class Test_C44870310_Verify_that_live_stream_from_different_providers_are_available_for_watching_and_bet_placement(Common):
    """
    TR_ID: C44870310
    NAME: Verify that live stream from different providers are available for watching and bet placement.
    DESCRIPTION: 
    PRECONDITIONS: 1. User is logged in the application.
    PRECONDITIONS: 2. Events with the following live stream providers are available - Perform, IgameMedia and ATR.
    """
    keep_browser_open = True

    def test_001_navigate_to_an_event_with_perform_as_the_live_stream_provider_play_the_live_stream_on_the_event_details_page_and_verify(self):
        """
        DESCRIPTION: Navigate to an event with Perform as the live stream provider. Play the live stream on the event details page and verify.
        EXPECTED: The live stream with audio should play smoothly.
        """
        pass

    def test_002_pause_and_play_the_live_stream_after_10_seconds_verify(self):
        """
        DESCRIPTION: Pause and play the live stream after 10 seconds. Verify.
        EXPECTED: The live stream with audio should play smoothly.
        """
        pass

    def test_003_scroll_the_page_and_verify(self):
        """
        DESCRIPTION: Scroll the page and verify.
        EXPECTED: The page is scrolled properly and live stream with audio should play smoothly.
        """
        pass

    def test_004_place_a_bet_on_the_currently_streaming_event_and_verify(self):
        """
        DESCRIPTION: Place a bet on the currently streaming event and verify.
        EXPECTED: The bet is placed successfully.
        """
        pass

    def test_005_place_bets_in_forecast_and_tricast_markets_for_races_on_the_currently_streaming_event_and_verify(self):
        """
        DESCRIPTION: Place bets in Forecast and Tricast markets (for races) on the currently streaming event and verify.
        EXPECTED: The bets are placed successfully.
        """
        pass

    def test_006_verify_the_bet_settlement_and_returns_in_my_bets_for_the_bets_placed_in_steps_45(self):
        """
        DESCRIPTION: Verify the bet settlement and returns in My bets for the bets placed in steps 4,5.
        EXPECTED: The settled bets with correct returns are displayed in My bets.
        """
        pass

    def test_007_perform_steps_1_6_for_the_following_live_stream_providers___igamemedia_atr_and_inspire_virtual_events(self):
        """
        DESCRIPTION: Perform steps 1-6 for the following live stream providers - IgameMedia, ATR and Inspire (virtual events).
        EXPECTED: The expected result is same as in steps 1-6.
        """
        pass
