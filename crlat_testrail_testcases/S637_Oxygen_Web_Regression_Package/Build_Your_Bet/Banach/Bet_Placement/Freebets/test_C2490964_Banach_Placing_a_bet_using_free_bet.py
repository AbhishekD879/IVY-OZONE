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
class Test_C2490964_Banach_Placing_a_bet_using_free_bet(Common):
    """
    TR_ID: C2490964
    NAME: Banach. Placing a bet using free bet
    DESCRIPTION: Test case verifies Banach bet placement using free bet token and Bet receipt
    DESCRIPTION: AUTOTEST [C2610640]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: * User has added at least two combinable selections to BYB **Coral**/Bet Builder **Ladbrokes** Dasboard
    PRECONDITIONS: * On Betslip user has selected free bet without cash stake
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap PLACE BET button
        EXPECTED: - On UI bet receipt is displayed
        EXPECTED: - User balance is not changed
        """
        pass

    def test_002_verify_channel_used_for_bybbet_builder_bets(self):
        """
        DESCRIPTION: Verify channel used for BYB/Bet builder bets
        EXPECTED: Channel: "e" is present in '50011' request in 'remotebetslip' websocket
        """
        pass

    def test_003_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet receipt
        EXPECTED: Bet receipt contains correct info for the following items:
        EXPECTED: * Title BET RECEIPT
        EXPECTED: * Selections names are displayed in the next format: - Market Name SELECTION NAME
        EXPECTED: * Odds
        EXPECTED: * Bet ID
        EXPECTED: * Free bet stake
        EXPECTED: * Total Stake and Total Est. Returns
        EXPECTED: * "Reuse selection" and "Done" buttons
        EXPECTED: **For OX100.X (fix version TBC):**
        EXPECTED: * Main Header: 'Bet receipt' title with 'X' button
        EXPECTED: * Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: * Block of Bet Type Summary:
        EXPECTED: * Win Alerts Toggle (if enabled in CMS)
        EXPECTED: * bet type name: e.g Single
        EXPECTED: * price of BYB selections bet : e.g @90/1
        EXPECTED: * Bet ID:(Coral)/Receipt No:(Ladbrokes) e.g Bet ID: 0/17781521/0000041
        EXPECTED: * For each selection:
        EXPECTED: * selection name
        EXPECTED: * market
        EXPECTED: * Footer:
        EXPECTED: * 'Total stake'(Coral) / 'Stake for this bet' (Ladbrokes): Free bet with icon e.g. FB £5.00
        EXPECTED: * 'Est. returns'(Coral) / 'Potential returns' (Ladbrokes)
        """
        pass

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet Receipt
        EXPECTED: * Bet receipt is removed
        EXPECTED: * Selections are cleared in markets accordions
        """
        pass
