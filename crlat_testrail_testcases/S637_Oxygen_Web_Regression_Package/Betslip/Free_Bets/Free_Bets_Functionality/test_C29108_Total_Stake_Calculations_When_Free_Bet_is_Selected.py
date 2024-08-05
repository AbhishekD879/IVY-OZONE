import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29108_Total_Stake_Calculations_When_Free_Bet_is_Selected(Common):
    """
    TR_ID: C29108
    NAME: 'Total Stake' Calculations When Free Bet is Selected
    DESCRIPTION: This test case verifies fields calculation when free bet is selected instead of stake amount
    DESCRIPTION: NOTE, UAT assistance is needed in order to get free bet tokens
    DESCRIPTION: AUTOTEST [C527788]
    PRECONDITIONS: Make sure user has free bets available
    """
    keep_browser_open = True

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_to_application(self):
        """
        DESCRIPTION: Log In to application
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_tree_selections_to_the_bet_slip_from_different_events_which_has_terms_available(self):
        """
        DESCRIPTION: Add tree selections to the Bet Slip from different events which has terms available
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip_singles_tab(self):
        """
        DESCRIPTION: Open Bet Slip, 'Singles' tab
        EXPECTED: 'Singles' tab is opened
        """
        pass

    def test_005_select_free_bet_option_from_the_drop_down_control(self):
        """
        DESCRIPTION: Select free bet option from the drop down control
        EXPECTED: Free bet is selected
        EXPECTED: 'Total Stake' and 'Free Bet Stake' fields are equal to the value chosen in the free bet
        """
        pass

    def test_006_tick_ew_checkbox(self):
        """
        DESCRIPTION: Tick 'E/W' checkbox
        EXPECTED: Each Way option is selected
        EXPECTED: 'Total Stake' is NOT doubled. It is equal to free bet value.
        """
        pass

    def test_007_select_free_bet_value_and_enter_stake_field_manuallyunselect_each_way_option(self):
        """
        DESCRIPTION: Select free bet value and enter stake field manually
        DESCRIPTION: Unselect each way option
        EXPECTED: 'Total Stake' is equal to value:
        EXPECTED: 'Free bet stake' + 'Stake'
        """
        pass

    def test_008_select_each_way_option(self):
        """
        DESCRIPTION: Select each way option
        EXPECTED: 'Total Stake' is equal to the value:
        EXPECTED: 'Free bet stake' + 'Stake'
        EXPECTED: where, 'Stake' is a doubled value of manually entered stake
        """
        pass

    def test_009_go_to_multiples_tab(self):
        """
        DESCRIPTION: Go to 'Multiples' tab
        EXPECTED: 'Multiples' tab is selected
        """
        pass

    def test_010_select_free_bet_amount_from_the_drop_down(self):
        """
        DESCRIPTION: Select free bet amount from the drop down
        EXPECTED: Free bet is selected
        EXPECTED: 'Total Stake' and 'Free Bet Stake' fields are equal to the value chosen in the free bet
        """
        pass

    def test_011_enter_stake_field_in_a_stake_fieldselect_free_bet_from_the_dropdown(self):
        """
        DESCRIPTION: Enter stake field in a 'Stake' field
        DESCRIPTION: Select free bet from the dropdown
        EXPECTED: 'Total Stake' is equal to:
        EXPECTED: **'Free bet stake'+ stake_quantity**
        EXPECTED: **stake_quantity= 'Stake' *k,**
        EXPECTED: where:
        EXPECTED: 'Stake' - stake amount which is entered manually
        EXPECTED: k - the quantity of combinations which form the multiple selection
        """
        pass
