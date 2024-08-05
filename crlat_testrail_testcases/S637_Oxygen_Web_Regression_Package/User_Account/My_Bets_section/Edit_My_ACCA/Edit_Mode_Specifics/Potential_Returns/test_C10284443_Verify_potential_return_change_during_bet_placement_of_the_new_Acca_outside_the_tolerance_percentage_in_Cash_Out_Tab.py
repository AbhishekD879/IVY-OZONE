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
class Test_C10284443_Verify_potential_return_change_during_bet_placement_of_the_new_Acca_outside_the_tolerance_percentage_in_Cash_Out_Tab(Common):
    """
    TR_ID: C10284443
    NAME: Verify potential return change during bet placement of the new Acca outside the tolerance percentage (in Cash Out Tab)
    DESCRIPTION: This test case verifies potential return change during bet placement of the new Acca outside the tolerance percentage
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button in  'Cash Out' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Click to remove selection from 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: **Coral** has 'EDIT MY BET'  button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_change_price_decrease_for_one_of_selection_from_my_acca_edit_mode_and_at_the_same_time__execute_step2(self):
        """
        DESCRIPTION: Change price (decrease) for one of selection from 'My Acca Edit' mode (and at the same time  execute Step2)
        EXPECTED: Price is decreased
        EXPECTED: The new potential returns decreased
        """
        pass

    def test_002_tap_confirm_while_price_is_changing_button_and_verify_that_bet_placement_of_the_new_acca_is_prevented(self):
        """
        DESCRIPTION: Tap 'Confirm' (while price is changing) button and verify that bet placement of the new Acca is prevented
        EXPECTED: Bet placement of the new Acca is prevented
        """
        pass

    def test_003_verify_that_the_bet_is_returned_in_edit_mode(self):
        """
        DESCRIPTION: Verify that the bet is returned in edit mode
        EXPECTED: The bet is returned in edit mode
        """
        pass

    def test_004_verify_that_the_new_decreased_potential_returns_are_displayed_in_the_potential_column_in_bet_details(self):
        """
        DESCRIPTION: Verify that the new decreased potential returns are displayed in the Potential column in Bet Details
        EXPECTED: The new decreased potential returns are displayed in the Potential column in Bet Details
        """
        pass

    def test_005_verify_that_updated_prices_are_shown_against_each_open_selections(self):
        """
        DESCRIPTION: Verify that updated prices are shown against each Open Selections
        EXPECTED: Updated prices are shown against each Open Selections
        """
        pass

    def test_006_verify_that_new_stake_information_is_shown(self):
        """
        DESCRIPTION: Verify that New stake information is shown
        EXPECTED: New stake information is shown
        """
        pass

    def test_007_verify_that_alert_is_displayed_advising_that_the_potential_returns_have_updated(self):
        """
        DESCRIPTION: Verify that alert is displayed advising that the potential returns have updated
        EXPECTED: Alert is displayed advising that the potential returns have updated
        """
        pass

    def test_008_verify_content_of_alert(self):
        """
        DESCRIPTION: Verify content of alert
        EXPECTED: Editing this bet changes the value of Cashout and Odds.
        EXPECTED: UPD: according to OX102 Ladbrokes behaviour and designs https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c6eb258154cb51b89166b30
        EXPECTED: error text is: "Sorry, editing was unsuccessful, please try again."
        """
        pass

    def test_009_verify_that_the_confirm_button_is_re_displayed(self):
        """
        DESCRIPTION: Verify that the Confirm button is re-displayed
        EXPECTED: The Confirm button is re-displayed
        """
        pass
