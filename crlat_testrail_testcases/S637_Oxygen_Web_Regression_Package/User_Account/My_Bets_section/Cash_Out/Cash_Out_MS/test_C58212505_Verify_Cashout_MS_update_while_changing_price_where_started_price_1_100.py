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
class Test_C58212505_Verify_Cashout_MS_update_while_changing_price_where_started_price_1_100(Common):
    """
    TR_ID: C58212505
    NAME: Verify Cashout MS update while changing price, where started price > 1/100
    DESCRIPTION: This test case verifies the updates in Cashout MS when event is suspended and price changes from A to A and from A to B, where:
    DESCRIPTION: A: price > 1/100
    DESCRIPTION: B: price <= 1/100
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51061
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMA-51067
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to 'Cashout/Open Bets' tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request)
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Price odds of the bet are > 1/100 (eg. 1/10, 1/2)
    PRECONDITIONS: - Connection is active (user has not left the Cashout/Open Bets tab)
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_in_ti_suspend_the_eventmarketselection_eg_event_save_changes(self):
        """
        DESCRIPTION: In TI suspend the event/market/selection (eg. Event), save changes
        EXPECTED: Event/market/selection becomes suspended
        """
        pass

    def test_002_in_app_check_the_updates(self):
        """
        DESCRIPTION: In app check the updates
        EXPECTED: In Cashout MS betUpdate 'CASHOUT_SELN_SUSPENDED' is received
        EXPECTED: ![](index.php?/attachments/get/101002547)
        EXPECTED: **From release XXX.XX**
        EXPECTED: * Cashout MS will send betUpdate message with 'CASHOUT_SELN_SUSPENDED'cashoutValue
        """
        pass

    def test_003_in_ti_change_price_from_a_to_a_wherea_price__1100eg_110_to_112(self):
        """
        DESCRIPTION: In TI change price from A to A, where
        DESCRIPTION: A: price > 1/100
        DESCRIPTION: (e.g. 1/10 to 1/12)
        EXPECTED: New price is saved
        """
        pass

    def test_004_in_app_check_the_updates(self):
        """
        DESCRIPTION: In app check the updates
        EXPECTED: CashoutMS does NOT make request to Cashout Offer service
        EXPECTED: and do NOT send any 'cashoutUpdate' message
        """
        pass

    def test_005_in_ti_change_price_from_a_to_b_wherea_price__1100b_price__1100eg_112_to_1200(self):
        """
        DESCRIPTION: In TI change price from A to B, where
        DESCRIPTION: A: price > 1/100
        DESCRIPTION: B: price <= 1/100
        DESCRIPTION: (e.g. 1/12 to 1/200)
        EXPECTED: New price is saved
        """
        pass

    def test_006_in_app_check_the_updates(self):
        """
        DESCRIPTION: In app check the updates
        EXPECTED: In Cashout MS betUpdate getBetDetail (full betUpdate)is received
        EXPECTED: ![](index.php?/attachments/get/101002549)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Cashout MS will send betUpdate message
        """
        pass

    def test_007_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet
        EXPECTED: Results are same as above
        """
        pass
