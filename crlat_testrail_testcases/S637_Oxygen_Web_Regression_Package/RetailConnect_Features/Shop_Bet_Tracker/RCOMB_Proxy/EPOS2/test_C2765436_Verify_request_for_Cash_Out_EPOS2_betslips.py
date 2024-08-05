import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2765436_Verify_request_for_Cash_Out_EPOS2_betslips(Common):
    """
    TR_ID: C2765436
    NAME: Verify request for Cash Out EPOS2 betslips
    DESCRIPTION: 
    PRECONDITIONS: Use postman collection EPOS2 for checking data sent from backend
    PRECONDITIONS: (collection is attached)
    PRECONDITIONS: Use https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/ to check correctness of PROXY responses
    """
    keep_browser_open = True

    def test_001_to_get_correct_cashout_value_open_postrcombv3connect_submit_valid_epos2_barcode_with_at_least_one_in_play_game(self):
        """
        DESCRIPTION: To get correct CashOut value
        DESCRIPTION: * Open POST/rcomb/v3/connect
        DESCRIPTION: * Submit valid EPOS2 barcode with at least one in-play game
        EXPECTED: * Barcode data are retrieved correctly including CashOut value
        """
        pass

    def test_002_to_verify_that_betslip_can_be_cashed_out_successfully_open_getrcombv2cashout_set_parameters_correctly_provider__epos2coupon_id__betid_amount__value_is_equal_to__cashoutvalue_from_previous_step_currency__gbp_receiptnumber__barcode_numbertap_try_it_out(self):
        """
        DESCRIPTION: To verify that betslip can be cashed out successfully
        DESCRIPTION: * Open GET/rcomb/v2/cashout
        DESCRIPTION: * Set parameters correctly:
        DESCRIPTION: * provider = Epos2Coupon
        DESCRIPTION: * id = betid
        DESCRIPTION: * amount = value is equal to  CashOutValue from previous step
        DESCRIPTION: * currency = GBP
        DESCRIPTION: * receiptNumber = barcode number
        DESCRIPTION: tap 'Try it out'
        EXPECTED: * Barcode data are retrieved correctly
        EXPECTED: * Bet is cashed out
        """
        pass

    def test_003_to_verify_that_user_cannot_cash_out_higher_value_than_actual_cash_cash_out_value_open_getrcombv2cashout_set_parameters_correctly_provider__epos2coupon_id__betid_amount__value_is_higher_than__cashoutvalue_from_ostrcombv3connect_currency__gbp_receiptnumber__barcode_numbertap_try_it_out(self):
        """
        DESCRIPTION: To verify that user cannot cash out higher value than actual cash cash out value
        DESCRIPTION: * Open GET/rcomb/v2/cashout
        DESCRIPTION: * Set parameters correctly:
        DESCRIPTION: * provider = Epos2Coupon
        DESCRIPTION: * id = betid
        DESCRIPTION: * amount = value is higher than  CashOutValue from OST/rcomb/v3/connect
        DESCRIPTION: * currency = GBP
        DESCRIPTION: * receiptNumber = barcode number
        DESCRIPTION: tap 'Try it out'
        EXPECTED: * Barcode data are retrieved correctly
        EXPECTED: * Error at the top says 'Cash Out value is higher'
        EXPECTED: * Bet is not cashed out (settled)
        """
        pass

    def test_004_to_verify_that_user_can_cash_out_smaller_value_than_actual_cash_cash_out_value_open_getrcombv2cashout_set_parameters_correctly_provider__epos2coupon_id__betid_amount__value_is_lower_than__cashoutvalue_from_ostrcombv3connect_currency__gbp_receiptnumber__barcode_numbertap_try_it_out(self):
        """
        DESCRIPTION: To verify that user can cash out smaller value than actual cash cash out value
        DESCRIPTION: * Open GET/rcomb/v2/cashout
        DESCRIPTION: * Set parameters correctly:
        DESCRIPTION: * provider = Epos2Coupon
        DESCRIPTION: * id = betid
        DESCRIPTION: * amount = value is lower than  CashOutValue from OST/rcomb/v3/connect
        DESCRIPTION: * currency = GBP
        DESCRIPTION: * receiptNumber = barcode number
        DESCRIPTION: tap 'Try it out'
        EXPECTED: * Barcode data are retrieved correctly
        EXPECTED: * Error at the top says 'Cash out pending'
        EXPECTED: * Bet is cashed out (settled)
        EXPECTED: * Actual Cash out (which is higher than value user is trying to cash out) is cashed out
        """
        pass

    def test_005_to_verify_that_user_cannot_cash_out_settled_betslip_open_getrcombv2cashout_set_parameters_correctly_provider__epos2coupon_id__betid_amount__value_that_corresponds_to__cashoutvalue_from_ostrcombv3connect_currency__gbp_receiptnumber__settled_barcode_numbertap_try_it_out(self):
        """
        DESCRIPTION: To verify that user cannot cash out settled betslip
        DESCRIPTION: * Open GET/rcomb/v2/cashout
        DESCRIPTION: * Set parameters correctly:
        DESCRIPTION: * provider = Epos2Coupon
        DESCRIPTION: * id = betid
        DESCRIPTION: * amount = value that corresponds to  CashOutValue from OST/rcomb/v3/connect
        DESCRIPTION: * currency = GBP
        DESCRIPTION: * receiptNumber = settled barcode number
        DESCRIPTION: tap 'Try it out'
        EXPECTED: * Barcode data are retrieved correctly
        EXPECTED: * Error at the top says  "CASHOUT_BET_ALREADY_SETTLED"
        EXPECTED: * Cash Out value is equal to 0
        EXPECTED: * Cash Out status and reason say:
        EXPECTED: },
        EXPECTED: "cashoutValue": {
        EXPECTED: "status": "CASHOUT_UNAVAILABLE",
        EXPECTED: "reason": "BET_SETTLED",
        EXPECTED: "amount": 0
        EXPECTED: },
        """
        pass
