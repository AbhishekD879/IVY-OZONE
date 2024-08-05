import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869657_Verify_Order_of_Selections_for_Total_Number_of_Points_market(Common):
    """
    TR_ID: C869657
    NAME: Verify Order of Selections for Total Number of Points market
    DESCRIPTION: This test case verifies that selections are ordered in Price/Odds order (lowest price first) in 'Total Number of Points' section.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_tennis_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Tennis' sport page
        EXPECTED: 'Virtual Tennis' sport page is opened
        """
        pass

    def test_002_go_to_total_number_of_points_section(self):
        """
        DESCRIPTION: Go to 'Total Number of Points' section
        EXPECTED: 
        """
        pass

    def test_003_verify_selectionsorder(self):
        """
        DESCRIPTION: Verify selections order
        EXPECTED: Selections are ordered in Price/Odds order by acsending
        """
        pass

    def test_004_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Selections are ordered in Price/Odds order by acsending
        """
        pass
