import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod # yourcall no in the scope of roxane release
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.cms
@pytest.mark.your_call
@pytest.mark.low
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.low
@vtest
class Test_C1232389_Tracking_of_Tweet_Now_button_clicks(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232389
    VOL_ID: C9690274
    NAME: Tracking of “Tweet Now” button clicks
    DESCRIPTION: This test case verifies GA tracking of “Tweet Now” button clicks.
    PRECONDITIONS: YourCall page is opened. (HR Landing page> YourCall tab)
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check Static Block parameters presence in= CMS
        """
        static_block_params = self.cms_config.get_your_call_static_block()
        yc_racing_block = next((block for block in static_block_params if block['title'] == 'yourcall-racing'), None)
        if not yc_racing_block:
            raise CmsClientException('Your Call racing block is not present')
        if not yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured')
        if 'twitter' not in yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured to show twitter button')

    def test_001_navigate_on_the_horse_racing_tab(self):
        """
        DESCRIPTION: Navigate on the Horse racing tab
        EXPECTED: When the page is loaded YOURCALL tab is present
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')
        self.site.horse_racing.tabs_menu.click_button('YOURCALL')

    def test_002_click_on_the_yourcall_tab(self):
        """
        DESCRIPTION: Click on the YOURCALL tab
        EXPECTED: The tab is shown as per design:
        EXPECTED: * configurable (on CMS) static text ('#YourCall' is highlighted with different color)
        EXPECTED: * "TWEET NOW" button
        EXPECTED: https://mobile.twitter.com/Coral (configured on CMS)
        """
        selected_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, 'YOURCALL',
                         msg='Selected tab is "%s" instead of "YOURCALL" tab' % selected_tab)
        static_block = self.site.horse_racing.tab_content.accordions_list.static_block
        self.assertTrue(static_block, msg='Can not find Static Block')
        static_block.tweet_now_button.click()

    def test_003_on_the_oxygen_browser_tab_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: On the Oxygen browser tab type in browser console "dataLayer" and press "Enter".
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'tweet now',
        EXPECTED: 'eventLabel' : 'horse racing'
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='horse racing')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': 'tweet now',
                             'eventLabel': 'horse racing',
                             }
        self.compare_json_response(actual_response, expected_response)
