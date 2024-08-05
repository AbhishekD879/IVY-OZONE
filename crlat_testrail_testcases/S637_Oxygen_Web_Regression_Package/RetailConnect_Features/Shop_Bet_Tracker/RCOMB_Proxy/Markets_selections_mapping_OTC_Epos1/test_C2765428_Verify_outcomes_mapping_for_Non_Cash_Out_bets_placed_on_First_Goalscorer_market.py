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
class Test_C2765428_Verify_outcomes_mapping_for_Non_Cash_Out_bets_placed_on_First_Goalscorer_market(Common):
    """
    TR_ID: C2765428
    NAME: Verify outcomes mapping for Non Cash Out bets placed on 'First Goalscorer' market
    DESCRIPTION: This test case verify outcomes mapping for Non Cash Out bets
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: HMN-2893 For mapping bet tracker’s selection
    DESCRIPTION: HMN-2917 Map outcome for first goalscorer market
    PRECONDITIONS: Request creation of Non Cash Out bets with following parameters
    PRECONDITIONS: |||:eventTypeName|:Market Name
    PRECONDITIONS: || First To Score |  First Goalscorer
    PRECONDITIONS: || Football HTFT |  Half Time/Full Time
    PRECONDITIONS: || Football CS  |  Correct Score
    PRECONDITIONS: || Football WLD |  Match Result
    PRECONDITIONS: || Half Time Win Lose Draw |  First Half Result
    PRECONDITIONS: || FB BIP FTWLD |  Match Result
    PRECONDITIONS: || FB BIP FT Correct Score |  Correct Score
    PRECONDITIONS: || FB BIP Next Player To Score |  Next Player To Score
    PRECONDITIONS: || FB BIP Next Team To Score |  Next Team To Score
    PRECONDITIONS: || FB BIP Half-Time/Full-Time |  Half Time / Full Time
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

    def test_001__select_barcode_which_contain_eventbet_placed_on_market_first_goalscorer_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which contain event/bet placed on market "First Goalscorer"
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_002_check_value_for_outcome___name_(self):
        """
        DESCRIPTION: Check value for "outcome": { ... "name" ..
        EXPECTED: "name" should contain player name in format 'Second_name,First_letter_of_first_name' or just 'Second_name' (e. g.: HLEB,A or HLEB),
        EXPECTED: Any additional/special characters are not supposed to be there (but '.' can be present at the end, if so PROXY will remove)
        """
        pass

    def test_003_check_if_name_outcome_name_is_present_in_openbet_outcomes_list_for_particular_event_using_a_linkhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown226eventtooutcomeforeventext_openbet20feed20formatopenbet_feedeventxxxxxxxxtranslationlangenincludeundisplayedtruewhere_xxxxxxxx___acoid_events_amelco_id(self):
        """
        DESCRIPTION: Check if "name" (outcome name) is present in OpenBet outcomes list for particular event using a link
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForEvent/~ext-Openbet%20Feed%20Format.OPENBET_FEED:EVENT:XXXXXXXX?translationLang=en&includeUndisplayed=true
        DESCRIPTION: where XXXXXXXX - ACOID (Event's Amelco ID)
        EXPECTED: * Outcome name is found in OB using second name and first letter of First name (e. g.: HLEB,A or HLEB)
        EXPECTED: * In OB outcome name is represented as 'First_name Second_name' (e. g.: Alieksandar Hleb)
        """
        pass

    def test_004__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_outcomename_value(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "outcomeName" value
        EXPECTED: *  "outcomeName" is populated with player name found in OB outcomes list (e. g.: Alieksandar Hleb)
        """
        pass

    def test_005_verify_proper_handling_of_error_when_outcomename_from_api_accounthistory_is_absent_in_openbet_outcomes_list_or_sent_in_incorrect_format_so_cannot_be_mapped_with_outcomes_from_ob(self):
        """
        DESCRIPTION: Verify proper handling of error when "outcomeName" from API <accountHistory> is absent in OpenBet outcomes list (or sent in incorrect format so cannot be mapped with outcomes from OB)
        EXPECTED: * "outcomeName" remains the same as it came from API <accountHistory>,  and corresponding error is added:
        EXPECTED: "otherAttributes": {..
        EXPECTED: "error": "Can't map outcome by : ...
        """
        pass
