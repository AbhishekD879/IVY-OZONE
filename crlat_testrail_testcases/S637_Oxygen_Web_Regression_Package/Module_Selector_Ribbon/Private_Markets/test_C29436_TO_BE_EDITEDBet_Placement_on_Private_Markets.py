import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29436_TO_BE_EDITEDBet_Placement_on_Private_Markets(Common):
    """
    TR_ID: C29436
    NAME: [TO BE EDITED]Bet Placement on Private Markets
    DESCRIPTION: Autotest - [C2377241]
    DESCRIPTION: This test case verifies Bet Placement on Private Markets.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: This testcase needs to be edited according to the latest changes.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 3.  User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 5.  Private market offers should be active (not expired)
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' tab is present and selected by default **for mobile/tablet**
        EXPECTED: *   'Your Enhanced Markets' section is present at the top of the page (below Hero Header) **for mobile/tablet**
        EXPECTED: *   All eligible private markets and associated selections are shown
        """
        pass

    def test_002_add_selection_from_private_market_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from private market to the Betslip
        EXPECTED: *   Selection is added
        EXPECTED: *   Betslip counter is increased **for mobile/tablet**
        """
        pass

    def test_003_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: *   Betslip page is opened
        EXPECTED: *   Added selection is displayed
        """
        pass

    def test_004_verify_added_selection_correctness(self):
        """
        DESCRIPTION: Verify added selection correctness
        EXPECTED: *   Selection name
        EXPECTED: *   Market name
        EXPECTED: *   Event start time and name
        EXPECTED: *   Odds
        EXPECTED: are correct and correspond to the information in response from SS
        """
        pass

    def test_005_enter_valid_stake_in_stake_field(self):
        """
        DESCRIPTION: Enter valid stake in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_006_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is shown
        """
        pass

    def test_007_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: 1. Bet Receipt contains the following information:
        EXPECTED: *   header 'Singles' with the total number of single bets - i.e. Singles (1)
        EXPECTED: *   the selection made by the customer - i.e. outcome (display the outcome name)
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name to which the outcome belongs to
        EXPECTED: *   the Bet ID. The Bet ID is start with O and contain numeric values - i.e. O/0123828/0000155
        EXPECTED: *   'i' icon
        EXPECTED: *   Odds of the selection (for <Race> with 'SP' price - N/A)
        EXPECTED: *   Stake
        EXPECTED: *   Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: *   Total Stake
        EXPECTED: *   Total Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: 2. Information in Bet Receipt corresponds to placed bet information
        """
        pass

    def test_008_check_placed_bet_correctness_in_ob_backoffice_using_the_bet_receipt_number(self):
        """
        DESCRIPTION: Check placed bet correctness in OB Backoffice using the Bet Receipt number
        EXPECTED: Information should be correct
        """
        pass

    def test_009_add_a_few_selections_to_the_betslip_from_different_private_markets(self):
        """
        DESCRIPTION: Add a few selections to the Betslip from different private markets
        EXPECTED: *   Selections are added
        EXPECTED: *   Betslip counter is increased **for mobile/tablet**
        """
        pass

    def test_010_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps #3-9
        EXPECTED: 
        """
        pass
