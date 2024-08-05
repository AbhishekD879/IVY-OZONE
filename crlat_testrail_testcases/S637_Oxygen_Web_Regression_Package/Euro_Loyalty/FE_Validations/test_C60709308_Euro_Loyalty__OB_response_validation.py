import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C60709308_Euro_Loyalty__OB_response_validation(Common):
    """
    TR_ID: C60709308
    NAME: Euro Loyalty - OB response validation
    DESCRIPTION: This test case is to validate OB response through API
    PRECONDITIONS: 1.  User should have Postman API tool
    PRECONDITIONS: 2.  In OB 8 offer should present with below configuration
    PRECONDITIONS: **Offer1 Configuration :**
    PRECONDITIONS: > with valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes, Disable Cashout Checks=Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day(for testing all badges in same day leave this field empty)
    PRECONDITIONS: > three generic bet triggers with ranks 1,2 and 3
    PRECONDITIONS: > Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: > Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: **Offer2 configuration :**
    PRECONDITIONS: > With valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day(for testing all badges in same day leave this field empty)
    PRECONDITIONS: > One offer trigger with rank 1 and offer trigger should linked to OFFER one
    PRECONDITIONS: > three generic bet triggers with ranks 2,3 and 4
    PRECONDITIONS: > Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: > Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: *Offer 3 should be same as offer2 but should have offer trigger  with offer2 link.Like create 7 offers*
    PRECONDITIONS: **Dummy Offer 8 Configuration :**
    PRECONDITIONS: > With valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day
    PRECONDITIONS: > One offer trigger with rank 1 and offer trigger should linked to OFFER 7
    PRECONDITIONS: > should not have generic bet triggers
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: ***to create dummy offer follow any one step from below***
    PRECONDITIONS: 1.  Add a bet trigger with a level that it's not possible to place a bet on
    PRECONDITIONS: 2.  Setup that pretty much disqualifies any customer. e.g an Acc20+ bet type with very big odds and very big stake
    PRECONDITIONS: 3.  Even if you leave an OFFER trigger with a token, the customer will not be able to get the token. Firing the OFFER trigger (with current code) doesn't grant you any tokens
    PRECONDITIONS: **What is qualifying bet?**
    PRECONDITIONS: In OB Euro offer configuration, we have to add generic bet triggers(Bet type,min price, EUR, GBP, stake and Is inplay ) and trigger level for each trigger based on requirement
    PRECONDITIONS: for Euros trigget level should be Football > Football international > UEFA champion league > event > market. If we want to give badge on all events, add till type level
    PRECONDITIONS: Now user has to place bet as per above config to get respective badge
    """
    keep_browser_open = True

    def test_001_launch_postman_and_authenticate_with_valid_fe_credentials__1_httpsobbackoffice_tst2gib1egalacoralcomaccount_creatoractiongenerate_oxi_tokenusernameeuro1083passwordlbr12345_to_generate_oxi_apiparameterize_oxi_api_to_use_it_in_next_api_callhow_to_parameterizegot_o_test_tab_in_request_section_of_generate_token_api_call_and_paste_below_codevar_jsondata__jsonparseresponse_bodypostmansetenvironmentvariableoxi_token_jsondataoxi_tokencreate_new_environment_variable_and_take_variable_name_as_oxi_token(self):
        """
        DESCRIPTION: Launch postman and authenticate with valid FE credentials  [1]: https://obbackoffice-tst2.gib1.egalacoral.com/account_creator?action=generate_oxi_token&username=Euro1083&password=Lbr12345 to generate oxi-api
        DESCRIPTION: Parameterize oxi_api to use it in next API call
        DESCRIPTION: **How to Parameterize?**
        DESCRIPTION: Got o Test tab in request section of Generate-token API call and paste below code
        DESCRIPTION: var jsonData = JSON.parse(response Body);
        DESCRIPTION: postman.setEnvironmentVariable("oxi_token", jsonData.oxi_token);
        DESCRIPTION: Create new environment variable and take variable name as oxi_token
        EXPECTED: User should authenticate and oxi-api should generate
        """
        pass

    def test_002_in_next_api_call_freebet_return_with_get_method_2_httpsobbackoffice_tst2gib1egalacoralcomoxiapibody_should_be_like_thisdoctype_oxip_system_respaccountgetfreebetsdtdoxip_version70requestreqclientauth_returntokennuseradministratoruserpassword1nchargepasswordreqclientauthreqaccountgetfreebetstokenoxi_tokentokenreturnoffersyreturnoffersreturnfreebettokensnreturnfreebettokensreqaccountgetfreebetsrequestoxip_username_and_password_should_be_from_ob_from_token_we_are_getting_fe_user_credentials_show_the_response_will_show_all_available_offer_to_that_user(self):
        """
        DESCRIPTION: In next API call Freebet_return with get method [2]: https://obbackoffice-tst2.gib1.egalacoral.com//oxi/api
        DESCRIPTION: Body should be like this
        DESCRIPTION: <!DOCTYPE oxip SYSTEM "respAccountGetFreebets.dtd">
        DESCRIPTION: <oxip version="7.0">
        DESCRIPTION: <request>
        DESCRIPTION: <reqClientAuth returnToken="N">
        DESCRIPTION: <user>Administrator</user>
        DESCRIPTION: <password>1ncharge</password>
        DESCRIPTION: </reqClientAuth>
        DESCRIPTION: <reqAccountGetFreebets>
        DESCRIPTION: <token>{{oxi_token}}</token>
        DESCRIPTION: <returnOffers>Y</returnOffers>
        DESCRIPTION: <returnFreebetTokens>N</returnFreebetTokens>
        DESCRIPTION: </reqAccountGetFreebets>
        DESCRIPTION: </request>
        DESCRIPTION: </oxip>
        DESCRIPTION: > Username and password should be from OB
        DESCRIPTION: > from token we are getting FE user credentials show the response will show all available offer to that user
        EXPECTED: In response user will get all 8 offers and their triggers with valid IDs and status of each trigger should INACTIVE
        EXPECTED: API Response when user not placed any bet
        EXPECTED: <oxip version="7.0">
        EXPECTED: <response requestTime="0.0191">
        EXPECTED: <returnStatus>
        EXPECTED: <code>001</code>
        EXPECTED: <message>success</message>
        EXPECTED: <debug>01/04-09:22:10</debug>
        EXPECTED: </returnStatus>
        EXPECTED: <respAccountGetFreebets>
        EXPECTED: <currency>GBP</currency>
        EXPECTED: <freebetOffer>
        EXPECTED: <freebetOfferId>26082</freebetOfferId>
        EXPECTED: <freebetOfferName>Euro Loyalties Lvl 1</freebetOfferName>
        EXPECTED: <startTime>2020-11-16 10:00:00</startTime>
        EXPECTED: <endTime>2021-01-18 10:00:00</endTime>
        EXPECTED: <description>LASPREALASPONONFRBNN</description>
        EXPECTED: <freebetOfferRepeatable>1</freebetOfferRepeatable>
        EXPECTED: <freebetOfferReward>
        EXPECTED: <tokenId>43536</tokenId>
        EXPECTED: <tokenType>SPORTS</tokenType>
        EXPECTED: <tokenAmount>5.00</tokenAmount>
        EXPECTED: <tokenAmountPercent></tokenAmountPercent>
        EXPECTED: </freebetOfferReward>
        EXPECTED: <freebetTrigger>
        EXPECTED: <freebetTriggerId>44500</freebetTriggerId>
        EXPECTED: <freebetTriggerType>BET</freebetTriggerType>
        EXPECTED: <freebetTriggerRank>1</freebetTriggerRank>
        EXPECTED: <freebetTriggerQualification>N</freebetTriggerQualification>
        EXPECTED: <freebetTriggerDescription>Action which will fire off on all bets to check for any triggers related to the current bet</freebetTriggerDescription>
        EXPECTED: <freebetTriggerState>INACTIVE</freebetTriggerState>
        EXPECTED: <contributingBetIds>
        EXPECTED: <betId></betId>
        EXPECTED: </contributingBetIds>
        EXPECTED: </freebetTrigger>
        EXPECTED: <freebetTrigger>
        EXPECTED: <freebetTriggerId>44501</freebetTriggerId>
        EXPECTED: <freebetTriggerType>BET</freebetTriggerType>
        EXPECTED: <freebetTriggerRank>2</freebetTriggerRank>
        EXPECTED: <freebetTriggerQualification>N</freebetTriggerQualification>
        EXPECTED: <freebetTriggerDescription>Action which will fire off on all bets to check for any triggers related to the current bet</freebetTriggerDescription>
        EXPECTED: <freebetTriggerState>INACTIVE</freebetTriggerState>
        EXPECTED: <contributingBetIds>
        EXPECTED: <betId></betId>
        EXPECTED: </contributingBetIds>
        EXPECTED: </freebetTrigger>
        EXPECTED: <freebetTrigger>
        EXPECTED: <freebetTriggerId>44502</freebetTriggerId>
        EXPECTED: <freebetTriggerType>BET</freebetTriggerType>
        EXPECTED: <freebetTriggerRank>3</freebetTriggerRank>
        EXPECTED: <freebetTriggerQualification>N</freebetTriggerQualification>
        EXPECTED: <freebetTriggerDescription>Action which will fire off on all bets to check for any triggers related to the current bet</freebetTriggerDescription>
        EXPECTED: <freebetTriggerState>INACTIVE</freebetTriggerState>
        EXPECTED: <contributingBetIds>
        EXPECTED: <betId></betId>
        EXPECTED: </contributingBetIds>
        EXPECTED: </freebetTrigger>
        EXPECTED: <!-- More Euro Loyalties offers with no fired triggers-->
        EXPECTED: </freebetOffer>
        EXPECTED: <token> {{token}} </token>
        EXPECTED: </respAccountGetFreebets>
        EXPECTED: </response>
        EXPECTED: </oxip>
        """
        pass

    def test_003_login_with_user___credentials_should_be_as_in_step_and_place_a_qualifying_bet___stake_or_price_should_be_as_configured_in_bet_trigger_of_offer1(self):
        """
        DESCRIPTION: Login with user - credentials should be as in step and place a qualifying bet - stake or price should be as configured in bet trigger of offer1
        EXPECTED: 1.  Bet placement should be success
        EXPECTED: 2.  User should notified with message and should awarded with badge in Matchday rewards page
        """
        pass

    def test_004_click_on_send_buton_in_postman_of_freebet_return_api_call(self):
        """
        DESCRIPTION: Click on send buton in postman of freebet_return API call
        EXPECTED: Generic bet trigger with rank1 in offer1 should updated like below
        EXPECTED: >> freebetTriggerState = Active
        EXPECTED: >> freebetTriggeredDate = triggerDate(Bet placement date)
        EXPECTED: >> BetID and freebetTriggerAmount should updated
        EXPECTED: **<freebetTriggerState>ACTIVE</freebetTriggerState> <freebetTriggeredDate>2021-01-04 00:03:46 </freebetTriggeredDate>
        EXPECTED: <contributingBetIds>
        EXPECTED: <betId>931759</betId>
        EXPECTED: </contributingBetIds>
        EXPECTED: <freebetTriggerAmount>10.00</freebetTriggerAmount>**
        """
        pass

    def test_005_place_2nd_and_3rd_qualifying_bets_and_validate_response(self):
        """
        DESCRIPTION: Place 2nd and 3rd qualifying bets and validate response
        EXPECTED: 1.  Respective triggerID's in offer1 should updated as per above step
        EXPECTED: 2.  Offer1 details should disappear from response
        EXPECTED: 3.  User should awarded a freebet token
        EXPECTED: 4.  Awarded free bet token should show in user account - offers and free bets - sports free bet tokens
        """
        pass

    def test_006_verify_response_after_completing_of_stage1after_getting_one_freebet_and_before_placing_any_bets_in_stage2(self):
        """
        DESCRIPTION: Verify response after completing of stage1(after getting one freebet) and before placing any bets in stage2
        EXPECTED: 1.  Offer trigger in offer2 should become active
        EXPECTED: 2.  Last freebet trigger date should display
        EXPECTED: 3.  Offer1 and it's triggers should disappear
        EXPECTED: **<freebetTriggerType>OFFER</freebetTriggerType>
        EXPECTED: <freebetTriggerRank>1</freebetTriggerRank>
        EXPECTED: <freebetTriggerQualification>N</freebetTriggerQualification>
        EXPECTED: <freebetTriggerDescription>Offer trigger </freebetTriggerDescription>
        EXPECTED: <freebetTriggerState></freebetTriggerState>
        EXPECTED: <freebetTriggeredDate>2021-01-03 16:04:59</freebetTriggeredDate>**
        """
        pass

    def test_007_place_first_bet_in_stage_2_and_verify_response(self):
        """
        DESCRIPTION: Place first bet in stage 2 and verify response
        EXPECTED: Generic bet trigger with rank2 in offer2 should updated like below
        EXPECTED: >> freebetTriggerState = Active
        EXPECTED: >> freebetTriggeredDate = triggerDate(Bet placement date)
        EXPECTED: >> BetID and freebetTriggerAmount should updated
        EXPECTED: **<freebetTriggerState>ACTIVE</freebetTriggerState> <freebetTriggeredDate>2021-01-04 00:03:46 </freebetTriggeredDate>
        EXPECTED: <contributingBetIds>
        EXPECTED: <betId>931759</betId>
        EXPECTED: </contributingBetIds>
        EXPECTED: <freebetTriggerAmount>10.00</freebetTriggerAmount>**
        """
        pass

    def test_008_repeat_above_step_till_offer7_and_verify_response(self):
        """
        DESCRIPTION: repeat above step till offer7 and verify response
        EXPECTED: 1.  Should work as expected
        EXPECTED: 2.  Offer trigger in offer8 should active
        EXPECTED: 3.  Since there are no bet triggers offer should act as dummy offer
        """
        pass
