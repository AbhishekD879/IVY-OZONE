import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1159080_Tracking_of_Timeform_Summary_Information_opening(Common):
    """
    TR_ID: C1159080
    NAME: Tracking of Timeform Summary Information opening
    DESCRIPTION: This test case verifies tracking of Timeform Summary Information opening on Greyhounds event details page
    DESCRIPTION: AUTOTEST [C1965337]
    PRECONDITIONS: * Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * Timeform overview is displayed above markets
        EXPECTED: * 'Show more' link is available
        """
        pass

    def test_004_tap_show_more_link(self):
        """
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: Timeform Summary Information is displayed
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push{
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'greyhounds',
        EXPECTED: 'eventAction' : 'race card',
        EXPECTED: 'eventLabel' : 'show more'
        EXPECTED: }
        """
        pass

    def test_006_go_to_selection_area_and_tap_on_it(self):
        """
        DESCRIPTION: Go to selection area and tap on it
        EXPECTED: * Timeform Selection Summary Information is expanded
        EXPECTED: * 'Show more' link is available if there are more than 100 characters in Timeform Selection Summary Information
        """
        pass

    def test_007_tap_show_more_link(self):
        """
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: Timeform Summary Information is displayed for particular selection
        """
        pass

    def test_008_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step #5
        EXPECTED: 
        """
        pass
