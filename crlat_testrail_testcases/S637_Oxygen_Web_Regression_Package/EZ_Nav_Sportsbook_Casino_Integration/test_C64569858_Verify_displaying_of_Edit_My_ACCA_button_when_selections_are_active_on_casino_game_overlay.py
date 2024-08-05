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
class Test_C64569858_Verify_displaying_of_Edit_My_ACCA_button_when_selections_are_active_on_casino_game_overlay(Common):
    """
    TR_ID: C64569858
    NAME: Verify displaying of Edit My ACCA button when selections are active on casino game overlay.
    DESCRIPTION: Verify displaying of Edit My ACCA button when selections are active on casino game overlay.
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

    def test_004_click_on_edit_my_betedit_my_acca_buttonverify_that_edit_mode_of_the_acca_is_shown(self):
        """
        DESCRIPTION: Click on 'EDIT MY BET/EDIT MY ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is shown
        EXPECTED: * Edit mode of the Acca is shown
        EXPECTED: * 'EDIT MY BET/EDIT MY ACCA' button changes to the 'CANCEL EDITING' button
        """
        pass

    def test_005_repeat_steps_3_4_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat steps 3-4 in 'Openbets' tab
        EXPECTED: 
        """
        pass
