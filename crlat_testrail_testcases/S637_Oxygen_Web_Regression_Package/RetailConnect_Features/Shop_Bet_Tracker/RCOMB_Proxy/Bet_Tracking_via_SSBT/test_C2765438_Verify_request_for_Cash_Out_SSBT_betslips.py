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
class Test_C2765438_Verify_request_for_Cash_Out_SSBT_betslips(Common):
    """
    TR_ID: C2765438
    NAME: Verify request for Cash Out SSBT betslips
    DESCRIPTION: This test case verify '/rcomb/v2/cashout' endpoint for cash out SSBT betslips
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-3282 Proxy: Create codebase for SSBT API for cashout
    PRECONDITIONS: Request in 'SSBT test data' chat creating of SSBS barcodes
    PRECONDITIONS: Use [DX postman collection](https://confluence.egalacoral.com/download/attachments/53838690/DX.postman_collection.json?version=1&modificationDate=1509720767000&api=v2) to get SSBT betslips data from DX service (turn on VPN)
    PRECONDITIONS: To find <cashoutAmount> run GetCashOutDetails request from the collection
    PRECONDITIONS: Open following request:
    PRECONDITIONS: [GET /rcomb/v2/cashout](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/cashoutBetPlacmentAndSSBTUsingGET)
    """
    keep_browser_open = True

    def test_001_run_getbetslip_getcashoutdetails__requests_from_dx_postman_collection_set_into__betslipkey_your_test_barcode_in_format_bxxxxxxxxxxxxx(self):
        """
        DESCRIPTION: Run 'GetBetSlip', 'GetCashOutDetails ' requests from 'DX postman collection' (set into  <betslipKey> your test barcode in format BXXXXXXXXXXXXX)
        EXPECTED: * Betslip data are retrieved correctly
        """
        pass

    def test_002_to_verify_that_user_cannot_cash_out_incorrect_not_relevant_valuerun_get_rcombv2cashouthttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointscashoutbetplacmentandssbtusinggetwith_following_parameters_provider__ssbt_id__barcode_without_letter_b_amount__value_is_not_equal_to__cashoutamount__from_dx_service_currency__corresponds_to__isocode__from_dx_service(self):
        """
        DESCRIPTION: To verify that user cannot cash out incorrect/ not relevant value
        DESCRIPTION: Run [GET /rcomb/v2/cashout](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/cashoutBetPlacmentAndSSBTUsingGET)
        DESCRIPTION: with following parameters:
        DESCRIPTION: * provider = SSBT
        DESCRIPTION: * id = Barcode (without letter 'B')
        DESCRIPTION: * amount = value is not equal to  <cashoutAmount>  from DX service
        DESCRIPTION: * currency = corresponds to  <isoCode>  from DX service
        EXPECTED: * Betslip response is received as "betError"
        EXPECTED: * "subErrorCode" says "CASHOUT_VALUE_OUT_OF_RANGE"
        EXPECTED: * All information about bet is retrieved correctly
        EXPECTED: * Cash Out value correspond to <cashoutAmount>  from DX service:
        EXPECTED: },
        EXPECTED: "cashoutValue": {
        EXPECTED: "amount": XXX
        EXPECTED: },
        """
        pass

    def test_003_to_verify_that_betslip_can_be_cashed_out_successfullyrun_get_rcombv2cashouthttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointscashoutbetplacmentandssbtusinggetwith_following_parameters_provider__ssbt_id__barcode_without_letter_b_amount__equal_to_cashoutamount__from_dx_service_currency__corresponds_to__isocode__from_dx_service(self):
        """
        DESCRIPTION: To verify that betslip can be cashed out successfully
        DESCRIPTION: Run [GET /rcomb/v2/cashout](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/cashoutBetPlacmentAndSSBTUsingGET)
        DESCRIPTION: with following parameters:
        DESCRIPTION: * provider = SSBT
        DESCRIPTION: * id = Barcode (without letter 'B')
        DESCRIPTION: * amount = equal to <cashoutAmount>  from DX service
        DESCRIPTION: * currency = corresponds to  <isoCode>  from DX service
        EXPECTED: * Betslip response is received
        EXPECTED: * All information about bet is retrieved correctly
        EXPECTED: * No "betError" messages
        EXPECTED: * Cash Out value corresponds to that one which was cashed out
        EXPECTED: },
        EXPECTED: "cashoutValue": {
        EXPECTED: "amount": XXX
        EXPECTED: },
        EXPECTED: * Parameters  (at the bottom) say:
        EXPECTED: "isSettled": "Y",
        EXPECTED: "isCashedOut": "Y"
        """
        pass

    def test_004_to_verify_that_user_cannot_cash_out_settled_betsliprun_get_rcombv2cashouthttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointscashoutbetplacmentandssbtusinggetwith_following_parameters_provider__ssbt_id__barcode_of_settled_betslip_amount__equal_to_cashoutamount__from_dx_service_currency__corresponds_to__isocode__from_dx_service(self):
        """
        DESCRIPTION: To verify that user cannot cash out settled betslip
        DESCRIPTION: Run [GET /rcomb/v2/cashout](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/cashoutBetPlacmentAndSSBTUsingGET)
        DESCRIPTION: with following parameters:
        DESCRIPTION: * provider = SSBT
        DESCRIPTION: * id = Barcode of settled betslip
        DESCRIPTION: * amount = equal to <cashoutAmount>  from DX service
        DESCRIPTION: * currency = corresponds to  <isoCode>  from DX service
        EXPECTED: * Betslip response is received as "betError"
        EXPECTED: * "subErrorCode" says "CASHOUT_BET_ALREADY_SETTLED"
        EXPECTED: * All information about bet is retrieved correctly
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

    def test_005_to_verify_that_user_cannot_cash_out_betslip_at_the_moment_when_cash_out_value__0run_get_rcombv2cashouthttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointscashoutbetplacmentandssbtusinggetwith_following_parameters_provider__ssbt_id__use_barcode_which_currently_has__cashoutamount__0_to_check_this_run_getcashoutdetails_request_in_postman_amount__set_any_value_currency__corresponds_to__isocode__from_dx_service(self):
        """
        DESCRIPTION: To verify that user cannot cash out betslip at the moment when Cash Out value = 0
        DESCRIPTION: Run [GET /rcomb/v2/cashout](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/cashoutBetPlacmentAndSSBTUsingGET)
        DESCRIPTION: with following parameters:
        DESCRIPTION: * provider = SSBT
        DESCRIPTION: * id = use Barcode which currently has  <cashoutAmount> = 0 (to check this run 'GetCashOutDetails' request in Postman)
        DESCRIPTION: * amount = set any value
        DESCRIPTION: * currency = corresponds to  <isoCode>  from DX service
        EXPECTED: * Betslip response is received as "betError"
        EXPECTED: * "subErrorCode" says "CASHOUT_FAILED"
        EXPECTED: * All information about bet is retrieved correctly
        EXPECTED: * Cash Out value is equal to 0
        EXPECTED: * Cash Out status and reason say:
        EXPECTED: },
        EXPECTED: "cashoutValue": {
        EXPECTED: "status": "CASHOUT_UNAVAILABLE",
        EXPECTED: "reason": "BET_WORTH_NOTHING",
        EXPECTED: "amount": 0
        EXPECTED: },
        """
        pass
