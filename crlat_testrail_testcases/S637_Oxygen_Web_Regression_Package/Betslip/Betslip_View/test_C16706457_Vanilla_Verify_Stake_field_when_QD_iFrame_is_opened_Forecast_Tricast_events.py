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
class Test_C16706457_Vanilla_Verify_Stake_field_when_QD_iFrame_is_opened_Forecast_Tricast_events(Common):
    """
    TR_ID: C16706457
    NAME: [Vanilla] Verify 'Stake' field when QD iFrame is opened ( Forecast/Tricast events)
    DESCRIPTION: This test case verifies that stake becomes disabled at once QD iFrame opens (Tote events)
    PRECONDITIONS: Login into Application
    """
    keep_browser_open = True

    def test_001_navigate_to_hrgreyhounds_pagechoose_event_with_forecasttricast_tab_available(self):
        """
        DESCRIPTION: Navigate to 'HR/Greyhounds' page
        DESCRIPTION: Choose event with Forecast/Tricast Tab available
        EXPECTED: Event with available Forecast/Tricast Tab is opened
        """
        pass

    def test_002_select_two_selections_in_forecasttricast_tab_and_tap_add_to_bet_slip_button(self):
        """
        DESCRIPTION: Select two Selections in Forecast/Tricast Tab and tap "Add to bet slip" button.
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        pass

    def test_003_navigate_to_betslip_viewenter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Navigate to Betslip view
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        pass

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_005_tap_on_stake_textbox(self):
        """
        DESCRIPTION: Tap on 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: 'Stake' textbox is editable
        """
        pass

    def test_006_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_007_tap_on_any_space_inside_betslip_except_stake_textbox(self):
        """
        DESCRIPTION: Tap on any space inside Betslip except 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame overlay is still displayed, nothing is changed
        """
        pass
