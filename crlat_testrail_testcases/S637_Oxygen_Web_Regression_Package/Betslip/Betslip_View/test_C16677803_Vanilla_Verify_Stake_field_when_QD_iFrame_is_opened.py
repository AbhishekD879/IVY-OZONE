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
class Test_C16677803_Vanilla_Verify_Stake_field_when_QD_iFrame_is_opened(Common):
    """
    TR_ID: C16677803
    NAME: [Vanilla] Verify 'Stake' field when QD iFrame is opened
    DESCRIPTION: This test case verifies that Quick Deposit iFrame closes when tapping on Stake field
    PRECONDITIONS: Login into Application
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_1_sportraces_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 <Sport>/<Races> selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        pass

    def test_003_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_004_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        pass

    def test_005_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_006_tap_on_stake_textbox(self):
        """
        DESCRIPTION: Tap on 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: 'Stake' textbox is editable
        """
        pass

    def test_007_close_betslip_viewadd_at_least_3_selections_from_different_event_to_the_bet_slip(self):
        """
        DESCRIPTION: Close Betslip view
        DESCRIPTION: Add at least 3 selections from different event to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_008_navigate_to_betslip_viewenter_value_higher_than_user_balance_to_all_stake_textboxes_all_single_stakes_multiples_stakes_4_fold_acca_double_treble_yankee_lucky_flagtap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Navigate to Betslip view
        DESCRIPTION: Enter value higher than user balance to all 'Stake' textboxes (All Single Stakes; Multiples stakes: 4 Fold Acca, Double, Treble, Yankee, Lucky, Flag)
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: Betslip view is opened
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        pass

    def test_009_tap_on_any_stake_textbox_in_multiple_sectionobserve_all_stake_textboxes(self):
        """
        DESCRIPTION: Tap on any 'Stake' textbox in Multiple section
        DESCRIPTION: Observe all 'Stake' textboxes
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        """
        pass
