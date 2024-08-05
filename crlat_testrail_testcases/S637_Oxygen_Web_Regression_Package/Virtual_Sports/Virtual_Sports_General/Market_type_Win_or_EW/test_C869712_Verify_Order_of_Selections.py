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
class Test_C869712_Verify_Order_of_Selections(Common):
    """
    TR_ID: C869712
    NAME: Verify Order of Selections
    DESCRIPTION: This test case verifies order of selections by price and by name (in case of the equal prices) in Win or E/W section.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to 'Win or E/W' section
        EXPECTED: 
        """
        pass

    def test_002_verify_selectionsorder(self):
        """
        DESCRIPTION: Verify selections order
        EXPECTED: Selections are ordered in Price/Odds order by acsending and by name in case of equal prices
        """
        pass

    def test_003_repeat_step_4_for_several_events(self):
        """
        DESCRIPTION: Repeat step №4 for several events
        EXPECTED: Selections are ordered in Price/Odds order by acsending and by name in case of equal prices
        """
        pass

    def test_004_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following Virtual Sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
