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
class Test_C874334_Full_Cash_Out_singles_In_Play(Common):
    """
    TR_ID: C874334
    NAME: Full Cash Out singles In Play
    DESCRIPTION: Verify that the customer can perform a Full Cash Out (check balance and Bet History) for In Play bet
    PRECONDITIONS: * Login to Oxygen app
    PRECONDITIONS: * Go to In-Play page
    PRECONDITIONS: * Place a bet on In Play event e.g. on 'Match Betting' market
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

    def test_002_tap_cash_out_currency_symbolvalue_button_for_a_bet(self):
        """
        DESCRIPTION: Tap 'CASH OUT <currency symbol><value>' button for a bet
        EXPECTED: Green button 'CONFIRM CASH OUT <currency symbol><value>' is appear instead of 'CASH OUT <currency symbol><value>' button
        """
        pass

    def test_003_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_004_wait_until_spinner_disappears(self):
        """
        DESCRIPTION: Wait until spinner disappears
        EXPECTED: * The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: - A green box with "tick" in a circle and message of "Cash Out Successful" are shown below bet line details. The icon and text are centered within a green box.
        EXPECTED: * 'You Cashed Out: <currency icon> <cashout value>' message (with a green icon on the left side) is shown under bet header.
        EXPECTED: * Cashed Out bet is NOT disappeared from 'CashOut'/'Open Bets' tab.
        EXPECTED: * Cashed Out bet is disappeared ONLY after navigation from 'Cash Out'/'Open Bets' tab.
        EXPECTED: Design:
        EXPECTED: ![](index.php?/attachments/get/11084506)
        """
        pass

    def test_005_wait_for_balance_to_update(self):
        """
        DESCRIPTION: Wait for balance to update
        EXPECTED: The balance is updated in less than 1 min (should update within seconds)
        """
        pass

    def test_006_go_to_settled_bets_tab(self):
        """
        DESCRIPTION: Go to 'Settled Bets' tab
        EXPECTED: The cashed-out bet is present with the tab
        """
        pass

    def test_007_check_the_bet_details(self):
        """
        DESCRIPTION: Check the bet details
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name';
        EXPECTED: - 'market name';
        EXPECTED: - 'selection name';
        EXPECTED: - 'Stake';
        EXPECTED: - 'You Cashed Out' value;
        EXPECTED: - 'Bet Receipt' number.
        EXPECTED: * The status of the bet is "Cashed Out"
        EXPECTED: * 'You Cashed Out: <currency icon> <cashout value>' message (with green icon on the left side) is shown under bet header
        """
        pass

    def test_008_verify_that_the_events_clock_on_the_cashout_tab_is_consistent_with_the_match_time_in_play_page(self):
        """
        DESCRIPTION: Verify that the event's clock on the cashout tab is consistent with the match time In Play page
        EXPECTED: ![](index.php?/attachments/get/1651)
        """
        pass
