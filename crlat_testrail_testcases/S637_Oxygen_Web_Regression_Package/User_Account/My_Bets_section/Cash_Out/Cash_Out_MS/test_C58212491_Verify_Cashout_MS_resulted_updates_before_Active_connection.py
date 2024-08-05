import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C58212491_Verify_Cashout_MS_resulted_updates_before_Active_connection(Common):
    """
    TR_ID: C58212491
    NAME: Verify Cashout MS resulted updates before Active connection
    DESCRIPTION: This test case verifies the resulted updates in Cashout MS while before connection.
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51068
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to any page in the app except 'Cashout/Open Bets' tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request)
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page/tab
    PRECONDITIONS: - No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
    """
    keep_browser_open = True

    def test_001_in_ti_result_selection_save_changesindexphpattachmentsget100880880(self):
        """
        DESCRIPTION: In TI result selection, save changes.
        DESCRIPTION: ![](index.php?/attachments/get/100880880)
        EXPECTED: Selection becomes a resulted.
        """
        pass

    def test_002_navigate_to_cashoutopen_bets_tab_afterwards_and_check_the_updates_on_ui(self):
        """
        DESCRIPTION: Navigate to 'Cashout/Open Bets' tab afterwards and check the updates on UI
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In 'bet-details' EventStream appears ONLY 'Initial' call
        EXPECTED: ![](index.php?/attachments/get/100880927)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In WebSocket connection to Cashout MS is only initial bets response
        """
        pass

    def test_003_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet.
        EXPECTED: Results are same as above
        """
        pass
