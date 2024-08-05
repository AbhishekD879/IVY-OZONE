import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C77624_Application_handling_of_hazelcast_nodes_killing(Common):
    """
    TR_ID: C77624
    NAME: Application handling of hazelcast nodes killing
    DESCRIPTION: This test case verifies application handling of hazelcast nodes killing. Currently there are three of nodes instances and application should be stable if at least one of them is working
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [BMA-15706 ([BPP] As a TA I want to use Hazelcast multi-master cluster in BPP for storing user sensitive info (session tokens))] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15706
    PRECONDITIONS: DevOps assistance is needed for killing nodes.
    PRECONDITIONS: Checklist:
    PRECONDITIONS: * Log in
    PRECONDITIONS: * Placing Bet
    PRECONDITIONS: * Bet history page
    PRECONDITIONS: * Cash out
    """
    keep_browser_open = True

    def test_001_ask_devops_to_kill_one_of_the_three_node_instances_with_hazelcast(self):
        """
        DESCRIPTION: Ask DevOps to kill one of the three node instances with hazelcast
        EXPECTED: 
        """
        pass

    def test_002_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_003_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_004_enter_correct_credentials(self):
        """
        DESCRIPTION: Enter correct credentials
        EXPECTED: 
        """
        pass

    def test_005_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: * User is logged in successfully
        EXPECTED: * Page from which user made log in is shown
        EXPECTED: * Pop-ups are shown if they are expected for particular user
        """
        pass

    def test_006_add_any_cashout_available_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add any cashout available selection to Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_007_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Bet Slip is opened, added selection is displayed
        """
        pass

    def test_008_enter_valid_stake_in_stake_field(self):
        """
        DESCRIPTION: Enter valid stake in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_009_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_010_verify_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Verify 'Done' button on Bet Receipt page
        EXPECTED: * Bet Slip slider closes
        EXPECTED: * User stays on same page
        """
        pass

    def test_011_tap_right_menu___my_account___bet_history(self):
        """
        DESCRIPTION: Tap Right menu -> 'My Account' -> 'Bet History'
        EXPECTED: 'Bet History' page is opened with 'Bet History' header and Back button
        EXPECTED: Four sort filters are present :
        EXPECTED: * Regular (selected by default)
        EXPECTED: * Player Bets
        EXPECTED: * Lotto
        EXPECTED: *  Pools
        EXPECTED: Sorting section with four options is present:
        EXPECTED: * Last 2 days (selected by default)
        EXPECTED: * Last 7 days
        EXPECTED: * Last 14 days
        EXPECTED: * Show All
        EXPECTED: Note: Sorting option is not shown for 'Pick & Mix' sort filter
        """
        pass

    def test_012_verify_bet_user_placed_in_step_9_is_displayed(self):
        """
        DESCRIPTION: Verify bet user placed in step #9 is displayed
        EXPECTED: Bet from step #9 is displayed
        """
        pass

    def test_013_navigate_to_cash_out_pagewidget(self):
        """
        DESCRIPTION: Navigate to Cash out page/widget
        EXPECTED: 
        """
        pass

    def test_014_verify_bet_user_placed_in_step_9_is_displayed(self):
        """
        DESCRIPTION: Verify bet user placed in step #9 is displayed
        EXPECTED: Verify bet user placed in step #9 is displayed with two buttons: 'CASH OUT'/'FULL CASH OUT'
        """
        pass

    def test_015_tap_partial_cash_out_currency_symbol_xxxx_button_and_proceed_with_partial_cash_out_proccess(self):
        """
        DESCRIPTION: Tap 'PARTIAL CASH OUT <currency_symbol> XX.XX' button and proceed with partial cash out proccess
        EXPECTED: * Verify appropriate success message appears
        EXPECTED: * User balance is increased on XX.XX value
        EXPECTED: * Bet line remains in cash out page/widget
        """
        pass

    def test_016_tap_cash_outfull_cash_out_button_and_proceed_with_cash_out_proccess(self):
        """
        DESCRIPTION: Tap 'CASH OUT'/'FULL CASH OUT' button and proceed with cash out proccess
        EXPECTED: * Verify appropriate success message appears
        EXPECTED: * User balance is increased on XX.XX value
        EXPECTED: * Bet line disappears from cash out page/widget
        """
        pass

    def test_017_ask_devops_to_kill_one_more_node_instance_with_hazelcast_so_that_two_node_instances_dont_work_at_a_timerepeat_steps_2_16(self):
        """
        DESCRIPTION: Ask DevOps to kill one more node instance with hazelcast (so that two node instances don't work at a time)
        DESCRIPTION: Repeat steps #2-16
        EXPECTED: 
        """
        pass
