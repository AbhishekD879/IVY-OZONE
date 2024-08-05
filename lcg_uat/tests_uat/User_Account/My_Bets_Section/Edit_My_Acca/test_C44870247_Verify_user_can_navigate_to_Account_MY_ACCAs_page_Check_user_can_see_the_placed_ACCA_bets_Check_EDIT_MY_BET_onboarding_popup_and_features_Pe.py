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
class Test_C44870247_Verify_user_can_navigate_to_Account_MY_ACCAs_page_Check_user_can_see_the_placed_ACCA_bets_Check_EDIT_MY_BET_onboarding_popup_and_features_Perform_edit_my_bet_and_check_confirm_Cancel_features____When_Edited___The_ACCA_edited_s(Common):
    """
    TR_ID: C44870247
    NAME: "Verify user can navigate to Account > MY ACCAs page -Check user can see the placed ACCA bets -Check 'EDIT MY BET' onboarding popup and features -Perform edit my bet and check 'confirm' , 'Cancel' features       When Edited -->  The ""ACCA edited s
    DESCRIPTION: "Verify user can navigate to Account > MY ACCAs page
    DESCRIPTION: -Check user can see the placed ACCA bets
    DESCRIPTION: -Check 'EDIT MY BET' onboarding popup and features
    DESCRIPTION: -Perform edit my acca and check 'confirm' , 'Cancel' features
    DESCRIPTION: When Edited -->  The ""ACCA edited successfully""  message will be persist on the screen once the user finished editing. If they navigate away (e.g back to home page) and then return to view their acca, then they will see the 'Show Acca History' link
    DESCRIPTION: -Check when user removes selections user sees 'New Potential Returns' according to removed selections
    DESCRIPTION: -Check selection Undo button is displayed and functionality (if undo redisplay the selection)
    DESCRIPTION: When UNDO changes -->*Poten return values will be updated ,load (Spinner),and Acca edited sucessfully with Green tick is Disp
    DESCRIPTION: * And a label will be displayed with game/ selections which was removed.
    DESCRIPTION: When Changes not changes -->'Sorry, editing was unsuccessful, please try again'  and changes are not applied
    DESCRIPTION: -Check after closing 'EDIT MY ACCA' onboarding popup user is on My Accas page
    DESCRIPTION: - Verify tooltip telling user that they can edit their ACCA
    DESCRIPTION: -Verify below Pop Ups when user click on Edit my acca and navigates across web page.
    DESCRIPTION: Pop-up title: Do you want to cancel editing?
    DESCRIPTION: Pop-up Text: Moving away from this page will cancel changes already made to this bet! Are you sure you want to cancel?
    DESCRIPTION: Action buttons: 'Cancel Edit' & 'Continue editing'
    DESCRIPTION: -Check that the user is shown an 'i' icon when the user tries to edit the Acca, tap on it and verify pop up
    DESCRIPTION: - Verify Won/Lost indicator on Open bets/ Cash-out tab/ Settled bets .
    DESCRIPTION: - Verify Void/Suspended Selections behaviour
    DESCRIPTION: -->VOID: When editing an Accumulator BET, if a game is VOID, then they will see the label against that selection. They can't remove the VOID game, but they can still edit the remaining selections and 'Confirm'.
    DESCRIPTION: -->SUSPENDED: When editing an ACCA, if the game is SUSP, then they will see a label against that selection. They can not remove the SUSP selection, OR any of the other selection in that bet. SUSP status may be lifted later on, so they may come back to make changes later. "
    PRECONDITIONS: An ACCA has been placed already
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_open_bets_and_check_that_you_see_your_acca_and_if_its_the_first_time_that_you_have_accessed_my_bets_open_bets_you_should_see_a_tooltip_telling_you_that_you_can_edit_your_acca(self):
        """
        DESCRIPTION: Navigate to My Bets->Open Bets and check that you see your ACCA and if it's the first time that you have accessed My Bets->Open Bets, you should see a tooltip telling you that you can edit your ACCA
        EXPECTED: You should be able to see your ACCA in My Bets->Open Bets and a tooltip saying that you can edit your ACCA
        """
        pass

    def test_002_check_that_the_edit_my_bet_and_cancel_editing_buttons_work(self):
        """
        DESCRIPTION: Check that the Edit My BET and Cancel Editing buttons work
        EXPECTED: The Edit My BET and Cancel Editing buttons should work
        """
        pass

    def test_003_check_that_when_you_click_on_the_x_for_any_selection_that_the_selection_gets_greyed_out_and_you_see_an_undo_button_where_the_x_was_and_that_you_see_the_messageedit_my_bet_uses_the_cash_out_value_of_the_bet_and_the_latest_odds_of_each_selection(self):
        """
        DESCRIPTION: Check that when you click on the X for any selection that the selection gets greyed out and you see an UNDO button where the X was and that you see the message:
        DESCRIPTION: Edit My Bet uses the cash out value of the bet and the latest odds of each selection.
        EXPECTED: X should be clickable, the selection should be greyed out, you should see the UNDO button and see a message should be shown.
        """
        pass

    def test_004_check_that_when_you_click_on_an_x_to_remove_a_selection_you_see_new_potential_returns_and_that_the_undo_button_works(self):
        """
        DESCRIPTION: Check that when you click on an X to remove a selection, you see New Potential Returns and that the UNDO button works
        EXPECTED: You should see New Potential Returns and the UNDO button should work
        """
        pass

    def test_005_click_on_edit_my_bet_click_on_the_x_for_one_selection_and_then_click_on_the_home_or_menu_buttons_in_the_tab_bar_verify_that_you_see_the_do_you_want_to_cancel_editing_pop_up_and_it_should_have_the_buttons_cancel_edit_and_continue_editing_buttons_and_they_should_work(self):
        """
        DESCRIPTION: Click on Edit My BET, click on the X for one selection and then click on the Home or Menu buttons in the tab bar. Verify that you see the "Do you want to cancel editing?" pop up and it should have the buttons Cancel Edit and Continue Editing buttons and they should work
        EXPECTED: You should see the "Do you want to cancel editing?" pop up and both the Cancel Edit and Continue Editing should work as follows:
        EXPECTED: Cancel Edit should close the Edit Mode
        EXPECTED: Continue Editing should leave you in Edit Mode
        """
        pass

    def test_006_check_that_on_successful_editing_of_an_bet_you_see_the_acca_edited_successfully_message_and_on_the_left_of_the_message_is_a_green_circle_with_a_white_tick_and_also_that_your_removed_selection_is_greyed_out_and_has_the_text_removed(self):
        """
        DESCRIPTION: Check that on successful editing of an BET, you see the Acca Edited Successfully message and on the left of the message is a green circle with a white tick and also that your removed selection is greyed out and has the text REMOVED
        EXPECTED: You should see the message and for the selection(s) removed you should see the text REMOVED
        """
        pass

    def test_007_after_successfully_editing_an_accumulator_bet_navigate_away_and_back_and_check_that_bets_title_has_been_amended_to_be_a_double_if_the_original_acca_was_a_treble_a_treble_if_it_was_an_acca4_and_accax_1_if_x_was_greater_than_or_equal_to_5_and_also_check_that_you_see_a_show_edit_history_option(self):
        """
        DESCRIPTION: After successfully editing an Accumulator BET, navigate away and back and check that bet's title has been amended to be a double if the original ACCA was a treble, a treble if it was an ACCA(4) and ACCA(X-1) if X was greater than or equal to 5 and also check that you see a SHOW EDIT HISTORY option
        EXPECTED: The title of the ACCA should have changed and you should see the SHOW EDIT HISTORY option
        """
        pass

    def test_008_verify_the_sorry_editing_was_unsuccessful_please_try_again_when_it_has_not_been_possible_to_edit_an_acc(self):
        """
        DESCRIPTION: Verify the Sorry, editing was unsuccessful, please try again when it has not been possible to edit an ACC
        EXPECTED: You should see the message
        """
        pass

    def test_009_verify_that_you_see_the_won_indicator_in_an_acca_where_one_or_more_selections_have_been_won(self):
        """
        DESCRIPTION: Verify that you see the Won indicator in an ACCA where one or more selections have been won.
        EXPECTED: We should see the Won indicator for selections which have been won
        """
        pass

    def test_010_verify_that_if_one_of_your_selections_has_been_lost_you_should_see_that_acca_in_my_bets_settled_bets_as_being_lost(self):
        """
        DESCRIPTION: Verify that if one of your selections has been lost, you should see that ACCA in My Bets->Settled Bets as being lost.
        EXPECTED: You should see a losing ACCA in My Bets-Open Bets
        """
        pass

    def test_011_check_that_if_a_selection_in_an_acca_has_been_voided_then_you_should_not_be_able_to_remove_that_selection_but_other_selections_which_are_still_active_should_be_removable(self):
        """
        DESCRIPTION: Check that if a selection in an ACCA has been voided, then you should not be able to remove that selection, but other selections which are still active should be removable.
        EXPECTED: You should not be able to remove a voided selection, but other active selections should be removable.
        """
        pass

    def test_012_when_an_acca_is_suspended_either_in_edit_mode_or_non_edit_mode_you_should_not_be_able_to_edit_the_acca_and_you_should_see_an_appropriate_suspended_message(self):
        """
        DESCRIPTION: When an ACCA is suspended either in Edit mode or non-Edit mode, you should not be able to edit the ACCA and you should see an appropriate suspended message
        EXPECTED: You should not be able to edit a suspended ACCA.
        """
        pass
