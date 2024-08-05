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
class Test_C2765433_Verify_outcomes_mapping_for_Non_Cash_Out_bets_placed_on_Next_Player_To_Score_Next_Team_To_Score_markets(Common):
    """
    TR_ID: C2765433
    NAME: Verify outcomes mapping for Non Cash Out bets placed on 'Next Player To Score', 'Next Team To Score' markets
    DESCRIPTION: This test case verify outcomes mapping for Non Cash Out bets
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: HMN-2893 For mapping bet tracker’s selection
    PRECONDITIONS: Request creation of Non Cash Out bets with following parameters
    PRECONDITIONS: |||:eventTypeName|:Market Name
    PRECONDITIONS: || FB BIP Next Player To Score |  Next Player To Score
    PRECONDITIONS: || FB BIP Next Team To Score |  Next Team To Score
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

    def test_001__select_barcode_which_contain_eventbet_placed_on_market_next_player_to_score_event_type_name__fb_bip_next_player_to_score_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which contain event/bet placed on market "Next Player To Score" (Event Type Name = FB BIP Next Player To Score)
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_002_check_value_for_outcome___name_(self):
        """
        DESCRIPTION: Check value for "outcome": { ... "name" ..
        EXPECTED: * "name" contains player name in format 'Second_name,First_letter_of_first_name'  (e. g.: HLEB,A)
        EXPECTED: ('.' can be present at the end of outcome name, if so PROXY will remove)
        """
        pass

    def test_003__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_outcomename_value(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "outcomeName" value
        EXPECTED: * "outcomeName" remains the same as it came from API <accountHistory>,  and error is added:
        EXPECTED: "otherAttributes": {..
        EXPECTED: "error": "Can't map market by : ...
        EXPECTED: (outcome name cannot me mapped as market name is absent in OB markets list for test evetn)
        """
        pass

    def test_004__select_barcode_which_contain_eventbet_placed_on_market_next_team_to_score__event_type_name__fb_bip_next_team_to_score_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which contain event/bet placed on market "Next Team To Score " (Event Type Name = FB BIP Next Team To Score)
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_005_check_value_for_outcome___name_(self):
        """
        DESCRIPTION: Check value for "outcome": { ... "name" ..
        EXPECTED: * "name" contains Home team name or Away team name (e. g.: Brighton )
        """
        pass

    def test_006__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_outcomename_value(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "outcomeName" value
        EXPECTED: * "outcomeName" remains the same as it came from API <accountHistory>,  and error is added:
        EXPECTED: "otherAttributes": {..
        EXPECTED: "error": "Can't map market by : ...
        EXPECTED: (outcome name cannot me mapped as market name is absent in OB markets list for test evetn)
        """
        pass
