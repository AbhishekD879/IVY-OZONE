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
class Test_C64569859_Verify_that_the_Edit_My_Acca_button_no_longer_displayed_as_only_one_selection_remains_open_on_casino_game_overlay(Common):
    """
    TR_ID: C64569859
    NAME: Verify that the Edit My Acca button no longer displayed as only one selection remains open on casino game overlay.
    DESCRIPTION: Verify that the Edit My Acca button no longer displayed as only one selection remains open on casino game overlay.
    PRECONDITIONS: * Cashout Tab & EMA are enabled from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User has placed a bet on DOUBLE, TREBLE,ACCA4 and more
    PRECONDITIONS: *All selections in the placed bet are active
    PRECONDITIONS: Note:-
    PRECONDITIONS: *Coral has 'EDIT MY BET' button
    PRECONDITIONS: *Ladbrokes has 'EDIT MY ACCA' button
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_cashout_tabverify_that_edit_my_betedit_my_acca_button_is_shown_only_for_double_treble_and_acca4_bets(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE ,TREBLE and ACCA4 bets
        EXPECTED: '* Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE ,TREBLE and ACCA4 bets
        EXPECTED: * Stake is shown
        EXPECTED: * Est. Returns ( Coral )/ Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_004_click_on_edit_my_betedit_my_acca_button_for_treble_betdelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets__gt_cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_double_only(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button for TREBLE bet
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets -&gt; Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for DOUBLE only
        EXPECTED: * Two selections remained in edited ACCA
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is shown only for DOUBLE bet
        EXPECTED: * New Stake is shown
        EXPECTED: * New Est. Returns ( Coral )/New Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_005_repeat_step_4_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat step-4 in cashout tab
        EXPECTED: * ONE selection remained in edited ACCA
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is NOT shown for SINGLE bet
        EXPECTED: * New Stake is shown
        EXPECTED: * New Est. Returns ( Coral )/New Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_006_navigate_to_my_bets__gt_open_betsverify_that_edit_my_betedit_my_acca_button_is_shown_for_acca4(self):
        """
        DESCRIPTION: Navigate to My Bets -&gt; Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for ACCA4
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is shown for ACCA4 bet
        EXPECTED: * Stake is shown
        EXPECTED: * Est. Returns ( Coral )/ Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_007_click_on_edit_my_betedit_my_acca_button_for_acca4_betdelete_one_of_the_selections_and_confirm_changes_or_add_a_result_in_tinavigate_back_to_my_bets_gt_cashoutverify_that_edit_my_betedit_my_acca_button_is_shown_for_treble_only(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button for ACCA4 bet
        DESCRIPTION: Delete one of the selections and confirm changes OR add a result in TI
        DESCRIPTION: Navigate back to My Bets &gt; Cashout
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE only
        EXPECTED: * Three selections remained in edited ACCA
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: * New Stake is shown
        EXPECTED: * New Est. Returns ( Coral )/New Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_008_repeat_step_45_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat step-4,5 in 'Openbets' tab
        EXPECTED: 
        """
        pass
