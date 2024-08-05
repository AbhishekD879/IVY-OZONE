import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C60020581_Verify_Edit_mode_in_expanded_bet_slip_during_deleting_selections(Common):
    """
    TR_ID: C60020581
    NAME: Verify "Edit" mode in expanded bet slip during deleting selections
    DESCRIPTION: Test case verifies ability to exit from "Edit" mode   expanded bet slip
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Sports book home page is opened
    PRECONDITIONS: User has added 2 or more selections to bet slip (e.g.: 6 selections)
    PRECONDITIONS: 1 or more selections are with 'Odds Boost' button
    PRECONDITIONS: Bet slip expanded
    PRECONDITIONS: "Edit" and "Remove All / Clear" buttons are displayed in the left top of bet slip
    PRECONDITIONS: Coral / Ladbrokes designs :
    PRECONDITIONS: ![](index.php?/attachments/get/121107913) ![](index.php?/attachments/get/121107914)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Coral - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2ae62b7f82157bc985bf3
    PRECONDITIONS: Ladbrokes - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea989678beef8bc2366aa76
    """
    keep_browser_open = True

    def test_001__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to  update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107981) ![](index.php?/attachments/get/121107982)
        """
        pass

    def test_002__tap_on_x_button_next_to_2_selections_in_expanded_bet_slip_to_remove_2_selections(self):
        """
        DESCRIPTION: * Tap on 'X' button next to 2 selections in expanded bet slip to remove 2 selections
        EXPECTED: * bet slip remains expanded
        EXPECTED: * 2 selections were deleted from bet slip view
        """
        pass

    def test_003__tap_on_odds_boost_button_on_any_selections(self):
        """
        DESCRIPTION: * Tap on 'Odds Boost' button on any selections
        EXPECTED: * selected selection was boosted
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip  "Edit" mode disabled
        EXPECTED: * no ability to  update selections with a 'X' option next to each selection
        """
        pass

    def test_004__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to  update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107981) ![](index.php?/attachments/get/121107982)
        """
        pass

    def test_005__tap_on_done_button(self):
        """
        DESCRIPTION: * Tap on "Done" button
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip  "Edit" mode disabled
        EXPECTED: * no ability to  update selections with a 'X' option next to each selection
        EXPECTED: * no one selection was deleted
        """
        pass

    def test_006__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to  update selections with a 'X' option next to each selection
        """
        pass

    def test_007__tap_on_stake_filed_of_any_selection_in_bet_slip(self):
        """
        DESCRIPTION: * Tap on 'Stake' filed of any selection in bet slip
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip  "Edit" mode disabled
        EXPECTED: * no ability to  update selections with a 'X' option next to each selection
        EXPECTED: * keypad opens allowing user to enter the stake
        EXPECTED: * no one selection was deleted
        """
        pass

    def test_008__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * keypad closes
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to  update selections with a 'X' option next to each selection
        """
        pass

    def test_009__tap_on_x_button_next_to_1_selection_in_expanded_bet_slip_to_remove_1_selection(self):
        """
        DESCRIPTION: * Tap on 'X' button next to 1 selection in expanded bet slip to remove 1 selection
        EXPECTED: * bet slip remains expanded
        EXPECTED: * 1 selection was deleted from bet slip view
        """
        pass

    def test_010__collapse_bet_slip(self):
        """
        DESCRIPTION: * Collapse bet slip
        EXPECTED: * Bet slip collapsed
        """
        pass

    def test_011__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * bet slip expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip is not in "Edit" mode
        EXPECTED: * no ability to  update selections with a 'X' option next to each selection
        """
        pass

    def test_012__tap_on_edit_button(self):
        """
        DESCRIPTION: * Tap on "Edit" button
        EXPECTED: * bet slip expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to  update selections with a 'X' option next to each
        """
        pass

    def test_013__tap_on_x_button_next_to_1_selection_in_expanded_bet_slip_to_remove_1_selection(self):
        """
        DESCRIPTION: * Tap on 'X' button next to 1 selection in expanded bet slip to remove 1 selection
        EXPECTED: * bet slip remains expanded
        EXPECTED: * 1 selection was deleted from bet slip view
        """
        pass

    def test_014__tap_remove_all__clear_button(self):
        """
        DESCRIPTION: * Tap "Remove All / Clear" button
        EXPECTED: *  "Remove all?" popup with options to Confirm or Cancel appears
        EXPECTED: Coral / Ladbrokes designs :
        EXPECTED: ![](index.php?/attachments/get/121107915) ![](index.php?/attachments/get/121107916)
        """
        pass

    def test_015__user_taps_on_cancel_button_on_the_remove_all_popup(self):
        """
        DESCRIPTION: * User taps on "Cancel" button on the "Remove all?" popup
        EXPECTED: * "Remove all?" popup disappears
        EXPECTED: * bet slip remains expanded
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip  "Edit" mode disabled
        EXPECTED: * no ability to  update selections with a 'X' option next to each
        """
        pass
