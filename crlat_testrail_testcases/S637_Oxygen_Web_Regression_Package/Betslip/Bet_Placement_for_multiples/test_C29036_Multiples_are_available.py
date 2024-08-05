import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29036_Multiples_are_available(Common):
    """
    TR_ID: C29036
    NAME: Multiples are available
    DESCRIPTION: This test case verifies that Multiples are available for selections from different events
    DESCRIPTION: *Note:* Multiples may not be available after adding Special events to the Betslip
    DESCRIPTION: AUTOTEST [C1501915]
    DESCRIPTION: AUTOTEST [C528098]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_open_any_sport(self):
        """
        DESCRIPTION: Open any Sport
        EXPECTED: 
        """
        pass

    def test_003_add_several_selections_with_lp_price_type_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections with 'LP' price type from different events to the Betslip
        EXPECTED: 
        """
        pass

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: * 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: * Multiples are available for added selections
        """
        pass

    def test_005_add_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add more selections to the Betslip
        EXPECTED: List of available Multiples is updated, more Multiple types are available
        """
        pass

    def test_006_remove_some_selections(self):
        """
        DESCRIPTION: Remove some selections
        EXPECTED: List of Multiples is updated
        """
        pass

    def test_007_leave_only_1_selection_in_the_betslip(self):
        """
        DESCRIPTION: Leave only 1 selection in the Betslip
        EXPECTED: Multiples are not available for 1 selection
        """
        pass
