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
class Test_C76620_Verify_parameters_errorCode_and_errorMessage_for_Bet_Placement_Error_Tracking(Common):
    """
    TR_ID: C76620
    NAME: Verify parameters 'errorCode' and 'errorMessage' for Bet Placement Error Tracking
    DESCRIPTION: This test case verifies parameters 'errorCode' and 'errorMessage' in the 'dataLayer.push' for Bet Placement Error Tracking
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

    def test_004_open_placebet_beterror_from_the_devtools_network_and_remember_data_from_placebet(self):
        """
        DESCRIPTION: Open 'placeBet'->'betError' from the devtools->Network and remember data from 'placeBet'
        EXPECTED: 
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter'
        EXPECTED: Event 'trackEvent' is present in dataLayer
        """
        pass

    def test_006_verify_parameter_errorcode(self):
        """
        DESCRIPTION: Verify parameter 'errorCode'
        EXPECTED: 1.'errorCode' corresponds to
        EXPECTED: - **betslip.betError.i.subErrorCode** attribute  from 'placebet' request in first instance
        EXPECTED: - **betslip.betError.i.Code** attribute  from 'placebet' request in second instance
        EXPECTED: where **i** - number of placed bet
        EXPECTED: 2.'errorCode' attribute is displayed in lower case
        EXPECTED: 3. 'errorCode' parameter is equal to "multiple errors" in case of more than one error is occurred during submission
        """
        pass

    def test_007_verify_parameter_errormessage(self):
        """
        DESCRIPTION: Verify parameter 'errorMessage'
        EXPECTED: 1.'errorMessage' corresponds to error description displayed for the user on the Betslip in case of price/handicup change/suspension/event is started
        EXPECTED: in case of Openbet returns an error during bet placement
        EXPECTED: where **i** - number of placed bet
        EXPECTED: 2.'errorMessage'  attribute is displayed in lower case
        EXPECTED: 3. 'errorMessage' parameter is equal to "multiple errors" in case of more than one error is occurred during submission
        """
        pass

    def test_008_add_a_few_selections_to_betslip_from_sport_andor_race(self):
        """
        DESCRIPTION: Add a few selection(s) to Betslip from **<Sport>** and/or **<Race>**
        EXPECTED: 
        """
        pass

    def test_009_trigger_error_message_for_a_few_selections_at_the_same_time_during_bet_placement_immediately_after_placebet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Trigger error message for a few selections at the same time during bet placement immediately after **'placebet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: Error messages appear in the Betslip
        """
        pass

    def test_010_type_in_console_datalayer_tap_enter(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter'
        EXPECTED: Event 'trackEvent' is present in dataLayer
        """
        pass

    def test_011_verify_parameter_errorcode_and_errormessage(self):
        """
        DESCRIPTION: Verify parameter 'errorCode' and 'errorMessage'
        EXPECTED: 'errorCode' and 'errorMessage' are set to "Multiple errors"
        """
        pass

    def test_012_repeat_steps_2_11_with_in_play_events_buttrigger_error_message_during_bet_placement_immediately_after_readbet_request_is_senteg_price_changesuspension_etc(self):
        """
        DESCRIPTION: Repeat steps 2-11 with In-Play events BUT
        DESCRIPTION: Trigger error message during bet placement immediately after **'readbet'** request is sent
        DESCRIPTION: e.g.: price change/suspension etc.
        EXPECTED: 
        """
        pass
