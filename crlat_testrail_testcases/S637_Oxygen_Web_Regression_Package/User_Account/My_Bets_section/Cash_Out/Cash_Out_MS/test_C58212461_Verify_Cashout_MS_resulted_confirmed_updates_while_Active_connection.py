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
class Test_C58212461_Verify_Cashout_MS_resulted_confirmed_updates_while_Active_connection(Common):
    """
    TR_ID: C58212461
    NAME: Verify Cashout MS resulted/confirmed updates while Active connection
    DESCRIPTION: This test case verifies the resulted updates in Cashout MS while Active connection.
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51068
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to Cashout/Open Bets tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request)
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Connection is active (user has not left the Cashout/Open Bets tab)
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page/tab
    PRECONDITIONS: - No requests to BPP getBetDetails and getBetDetail should be performed on cashout page
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_in_ti_result_selection_save_changesindexphpattachmentsget100880880(self):
        """
        DESCRIPTION: In TI result selection, save changes.
        DESCRIPTION: ![](index.php?/attachments/get/100880880)
        EXPECTED: Selection becomes Resulted.
        """
        pass

    def test_002_in_app_check_the_updates(self):
        """
        DESCRIPTION: In app check the updates
        EXPECTED: - Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In 'bet-details' EventStream appears call 'betUpdate' with info about bet.
        EXPECTED: ![](index.php?/attachments/get/100880899)
        EXPECTED: ![](index.php?/attachments/get/100880920)
        EXPECTED: **From release OX105:**
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - In WebSocket connection to Cashout MS appears 'betUpdate' message
        """
        pass

    def test_003_in_ti_suspend_same_event_on_any_other_level_eg_market(self):
        """
        DESCRIPTION: In TI suspend same event on any other level (eg. Market)
        EXPECTED: In 'bet-details' EventStream appears the second call 'betUpdate' with info about bet.
        EXPECTED: ![](index.php?/attachments/get/100880920)
        EXPECTED: **From release OX105:**
        EXPECTED: - In WebSocket connection to Cashout MS appears 'betUpdate' message
        """
        pass

    def test_004_from_release_ox106in_ti_confirm_result(self):
        """
        DESCRIPTION: **From release OX106:**
        DESCRIPTION: In TI Confirm result
        EXPECTED: Selection becomes Confirmed.
        """
        pass

    def test_005_from_release_ox106in_app_check_the_updates(self):
        """
        DESCRIPTION: **From release OX106:**
        DESCRIPTION: In app check the updates
        EXPECTED: **From release OX106:**
        EXPECTED: - Bet is suspended (susp label is present on the left in event card, 'Cash Out suspended' button disappears)
        EXPECTED: - In WebSocket connection to Cashout MS appears 'betUpdate' message
        EXPECTED: - In WebSocket connection to Cashout MS appears 'cashoutUpdate' message
        """
        pass

    def test_006_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet.
        EXPECTED: Results are same as above
        """
        pass
