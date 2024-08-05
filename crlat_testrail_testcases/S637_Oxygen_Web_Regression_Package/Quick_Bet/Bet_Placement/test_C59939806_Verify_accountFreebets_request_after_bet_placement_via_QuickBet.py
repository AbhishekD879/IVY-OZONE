import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C59939806_Verify_accountFreebets_request_after_bet_placement_via_QuickBet(Common):
    """
    TR_ID: C59939806
    NAME: Verify accountFreebets request after bet placement via QuickBet
    DESCRIPTION: This TC verifies that request to BPP /accountFreebets?freebetTokenType=SPORTS&channel=M:
    DESCRIPTION: 1 Is sent when user places NON BIR bet via QuickBet and claimedOffers is returned from remotebetslip MS (user is granted with new freebet)
    DESCRIPTION: 2 Is NOT sent when NO claimedOffers returned from remotebetslip for NON BIR bet
    DESCRIPTION: 3 Is always sent for BIR bets
    PRECONDITIONS: Setup new offer in OB with the following settings:
    PRECONDITIONS: - Description = Sports Non VIP
    PRECONDITIONS: - Maximum Tokens Holdable = 1
    PRECONDITIONS: - Unlimited Claims = Yes
    PRECONDITIONS: - Trigger = Generic Bet Trigger
    PRECONDITIONS: - Reward = Sportsbook Token (with redemption value = any/any)
    """
    keep_browser_open = True

    def test_001___open_app__open_devtools__login__add_non_bir_event_is_not_live_selection_to_quickbet__place_bet(self):
        """
        DESCRIPTION: - Open app
        DESCRIPTION: - Open DevTools
        DESCRIPTION: - Login
        DESCRIPTION: - Add NON BIR (event is not live) selection to quickbet
        DESCRIPTION: - Place bet
        EXPECTED: - remotebetslip websocket response 30012 contains claimedOffers property with claimed freebet
        EXPECTED: ![](index.php?/attachments/get/119867465)
        """
        pass

    def test_002___check_bpp_accountfreebetsfreebettokentypesportschannelm_request(self):
        """
        DESCRIPTION: - Check BPP /accountFreebets?freebetTokenType=SPORTS&channel=M request
        EXPECTED: - request is sent
        """
        pass

    def test_003___add_the_same_selection_to_quickbet__place_bet(self):
        """
        DESCRIPTION: - Add the same selection to QuickBet
        DESCRIPTION: - Place bet
        EXPECTED: - remotebetslip websocket response 30012 does NOT contain claimedOffers property
        """
        pass

    def test_004___check_bpp_accountfreebetsfreebettokentypesportschannelm_request(self):
        """
        DESCRIPTION: - Check BPP /accountFreebets?freebetTokenType=SPORTS&channel=M request
        EXPECTED: - request is NOT sent
        """
        pass

    def test_005___add_bir_event_is_live_selection_to_quickbet__place_bet(self):
        """
        DESCRIPTION: - Add BIR (event is live) selection to QuickBet
        DESCRIPTION: - Place bet
        EXPECTED: - remotebetslip websocket response 30012 does NOT contain claimedOffers property
        """
        pass

    def test_006___check_bpp_accountfreebetsfreebettokentypesportschannelm_request(self):
        """
        DESCRIPTION: - Check BPP /accountFreebets?freebetTokenType=SPORTS&channel=M request
        EXPECTED: - request is sent
        """
        pass

    def test_007___use_freebet_from_preconditions__add_bir_selection_to_quickbet__place_bet(self):
        """
        DESCRIPTION: - Use freebet (from preconditions)
        DESCRIPTION: - Add BIR selection to QuickBet
        DESCRIPTION: - Place bet
        EXPECTED: - remotebetslip websocket response 30012 contains claimedOffers property with claimed freebet
        """
        pass

    def test_008___check_bpp_accountfreebetsfreebettokentypesportschannelm_request(self):
        """
        DESCRIPTION: - Check BPP /accountFreebets?freebetTokenType=SPORTS&channel=M request
        EXPECTED: - request is sent
        """
        pass
