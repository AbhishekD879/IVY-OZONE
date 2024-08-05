import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # coral only, ladbrokes uses Datafabric instead of Timeform
@pytest.mark.crl_stg2
# @pytest.mark.crl_hl
# @pytest.mark.crl_prod
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1159080_Tracking_of_Timeform_Summary_Information_opening(BaseGreyhound, BaseDataLayerTest):
    """
    TR_ID: C1159080
    VOL_ID: C9697736
    NAME: Tracking of Timeform Summary Information opening
    DESCRIPTION: This test case verifies tracking of Timeform Summary Information opening on Greyhounds event details page
    """
    keep_browser_open = True

    def test_001_get_greyhound_event_with_timeform_data(self):
        """
        DESCRIPTION: Get greyhound event with timeform data
        EXPECTED: Event id is found
        """
        racing_data_hub_config = self.get_initial_data_system_configuration().get('RacingDataHub', {})
        if not racing_data_hub_config:
            racing_data_hub_config = self.cms_config.get_system_configuration_item('RacingDataHub')
        if racing_data_hub_config.get('isEnabledForGreyhound') is True:
            raise CmsClientException('Datafabric data is enabled in CMS for Greyhounds. '
                                     'Time Form will not be available.')

        params = self.get_event_details(time_form_info=True)
        self.navigate_to_edp(event_id=params.event_id, sport_name='greyhound-racing')

    def test_002_tap_show_more_link(self):
        """
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: Timeform Summary Information is displayed
        """
        timeform_overview = self.site.greyhound_event_details.tab_content.timeform_overview
        timeform_overview.show_summary_button.click()
        summary = timeform_overview.summary_text
        self.assertTrue(summary.value, msg='No Timeform summary found')

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
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
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='race card')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'greyhounds',
                             'eventAction': 'race card',
                             'eventLabel': 'show more'}
        self.compare_json_response(actual_response, expected_response)

    def test_004_go_to_selection_area_and_tap_on_it(self):
        """
        DESCRIPTION: Go to selection area and tap on it
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: * Timeform Selection Summary Information is expanded
        EXPECTED: Timeform Selection Summary Information is expanded
        EXPECTED: 'Show more' link is available if there are more than 100 characters in Timeform Selection Summary Information
        """
        pass
        # cannot test as we never got Timeform Selection Summary Information with more than 100 symbols

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push{
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'greyhounds',
        EXPECTED: 'eventAction' : 'race card',
        EXPECTED: 'eventLabel' : 'show more'
        EXPECTED: }
        """
        pass
        # cannot test as we never got Timeform Selection Summary Information with more than 100 symbols
