import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29040_Bet_Receipt_for_Multiple_Bets(Common):
    """
    TR_ID: C29040
    NAME: Bet Receipt for Multiple Bets
    DESCRIPTION: This test case verifies Bet Receipt information for Multiple Bets
    DESCRIPTION: AUTOTEST [C527796]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for selections from different events (multiples)
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: *   For checking information in OB admin system navigates to queries > customers > fill in 'username' field in 'Customer Search Criteria' section > click 'Find Customers' button > choose your customer from 'Result' table > put receipt number e.g. "O/0123364/0000141" in 'Receipt like' field in 'Bet Search Criteria' section > click 'Find Bet' button > check the correctness of placed bet
    PRECONDITIONS: *   It is NOT possible to place a bet on 'Unnamed favorite' Racing selections with checked 'Each Way' option (ticket BMA-3935, to be changed with ticket BMA-6736 (Remove the E/W text and checkbox from Betslip for Favourite selections))
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_002_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: * Bet Receipt header and subheader
        EXPECTED: * Card with multiples information
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons
        EXPECTED: * Player Bets clickable banner (only for events from the following leagues: Football: England - Premier League, Spain - La Liga, Italy - Serie A, UEFA Champions League; Basketball: NBA; American Football: NFL) **NOTE:** Only for Mobile view
        """
        pass

    def test_003_verify_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        pass

    def test_004_verify_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 11:57 and aligned by the right side
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        EXPECTED: * Favorites icon for Football selection only (Coral)
        """
        pass

    def test_005_verify_multiples_information(self):
        """
        DESCRIPTION: Verify Multiples information
        EXPECTED: Bet Receipt contains information about just placed Multiple bets:
        EXPECTED: Bet Receipt details for each multiple selections:
        EXPECTED: * Boosted bet section (in case of bet has been boosted)
        EXPECTED: * 'Multiples Type' text on each card (i.e. Double)
        EXPECTED: * Odds (for <Race> with 'SP' price - N/A) in the next format: i.e. @1/2 or @N/A
        EXPECTED: * Bet ID (Coral)/Receipt No (Ladbrokes). It starts with O and contains numeric values - i.e. O/0123828/0000155
        EXPECTED: * The outcome name
        EXPECTED: * Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: * Market type user has bet on - i.e. Win or Each Way and Event name to which the outcome belongs to. Should display in the next format: Market Name/Event Name
        EXPECTED: * 'CashOut' label if available
        EXPECTED: * 'Promo' icon if available (Ladbrokes only)
        EXPECTED: * 'Favourites' icon for Football stakes (Coral only)
        EXPECTED: *  'Win Alerts' toggle (Wrapper only)
        EXPECTED: *  Total Stake (Coral)/Stake for this bet (Ladbrokes)
        EXPECTED: *  Free Bet Amount  (if Free bet was selected)
        EXPECTED: *  Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        EXPECTED: Total Bet Receipt details:
        EXPECTED: * Total Stake
        EXPECTED: * Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        """
        pass

    def test_006_verify_buttons_displaying(self):
        """
        DESCRIPTION: Verify buttons displaying
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons are displayed
        EXPECTED: * Buttons are located in the bottom area of Bet Receipt
        """
        pass

    def test_007_check_placed_bets_correctness_in_ob_adminsystem_send_to_uat_receipt_number_eg_o01233640000141(self):
        """
        DESCRIPTION: Check placed bets correctness in OB admin system (send to UAT receipt number e.g. "O/0123364/0000141")
        EXPECTED: Information on Bet Receipt should correspond to data in OB admin system
        """
        pass
