import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C14876363_Vanilla__Quick_Bet__GVC_iFrame_appearance(Common):
    """
    TR_ID: C14876363
    NAME: [Vanilla] - Quick Bet - GVC iFrame appearance
    DESCRIPTION: This test case verifies the appearance of GVC iFrame
    PRECONDITIONS: User balance is more than 0
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_002_enter_value_less_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value less than user balance in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        EXPECTED: 'Place Bet' button becomes enabled
        """
        pass

    def test_003_change_value_in_stake_field_for_value_higher_than_user_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field for value higher than user balance
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass

    def test_004_tap_on_make_a_deposit_buttonobserve_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        DESCRIPTION: Observe 'Make a Deposit' button
        EXPECTED: Spinner and 'Make a Deposit' text is displayed on the 'Make a Quick Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay appears with available payment method set for User
        """
        pass

    def test_005_observe_the_header_of_iframe_overlay(self):
        """
        DESCRIPTION: Observe the header of iFrame overlay
        EXPECTED: The label 'Quick Deposit' is displayed on the iFrame header
        EXPECTED: Close (X) button is displayed on the right top corner on the iFrame header
        """
        pass

    def test_006_tap_close_x_button(self):
        """
        DESCRIPTION: Tap close (X) button
        EXPECTED: The Quick Deposit overlay is closed
        EXPECTED: User returns to the Quick Bet overlay
        """
        pass

    def test_007_observe_the_warning_message(self):
        """
        DESCRIPTION: Observe the warning message
        EXPECTED: The warning message "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        pass
