import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C1922177_Banach_Successful_bet_placement_and_Bet_receipt(Common):
    """
    TR_ID: C1922177
    NAME: Banach. Successful bet placement and Bet receipt
    DESCRIPTION: Test case verifies successful Banach bet placement and Bet receipt
    DESCRIPTION: Win Alerts Toggle (if enabled in CMS) - is not present on Bet receipt (may be after redesign)
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **NOTE:** Banach Bets place via RemoteBetslip websocket
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for successful selections adding  | 51001
    PRECONDITIONS: || Response message for failed selections adding | 51002
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: To retrieve Banach Odds value check Network tab : price request
    PRECONDITIONS: - Open the app (site)
    PRECONDITIONS: - Navigate to the Football Event Details Page (EDP) with Banach markets available
    PRECONDITIONS: - Tap on the 'BUILD YOUR BET' CORAL / 'BET BUILDER' LADBROKES edp market name
    PRECONDITIONS: - Add few combinable selections to Build Your Bet **CORAL** / Bet Builder **LADBROKES** Dashboard from different markets accordions (Match Betting or Both teams to score, Double Chance)
    PRECONDITIONS: - Tap on the 'Place Bet' button on the Build Your Bet **CORAL** / Bet Builder **LADBROKES** Dashboard
    PRECONDITIONS: **Banach Betslip is opened**
    """
    keep_browser_open = True

    def test_001_verify_betslip_selections(self):
        """
        DESCRIPTION: Verify Betslip selections
        EXPECTED: - Selections are shown in the list;
        EXPECTED: - Player bets selections are shown in the format:
        EXPECTED: X.X To Make X+ Assists
        EXPECTED: X.X To Score X+ Goals (1+ Goals will be displayed as 'Anytime Goalscorer')
        EXPECTED: ![](index.php?/attachments/get/113549694)
        """
        pass

    def test_002_fill_some_value_in_the_stake_field_and_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Fill some value in the 'Stake' field and click/tap 'Place bet' button
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User Balance is updated
        """
        pass

    def test_003_verify_channel_used_for_bybbet_builder_bets(self):
        """
        DESCRIPTION: Verify channel used for BYB/Bet builder bets
        EXPECTED: Channel: "e" is present in '50011' request in 'remotebetslip' websocket
        """
        pass

    def test_004_verify_bet_receipt_on_ui(self):
        """
        DESCRIPTION: Verify Bet receipt on UI
        EXPECTED: Bet receipt contains correct info for the following items:
        EXPECTED: * Title BET RECEIPT
        EXPECTED: * Selections names are displayed as the list
        EXPECTED: * Odds
        EXPECTED: * Bet ID
        EXPECTED: * Total Stake and Total Est. Returns
        EXPECTED: * "Reuse selection" and "Done" buttons
        EXPECTED: **From OX100.3 ( **LADBROKES** ), OX 101.1 ( **CORAL** ) (fix version TBC):**
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
        EXPECTED: * Footer:
        EXPECTED: * 'Total stake'( **Coral** ) / 'Stake for this bet' ( **Ladbrokes** )
        EXPECTED: * 'Est. returns'( **Coral** ) / 'Potential returns' ( **Ladbrokes** )
        EXPECTED: ![](index.php?/attachments/get/113549705)
        """
        pass

    def test_005_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet Receipt
        EXPECTED: - Bet receipt is removed
        EXPECTED: - Selections are cleared in markets accordions
        """
        pass
