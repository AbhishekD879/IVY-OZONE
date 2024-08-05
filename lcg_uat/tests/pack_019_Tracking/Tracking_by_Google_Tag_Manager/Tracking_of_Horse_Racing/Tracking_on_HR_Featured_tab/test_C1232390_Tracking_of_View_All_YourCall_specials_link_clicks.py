import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod # yourcall no in the scope of roxane release
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1232390_Tracking_of_View_All_YourCall_specials_link_clicks(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232390
    VOL_ID: C1747540
    NAME: Tracking of View All YourCall specials link clicks
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers.
    PRECONDITIONS: Browser console should be opened.
    """
    prices = {0: '1/4', 1: '1/2', 2: '2/3', 3: '1/3', 4: '3/2'}
    keep_browser_open = True

    def test_000_create_event_in_backoffice(self):
        """
        DESCRIPTION: Create Horse Racing Your Call Specials event
        EXPECTED: Event is created
        """
        self.ob_config.add_racing_your_call_specials_event(number_of_runners=4, lp_prices=self.prices)

    def test_001_navigate_to_hr_featured_tab_your_call_specials_widget(self):
        """
        DESCRIPTION: Navigate to Horse Racing tab.
        EXPECTED: YourCall Specials accordion is named "YOURCALL SPECIALS"
        """
        self.navigate_to_page(name='horse-racing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab {current_tab} is not the same as expected {vec.racing.RACING_DEFAULT_TAB_NAME}')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any sections')
        self.__class__.yc_specials_section = sections.get(self.yc_specials_type_name)
        self.assertTrue(self.yc_specials_section, msg='Widget: "%s" was not found in list of widgets: "%s"' %
                                                      (self.yc_specials_type_name, sections))

    def test_002_on_horse_racing_landing_page_scroll_to_yourcall_specials_module_click_on_view_all_yourcall_specials_link(self):
        """
        DESCRIPTION: On Horse Racing landing page scroll to YourCall Specials module
        DESCRIPTION: Click on “View All YourCall specials” link.
        """
        self.yc_specials_section.view_all_link.click()

    def test_003_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'your call',
        EXPECTED: 'eventLabel' : 'more your call specials'
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='your call')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': 'your call',
                             'eventLabel': 'more your call specials'
                             }
        self.compare_json_response(actual_response, expected_response)
