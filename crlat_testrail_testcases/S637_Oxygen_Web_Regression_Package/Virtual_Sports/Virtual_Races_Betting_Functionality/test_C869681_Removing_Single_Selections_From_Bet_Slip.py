import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869681_Removing_Single_Selections_From_Bet_Slip(Common):
    """
    TR_ID: C869681
    NAME: Removing Single Selections From Bet Slip
    DESCRIPTION: This test case verifies removing of Virtual Sport single selections from Bet Slip.
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: User is logged in or logged out
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_add_3_single_selections_from_the_event_details_page(self):
        """
        DESCRIPTION: Add 3 single selections from the event details page
        EXPECTED: Betslip counter is increased to 3
        """
        pass

    def test_002_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: *   Bet Slip is opened
        EXPECTED: *   Selections are displayed in Bet Slip
        EXPECTED: *   Section header counter is 3
        """
        pass

    def test_003_add_amount_to_any_selection_using_stake_box_quick_stake_buttons_are_not_visible_for_more_than_one_selection(self):
        """
        DESCRIPTION: Add amount to any selection using Stake box (Quick Stake buttons are not visible for more than one selection)
        EXPECTED: The total wager for the selection is entered. The following fields are changed due to selected stake:
        EXPECTED: 1.  **Stake **box of selection
        EXPECTED: 2.  **Estimated Returns **of selection
        EXPECTED: 3.  **Total Stake**
        EXPECTED: 4.  **Total Est. Returns**
        """
        pass

    def test_004_unselect_one_of_the_selections_placed_during_step_3_from_the_event_page(self):
        """
        DESCRIPTION: Unselect one of the selections (placed during step №3) from the event page
        EXPECTED: 1.  Selection is removed from the Bet Slip
        EXPECTED: 2.  The **counter in the 'Single' section header** is decremented by 1
        EXPECTED: 3.  The betslip **counter in the Global Header** is decremented by 1
        EXPECTED: 4.  The **'Total Stake' **field is decremented by stake defined in the removed selection
        EXPECTED: 5.  The **'Total Est. Returns'** field is decremented by the estimated return in removed selection
        """
        pass

    def test_005_remove_all_selections_from_the_event_details_page(self):
        """
        DESCRIPTION: Remove all selections from the event details page
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  User sees a message 'Your betslip is empty'
        """
        pass

    def test_006_repeat_this_test_case_for_all_virtual_racesvirtual_motorsports_class_id_288virtual_cycling_class_id_290virtual_horse_racing_class_id_285virtual_greyhound_racing_class_id_286virtual_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Motorsports (Class ID 288)
        DESCRIPTION: Virtual Cycling (Class ID 290)
        DESCRIPTION: Virtual Horse Racing (Class ID 285)
        DESCRIPTION: Virtual Greyhound Racing (Class ID 286)
        DESCRIPTION: Virtual Grand National (Class ID 26604)
        EXPECTED: 
        """
        pass
