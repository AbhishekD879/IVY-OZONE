import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C710605_Numeric_keyboard_displaying_for_1_selections(Common):
    """
    TR_ID: C710605
    NAME: Numeric keyboard displaying for >1 selections
    DESCRIPTION: This test case verifies displaying numeric keyboard for >1 selections in Betslip
    DESCRIPTION: Applies for Mobile only
    DESCRIPTION: AUTOTEST: [C9698421]
    PRECONDITIONS: - Oxygen application
    PRECONDITIONS: - Several selections are added to the Betslip
    PRECONDITIONS: - Betslip is opened
    """
    keep_browser_open = True

    def test_001_verify_availability_of_numeric_keyboard(self):
        """
        DESCRIPTION: Verify availability of numeric keyboard
        EXPECTED: - Numeric keyboard is NOT available above 'BET NOW'/'LOG IN & BET' button
        EXPECTED: - NO 'Stake' boxes are focused
        """
        pass

    def test_002_set_focus_over_any_stake_or_all_single_stakes_box(self):
        """
        DESCRIPTION: Set focus over any 'Stake' or 'All single stakes' box
        EXPECTED: Numeric keyboard is available above 'BET NOW'/'LOG IN & BET' button
        """
        pass
