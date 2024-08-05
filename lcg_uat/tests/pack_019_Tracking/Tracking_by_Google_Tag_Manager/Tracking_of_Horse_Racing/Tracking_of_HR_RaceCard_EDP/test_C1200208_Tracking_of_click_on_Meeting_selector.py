import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C1200208_Tracking_of_click_on_Meeting_selector(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1200208
    NAME: Tracking of click on Meeting selector
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of 'click on Meeting' selector
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event in OB TI
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2)
        self._logger.info(f'*** Created Horse racing event with params {event_params}')
        self.__class__.eventID = event_params.event_id

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_click_on_meetings_selector(self):
        """
        DESCRIPTION: Click on 'Meetings' selector
        EXPECTED: 'Meetings' drop down is shown
        """
        meeting_selector = self.site.racing_event_details.meeting_selector
        self.assertTrue(meeting_selector, msg='Race meeting selector not displayed')
        meeting_selector.click()
        meetings_list = self.site.racing_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(meetings_list, msg='Can not find meeting list in dropdown')

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'race card',
        EXPECTED: 'eventLabel' : 'meetings'
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='meetings')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': 'race card',
                             'eventLabel': 'meetings',
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_004_repeat_steps_1_3_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps for Logged In user
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.login()
        self.test_001_go_to_the_event_details_page()
        self.test_002_click_on_meetings_selector()
        self.test_003_type_in_browser_console_datalayer_and_tap_enter()
