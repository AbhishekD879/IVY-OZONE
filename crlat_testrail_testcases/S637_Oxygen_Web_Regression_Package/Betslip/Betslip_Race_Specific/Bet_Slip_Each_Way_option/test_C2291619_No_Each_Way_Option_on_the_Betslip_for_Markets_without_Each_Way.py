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
class Test_C2291619_No_Each_Way_Option_on_the_Betslip_for_Markets_without_Each_Way(Common):
    """
    TR_ID: C2291619
    NAME: No Each Way Option on the Betslip for Markets without Each Way
    DESCRIPTION: This test case verifies Absence of Each Way Option on the Betslip for Markets without Each Way available
    PRECONDITIONS: **There is a race event with market without Each Way available**
    """
    keep_browser_open = True

    def test_001_add_race_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add race selection to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: *  Selection is displayed on the Betslip
        EXPECTED: *  There is no Each Way checkbox
        """
        pass
