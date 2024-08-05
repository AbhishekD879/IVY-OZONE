import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.low
@pytest.mark.mobile_only
@vtest
class Test_C1234499_Tracking_of_Collapsing_Expanding_Enhanced_Multiples_module(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1234499
    VOL_ID: C9698062
    NAME: Tracking of Collapsing/Expanding Enhanced Multiples module
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Collapse/Expand the Enhanced multiples Carousel module
    PRECONDITIONS: 1. Test case should be run on Mobile
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True
    enhanced_multiples_name = vec.racing.ENHANCED_MULTIPLES_NAME
    enhanced_multiples_section = None
    expected_response = {'event': 'trackEvent',
                         'eventCategory': 'horse racing',
                         'eventAction': 'enhanced multiples',
                         'eventLabel': 'collapse',
                         }

    def test_001_create_racing_enhanced_multiples_event(self):
        """
        DESCRIPTION: Create racing enhanced multiples event
        """
        self.ob_config.add_enhanced_multiples_racing_event(number_of_runners=1)

    def test_002_navigate_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page(name='horse-racing')

    def test_003_scroll_down_to_enhanced_multiples_module(self):
        """
        DESCRIPTION: Scroll down to 'Enhanced multiples' module
        EXPECTED: 'Enhanced multiples' module is shown as carousel
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.enhanced_multiples_name, sections, msg=f'No "{self.enhanced_races_name}" in {list(sections.keys())}')
        self.__class__.enhanced_multiples_section = sections[self.enhanced_multiples_name]
        self.enhanced_multiples_section.scroll_to()

    def test_004_collapse_the_enhanced_multiples_module(self):
        """
        DESCRIPTION: Collapse the 'Enhanced multiples' module
        EXPECTED: Module is collapsed
        """
        self.enhanced_multiples_section.collapse()
        self.assertFalse(self.enhanced_multiples_section.is_expanded(),
                         msg=f'"{self.enhanced_multiples_name}" section is still expanded after collapsing')

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in Data Layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'})
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='enhanced multiples')
        self.compare_json_response(actual_response, self.expected_response)

    def test_006_expands_and_collapses_the_enhanced_multiples_module_one_more_time(self):
        """
        DESCRIPTION: Expands and collapses the 'Enhanced multiples' module one more time
        EXPECTED: Module is collapsed
        """
        self.enhanced_multiples_section.expand()
        self.assertTrue(self.enhanced_multiples_section.is_expanded(),
                        msg=f'"{self.enhanced_multiples_name}" section is not expanded after expanding it')
        self.test_004_collapse_the_enhanced_multiples_module()

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event is **NOT** present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'})
        """
        objects_count = self.get_data_layer_objects_count(object_key='eventAction', object_value='enhanced multiples')
        self.assertEqual(objects_count, 1,
                         msg=f'Event "{self.expected_response}" should be present in datalayer once, '
                         f'but found "{objects_count}"')

    def test_008_leave_the_page_and_come_back_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Leave the page and come back to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state('HomePage', timeout=5)
        self.test_002_navigate_to_the_horse_racing_page()

    def test_009_collapse_the_enhanced_multiples_module(self):
        """
        DESCRIPTION: Collapse the 'Enhanced multiples' module
        EXPECTED: Module is collapsed
        """
        self.test_003_scroll_down_to_enhanced_multiples_module()
        self.test_004_collapse_the_enhanced_multiples_module()

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'enhanced multiples',
        EXPECTED: 'eventLabel' : 'collapse'})
        """
        objects_count = self.get_data_layer_objects_count(object_key='eventAction', object_value='enhanced multiples')
        self.assertEqual(objects_count, 1,
                         msg=f'Event "{self.expected_response}" should be present in datalayer once, '
                         f'but found "{objects_count}"')
