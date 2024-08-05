import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C883421_Verify_Bet_Receipt_within_Quick_Bet(Common):
    """
    TR_ID: C883421
    NAME: Verify Bet Receipt within Quick Bet
    DESCRIPTION: This test case verifies Bet Receipt within Quick Bet
    DESCRIPTION: AUTOTEST [C1282623]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in and has a positive balance
    PRECONDITIONS: 3. Tap one <Sport>/<Race> selection
    PRECONDITIONS: 4. Make sure that Quick Bet is displayed at the bottom of the page
    PRECONDITIONS: 5. Enter value in 'Stake' field and select 'E/W' option if available
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully with correct date and time
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_002_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: * Bet Receipt header and subheader
        EXPECTED: * Card with bet information
        """
        pass

    def test_003_verify_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'X' button aligned by the right side
        """
        pass

    def test_004_verify_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 14:57 and aligned by the right side
        """
        pass

    def test_005_verify_card_layout(self):
        """
        DESCRIPTION: Verify card layout
        EXPECTED: Bet Receipt details for added selection:
        EXPECTED: * Boosted bet section (in case of bet has been boosted)
        EXPECTED: * 'Single' text on the card
        EXPECTED: * Odds of the selection (for <Race> with 'SP' price - N/A) in the next format: i.e. @1/2 or @SP
        EXPECTED: * Bet ID: (Coral)/Receipt No: (Ladbrokes). It starts with O and contains numeric values - i.e. O/0123828/0000155
        EXPECTED: * The outcome name
        EXPECTED: * Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: * Market type user has bet on - i.e. Win or Each Way and Event name to which the outcome belongs to. Should display in the next format: Market Name/Event Name
        EXPECTED: * 'CashOut' label if available
        EXPECTED: * 'Promo' icons if available
        EXPECTED: * 'Win Alerts' toggle (Wrapper only)
        EXPECTED: * Total Stake (Coral)/Stake for this bet (Ladbrokes)
        EXPECTED: * Free Bet Amount (if Free bet was selected)
        EXPECTED: * Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        """
        pass

    def test_006_verify_placed_bet_correctness_in_ob_admin_system_by_receipt_number_eg_o01233640000141(self):
        """
        DESCRIPTION: Verify placed bet correctness in OB admin system by receipt number e.g. "O/0123364/0000141"
        EXPECTED: Information on Bet Receipt should correspond to data in OB admin system
        """
        pass
