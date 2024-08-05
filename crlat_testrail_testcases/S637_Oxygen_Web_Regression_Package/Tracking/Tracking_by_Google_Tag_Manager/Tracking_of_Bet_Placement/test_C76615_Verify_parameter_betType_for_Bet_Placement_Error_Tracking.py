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
class Test_C76615_Verify_parameter_betType_for_Bet_Placement_Error_Tracking(Common):
    """
    TR_ID: C76615
    NAME: Verify parameter 'betType' for Bet Placement Error Tracking
    DESCRIPTION: This test case verifies parameter 'betType' in the 'dataLayer.push' for Bet Placement Error Tracking
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. To trigger errors during Jackpot and Lotto bet placement ask UAT to suspend certain jackpot or lotto
    PRECONDITIONS: 3. Alternative way to trigger error during Lotto bet placement - place bet which is higher than your current balance
    PRECONDITIONS: OR you may use suspended user - In order to close (suspend) user:
    PRECONDITIONS: Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: and proceed with account closure flow.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_betslip_from_sport_or_race_and_place_single_bet(self):
        """
        DESCRIPTION: Add ONE selection to Betslip from **<Sport>** or **<Race>** and place Single bet
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

    def test_005_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Single"** in dataLayer object
        """
        pass

    def test_006_add_a_few_selection_to_betslip_from_sport_or_race_and_place_a_few_single_bets(self):
        """
        DESCRIPTION: Add a few selection to Betslip from **<Sport>** or **<Race>** and place a few Single bets
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_008_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Single"** in dataLayer object
        """
        pass

    def test_009_add_a_few_selections_to_betslip_from_sport_andor_race_and_place_multiple_bet(self):
        """
        DESCRIPTION: Add a few selection(s) to Betslip from **<Sport>** and/or **<Race>** and place Multiple bet
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_011_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Multiple"** in dataLayer object
        """
        pass

    def test_012_add_a_few_selection_to_betslip_from_different_events_and_place_single_and_multiple_bets(self):
        """
        DESCRIPTION: Add a few selection to Betslip from different events and place Single and Multiple bets
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_014_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Both"** in dataLayer object
        """
        pass

    def test_015_open_lotto_page_and_place_lotto_bet(self):
        """
        DESCRIPTION: Open **Lotto** page and place Lotto bet
        EXPECTED: 
        """
        pass

    def test_016_trigger_error_message_during_bet_placement_on_lotto(self):
        """
        DESCRIPTION: Trigger error message during bet placement on Lotto
        EXPECTED: 
        """
        pass

    def test_017_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass

    def test_018_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Single"** in dataLayer object
        """
        pass

    def test_019_open_football_jackpot_page_and_place_jackpot_bet(self):
        """
        DESCRIPTION: Open **Football->Jackpot** page and place Jackpot bet
        EXPECTED: 
        """
        pass

    def test_020_trigger_error_message_during_bet_placement_on_jackpot(self):
        """
        DESCRIPTION: Trigger error message during bet placement on Jackpot
        EXPECTED: 
        """
        pass

    def test_021_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass

    def test_022_verify_parameter_bettype(self):
        """
        DESCRIPTION: Verify parameter 'betType'
        EXPECTED: Parameter **betType: "Single"** in dataLayer object
        """
        pass

    def test_023_repeat_steps_2_14_with_in_play_events_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 2-14 with In-Play events BUT
        DESCRIPTION: Trigger error message during bet placement immediately after **'readbet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass
