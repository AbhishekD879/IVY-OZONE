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
class Test_C9489630_Verify_view_of_an_edited_acca_in_Open_Bets_Cash_Out_Tab(Common):
    """
    TR_ID: C9489630
    NAME: Verify view of an edited acca in 'Open Bets'/'Cash Out' Tab
    DESCRIPTION: This test case view of an edited acca in 'Open Bets'/Cash Out Tab
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -&gt; System Configuration -&gt; Structure -&gt; EMA -&gt; Enabled
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -&gt; verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button -&gt; verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Remove selection from 'My Acca Edit' mode
    PRECONDITIONS: Tap 'Confirm' button -&gt; user has successfully edited their acca
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_verify_that_the_new_bet_type_name_is_displayed(self):
        """
        DESCRIPTION: Verify that the new bet type name is displayed
        EXPECTED: The new bet type name is displayed
        """
        pass

    def test_002_verify_that_all_selections_from_the_original_acca_are_displayed(self):
        """
        DESCRIPTION: Verify that all selections from the original acca are displayed
        EXPECTED: All selections from the original acca are displayed
        """
        pass

    def test_003_verify_that_the_selections_which_were_removed_have_a_removed_token_displayed(self):
        """
        DESCRIPTION: Verify that the selection(s) which were removed have a Removed token displayed
        EXPECTED: The selection(s) which were removed have a Removed token displayed
        EXPECTED: Removed selections should appear below Open selections
        """
        pass

    def test_004_verify_that_the_stake_is_displayed(self):
        """
        DESCRIPTION: Verify that the stake is displayed
        EXPECTED: The stake is displayed
        EXPECTED: New stake value is received from validateBet request - 'newBetStake' parameter
        """
        pass

    def test_005_verify_that_prices_are_displayed_for_any_selections(self):
        """
        DESCRIPTION: Verify that prices are displayed for any selections
        EXPECTED: Prices are displayed for any selections
        """
        pass

    def test_006_verify_that_the_new_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the new potential returns are displayed
        EXPECTED: The new potential returns are displayed
        EXPECTED: New potential return value is received from validateBet request - 'betPotentialWin' parameter
        """
        pass

    def test_007_repeat_all_from_1_to_6_steps_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat all from 1 to 6 steps in 'Cash Out' tab
        EXPECTED: results are the same, but removed selections are not shown
        """
        pass
