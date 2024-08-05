import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C12834645_Verify_Stake_and_Potential_Return_when_price_chaged_while_Edit_ACCA_mode_is_opened(Common):
    """
    TR_ID: C12834645
    NAME: Verify Stake and Potential Return when price chaged while Edit ACCA mode is opened
    DESCRIPTION: 
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login into App
    PRECONDITIONS: 2. Place Multiple bet (e. g. ACCA5)
    PRECONDITIONS: 3. Navigate to the My Bets>Open Bets
    PRECONDITIONS: 4. Tap on 'Edit My Acca' button -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: 5. Remove selection and stay in 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_change_price_for_one_of_selection_from_my_acca_edit_mode(self):
        """
        DESCRIPTION: Change price for one of selection from 'My Acca Edit' mode
        EXPECTED: * Price is changed
        EXPECTED: * The new potential returns is shown
        EXPECTED: * New Potential Returns are taken from ValidateBet request
        """
        pass

    def test_002_tap_confirm_buttonverify_that_the_new_acca_is_successfully_placed_at_the_higher_potential_returns(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        DESCRIPTION: Verify that the new ACCA is successfully placed at the higher potential returns
        EXPECTED: The new Acca is successfully placed at the higher potential returns
        """
        pass

    def test_003_verify_that_updated_prices_are_shown_against_each_open_selections(self):
        """
        DESCRIPTION: Verify that updated prices are shown against each Open Selections
        EXPECTED: Updated prices are shown against each Open Selections
        """
        pass

    def test_004_verify_that_new_stake_and_new_potential_returns_are_shown(self):
        """
        DESCRIPTION: Verify that New stake and new Potential Returns are shown
        EXPECTED: New stake and new Potential Returns are shown
        """
        pass

    def test_005_edit_my_acca_button__remove_one_more_selectionstay_in_my_acca_edit_mode(self):
        """
        DESCRIPTION: 'Edit My Acca' button > Remove one more selection
        DESCRIPTION: Stay in 'My Acca Edit' mode
        EXPECTED: Selection is removed
        """
        pass

    def test_006_tap_confirm_button_and_in_same_time_change_price_in_ti_for_one_of_selections_price_should_be_increased_so_that_the_potential_return_should_be_decreased_more_than_tolerance_percentage_value___10(self):
        """
        DESCRIPTION: Tap 'Confirm' button and in same time change price in TI for one of selections (price should be increased so that the potential return should be decreased more than tolerance percentage value - 10%)
        EXPECTED: * Price is changed
        EXPECTED: * The new potential returns decreased
        EXPECTED: * New Potential Returns are taken from ValidateBet request
        """
        pass

    def test_007_verify_that_bet_placement_of_the_new_acca_is_prevented(self):
        """
        DESCRIPTION: Verify that bet placement of the new Acca is prevented
        EXPECTED: Bet placement of the new Acca is prevented
        """
        pass

    def test_008_verify_that_the_bet_is_returned_in_edit_mode(self):
        """
        DESCRIPTION: Verify that the bet is returned in edit mode
        EXPECTED: The bet is returned in edit mode
        """
        pass

    def test_009_verify_that_the_new_decreased_potential_returns_and_new_stake_are_shown(self):
        """
        DESCRIPTION: Verify that the new decreased Potential Returns and new Stake are shown
        EXPECTED: * The new decreased potential returns are displayed
        EXPECTED: * New Stake is shown (New Stake is taken from ValidateBet request)
        """
        pass

    def test_010_verify_that_updated_prices_are_shown_against_each_open_selections(self):
        """
        DESCRIPTION: Verify that updated prices are shown against each Open Selections
        EXPECTED: Updated prices are shown against each Open Selections
        """
        pass

    def test_011_verify_that_information_message_is_shown_under_the_confirm_button(self):
        """
        DESCRIPTION: Verify that information message is shown under the 'Confirm' button
        EXPECTED: Message text is configured in CMS:
        EXPECTED: System Configuration > Structure > EMA > genericErrorTitle
        """
        pass

    def test_012_verify_that_the_confirm_button_is_re_displayed(self):
        """
        DESCRIPTION: Verify that the Confirm button is re-displayed
        EXPECTED: The Confirm button is re-displayed
        """
        pass
