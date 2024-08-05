import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C2490652_Banach_Quick_deposit_during_bet_placement(Common):
    """
    TR_ID: C2490652
    NAME: Banach. Quick deposit during bet placement
    DESCRIPTION: Test case describes Quick deposit during Banach bet placement
    DESCRIPTION: AUTOTEST [C2637448]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: STEP 2: To be updated with correct messages and actual content after Redesign
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: * User has added at least two combinable selections to BYB **Coral**/Bet Builder **Ladbrokes** Dashboard
    PRECONDITIONS: * User has triggered Quick deposit menu and entered CVV and Amount
    """
    keep_browser_open = True

    def test_001_tap_on_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Tap on DEPOSIT AND PLACE BET button
        EXPECTED: - On UI bet receipt is displayed
        EXPECTED: - User Balance is updated
        """
        pass

    def test_002_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: Correct values are displayed
        EXPECTED: - BET RECEIPT title
        EXPECTED: - 'Bet Placed Successfully' label and betting date and time
        EXPECTED: - Message **Your deposit was successful and your bet has been placed**
        EXPECTED: - Selections names
        EXPECTED: - Odds
        EXPECTED: - Bet ID
        EXPECTED: - Stake and Estimated Returns
        EXPECTED: From OX100.3 ( **LADBROKES ), OX 101.1 ( CORAL ) (fix version TBC):**
        EXPECTED: * Main Header: 'Bet receipt' title with 'X' button
        EXPECTED: * Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: * Block of Bet Type Summary:
        EXPECTED: * Win Alerts Toggle (if enabled in CMS)
        EXPECTED: * bet type name: i.e. Bet Builder / Build Your Bet
        EXPECTED: * price of BYB selections bet : e.g @90/1
        EXPECTED: * Bet ID:( **Coral** )/Receipt No:( **Ladbrokes** ) e.g Bet ID: 0/17781521/0000041
        EXPECTED: * For each selection:
        EXPECTED: * selection name
        EXPECTED: * market
        EXPECTED: * (for Player bets: selection name and market in the format of X.X To Make X+ Passes)
        EXPECTED: * event name
        EXPECTED: Footer:
        EXPECTED: 'Total stake'( Coral ) / 'Stake for this bet' ( Ladbrokes )
        EXPECTED: 'Est. returns'( Coral ) / 'Potential returns' ( Ladbrokes )
        EXPECTED: Before OX100:
        EXPECTED: - Reuse Selection and Done buttons
        EXPECTED: After OX100:
        EXPECTED: - Close button ('X')
        """
        pass

    def test_003_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: - Bet receipt is removed
        EXPECTED: - Selections are cleared in markets accordions
        """
        pass
