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
class Test_C2765437_Verify_request_for_retrieving_SSBT_betslip(Common):
    """
    TR_ID: C2765437
    NAME: Verify request for retrieving SSBT betslip
    DESCRIPTION: This test case verify '/rcomb/v2/barcode' and '/rcomb/v2/barcodes' endpoints for retrieving SSBT betslips
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-3162 Proxy: Create codebase for SSBT API for betslip
    PRECONDITIONS: Request in 'SSBT test data' chat creating of SSBS barcodes
    PRECONDITIONS: Use [DX postman collection](https://confluence.egalacoral.com/download/attachments/53838690/DX.postman_collection.json?version=1&modificationDate=1509720767000&api=v2) to get SSBT betslips data from DX service (turn on VPN)
    PRECONDITIONS: Open following requests:
    PRECONDITIONS: [GET /rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET)
    PRECONDITIONS: [GET /rcomb/v2/barcodes](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodesUsingGET)
    PRECONDITIONS: Football markets whith DX supports for SSBT at the moment:
    PRECONDITIONS: Match Betting
    PRECONDITIONS: Total Goals (Over/Under 2.5)
    PRECONDITIONS: Both Team To Score
    PRECONDITIONS: Total Goals (Over/Under 0.5)
    PRECONDITIONS: Total Goals (Over/Under 1.5)
    PRECONDITIONS: Total Goals (Over/Under 3.5)
    PRECONDITIONS: Total Goals (Over/Under 4.5)
    PRECONDITIONS: Total Goals (Over/Under 5.5)
    PRECONDITIONS: Handicap
    PRECONDITIONS: Correct scores
    PRECONDITIONS: Matchbet & BTTS
    PRECONDITIONS: Matchbet & Total Goals
    PRECONDITIONS: Possible values of 'results' and 'progress' parameters: "Win", "Lose", "Void", "Place", "Unset", "Handicap", "ResultedNotSettled", "Pending", "Winning", "Losing", "NotStarted"
    """
    keep_browser_open = True

    def test_001__run_getbetslip_request_from_dx_postman_collection_set_into__betslipkey_your_test_barcode_in_format_bxxxxxxxxxxxxx_run_betsliptracker_request_from_dx_postman_collection_set_into__betslipkey_your_test_barcode_in_format_bxxxxxxxxxxxxx(self):
        """
        DESCRIPTION: * Run 'GetBetSlip' request from 'DX postman collection' (set into  <betslipKey> your test barcode in format BXXXXXXXXXXXXX)
        DESCRIPTION: * Run 'BetSlipTracker' request from 'DX postman collection' (set into  <betslipKey> your test barcode in format BXXXXXXXXXXXXX)
        EXPECTED: Betslip data are retrieved correctly
        """
        pass

    def test_002_run_get_rcombv2barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeusingget_using_barcode_without_letter_b_as_parameter(self):
        """
        DESCRIPTION: Run [GET /rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET) using Barcode (without letter 'B') as parameter
        EXPECTED: Response with bets information is received
        """
        pass

    def test_003_verify_externalref_section(self):
        """
        DESCRIPTION: Verify 'externalRef' section
        EXPECTED: * id is equal to submitted burcode (without letter 'B')
        EXPECTED: * provider	: SSBT
        """
        pass

    def test_004_verify_bettyperef_section(self):
        """
        DESCRIPTION: Verify 'betTypeRef' section
        EXPECTED: Data are taken from 'GetBetSlip' response: <bet>/<BetType> tags:
        EXPECTED: * id <-- <code>
        EXPECTED: * name <-- <name>
        EXPECTED: received from DX service
        """
        pass

    def test_005_verify_stake_section(self):
        """
        DESCRIPTION: Verify 'stake' section
        EXPECTED: Data are taken from 'GetBetSlip' response: <betStake>/<stake> tags:
        EXPECTED: * amount <-- <amount> divided by 100
        EXPECTED: * (currency) id <-- <isoCode>
        EXPECTED: received from DX service
        """
        pass

    def test_006_verify_cashoutvalue_section(self):
        """
        DESCRIPTION: Verify 'cashoutValue' section
        EXPECTED: Data are taken from 'GetBetSlip' response: <betCashout>/<cashoutAmount> tags:
        EXPECTED: * amount <-- <amount> divided by 100
        EXPECTED: * status <-- "CASHOUT_UNAVAILABLE" if bet is settled or Cash Out value  = 0
        EXPECTED: * reason <-- "BET_SETTLED" if bet was settled,
        EXPECTED: "BET_WORTH_NOTHING" if Cash Out value  = 0
        EXPECTED: 'status' and 'reason' are absent when bet had not been settled yet and Cash Out value >0
        """
        pass

    def test_007_verify_bet___leg___sportsleg_price_sectionverify_for_each_selection_separately(self):
        """
        DESCRIPTION: Verify (bet -> leg -> sportsLeg) 'price' section
        DESCRIPTION: (verify for each selection separately)
        EXPECTED: Data are taken from 'GetBetSlip' response:
        EXPECTED: <legGroup>/<leg>/<betPrice> tags:
        EXPECTED: * priceNum <-- <numFractionalPrice>
        EXPECTED: * priceDen  <-- <denFractionalPrice>
        """
        pass

    def test_008_verify_bet___leg___sportsleg___legpart___otherattributes_sectionverify_for_each_selection_separately(self):
        """
        DESCRIPTION: Verify (bet -> leg -> sportsLeg -> legPart ->) "otherAttributes" section
        DESCRIPTION: (verify for each selection separately)
        EXPECTED: Data are taken from 'GetBetSlip' response:
        EXPECTED: <legGroup>/<leg>/<part>/<partSelection> tags:
        EXPECTED: * outcomeName <--  <selectionName>
        EXPECTED: * eventClassName <--  <eventClassName>
        EXPECTED: * SSBT_EVENT_KEY <--   <eventKey>/<retailSportsDBKey>
        EXPECTED: * isStarted <-- <isInRunning>
        EXPECTED: * SSBT_EVENT_CLASS_KEY <-- <eventClassKey>/<retailSportsDBKey>
        EXPECTED: * isFinished <-- <isInRunning>,  <resultConfirmed>
        EXPECTED: * result <-- <resultDetail>/<result>
        EXPECTED: * marketName <--  <marketName>
        EXPECTED: * SSBT_MARKET_KEY <-- <marketKey>/<retailSportsDBKey>
        EXPECTED: * eventName <--  <eventName>
        EXPECTED: * progress <-- <betStatus> from 'BetSlipTracker' request
        EXPECTED: * startTime <--  <eventStartDateTime>
        EXPECTED: * priceNum and priceDen are the same as in previous step
        """
        pass

    def test_009_verify_bet_section(self):
        """
        DESCRIPTION: Verify 'bet' section
        EXPECTED: Data are taken from 'GetBetSlip' response: <betslip> tags:
        EXPECTED: * isSettled <-- <betslip>/<isSettled>
        EXPECTED: * timeStamp <-- <bet>/<betStatus>/<validFrom>
        EXPECTED: * provider <-- SSBT
        """
        pass

    def test_010_verify_bet___otherattributes_trackable_value(self):
        """
        DESCRIPTION: Verify (bet -> otherAttributes) 'trackable' value
        EXPECTED: Data are taken from 'GetBetSlip' response:  <betCharacteristics> tags:
        EXPECTED: * trackable <-- <value> (true/false)
        """
        pass

    def test_011_verify_betslip_section(self):
        """
        DESCRIPTION: Verify 'betslip' section
        EXPECTED: Data are taken from <betslip> tags:
        EXPECTED: * provider <-- SSBT
        EXPECTED: * isPaid <-- <isPaid>
        EXPECTED: * isSettled <-- <isSettled>
        """
        pass

    def test_012_verify_bet___betslip_payout_section(self):
        """
        DESCRIPTION: Verify (bet -> betslip) 'payout' section
        EXPECTED: Data are taken from 'GetBetSlip' response:  <betslipPayout> tags
        EXPECTED: * 'potential' <-- <potentialPayout> divided by 100
        EXPECTED: * (currency) id <-- <isoCode>
        EXPECTED: * winnings <--  <winnings>/ <sourceMoney>/  <amount> divided by 100
        """
        pass

    def test_013_verify_bet___betslip_stake_section(self):
        """
        DESCRIPTION: Verify (bet -> betslip) 'stake' section
        EXPECTED: Data are taken from 'GetBetSlip' response:  <betslipStake> tags
        EXPECTED: * 'amount' <-- <stake> divided by 100
        EXPECTED: * (currency) id <-- <isoCode>
        """
        pass

    def test_014_repeat_steps_3_9_runningget_rcombv2barcodeshttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodesusinggetuse_several_barcodes_coma_separated_as_parameters(self):
        """
        DESCRIPTION: Repeat steps №3-9 running
        DESCRIPTION: [GET /rcomb/v2/barcodes](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodesUsingGET),
        DESCRIPTION: use several Barcodes (coma separated) as parameters
        EXPECTED: 
        """
        pass
