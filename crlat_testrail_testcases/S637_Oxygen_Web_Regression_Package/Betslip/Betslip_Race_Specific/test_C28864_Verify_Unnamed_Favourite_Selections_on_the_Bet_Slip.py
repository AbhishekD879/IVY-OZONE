import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C28864_Verify_Unnamed_Favourite_Selections_on_the_Bet_Slip(Common):
    """
    TR_ID: C28864
    NAME: Verify Unnamed Favourite Selections on the Bet Slip
    DESCRIPTION: This test case verifies how Favourite selections added to the Bet Slip are displayed
    PRECONDITIONS: 'Unnamed Favourite' and 'Unnamed 2nd Favourite' selections are present in Race event
    """
    keep_browser_open = True

    def test_001_add_the_following_selections_to_the_betslip___unnamed_favourite___unnamed_2nd_favourite(self):
        """
        DESCRIPTION: Add the following selections to the Betslip:
        DESCRIPTION: *   'Unnamed Favourite'
        DESCRIPTION: *   'Unnamed 2nd Favourite'
        EXPECTED: 
        """
        pass

    def test_002_open_bet_slip_and_verify_display_of_both_selections(self):
        """
        DESCRIPTION: Open Bet Slip and verify display of both selections
        EXPECTED: The following correct information is displayed for each selection in 'Singles' section:
        EXPECTED: *   'Unnamed Favourite'/'Unnamed 2nd Favourite' selection name
        EXPECTED: *   Market Name (e.g. Win or Each Way)
        EXPECTED: *   Event Start Time and  Name (e.g. 12:40 Newbury)
        EXPECTED: *  **NO E/W text and checkbox is displayed**
        """
        pass
