import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29438_Bet_Placement_on_Private_Market_when_offer_has_already_been_redeemed(Common):
    """
    TR_ID: C29438
    NAME: Bet Placement on Private Market when offer has already been redeemed
    DESCRIPTION: This test case verifies Bet Placement on Private Market when offer has already been redeemed.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: Note: **Max bet limit for offer** - amount of placed bet on some market (e.g. Max bet limit for offer=1, user is able to place a bet on such private market only once).
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    PRECONDITIONS: TO UPDATE:
    PRECONDITIONS: -error message
    PRECONDITIONS: -steps to reproduce the error
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' displayed
        """
        pass

    def test_002_add_selection_from_private_market_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from private market to the Betslip
        EXPECTED: Selection is added
        """
        pass

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Added selection is displayed
        """
        pass

    def test_004_reach_the_max_bet_limit_for_offer_from_step_2(self):
        """
        DESCRIPTION: Reach the max bet limit for offer from step #2
        EXPECTED: Private markets offer becomes redeemed
        """
        pass

    def test_005_enter_stake_in_stake_field(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_006_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   Error message informs that offer has already been redeemed is displayed
        EXPECTED: *   Impossible to place a bet on outcome from redeemed private market
        """
        pass
