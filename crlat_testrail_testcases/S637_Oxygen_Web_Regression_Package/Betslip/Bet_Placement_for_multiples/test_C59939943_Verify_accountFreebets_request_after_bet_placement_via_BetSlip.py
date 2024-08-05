import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59939943_Verify_accountFreebets_request_after_bet_placement_via_BetSlip(Common):
    """
    TR_ID: C59939943
    NAME: Verify accountFreebets request after bet placement via BetSlip
    DESCRIPTION: This TC verifies that request to BPP /accountFreebets?freebetTokenType=SPORTS&channel=M:
    DESCRIPTION: 1 Is sent when a user places NON-BIR bet via BetSlip and claimedOffers is returned from placeBet MS (user is granted with new freebet)
    DESCRIPTION: 2 Is NOT sent when NO claimedOffers returned from placeBet for NON-BIR bet
    DESCRIPTION: 3 Is always sent for BIR bets
    PRECONDITIONS: Setup new offer in OB with the following settings:
    PRECONDITIONS: - Description = Sports Non VIP
    PRECONDITIONS: - Maximum Tokens Holdable = 1
    PRECONDITIONS: - Unlimited Claims = Yes
    PRECONDITIONS: - Trigger = Generic Bet Trigger
    PRECONDITIONS: - Reward = Sportsbook Token (with redemption value = any/any)
    PRECONDITIONS: OR - use created on from TI (need to search)
    """
    keep_browser_open = True

    def test_001_verify_that__accountfreebets_request_is_sent_when_placebet_response_from_bpp__has_status__claimed_in_all_claimedoffers_elements__open_app__open_devtools__login__add_non_bir_event_is_not_live_selection_to_betslip__place_bet(self):
        """
        DESCRIPTION: Verify that  /accountFreebets request is sent when /placeBet response from BPP  has "status = claimed" in all claimedOffers elements:
        DESCRIPTION: - Open app
        DESCRIPTION: - Open DevTools
        DESCRIPTION: - Login
        DESCRIPTION: - Add NON-BIR (event is not live) selection to betslip
        DESCRIPTION: - Place bet
        EXPECTED: - /placeBet response from BBP contains parsed claimedOffers data from respBetPlace  (claimedOffers property with claimed freebet)
        EXPECTED: ![](index.php?/attachments/get/119870640)
        """
        pass

    def test_002___check_that_accountfreebetsfreebettokentypesportschannelm_request_is_sent_in_network_tab(self):
        """
        DESCRIPTION: - Check that "accountFreebets?freebetTokenType=SPORTS&channel=M" request is sent in Network tab;
        EXPECTED: - the request is sent;
        EXPECTED: - the request contains list of all freebet offers that User has;
        """
        pass

    def test_003_verify_that_no_accountfreebets_request_is_sent_when_placebet_response_from_bpp__has_no_status__claimed_in_all_claimedoffers_elements__reuse_selection_or_place_new_bet_for_non_bir_event__check_placebet_response_from_bpp(self):
        """
        DESCRIPTION: Verify that NO /accountFreebets request is sent when /placeBet response from BPP  has no "status = claimed" in all claimedOffers elements:
        DESCRIPTION: - Reuse selection or place new bet for NON-BIR event;
        DESCRIPTION: - Check /placeBet response from BPP;
        EXPECTED: - /placeBet response from BBP DOESN'T contain "status = claimed" in all claimedOffers elements;
        """
        pass

    def test_004___check_that_no_accountfreebetsfreebettokentypesportschannelm_request_is_sent_in_network_tab(self):
        """
        DESCRIPTION: - Check that NO "accountFreebets?freebetTokenType=SPORTS&channel=M" request is sent in Network tab;
        EXPECTED: - request is NOT sent
        """
        pass

    def test_005_verify_that_placing_bet_for_bir_event_will_always_make_additional_accountfreebets_call__add_bir_event_is_live_selection_to_betslip__place_bet(self):
        """
        DESCRIPTION: Verify that placing bet for BIR event will always make additional /accountFreebets call;
        DESCRIPTION: - Add BIR (event is live) selection to betSlip
        DESCRIPTION: - Place bet
        EXPECTED: - /placeBet response from BBP received;
        EXPECTED: - /placeBet response from BBP DOESN'T contain "status = claimed" in all claimedOffers elements;
        """
        pass

    def test_006___check_that_accountfreebetsfreebettokentypesportschannelm_request_is_sent_in_network_tab(self):
        """
        DESCRIPTION: - Check that "accountFreebets?freebetTokenType=SPORTS&channel=M" request is sent in Network tab;
        EXPECTED: - request is sent
        """
        pass

    def test_007_verify_that_accountfreebets_request_is_sent_when_bet_contains_freebet_odder_and__placed_for_bir_event__use_freebet_from_preconditions__add_bir_selection_to_betslip__place_bet(self):
        """
        DESCRIPTION: Verify that /accountFreebets request is sent when bet contains freeBet odder and  placed for BIR event:
        DESCRIPTION: - Use freebet (from preconditions)
        DESCRIPTION: - Add BIR selection to betSlip
        DESCRIPTION: - Place bet
        EXPECTED: - /placeBet response from BBP contains claimedOffers property with claimed freebet
        """
        pass

    def test_008___check_bpp_accountfreebetsfreebettokentypesportschannelm_request(self):
        """
        DESCRIPTION: - Check BPP /accountFreebets?freebetTokenType=SPORTS&channel=M request
        EXPECTED: - request is sent
        """
        pass
