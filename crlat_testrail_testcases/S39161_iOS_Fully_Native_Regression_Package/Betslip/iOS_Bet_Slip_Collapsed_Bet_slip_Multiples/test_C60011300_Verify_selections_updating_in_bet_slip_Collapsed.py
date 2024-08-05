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
class Test_C60011300_Verify_selections_updating_in_bet_slip_Collapsed(Common):
    """
    TR_ID: C60011300
    NAME: Verify selections updating in bet slip (Collapsed)
    DESCRIPTION: Test case verifies selections updating in bet slip (Collapsed)
    PRECONDITIONS: App installed and opened
    PRECONDITIONS: Bet slip contains  2 added selections
    PRECONDITIONS: Designs
    PRECONDITIONS: Ladbrokes - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98a80395ffa255f45d4db
    PRECONDITIONS: Coral - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa98a5c4cec8bf7b2aff32
    """
    keep_browser_open = True

    def test_001__add_6_new_selections_to_bet_slip(self):
        """
        DESCRIPTION: * Add 6 new selections to bet slip
        EXPECTED: * 6 new selections were successfully added to bet slip
        EXPECTED: * bet slip in collapsed state
        EXPECTED: * bet slip counter increased into appropriate amount of new added selections (e.g. "Betslip 8" )
        EXPECTED: * bet slip displays update of accumulative Odds for added selections including the bet type (E.G User adds 3 selections to bet slip and the accumulator price of those selections is 6.9 must display Treble @ 6/1'
        """
        pass

    def test_002__remove_2_selection_from_bet_slip_one_by_one(self):
        """
        DESCRIPTION: * Remove 2 selection from bet slip one by one
        EXPECTED: * 2 selection were successfully removed
        EXPECTED: * bet slip in collapsed state
        EXPECTED: * bet slip counter decreased into appropriate amount of removed selections (e.g. "Betslip 6" )
        EXPECTED: * bet slip displays update of the accumulative Odds for removed selections including the bet type
        """
        pass

    def test_003__remove_5_selection_from_bet_slip_one_by_one(self):
        """
        DESCRIPTION: * Remove 5 selection from bet slip one by one
        EXPECTED: * 5 selection were successfully removed
        EXPECTED: * bet slip in collapsed state
        EXPECTED: * bet slip counter and accumulative Odds disappeared
        EXPECTED: * bet slip displays single selection with next items:
        EXPECTED: -- Selection name;
        EXPECTED: -- Selection Odds;
        EXPECTED: -- Stake field;
        EXPECTED: E.g.:
        EXPECTED: ![](index.php?/attachments/get/120925776)
        """
        pass

    def test_004__repeat_steps_1_3_and_verify_that_animation_of_bet_slip_during_adding_new_selections_conforms_to_the_one_that_was_define(self):
        """
        DESCRIPTION: * Repeat steps 1-3 and verify that animation of bet slip during adding new selections conforms to the one that was define
        EXPECTED: *  Animation of bet slip during adding new selections conforms to the one that was define
        EXPECTED: Coral/Ladbrokes animation (animation for both brands, should work the same way)
        EXPECTED: https://coralracing.sharepoint.com/:v:/s/SymphonyNativeQA/ERKb64xqie5EmX1gXTGqmckBEQAEwY7CC1zFyOehfvzOmg?e=p9qE1N
        """
        pass
