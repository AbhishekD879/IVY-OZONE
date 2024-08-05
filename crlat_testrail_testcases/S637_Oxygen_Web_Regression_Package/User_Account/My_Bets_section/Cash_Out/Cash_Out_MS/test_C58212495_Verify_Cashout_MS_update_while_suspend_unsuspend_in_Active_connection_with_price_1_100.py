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
class Test_C58212495_Verify_Cashout_MS_update_while_suspend_unsuspend_in_Active_connection_with_price_1_100(Common):
    """
    TR_ID: C58212495
    NAME: Verify Cashout MS update while suspend/unsuspend in Active connection with price <= 1/100
    DESCRIPTION: This test case verifies the updates in Cashout MS when event becomes suspended and has odds price <= 1/100
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
    PRECONDITIONS: **From OX105:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WS connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Price odds of the bet are <= 1/100 (eg. 1/101, 1/102)
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
        EXPECTED: - Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: Note: if bet is suspended on Selection level 'Cash Out <value>' button is still active, only bet is displayed with susp label!
        EXPECTED: - In Cashout MS betUpdate getBetDetail (full betUpdate)is received
        EXPECTED: ![](index.php?/attachments/get/100978309)
        EXPECTED: **From OX105:**
        EXPECTED: * Cashout MS will send betUpdate message with an updated bet after event/market/selection update
        EXPECTED: * Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: Note: if bet is suspended on Selection level 'Cash Out <value>' button is still active, only bet is displayed with susp label!
        """
        pass

    def test_003_in_ti_suspend_same_event_on_any_other_level_eg_selection(self):
        """
        DESCRIPTION: In TI suspend same event on any other level (eg. Selection)
        EXPECTED: Another betUpdate getBetDetail (full betUpdate)is received In Cashout MS
        EXPECTED: **From OX105:**
        EXPECTED: * Cashout MS will send betUpdate message with an updated bet after event/market/selection update
        """
        pass

    def test_004_in_ti_unsuspend_the_event_on_one_of_the_levels_eg_event_and_check_the_updates_on_ui(self):
        """
        DESCRIPTION: In TI unsuspend the event on one of the levels (eg. Event) and check the updates on UI
        EXPECTED: - Bet is still suspended
        EXPECTED: Note: If bet remains suspended only on selection level, 'Cash Out <value>' button becomes active and available for cashout
        EXPECTED: - In Cashout MS betUpdate getBetDetail (full betUpdate)is received
        EXPECTED: **From OX105:**
        EXPECTED: * Cashout MS will send betUpdate message with an updated bet after event/market/selection update
        EXPECTED: * Bet is still suspended
        EXPECTED: Note: If bet remains suspended only on selection level, 'Cash Out <value>' button becomes active and available for cashout
        """
        pass

    def test_005_in_ti_unsuspend_the_event_on_the_last_suspended_level_and_check_the_updates_on_ui_eg_selection(self):
        """
        DESCRIPTION: In TI unsuspend the event on the last suspended level and check the updates on UI (eg. Selection)
        EXPECTED: - Bet becomes active
        EXPECTED: - In Cashout MS cashoutUpdate 'shouldActivate":true' parameter is received
        EXPECTED: ![](index.php?/attachments/get/100978310)
        EXPECTED: **From OX105:**
        EXPECTED: * Cashout MS will send cashoutUpdate message
        EXPECTED: * Bet becomes active
        """
        pass

    def test_006_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet.
        EXPECTED: Results are same as above
        """
        pass
