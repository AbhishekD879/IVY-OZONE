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
class Test_C76623_Verify_parameter_bonusBet_for_Bet_Placement_Error_Tracking(Common):
    """
    TR_ID: C76623
    NAME: Verify parameter 'bonusBet' for Bet Placement Error Tracking
    DESCRIPTION: This test case verifies parameter 'bonusBet' in the 'dataLayer.push' for Bet Placement Error Tracking
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. User has Free bets granted
    PRECONDITIONS: 3. Should be tested for Singles and Multiples bets
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_betslip_from_sport_or_race_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection to Betslip from **<Sport>** or **<Race>** enter Stake and place a bet
        EXPECTED: 
        """
        pass

    def test_003_trigger_error_message_during_bet_placement_immediately_after_placebet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Trigger error message during bet placement immediately after **'placebet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: Error message appears in the Betslip
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter'
        EXPECTED: Event 'trackEvent' is present in dataLayer
        """
        pass

    def test_005_verify_parameter_bonusbet(self):
        """
        DESCRIPTION: Verify parameter 'bonusBet'
        EXPECTED: Parameter **bonusBet: "false"** in dataLayer object
        """
        pass

    def test_006_repeat_steps_2_4_but_use_free_bet_for_bet_placement(self):
        """
        DESCRIPTION: Repeat steps 2-4 but use Free bet for bet placement
        EXPECTED: 
        """
        pass

    def test_007_verify_parameter_bonusbet(self):
        """
        DESCRIPTION: Verify parameter 'bonusBet'
        EXPECTED: Parameter **bonusBet: "true"** in dataLayer object
        """
        pass

    def test_008_repeat_steps_2_8_with_in_play_events_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 2-8 with In-Play events BUT
        DESCRIPTION: Trigger error message during bet placement immediately after **'readbet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass
