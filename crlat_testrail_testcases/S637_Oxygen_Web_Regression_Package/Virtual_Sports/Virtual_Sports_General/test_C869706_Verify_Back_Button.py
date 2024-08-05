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
class Test_C869706_Verify_Back_Button(Common):
    """
    TR_ID: C869706
    NAME: Verify Back Button
    DESCRIPTION: This test case verifies Back button functionality
    DESCRIPTION: BMA-3547, BMA-4830
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_virtual_sport_homepage(self):
        """
        DESCRIPTION: Open <Virtual Sport> Homepage
        EXPECTED: Virtual Sports successfully opened
        """
        pass

    def test_002_navigate_between_this_virtual_sport_events(self):
        """
        DESCRIPTION: Navigate between this <Virtual Sport> events
        EXPECTED: 
        """
        pass

    def test_003_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is redirected to the Homepage
        """
        pass

    def test_004_repeat_steps_4_5_for__greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat Steps 4-5 for :
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass

    def test_005_navigate_to_all_sports_page(self):
        """
        DESCRIPTION: Navigate to All Sports page
        EXPECTED: 
        """
        pass

    def test_006_open_virtuals(self):
        """
        DESCRIPTION: Open 'Virtuals'
        EXPECTED: Virtual Sports successfully opened
        """
        pass

    def test_007_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is redirected to the 'All sports' page
        """
        pass

    def test_008_repeat_steps_6_8_for__greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat Steps 6-8 for :
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
