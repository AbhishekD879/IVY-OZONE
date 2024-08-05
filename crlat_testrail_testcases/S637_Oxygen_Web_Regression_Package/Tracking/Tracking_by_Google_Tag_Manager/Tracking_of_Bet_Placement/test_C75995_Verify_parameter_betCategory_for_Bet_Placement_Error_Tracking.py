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
class Test_C75995_Verify_parameter_betCategory_for_Bet_Placement_Error_Tracking(Common):
    """
    TR_ID: C75995
    NAME: Verify parameter 'betCategory' for Bet Placement Error Tracking
    DESCRIPTION: This test case verifies parameter 'betCategory' in the 'dataLayer.push' for Bet Placement Error Tracking
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. To trigger errors during Jackpot and Lotto bet placement ask UAT to suspend certain jackpot or lotto
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_betslip_from_sport_or_race(self):
        """
        DESCRIPTION: Add ONE selection to Betslip from **<Sport>** or **<Race>**
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

    def test_005_verify_parameter_betcategory(self):
        """
        DESCRIPTION: Verify parameter 'betCategory'
        EXPECTED: Parameter **betCategory: "categoryName"** in dataLayer object
        EXPECTED: where categoryName is taken from SiteServer response of event (e.g. "Horse Racing")
        """
        pass

    def test_006_add_a_few_selections_to_betslip_from_sport_andor_race(self):
        """
        DESCRIPTION: Add a few selection(s) to Betslip from **<Sport>** and/or **<Race>**
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_008_verify_parameter_betcategory(self):
        """
        DESCRIPTION: Verify parameter 'betCategory'
        EXPECTED: Parameter betCategory consists of the list of each categoryName separated by ","
        EXPECTED: (e.g.: 'betCategory': "Football","Tennis","Horse Racing")
        """
        pass

    def test_009_open_lotto_page(self):
        """
        DESCRIPTION: Open **Lotto** page
        EXPECTED: 
        """
        pass

    def test_010_trigger_error_message_during_bet_placement_on_lotto(self):
        """
        DESCRIPTION: Trigger error message during bet placement on Lotto
        EXPECTED: 
        """
        pass

    def test_011_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass

    def test_012_verify_parameter_betcategory(self):
        """
        DESCRIPTION: Verify parameter 'betCategory'
        EXPECTED: Parameter **betCategory: "Lotto"** in dataLayer object
        """
        pass

    def test_013_open_football_jackpot_page(self):
        """
        DESCRIPTION: Open **Football->Jackpot** page
        EXPECTED: 
        """
        pass

    def test_014_trigger_error_message_during_bet_placement_on_jackpot(self):
        """
        DESCRIPTION: Trigger error message during bet placement on Jackpot
        EXPECTED: 
        """
        pass

    def test_015_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass

    def test_016_verify_parameter_betcategory(self):
        """
        DESCRIPTION: Verify parameter 'betCategory'
        EXPECTED: Parameter **betCategory: "Football"** in dataLayer object
        """
        pass

    def test_017_repeat_steps_2_8_with_in_play_events_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 2-8 with In-Play events BUT
        DESCRIPTION: Trigger error message during bet placement immediately after **'readbet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass
