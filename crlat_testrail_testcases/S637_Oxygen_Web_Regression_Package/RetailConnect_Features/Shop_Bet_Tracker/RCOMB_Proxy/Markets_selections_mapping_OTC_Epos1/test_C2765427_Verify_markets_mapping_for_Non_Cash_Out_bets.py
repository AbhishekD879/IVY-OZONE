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
class Test_C2765427_Verify_markets_mapping_for_Non_Cash_Out_bets(Common):
    """
    TR_ID: C2765427
    NAME: Verify markets mapping for Non Cash Out bets
    DESCRIPTION: This test case verify markets mapping for Non Cash Out bets
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-2892 Story for mapping bettracker
    DESCRIPTION: HMN-2918 Proxy: Unable to map outcome when markename = NULL
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
    PRECONDITIONS: ||   |
    PRECONDITIONS: || Football Competition |  Team1 V Team2 FPTS
    PRECONDITIONS: || Football Competition |  Team1 V Team2 LPTS
    PRECONDITIONS: || Football Competition |  Team1 V Team2 ATS
    PRECONDITIONS: || Football Competition |  Team1 V Team2 HAT
    PRECONDITIONS: || Football Competition |  Team1 V Team2 TOMG
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

    def test_001__select_barcode_which_contain_event_with_eventtype__first_to_score_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which contain event with "eventType" = "First To Score"
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_002__check_value_for_market___name__check_value_for__eventtype___name_(self):
        """
        DESCRIPTION: * Check value for "market": { ... "name" ..
        DESCRIPTION: * Check value for  "eventType": {  "name" ..
        EXPECTED: * Market Name is empty
        EXPECTED: * eventType Name is "First To Score"
        """
        pass

    def test_003__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_marketname_and_marketid_values_check_if_marketname_is_present_in_openbet_markets_list_for_particular_event_using_a_linkhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown226eventtooutcomeforeventext_openbet20feed20formatopenbet_feedeventxxxxxxxxtranslationlangenincludeundisplayedtruewhere_xxxxxxxx___acoid_events_amelco_id(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "marketName" and "marketId" values
        DESCRIPTION: * Check if "marketName" is present in OpenBet markets list for particular event using a link
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForEvent/~ext-Openbet%20Feed%20Format.OPENBET_FEED:EVENT:XXXXXXXX?translationLang=en&includeUndisplayed=true
        DESCRIPTION: where XXXXXXXX - ACOID (Event's Amelco ID)
        EXPECTED: * "marketName" is populated with "First Goal Scorer"
        EXPECTED: * "marketName" "First Goal Scorer" is present in OpenBet markets list
        EXPECTED: * "marketId" is populated with correct id of "First Goal Scorer" market
        """
        pass

    def test_004_repeat_steps_1_3_for_following_events_types_football_htft_football_cs_football_wld_half_time_win_lose_draw_fb_bip_ftwld_fb_bip_ft_correct_score_fb_bip_next_player_to_score_fb_bip_next_team_to_score_fb_bip_half_timefull_time(self):
        """
        DESCRIPTION: Repeat steps №1-3 for following Events Types:
        DESCRIPTION: || Football HTFT
        DESCRIPTION: || Football CS
        DESCRIPTION: || Football WLD
        DESCRIPTION: || Half Time Win Lose Draw
        DESCRIPTION: || FB BIP FTWLD
        DESCRIPTION: || FB BIP FT Correct Score
        DESCRIPTION: || FB BIP Next Player To Score
        DESCRIPTION: || FB BIP Next Team To Score
        DESCRIPTION: || FB BIP Half-Time/Full-Time
        EXPECTED: * "marketName" is populated with correct Market Name associated with corresponding Events Types (see precondition)
        EXPECTED: * "marketName"  is present in OpenBet markets list
        EXPECTED: * "marketId" is populated with correct id of corresponding market
        """
        pass

    def test_005_repeat_steps_1_3_with_all_markets_of_events_type_football_competition_team1_v_team2_fpts_team1_v_team2_lpts_team1_v_team2_ats_team1_v_team2_hat_team1_v_team2_tomg(self):
        """
        DESCRIPTION: Repeat steps №1-3 with all markets of Events Type "Football Competition":
        DESCRIPTION: || Team1 V Team2 FPTS
        DESCRIPTION: || Team1 V Team2 LPTS
        DESCRIPTION: || Team1 V Team2 ATS
        DESCRIPTION: || Team1 V Team2 HAT
        DESCRIPTION: || Team1 V Team2 TOMG
        EXPECTED: * "marketName" is mapped correctly accordingly to the rule:
        EXPECTED: "Team1 V Team2 FPTS" is  mapped with market "First Goal Scorer"
        EXPECTED: "Team1 V Team2 LPTS" is  mapped with market ""Last Goal Scorer"
        EXPECTED: "Team1 V Team2 ATS" is  mapped with market "Goal Scorer - Anytime"
        EXPECTED: "Team1 V Team2 HAT" is  mapped with market "Goal Scorer - Hat-Trick"
        EXPECTED: "Team1 V Team2 TOMG" is  mapped with market "Goal Scorer - 2 or more"
        EXPECTED: * mapped "marketName"  is present in OpenBet markets list
        EXPECTED: * "marketId" is populated with correct id of corresponding market
        """
        pass

    def test_006__select_barcode_which_is_coming_from_api_accounthistory_with_already_populated_market_name_load_api_accounthistory_service_via_this_barcode(self):
        """
        DESCRIPTION: * Select barcode which is coming from API <accountHistory> with already populated Market Name
        DESCRIPTION: * Load API <accountHistory> service via this barcode
        EXPECTED: Information about barcode is retrieved correctly
        """
        pass

    def test_007__check_value_for_market___name__check_value_for__eventtype___name_(self):
        """
        DESCRIPTION: * Check value for "market": { ... "name" ..
        DESCRIPTION: * Check value for  "eventType": {  "name" ..
        EXPECTED: * Market Name is populated with some value
        EXPECTED: * eventType Name - any from preconditions
        """
        pass

    def test_008__load_the_bet_details_via_use_the_barcode__as_a_parameter_httpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusingget_check_marketname_and_marketid_values_check_if_marketname_is_present_in_openbet_markets_list_for_particular_event_using_a_linkhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown226eventtooutcomeforeventext_openbet20feed20formatopenbet_feedeventxxxxxxxxtranslationlangenincludeundisplayedtruewhere_xxxxxxxx___acoid_events_amelco_id(self):
        """
        DESCRIPTION: * Load the bet details via (Use the barcode  as a parameter) https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: * Check "marketName" and "marketId" values
        DESCRIPTION: * Check if "marketName" is present in OpenBet markets list for particular event using a link
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForEvent/~ext-Openbet%20Feed%20Format.OPENBET_FEED:EVENT:XXXXXXXX?translationLang=en&includeUndisplayed=true
        DESCRIPTION: where XXXXXXXX - ACOID (Event's Amelco ID)
        EXPECTED: * if "marketName" from API <accountHistory> is found in OpenBet markets list then "marketName" and "marketId" are populated accordingly
        EXPECTED: * If  "marketName" from API <accountHistory> is absent in OpenBet markets list then "marketName"  is mapped by  "eventType" (see precondition)
        EXPECTED: * If  "marketName" from API <accountHistory> is absent in OpenBet markets list and  "eventType" is unexpected so cannot be used for mapping then  "marketName" remains the same as it came from API <accountHistory>, "marketId" parameter is missed and corresponding error is added:
        EXPECTED: "otherAttributes": {..
        EXPECTED: "error": "Can't map market by : ...
        """
        pass
