import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C76618_Tracking_of_Unsuccessful_Bet_Placement(Common):
    """
    TR_ID: C76618
    NAME: Tracking of Unsuccessful Bet Placement
    DESCRIPTION: 
    PRECONDITIONS: 1. Browser console is opened
    PRECONDITIONS: 2. To trigger errors during Jackpot and Lotto bet placement contact UAT for suspensions
    PRECONDITIONS: 3.  Attribute <<CUSTOMER BUILT>> populates with '1' and '0', if bet type = "Build Your Bet shows '1'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen application and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selections_and_open_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection(s) and open Betslip, **'Singles' section**
        EXPECTED: 
        """
        pass

    def test_003_trigger_error_message_during_bet_placement_immediately_after_placebet_request_is_senteg_price_changesuspension_etcmake_sure_error_occurred_during_placebet(self):
        """
        DESCRIPTION: Trigger error message during bet placement immediately after 'placebet' request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        DESCRIPTION: Make sure, error occurred during 'placeBet'
        EXPECTED: Error message appears in the Betslip
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The following parameters are present in dataLayer object:
        EXPECTED: event
        EXPECTED: eventCategory
        EXPECTED: eventAction
        EXPECTED: eventLabel
        EXPECTED: errorMessage
        EXPECTED: errorCode
        EXPECTED: betType
        EXPECTED: betCategory
        EXPECTED: betInPlay
        EXPECTED: bonusBet
        """
        pass

    def test_005_verify_static_parameters_in_response(self):
        """
        DESCRIPTION: Verify static parameters in response
        EXPECTED: The next parameters are static and not changeable for all dataLayer objects for failed bet placements:
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventLabel: "failure"
        EXPECTED: 'location' :  "LOCATION"
        EXPECTED: 'customerBuilt' : "CUSTOMER BUILT"
        """
        pass

    def test_006_repeat_steps_2_5_with_in_play_events_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 2-5 with In-Play events BUT
        DESCRIPTION: Trigger error message during bet placement immediately after 'readbet' request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass

    def test_007_add_a_few_selections_open_betslip_multiples_section_and_place_a_bet(self):
        """
        DESCRIPTION: Add a few selections, open Betslip, **'Multiples' section** and place a bet
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_5_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-5 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_009_add_a_few_selections_from_the_same_race_event_open_betslip_forecaststricasts_section_and_place_a_bet(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event, open Betslip, **'Forecasts/Tricasts' section** and place a bet
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__3_5_for_forecaststricasts_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-5 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass

    def test_011_add_sport_or_race_selection_from_inspired_virtual_sports_open_betslip_and_place_a_bet(self):
        """
        DESCRIPTION: Add <Sport> or <Race> selection from **Inspired Virtual Sports**, open Betslip and place a bet
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps__3_5_for_inspired_virtual_sport_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-5 for Inspired Virtual Sport bet
        EXPECTED: 
        """
        pass

    def test_013_add_selection_from_betradar_virtual_tournament_open_betslip_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection from **BetRadar Virtual Tournament**, open Betslip and place a bet
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps__3_5_for_betradar_virtual_tournament_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-5 for BetRadar Virtual Tournament bet
        EXPECTED: 
        """
        pass

    def test_015_go_to_football___jackpot_tab(self):
        """
        DESCRIPTION: Go to **Football -> Jackpot tab**
        EXPECTED: 
        """
        pass

    def test_016_select_buttons_by_tapping_lucky_dip_button_or_manually_place_a_bet_and_repeat_steps__3_5_for_jackpot_bet(self):
        """
        DESCRIPTION: Select buttons by tapping 'Lucky dip' button or manually, place a bet and repeat steps № 3-5 for Jackpot bet
        EXPECTED: 
        """
        pass

    def test_017_go_to_lotto_page(self):
        """
        DESCRIPTION: Go to **Lotto** page
        EXPECTED: 
        """
        pass

    def test_018_select_balls_place_a_bet_and_repeat_steps__3_5_for_lotto_bet(self):
        """
        DESCRIPTION: Select balls, place a bet and repeat steps № 3-5 for Lotto bet
        EXPECTED: 
        """
        pass
