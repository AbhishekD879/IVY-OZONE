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
class Test_C2765432_Verify_outcomes_mapping_for_Non_Cash_Out_bets_placed_on_First_Half_Result_market(Common):
    """
    TR_ID: C2765432
    NAME: Verify outcomes mapping for Non Cash Out bets placed on 'First Half Result' market
    DESCRIPTION: This test case verify outcomes mapping for Non Cash Out bets
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: HMN-2893 For mapping bet tracker’s selection
    PRECONDITIONS: Request creation of Non Cash Out bets with following parameters
    PRECONDITIONS: |||:eventTypeName|:Market Name
    PRECONDITIONS: || Half Time Win Lose Draw |  First Half Result
    PRECONDITIONS: To get bets from Apollo account history (BetTracker) use Postman configurations (TST2 environment):
    PRECONDITIONS: 1. Request method: GET
    PRECONDITIONS: 2. Request URL:
    PRECONDITIONS: http://apollo-tst2.coral.co.uk/apollo-rcomb/index.php/accounthistory
    PRECONDITIONS: Body: {"slip": "xxxxxxxxxxxx"} - to get info about particular coupon
    PRECONDITIONS: 3. Headers: Authorization Bearer {{token}}
    PRECONDITIONS: 4. token is set in environmental variable and is taken from the link:
    PRECONDITIONS: http://apollo-tst2.coral.co.uk/rcomb_api_index.php/getwebtokenbyusername
    PRECONDITIONS: Body: {"username":"combtester","password":"swordfish"}
    PRECONDITIONS: Other endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Connect+App+API+endpoints
    PRECONDITIONS: Use link for retrieving barcodes (for dev):
    PRECONDITIONS: https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
    """
    keep_browser_open = True

    def test_001__select_barcode_which_contain_eventbet_placed_on_market_first_half_result_event_type_name__half_time_win_lose_draw_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which contain event/bet placed on market "First Half Result" (Event Type Name = Half Time Win Lose Draw)
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_002_check_value_for_outcome___name_(self):
        """
        DESCRIPTION: Check value for "outcome": { ... "name" ..
        EXPECTED: * "name" is represented as 'Home team name' or 'Away team name' or 'Draw' (e. g.: 'Brighton')
        EXPECTED: ('.' can be present at the end of outcome name, if so PROXY will remove)
        """
        pass

    def test_003_check_if_name_outcome_name_is_present_in_openbet_outcomes_list_for_particular_event_using_a_linkhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown226eventtooutcomeforeventext_openbet20feed20formatopenbet_feedeventxxxxxxxxtranslationlangenincludeundisplayedtruewhere_xxxxxxxx___acoid_events_amelco_id(self):
        """
        DESCRIPTION: Check if "name" (outcome name) is present in OpenBet outcomes list for particular event using a link
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForEvent/~ext-Openbet%20Feed%20Format.OPENBET_FEED:EVENT:XXXXXXXX?translationLang=en&includeUndisplayed=true
        DESCRIPTION: where XXXXXXXX - ACOID (Event's Amelco ID)
        EXPECTED: * "name" (outcome name) is found in OB ("Brighton")
        """
        pass

    def test_004__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_outcomename_value(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "outcomeName" value
        EXPECTED: *  "outcomeName" is populated with outcome from OB outcomes list (e. g.: Brighton)
        """
        pass

    def test_005_verify_proper_handling_of_error_when_outcomename_from_api_accounthistory_is_absent_in_openbet_outcomes_list_or_sent_in_incorrect_format_so_cannot_be_converted_properly_and_mapped_with_outcomes_from_ob(self):
        """
        DESCRIPTION: Verify proper handling of error when "outcomeName" from API <accountHistory> is absent in OpenBet outcomes list (or sent in incorrect format so cannot be converted properly and mapped with outcomes from OB)
        EXPECTED: * "outcomeName" remains the same as it came from API <accountHistory>,  and corresponding error is added:
        EXPECTED: "otherAttributes": {..
        EXPECTED: "error": "Can't map outcome by : ...
        """
        pass
