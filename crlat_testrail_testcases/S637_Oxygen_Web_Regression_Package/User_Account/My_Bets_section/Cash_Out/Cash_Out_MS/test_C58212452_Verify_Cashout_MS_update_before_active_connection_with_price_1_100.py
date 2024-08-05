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
class Test_C58212452_Verify_Cashout_MS_update_before_active_connection_with_price_1_100(Common):
    """
    TR_ID: C58212452
    NAME: Verify Cashout MS update before active connection with price > 1/100
    DESCRIPTION: This test case verifies the updates in Cashout MS when event becomes suspended before user navigates to 'My Bets' tab and when the price/s of selection is > 1/100
    PRECONDITIONS: Story related: https://jira.egalacoral.com/browse/BMA-51061
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMA-51067
    PRECONDITIONS: Epic related: https://jira.egalacoral.com/browse/BMA-51056
    PRECONDITIONS: Pre-conditions:
    PRECONDITIONS: In CMS: System Config: Structure: CashOut: Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: In app:
    PRECONDITIONS: - Login
    PRECONDITIONS: - Place few bets (Single and Multiple) with CashOut available option
    PRECONDITIONS: - Navigate to any page in the app except 'Cashout/Open Bets' tab
    PRECONDITIONS: - Open Dev Tools -> Network tab -> XHR filter (bet-details request) for checking cashout MS once on 'Cashout/Open Bets' tab
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    PRECONDITIONS: In Bet placed:
    PRECONDITIONS: - **Price of the selections in the bet placed should have price update within last 24 hours!**
    PRECONDITIONS: - Price odds of the bet are > 1/100 (eg. 1/2)
    PRECONDITIONS: - Bet/s is active/not resulted
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_in_ti_suspend_the_event_on_any_level_eventmarketselectionnote_user_is_on_home_page_meanwhile_or_any_other_except_cashoutopen_bets_tab(self):
        """
        DESCRIPTION: In TI suspend the event on any level (event/market/selection)
        DESCRIPTION: Note: user is on Home page meanwhile or any other except 'Cashout/Open Bets' tab
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_cashoutopen_bets_tab_afterwards_and_check_the_updates_on_ui(self):
        """
        DESCRIPTION: Navigate to 'Cashout/Open Bets' tab afterwards and check the updates on UI
        EXPECTED: Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Bet becomes suspended (susp label is present on the left in event card, 'Cash Out <value>' button becomes 'Cash Out suspended' and greyed out)
        EXPECTED: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
        EXPECTED: - initial bets data will be returned after establishing connection
        """
        pass

    def test_003_in_ti_unsuspend_the_bet_on_the_level_suspended_before_and_meanwhile_check_the_ui_for_updated(self):
        """
        DESCRIPTION: In TI unsuspend the bet on the level suspended before and meanwhile check the UI for updated
        EXPECTED: - Bet becomes active
        EXPECTED: - In Cashout MS betUpdate: getBetDetail (full betUpdate) is received
        EXPECTED: ![](index.php?/attachments/get/100880923)
        EXPECTED: From release OX105:
        EXPECTED: * Bet becomes active
        EXPECTED: * Cashout MS will send betUpdate message
        EXPECTED: From release OX106:
        EXPECTED: * Bet becomes active
        EXPECTED: * Cashout MS will send cashoutUpdate message
        """
        pass

    def test_004_repeat_steps_above_for_the_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Multiple bet
        EXPECTED: Results are the same as above
        """
        pass
