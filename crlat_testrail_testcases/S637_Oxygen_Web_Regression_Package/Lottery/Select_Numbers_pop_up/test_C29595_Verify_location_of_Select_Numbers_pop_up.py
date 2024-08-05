import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C29595_Verify_location_of_Select_Numbers_pop_up(Common):
    """
    TR_ID: C29595
    NAME: Verify location of Select Numbers pop-up
    DESCRIPTION: This test case verifies location of Select Numbes pop-up.
    DESCRIPTION: JIRA TICKETS:
    DESCRIPTION: BMA-8952: Lottery - number picker popup to start on top of screen
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_lotto_page(self):
        """
        DESCRIPTION: Go to Lotto page
        EXPECTED: Lotto page is opened
        """
        pass

    def test_003_select_lottery_and_tapany_ball_of_a_number_line_on_the_main_page(self):
        """
        DESCRIPTION: Select Lottery and tap any ball of a number line on the main page
        EXPECTED: *   Select Number pop-up appears at the top of the page
        EXPECTED: *   There is no space between Select Number pop-up and the top edge of the page
        """
        pass

    def test_004_mobile_rotate_device_to_landscape_mode(self):
        """
        DESCRIPTION: (Mobile) Rotate device to Landscape mode
        EXPECTED: *   Select Number pop-up is displayed at the top of the page
        EXPECTED: *   There is no space between Select Number pop-up and the top edge of the page
        """
        pass

    def test_005_mobile_rotate_device_to_portrait_mode(self):
        """
        DESCRIPTION: (Mobile) Rotate device to Portrait mode
        EXPECTED: *   Select Number pop-up is displayed at the top of the page
        EXPECTED: *   There is no space between Select Number pop-up and the top edge of the page
        """
        pass
