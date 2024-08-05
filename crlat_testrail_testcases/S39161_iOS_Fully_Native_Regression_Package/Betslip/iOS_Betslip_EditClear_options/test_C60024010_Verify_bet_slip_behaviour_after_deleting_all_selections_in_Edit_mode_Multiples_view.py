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
class Test_C60024010_Verify_bet_slip_behaviour_after_deleting_all_selections_in_Edit_mode_Multiples_view(Common):
    """
    TR_ID: C60024010
    NAME: Verify bet slip behaviour after deleting  all selections in 'Edit' mode  (Multiples view)
    DESCRIPTION: Test case verifies bet slip behaviour after deleting all selections (Multiples)
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Sports book home page is opened
    PRECONDITIONS: User has added 2 or more selections to bet slip (e.g.: 5 selections)
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
        EXPECTED: * bet slip expanded
        EXPECTED: * "Edit" button transforms into "Done" button
        EXPECTED: * bet slip in "Edit" mode with ability to update selections with a 'X' option next to each selection
        EXPECTED: Coral / Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121107981) ![](index.php?/attachments/get/121107982)
        """
        pass

    def test_002__tap_on_x_button_next_to_all_selections_in_expanded_bet_slip_to_remove_all_selections(self):
        """
        DESCRIPTION: * Tap on 'X' button next to all selections in expanded bet slip to remove all selections
        EXPECTED: * bet slip remains expanded
        EXPECTED: * selections were deleted from bet slip view
        EXPECTED: * Bet slip selections counter is not decreased
        """
        pass

    def test_003__tap_on_done_button(self):
        """
        DESCRIPTION: * Tap on "Done" button
        EXPECTED: * selections were deleted from bet slip
        EXPECTED: * bet slip empty and closes
        """
        pass
