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
class Test_C64569860_verify_displaying_of_Edit_My_Acca_button_when_any_selection_is_suspended_on_casino_game_overlay(Common):
    """
    TR_ID: C64569860
    NAME: verify displaying of Edit My Acca button when any selection is suspended on casino game overlay.
    DESCRIPTION: verify displaying of Edit My Acca button when any selection is suspended on casino game overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * Cashout Tab & EMA are enabled from CMS
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

    def test_003_tap_cashout_tabverify_that_edit_my_betedit_my_acca_button_is_shown_only_for_treble_bet(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is shown only for TREBLE bet
        EXPECTED: '* Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE bet
        EXPECTED: * Stake is shown
        EXPECTED: * Est. Returns ( Coral )/ Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_004_click_on_edit_my_betedit_my_acca_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: * Edit mode of the Acca is shown
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        pass

    def test_005_suspended_one_of_the_selections_of_the_treble_in_backoffice(self):
        """
        DESCRIPTION: Suspended one of the selections of the TREBLE in Backoffice
        EXPECTED: * Selection is suspended
        """
        pass

    def test_006_verify_that_the_edit_my_accabet_button_is_greyed_out_disabled_and_the_button_is_not_clickable(self):
        """
        DESCRIPTION: Verify that the 'EDIT MY ACCA/Bet' button is greyed out (disabled) and the button is NOT clickable
        EXPECTED: * Grey (disabled) 'EDIT MY BET/EDIT MY ACCA' button is shown for TREBLE
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button is NOT clickable
        EXPECTED: * Suspended selection is greyed out and has 'SUSP' label
        EXPECTED: Stake is shown
        EXPECTED: * Est. Returns ( Coral )/ Potential Returns ( Ladbrokes ) is shown
        """
        pass

    def test_007_repeat_step_456_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat step-4,5,6 in 'Openbets' tab
        EXPECTED: 
        """
        pass
