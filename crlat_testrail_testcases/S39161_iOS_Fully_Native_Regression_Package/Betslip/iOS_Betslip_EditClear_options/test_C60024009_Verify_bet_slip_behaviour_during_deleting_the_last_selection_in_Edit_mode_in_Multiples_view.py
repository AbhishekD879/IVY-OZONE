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
class Test_C60024009_Verify_bet_slip_behaviour_during_deleting_the_last_selection_in_Edit_mode_in_Multiples_view(Common):
    """
    TR_ID: C60024009
    NAME: Verify bet slip behaviour during deleting the last selection in "Edit" mode in Multiples view
    DESCRIPTION: Test case verifies  "Edit" mode   expanded bet slip
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Sports book home page is opened
    PRECONDITIONS: User has added 2 or more selections to bet slip (e.g.: 3 selections)
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
        EXPECTED: * bet slip in "Edit" mode with ability to update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107981) ![](index.php?/attachments/get/121107982)
        """
        pass

    def test_002__tap_on_x_button_next_to_2_selections_to_remove_2_selections_from_bet_slip(self):
        """
        DESCRIPTION: * Tap on 'X' button next to 2 selections to remove 2 selections from bet slip
        EXPECTED: * bet slip remains opened
        EXPECTED: * 2 selection were deleted (e.g: 3-2=1 selection remains in bet slip)
        EXPECTED: * Bet slip selections counter is not decreased
        EXPECTED: * Multiples view remains in bet slip
        """
        pass

    def test_003__tap_on_done_button_to_exit_from_bet_slip_edit_mode(self):
        """
        DESCRIPTION: * Tap on 'Done' button to exit from bet slip "Edit" mode
        EXPECTED: * "Done" button transforms into "Edit" button
        EXPECTED: * bet slip remains opened
        EXPECTED: * 2 selections were deleted
        EXPECTED: * bet slip is not in "Edit" mode
        EXPECTED: * Bet slip selections counter is  decreased (e.g: 3-2=1 selection remains in bet slip)
        EXPECTED: * Multiples view remains in bet slip
        """
        pass

    def test_004__collapse_bet_slip(self):
        """
        DESCRIPTION: * Collapse bet slip
        EXPECTED: * Bet slip collapsed
        """
        pass

    def test_005__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bet slip expanded
        EXPECTED: * "Edit" and "Remove All / Clear" buttons are not displayed in the left top of bet slip
        EXPECTED: * Multiples view is no more available in bet slip
        EXPECTED: * bet slip displays in single view (without multiples section)
        EXPECTED: Coral / Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/121107995) ![](index.php?/attachments/get/121107996)
        """
        pass
