import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28979_Verify_Event_Ordering_When_By_Latest_Results_Sorting_Type_is_Selected___To_be_archived(Common):
    """
    TR_ID: C28979
    NAME: Verify Event Ordering When 'By Latest Results' Sorting Type is Selected  -  To be archived
    DESCRIPTION: This test case verifies order of events when 'By Latest Result' sorting type is selected
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the Sports Menu Ribbon tap 'Greyhounds' icon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        EXPECTED: 'By Latest Result' sorting type is selected by default
        """
        pass

    def test_004_check_order_of_the_results(self):
        """
        DESCRIPTION: Check order of the results
        EXPECTED: Event results are shown based on **'startTime'** attribute in ascending order:
        EXPECTED: *   The most up to date results will be displayed at the top of 5
        EXPECTED: *   The oldest of 5 will be shown the last
        """
        pass
