import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C14640142_Verify_balance_update_after_bet_placement_cash_out_action(Common):
    """
    TR_ID: C14640142
    NAME: Verify balance update after bet placement, cash out action
    DESCRIPTION: This test case verifies successful balance update after bet placement, cash out action, at betslip header.
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_002_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        pass

    def test_003_tap_place_bet_buttontap_close_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Tap 'Close' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is closed
        """
        pass

    def test_004_verify_the_balance(self):
        """
        DESCRIPTION: Verify the balance
        EXPECTED: Balance is updated automatically after successful bet placement, it is decremented by entered stake
        """
        pass

    def test_005_add_one_selection_to_betsliptap_on_add_to_betslip_buttonclick_on_betslip_icon(self):
        """
        DESCRIPTION: Add one selection to Betslip
        DESCRIPTION: Tap on 'Add to betslip' button
        DESCRIPTION: Click on Betslip icon
        EXPECTED: Betslip view is opened. Balance is displayed in the header
        """
        pass

    def test_006_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Place Bet' button becomes enabled
        """
        pass

    def test_007_tap_on_place_bet_button_verify_the_balance_in_the_header_of_betslip_view(self):
        """
        DESCRIPTION: Tap on 'Place Bet' button. Verify the balance in the header of Betslip view
        EXPECTED: Balance is updated automatically, it is decremented by entered stake
        """
        pass

    def test_008_tap_on_go_betting_buttonverify_the_balance(self):
        """
        DESCRIPTION: Tap on 'GO BETTING' button
        DESCRIPTION: Verify the balance
        EXPECTED: Betslip view is closed after tapping 'GO BETTING' button
        EXPECTED: Balance is updated
        """
        pass

    def test_009_navigate_to_cash_out_tab_on_my_bets_page_coral__open_bets_page_ladbrokes(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page (Coral) / 'Open Bets' page (Ladbrokes)
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_010_tap_cash_out_button_for_last_added_bettap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button for last added bet
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_011_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: 'Cashed out' label is displayed ath the top right corner on the header
        EXPECTED: Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: Message "Cashout Successfully" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        pass

    def test_012_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on full cash out value
        """
        pass

    def test_013_place_one_more_betnavigate_to_cash_out_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Place one more bet
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_014_tap_partial_cashout_button_for_last_added_bet(self):
        """
        DESCRIPTION: Tap 'PARTIAL CASHOUT' button for last added bet
        EXPECTED: Sum of cash out is counted
        """
        pass

    def test_015_tap_cashout_buttontap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASHOUT' button
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_016_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed below 'CASH OUT' button "Partial Cash Out Successful"
        """
        pass

    def test_017_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on previously cashed out value
        """
        pass
