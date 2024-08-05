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
class Test_C29439_Bet_Placement_on_a_few_selections_from_Private_Market_when_max_bet_limit_is_1(Common):
    """
    TR_ID: C29439
    NAME: Bet Placement on a few selections from Private Market when max bet limit is '1'
    DESCRIPTION: This test case verifies Bet Placement on a few selections from Private Market when max bet limit  is 'n' (n-any number of betting)
    DESCRIPTION: Note: **Max bet limit for offer** - the amount of placed bet on some market (Max bet limit for offer=1, the user is able to place a bet on such private market only once).
    DESCRIPTION: According to https://jira.openbet.com/browse/CORAGILE-6285 ticket, max bet limit could have only '1' value.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4.  Max bet limit for offer=1
    PRECONDITIONS: 5. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    """
    keep_browser_open = True

    def test_001_open_oxygen_app(self):
        """
        DESCRIPTION: Open Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' tab is present and selected by default **for mobile/tablet**
        EXPECTED: *   'Your Enhanced Markets' section is present at the top of the page (below Hero Header) **for mobile/tablet**
        """
        pass

    def test_002_add_a_few_selections_from_private_market_to_the_betslip(self):
        """
        DESCRIPTION: Add a few selections from private market to the Betslip
        EXPECTED: *   Selections are added
        EXPECTED: *   Betslip counter is increased **for mobile/tablet**
        """
        pass

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: *   Betslip page is opened
        EXPECTED: *   Added selections are displayed
        """
        pass

    def test_004_enter_stakes_in_stake_fields(self):
        """
        DESCRIPTION: Enter stakes in 'Stake' fields
        EXPECTED: 
        """
        pass

    def test_005_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   Error message: 'This offer applies to one selection only, please check & try again' is displayed on red background
        EXPECTED: *   Bets are not placed
        """
        pass
