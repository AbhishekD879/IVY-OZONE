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
class Test_C9607318_Verify_potential_return_change_during_bet_placement_of_the_new_Acca_outside_the_tolerance_percentage_in_My_Bets_Tab(Common):
    """
    TR_ID: C9607318
    NAME: Verify potential return change during bet placement of the new Acca outside the tolerance percentage (in My Bets Tab)
    DESCRIPTION: This test case verifies potential return change during bet placement of the new Acca outside the tolerance percentage
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button in  'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Tap 'Remove selection' button for any selection
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: Tolerance value is shown in TI:
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/office >admin>miscellaneous>OpenbetConfig>Cashout Tolerance Percentage
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com/office >admin>miscellaneous>OpenbetConfig>Cashout Tolerance Percentage
    PRECONDITIONS: **Coral** has 'EDIT MY BET'  button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_tap_confirm_button_and_in_same_time_change_price_in_ti_for_one_of_selection_price_should_be_increased_so_that_the_potential_return_should_be_decreased_more_than_tolerance_percentage_value___10(self):
        """
        DESCRIPTION: Tap 'Confirm' button and in same time change price in TI for one of selection (price should be increased so that the potential return should be decreased more than tolerance percentage value - 10%)
        EXPECTED: - Changed price is shown
        EXPECTED: - The new potential returns decreased
        EXPECTED: - New Potential Returns are taken from *ValidateBet* request
        """
        pass

    def test_002_verify_that_bet_placement_of_the_new_acca_is_prevented(self):
        """
        DESCRIPTION: Verify that bet placement of the new Acca is prevented
        EXPECTED: Bet placement of the new Acca is prevented
        """
        pass

    def test_003_verify_that_the_bet_is_returned_in_edit_mode(self):
        """
        DESCRIPTION: Verify that the bet is returned in edit mode
        EXPECTED: The bet is returned in edit mode
        """
        pass

    def test_004_verify_that_the_new_decreased_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the new decreased potential returns are displayed
        EXPECTED: The new decreased potential returns are displayed
        """
        pass

    def test_005_verify_that_updated_prices_are_shown(self):
        """
        DESCRIPTION: Verify that updated prices are shown
        EXPECTED: Updated prices are shown
        """
        pass

    def test_006_verify_that_new_stake_information_is_shown(self):
        """
        DESCRIPTION: Verify that New stake information is shown
        EXPECTED: New stake information is shown
        EXPECTED: New Stake is taken from *ValidateBet* request
        """
        pass

    def test_007_verify_that_information_message_is_shown_under_the_confirm_button(self):
        """
        DESCRIPTION: Verify that information message is shown under the 'Confirm' button
        EXPECTED: Message text is configured in CMS:
        EXPECTED: System Configuration>Structure>EMA>genericErrorTitle
        """
        pass

    def test_008_verify_that_the_confirm_button_is_re_displayed(self):
        """
        DESCRIPTION: Verify that the Confirm button is re-displayed
        EXPECTED: The Confirm button is re-displayed
        """
        pass
