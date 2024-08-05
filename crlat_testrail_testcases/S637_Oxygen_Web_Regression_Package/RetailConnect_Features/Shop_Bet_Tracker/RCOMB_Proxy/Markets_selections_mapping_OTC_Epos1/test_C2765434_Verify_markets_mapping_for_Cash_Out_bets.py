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
class Test_C2765434_Verify_markets_mapping_for_Cash_Out_bets(Common):
    """
    TR_ID: C2765434
    NAME: Verify markets mapping for Cash Out bets
    DESCRIPTION: This test case verify markets mapping for Cash Out bets
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: HMN-2893 For mapping bet tracker’s selection
    DESCRIPTION: HMN-2894 For mapping bet tracker’s bet placement
    PRECONDITIONS: **Request creation of Cash Out coupon with several bets in it, each bet contains several events placed on different markets**
    PRECONDITIONS: Use link for retrieving barcodes (for dev):
    PRECONDITIONS: https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
    """
    keep_browser_open = True

    def test_001__load_the_bet_details_via_use_the_barcode__as_a_parameterhttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_get_outcome_id_from_request_result(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter)
        DESCRIPTION: https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Get Outcome ID from request result
        EXPECTED: * Bet details are retrieved successfully
        EXPECTED: * Outcome ID is preset  in section:
        EXPECTED: "leg": [
        EXPECTED: {
        EXPECTED: "sportsLeg": {
        EXPECTED: ...
        EXPECTED: "legPart": [
        EXPECTED: {
        EXPECTED: "outcomeRef": {
        EXPECTED: "id": "XXXXXXXXX",
        EXPECTED: "provider": "OpenBet"
        EXPECTED: },
        EXPECTED: where XXXXXXXXX is Outcome ID
        """
        pass

    def test_002__retrieve_information_about_event_from_obhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown216eventtooutcomeforeventxxxxxxxtranslationlangenwhere_xxxxxxx___eventid_find_outcome_id_there(self):
        """
        DESCRIPTION: * Retrieve information about event from OB:
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.16/EventToOutcomeForEvent/XXXXXXX?translationLang=en
        DESCRIPTION: where XXXXXXX - eventID
        DESCRIPTION: * Find Outcome ID there
        EXPECTED: *  Outcome ID is present in outcomes list of event's market
        """
        pass

    def test_003__load_the_bet_details_via_use_the_barcode__as_a_parameterhttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_verify_outcomename_and_marketname(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter)
        DESCRIPTION: https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Verify OutcomeName and MarketName
        EXPECTED: *  OutcomeName correspond to OutcomeName  from OB (fount by Outcome ID)
        EXPECTED: * MarketName correspond to MarketName from OB (Market which contain outcome with Outcome ID from previous step)
        """
        pass
