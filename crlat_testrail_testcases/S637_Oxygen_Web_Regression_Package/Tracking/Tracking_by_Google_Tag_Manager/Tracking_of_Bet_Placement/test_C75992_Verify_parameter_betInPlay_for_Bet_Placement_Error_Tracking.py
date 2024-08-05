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
class Test_C75992_Verify_parameter_betInPlay_for_Bet_Placement_Error_Tracking(Common):
    """
    TR_ID: C75992
    NAME: Verify parameter 'betInPlay' for Bet Placement Error Tracking
    DESCRIPTION: This test case verifies parameter 'betInPlay' in the 'dataLayer.push' for Bet Placement Error Tracking
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selections_to_betslip_from_not_in_play_events(self):
        """
        DESCRIPTION: Add selection(s) to Betslip from **NOT In-Play event(s)**
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

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: * Event 'trackEvent' is present in dataLayer
        EXPECTED: * **'cd102'** parameter = <<IN PLAY STATUS>>
        """
        pass

    def test_005_verify_parameter_betinplay(self):
        """
        DESCRIPTION: Verify parameter **'betInPlay'**
        EXPECTED: Parameter **betInPlay: "No"** in dataLayer object
        """
        pass

    def test_006_add_a_selections_to_betslip_from_in_play_events(self):
        """
        DESCRIPTION: Add a selection(s) to Betslip from **In-Play event(s)**
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_008_verify_parameter_betinplay(self):
        """
        DESCRIPTION: Verify parameter **'betInPlay'**
        EXPECTED: Parameter **betInPlay: "Yes"** in dataLayer object
        """
        pass

    def test_009_add_not_in_play_selections_and_in_play_selections_to_betslip(self):
        """
        DESCRIPTION: Add **NOT In-Play selection(s) and In-Play selection(s)** to Betslip
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass

    def test_011_verify_parameter_betinplay(self):
        """
        DESCRIPTION: Verify parameter **'betInPlay'**
        EXPECTED: Parameter betInPlay: "Both" in dataLayer object
        """
        pass

    def test_012_repeat_steps_6_11_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 6-11 BUT
        DESCRIPTION: Trigger error message during bet placement immediately after **'readbet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass
