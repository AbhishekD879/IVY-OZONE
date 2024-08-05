import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28139_Verify_Settled_Bets_tab_when_Settled_Bets_is_empty(Common):
    """
    TR_ID: C28139
    NAME: Verify Settled Bets tab when Settled Bets is empty
    DESCRIPTION: This test case verifies Settled Bets tab when Settled Bets is empty.
    DESCRIPTION: Test case is not updated, Player Bets tab is not available anymore, messages are different on Sports, Lotto, Pools tabs
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-3145 'Implement Football Jackpot '][1]
    DESCRIPTION: *   [BMA- 5880 'Lottery - View history for lottery bets'][2]
    DESCRIPTION: *   [BMA-9153 Add extra filters to Bet History][3]
    DESCRIPTION: *   [BMA-13748 Add Digital Sports Bet History in Oxygen platform][4]
    DESCRIPTION: *   [BMA-12422: Digital Sports - Change name Pick & Mix to Player Bets][5]
    DESCRIPTION: * [BMA-15524: Removing Bet History Download Links from Bet History Pages] [6]
    DESCRIPTION: * [BMA-24318 RTS: Account history > Bet History] [7]
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [8]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-3145
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-5880
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-9153
    DESCRIPTION: [4]: https://jira.egalacoral.com/browse/BMA-13748
    DESCRIPTION: [5]: https://jira.egalacoral.com/browse/BMA-12422
    DESCRIPTION: [6]: https://jira.egalacoral.com/browse/BMA-15524
    DESCRIPTION: [7]: https://jira.egalacoral.com/browse/BMA-24318
    DESCRIPTION: [8]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: * User should be logged in to view their settled bets
    PRECONDITIONS: * User should NOT have settled bet
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: 1. 'Settled Bets' tab is opened
        EXPECTED: 2. Four sort filters are present :
        EXPECTED: *   Sports (selected by default)
        EXPECTED: *   Player Bets
        EXPECTED: *   Lotto
        EXPECTED: *   Pools
        EXPECTED: 3. "From" and "To" date pickers are present allowing the user to select a date range.
        EXPECTED: 4. Default dates in both date pickers: user's current date selected in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: Note: Date pickers are not shown for 'Player Bets' sort filter
        EXPECTED: 5. "Settled Bets" accordion is collapsed by default
        EXPECTED: 6. **"You have no bet history."** message is displayed
        """
        pass

    def test_002_repeat_steps_2_3_when_lotto_sort_filter_is_selected(self):
        """
        DESCRIPTION: Repeat steps #2-3 when 'Lotto' sort filter is selected
        EXPECTED: 
        """
        pass

    def test_003_repeat_steps_2_3_when_pools_sort_filter_is_selected(self):
        """
        DESCRIPTION: Repeat steps #2-3 when 'Pools' sort filter is selected
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_2_4_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop_settled_bets_page_for_tabletdesktop___can_be_reached_via_entering_direct_url(self):
        """
        DESCRIPTION: Repeat steps 2-4 for:
        DESCRIPTION: * Settled Bets tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        DESCRIPTION: * "Settled Bets" page (for Tablet/Desktop) - can be reached via entering direct URL
        EXPECTED: 
        """
        pass
