import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C16694105_Vanilla_Bet_Receipt_for_single_selection(Common):
    """
    TR_ID: C16694105
    NAME: [Vanilla] Bet Receipt for single selection
    DESCRIPTION: This test case verifies bet receipt after placing a single bet
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for single selection
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: NOTE:
    PRECONDITIONS: * For checking information in OB admin system navigates to queries > customers > fill in 'username' field in 'Customer Search Criteria' section > click 'Find Customers' button > choose your customer from 'Result' table > put receipt number e.g. "O/0123364/0000141" in 'Receipt like' field in 'Bet Search Criteria' section > click 'Find Bet' button > check the correctness of placed bet
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button
        EXPECTED: Bet is placed successfully
        EXPECTED: User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_002_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: **Mobile view:**
        EXPECTED: **QD:**
        EXPECTED: * Bet Receipt header and subheader
        EXPECTED: * Card with bet information
        EXPECTED: ![](index.php?/attachments/get/34351)
        EXPECTED: **BetSlip:**
        EXPECTED: * Header & subheader
        EXPECTED: * Card with bet information
        EXPECTED: * Buttons 'Reuse selection' & 'Go betting'
        EXPECTED: ![](index.php?/attachments/get/397502)
        EXPECTED: **Desktop view:**
        EXPECTED: * Subheader
        EXPECTED: * Card with bet information
        EXPECTED: * Buttons 'Reuse selection' & 'Go betting'
        EXPECTED: ![](index.php?/attachments/get/397492)
        """
        pass

    def test_003_verify_bet_receipt_header_mobile_qd_mobile_betslip(self):
        """
        DESCRIPTION: Verify Bet Receipt header (mobile QD/ Mobile Betslip)
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: **Quick Bet:**
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: ![](index.php?/attachments/get/412704)
        EXPECTED: **Betslip:**
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * user's balance
        EXPECTED: ![](index.php?/attachments/get/412705)
        """
        pass

    def test_004_verify_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: **Desktop/Mobile Betslip:**
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: e.g. 09/19/2019, 11:57
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        EXPECTED: * 'Favourite all' with a star icon for Football selection only (Coral)
        EXPECTED: ![](index.php?/attachments/get/397503)
        EXPECTED: **Mobile Quick Bet:**
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: e.g. 09/19/2019, 11:57
        EXPECTED: ![](index.php?/attachments/get/34373)
        """
        pass

    def test_005_verify_card_layout(self):
        """
        DESCRIPTION: Verify card layout
        EXPECTED: Bet Receipt details for each selection:
        EXPECTED: * Boosted bet section (in case of bet has been boosted)
        EXPECTED: * 'Single' text on the card
        EXPECTED: * Odds of the selection (for <Race> with 'SP' price - N/A) in the next format: e.g. @1/2 or @SP
        EXPECTED: * Bet ID - starts with O and contains numeric values - i.e. O/0123828/0000155
        EXPECTED: * The outcome name
        EXPECTED: * Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: * Market type user has bet on - e.g. Win or Each Way and Event name to which the outcome belongs to. Should display in the next format: Market Name/Event Name
        EXPECTED: * 'Cash Out' label if available /other signposting labels
        EXPECTED: * 'Stake'
        EXPECTED: * 'Est. Returns'
        EXPECTED: Total Bet Receipt details for Desktop/Mobile Betslip:
        EXPECTED: * 'Total Stake'
        EXPECTED: * 'Estimated Returns'
        EXPECTED: ![](index.php?/attachments/get/34376)
        """
        pass

    def test_006_verify_buttons_desktop_betslip_mobile_betslip(self):
        """
        DESCRIPTION: Verify buttons (Desktop Betslip/ Mobile Betslip)
        EXPECTED: 'Reuse Selections' and 'Go Betting' buttons are displayed
        EXPECTED: Buttons are located in the bottom area of Bet Receipt
        EXPECTED: ** Buttons are not displayed in Quick Bet on Mobile
        """
        pass

    def test_007_verify_placed_bet_correctness_in_ob_admin_system_by_receipt_number_eg_o01233640000141(self):
        """
        DESCRIPTION: Verify placed bet correctness in OB admin system by receipt number e.g. "O/0123364/0000141"
        EXPECTED: Information on Bet Receipt should correspond to data in OB admin system
        """
        pass
