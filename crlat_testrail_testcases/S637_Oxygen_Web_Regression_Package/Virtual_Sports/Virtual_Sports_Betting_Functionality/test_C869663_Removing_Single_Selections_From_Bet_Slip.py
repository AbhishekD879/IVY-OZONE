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
class Test_C869663_Removing_Single_Selections_From_Bet_Slip(Common):
    """
    TR_ID: C869663
    NAME: Removing Single Selections From Bet Slip
    DESCRIPTION: This test case verifies removing of Virtual Sport single selections from Bet Slip.
    DESCRIPTION: NOTE, **User Story: **BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_tap_virtual_football_icon_on_the_sports_carousel(self):
        """
        DESCRIPTION: Tap 'Virtual Football' icon on the sports carousel
        EXPECTED: 'Virtual Football' homepage is opened
        """
        pass

    def test_002_add_3_single_selections_from_the_event_details_page(self):
        """
        DESCRIPTION: Add 3 single selections from the event details page
        EXPECTED: Betslip counter is increased to 3
        """
        pass

    def test_003_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: *   Bet Slip is opened
        EXPECTED: *   Selections are displayed in Bet Slip
        EXPECTED: *   Section header counter is 3
        """
        pass

    def test_004_add_amount_to_any_selection_using_stake_box_quick_stake_buttons_are_not_visible_for_more_than_one_selection(self):
        """
        DESCRIPTION: Add amount to any selection using Stake box (Quick Stake buttons are not visible for more than one selection)
        EXPECTED: The total wager for the selection is entered. The following fields are changed due to selected stake:
        EXPECTED: 1.  **Stake **box of selection
        EXPECTED: 2.  **Estimated Returns **of selection
        EXPECTED: 3.  **Total Stake**
        EXPECTED: 4.  **Total Est. Returns**
        """
        pass

    def test_005_unselect_one_of_the_selections_placed_during_step_3_from_the_event_page(self):
        """
        DESCRIPTION: Unselect one of the selections (placed during step №3) from the event page
        EXPECTED: 1.  Selection is removed from the Bet Slip
        EXPECTED: 2.  The **counter in the 'Single' section header** is decreased by 1
        EXPECTED: 3.  The betslip **counter in the Global Header** is decreased by 1
        EXPECTED: 4.  The **'Total Stake' **field is decreased by stake defined in the removed selection
        EXPECTED: 5.  The **'Total Est. Returns'** field is decreased by the estimated return in removed selection
        """
        pass

    def test_006_unselect_all_selections_on_the_event_details_page_and_open_betslip(self):
        """
        DESCRIPTION: Unselect all selections on the event details page and open betslip
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  User sees a message 'Your betslip is empty'
        """
        pass

    def test_007_repeat_this_test_case_for_the_following_virtual_sports_football_speedway_tennis(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Football,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        EXPECTED: 
        """
        pass
