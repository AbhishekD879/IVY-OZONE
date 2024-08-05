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
class Test_C1232397_Tracking_of_click_on_Extra_Places_card(Common):
    """
    TR_ID: C1232397
    NAME: Tracking of click on Extra Places card
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of click on 'Extra Places' card on the Extra places Carousel module
    DESCRIPTION: AUTOTEST [C1232397]
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_the_horse_race_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Race' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_scroll_down_to_extra_places_module(self):
        """
        DESCRIPTION: Scroll down to 'Extra Places' module
        EXPECTED: 'Extra Places' module is shown as carousel
        """
        pass

    def test_004_click_on_extra_place_card(self):
        """
        DESCRIPTION: Click on Extra place card
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        """
        pass

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Logged In user
        EXPECTED: 
        """
        pass
