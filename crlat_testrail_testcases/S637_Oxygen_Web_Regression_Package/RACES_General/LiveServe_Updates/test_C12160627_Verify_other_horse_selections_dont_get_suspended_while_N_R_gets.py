import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C12160627_Verify_other_horse_selections_dont_get_suspended_while_N_R_gets(Common):
    """
    TR_ID: C12160627
    NAME: Verify other horse selections don’t get suspended while N/R gets
    DESCRIPTION: This test case verifies other horse selections don’t get suspended while N/R gets
    PRECONDITIONS: 1. Open horse racing event
    PRECONDITIONS: 2. Add market Top 2 Finish in TI tool for this event
    PRECONDITIONS: 3. Add selections to market
    PRECONDITIONS: 4. Set 1-2 selections as N/R (to mark selection as non runner just add 'N/R' in the end of selection name in TI, e.g. '|Horse Lily N/R|')
    PRECONDITIONS: 5. Repeat steps 3-4 for Win or Each Way market
    """
    keep_browser_open = True

    def test_001_suspend_nr_selection_for_win_or_each_way_market(self):
        """
        DESCRIPTION: Suspend N/R selection for Win or Each Way market
        EXPECTED: Only 1 N/R selection is suspended
        """
        pass

    def test_002_suspend_nr_selection_for_top_2_finish_market(self):
        """
        DESCRIPTION: Suspend N/R selection for Top 2 Finish market
        EXPECTED: Only 1 N/R selection is suspended
        """
        pass
