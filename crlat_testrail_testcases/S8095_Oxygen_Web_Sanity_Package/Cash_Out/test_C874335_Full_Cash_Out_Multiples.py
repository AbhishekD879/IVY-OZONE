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
class Test_C874335_Full_Cash_Out_Multiples(Common):
    """
    TR_ID: C874335
    NAME: Full Cash Out Multiples
    DESCRIPTION: Verify that the customer can perform a Full Cash Out (check balance and Bet History)
    DESCRIPTION: AUTOTEST [C48531944] [C48577672]
    PRECONDITIONS: * Login to Oxygen app and log in
    PRECONDITIONS: * Place a multiple bet on any Pre-Match or In-Play events that have Cashout option
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        EXPECTED: * A list with COMB eligible bets is displayed
        EXPECTED: * **Verify that the event time in the cashout tab is the same as on the "In-Play" page**
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

    def test_004_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: * The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: - Green box with "tick" in a circle and message of "Cash Out Successful" are shown below bet line details. The icon and text are centered within green box.
        EXPECTED: * Cashed Out bet remains displayed until page refresh or navigating away from the tab and then returning back
        EXPECTED: ![](index.php?/attachments/get/11918128)
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

    def test_007_expand_the_bet_in_order_to_check_the_bet_details(self):
        """
        DESCRIPTION: Expand the bet in order to check the bet details
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name' for each selection;
        EXPECTED: - 'market name' for each selection;
        EXPECTED: - 'selection name' for each selection;
        EXPECTED: - 'Stake';
        EXPECTED: - 'You Cashed Out' value;
        EXPECTED: - 'Bet Receipt' number.
        EXPECTED: * The status of the bet is "Cashed Out"
        EXPECTED: ![](index.php?/attachments/get/11918129)
        """
        pass
