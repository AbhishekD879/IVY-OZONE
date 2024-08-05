import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C1933495_Banach_Placing_bet_with_cash_stake_and_free_bet_stake(Common):
    """
    TR_ID: C1933495
    NAME: Banach. Placing bet with cash stake and free bet stake
    DESCRIPTION: Test case verifies successful Banach bet placement using freebet and cash stake
    DESCRIPTION: AUTOTEST [C2635856]
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels. Ahhoc tokens with default offer ID will not work for Banach bets. Only adhoc tokens created with associated Banach offer as mentioned above.
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
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
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: To check Odds value: Network tab -> price request
    PRECONDITIONS: **User has added at least two combinable selections to BYB/Bet Builder Dashboard**
    PRECONDITIONS: **User has selected Banach free bet and entered cash stake on Betslip**
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap PLACE BET button
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User balance is updated
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
        EXPECTED: - Title Bet receipt
        EXPECTED: - Names of markets with selections
        EXPECTED: - Odds
        EXPECTED: - Bet id
        EXPECTED: - Freebet stake
        EXPECTED: - Total Stake (Free bet + Cash stake) and Total Est. Returns
        EXPECTED: - buttons "Reuse selection" and "Done"
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
        EXPECTED: * 'Total stake'(Coral) / 'Stake for this bet' (Ladbrokes): Free bet with icon + Cash stake
        EXPECTED: * 'Est. returns'(Coral) / 'Potential returns' (Ladbrokes)
        """
        pass

    def test_004_close_bet_receipt(self):
        """
        DESCRIPTION: Close Bet receipt
        EXPECTED: - Bet receipt is removed
        EXPECTED: - Selections are cleared from markets accordions
        """
        pass
