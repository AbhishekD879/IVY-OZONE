import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C17329163_Vanilla_Verify_QD_iFrame_behavior_when_selection_is_removed_from_Betslip(Common):
    """
    TR_ID: C17329163
    NAME: [Vanilla] Verify QD iFrame behavior when selection is removed from Betslip
    DESCRIPTION: This test case verifies the QD iFrame behavior when selection is removed from Betslip
    PRECONDITIONS: Login into Application (user should have positive balance)
    """
    keep_browser_open = True

    def test_001_add_at_least_3_sportraces_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add at least 3 <Sport>/<Races> selection to the betslip
        EXPECTED: Selections are added
        """
        pass

    def test_002_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selections are displayed
        """
        pass

    def test_003_enter_value_higher_than_user_balance_in_stake_field_for_first_selection(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field for first selection
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        pass

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_005_tap_on_close_button_for_first_selection_in_the_betslip(self):
        """
        DESCRIPTION: Tap on Close button for first selection in the Betslip
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        EXPECTED: Betslip view with disabled Place Bet button is displayed
        """
        pass

    def test_006_enter_value_higher_than_user_balance_in_stake_field_for_first_selection_and_value_less_than_user_balance_in_stake_field_for_second_selection_in_the_betslip(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field for first selection and value less than user balance in 'Stake' field for second selection in the Betslip
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        pass

    def test_007_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_008_tap_on_close_button_for_second_selection(self):
        """
        DESCRIPTION: Tap on Close button for second selection
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        EXPECTED: Betslip view with enabled Make a Deposit button is displayed
        """
        pass
