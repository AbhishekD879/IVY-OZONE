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
class Test_C1200218_Tracking_of_Racing_Post_Spotlight(Common):
    """
    TR_ID: C1200218
    NAME: Tracking of Racing Post 'Spotlight'
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of click on 'Show more' link in Racing Post 'Spotlight'
    PRECONDITIONS: 1. Test case should be run on Mobile
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_navigate_to_the_event_details_page_where_horse_additional_info_is_present_silks_number_etc(self):
        """
        DESCRIPTION: Navigate to the event details page where horse additional info is present (silks, number, etc)
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_click_on_the_show_more_link_to_expend_racing_post_spotlight(self):
        """
        DESCRIPTION: Click on the 'Show More' link to expend Racing Post 'Spotlight'
        EXPECTED: Racing Post 'Spotlight' is shown expanded
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'race card',
        EXPECTED: 'eventLabel' : 'details'
        EXPECTED: })
        """
        pass

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Logged In user
        EXPECTED: 
        """
        pass
