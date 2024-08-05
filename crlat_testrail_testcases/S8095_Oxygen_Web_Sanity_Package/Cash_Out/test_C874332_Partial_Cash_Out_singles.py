import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.cash_out
@vtest
class Test_C874332_Partial_Cash_Out_singles(Common):
    """
    TR_ID: C874332
    NAME: Partial Cash Out singles
    DESCRIPTION: Verify that the customer can perform a Partial Cash Out (check balance and Bet History)
    DESCRIPTION: is covered in AUTOTESTS [C48912230]
    PRECONDITIONS: * Login to Oxygen app and log in
    PRECONDITIONS: * Place a single bet on any Pre-Match or In-Play event e.g. on 'Match Betting' market
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        EXPECTED: * A list with COMB eligible bets is displayed
        EXPECTED: * The currency is as per user registration setting
        """
        pass

    def test_002_click_on_partial_cash_out_button_on_cash_out_bar_for_a_single_bet(self):
        """
        DESCRIPTION: Click on 'Partial Cash Out' button on 'Cash Out' bar for a single bet
        EXPECTED: * Partial Cash Out slider bar is displayed
        EXPECTED: * The percentage selected by default is 50%
        EXPECTED: * The 'Partial Cash Out' value is displayed on the 'Cash Out' button
        """
        pass

    def test_003_click_on_the_cash_out_button_again(self):
        """
        DESCRIPTION: Click on the 'Cash Out' button again
        EXPECTED: 'CONFIRM CASHOUT' green button is displayed (instead of 'Partial Cash Out' slider bar)
        """
        pass

    def test_004_click_on_confirm_cashout_green_button_in_order_to_confirm_the_partial_cash_out(self):
        """
        DESCRIPTION: Click on 'CONFIRM CASHOUT' green button in order to confirm the Partial Cash Out
        EXPECTED: * The Partial cash Out is now in Progress
        EXPECTED: * 'Partial Cash Out Successful' message is displayed when the COMB delay ends and the message does not disappear from the tab
        EXPECTED: * 'Stake' and 'Est.Returns'/'Potential Returns' values are decreased
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/11918119)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/11918125)
        """
        pass

    def test_005_wait_for_the_balance_to_update(self):
        """
        DESCRIPTION: Wait for the balance to update
        EXPECTED: The balance should update in a couple of seconds (but no longer than 1 min)
        """
        pass

    def test_006_go_to_open_bets_tab_on_coral_brand_or_refresh_page_on_ladbrokes_brand_and_go_to_cashed_out_bet(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab on **Coral** brand or refresh page on **Ladbrokes** brand and go to cashed out bet
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name';
        EXPECTED: - 'market name';
        EXPECTED: - 'selection name';
        EXPECTED: - 'Odds';
        EXPECTED: * 'Show Partial Cash Out History' link is displayed at the bottom of the bet details
        """
        pass

    def test_007_tap_the_show_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Tap the 'Show Partial Cash Out History' link
        EXPECTED: * 'Show Partial Cash Out History' link becomes 'Hide Partial Cash Out History'
        EXPECTED: * Details regarding the Partial Cash Out are displayed in a table view
        EXPECTED: ![](index.php?/attachments/get/11918122)
        """
        pass

    def test_008_tap_the_hide_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Tap the 'Hide Partial Cash Out History' link
        EXPECTED: * 'Hide Partial Cash Out History' link becomes 'Show Partial Cash Out History'
        EXPECTED: * Details regarding the Partial Cash Out are no more displayed
        """
        pass
