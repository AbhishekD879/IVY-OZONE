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
class Test_C29024_Undisplayed_selections_not_removed_from_the_Betslip(Common):
    """
    TR_ID: C29024
    NAME: Undisplayed selections not removed from the Betslip
    DESCRIPTION: This test case verifies that undisplayed selections are not removed from the bet slip.
    DESCRIPTION: AUTOTEST [C9690033]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_two_active_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add two active selections to the Betslip
        EXPECTED: Betslip counter shows "2"
        """
        pass

    def test_002_trigger_the_situation_when_data_of_one_selected_outcomes_is_undisplayed_in_ss(self):
        """
        DESCRIPTION: Trigger the situation when data **of one selected outcomes** is undisplayed in SS
        EXPECTED: 
        """
        pass

    def test_003_go_to_betslip_page(self):
        """
        DESCRIPTION: Go to Betslip page
        EXPECTED: Unchanged content of Betslip is shown, both selections are still present
        """
        pass

    def test_004_refresh_the_page_and_open_betslip(self):
        """
        DESCRIPTION: Refresh the page and open Betslip
        EXPECTED: *   Undisplayed Selection remains present in the Betslip
        EXPECTED: *   Active selection remains present in the Betslip
        EXPECTED: *   Betslip counter still shows "2"
        """
        pass
