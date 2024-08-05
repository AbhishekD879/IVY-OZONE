import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.mobile_only  # applicable for tablet as well
@vtest
class Test_C1232398_Tracking_of_Collapsing_Expanding_Extra_Places_module(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232398
    VOL_ID: C9698054
    NAME: Tracking of Collapsing/Expanding Extra Places module
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Collapse/Expand the Extra places Carousel module
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True
    enhanced_races_section = None
    expected_response = {'event': 'trackEvent',
                         'eventCategory': 'horse racing',
                         'eventAction': 'extra place',
                         'eventLabel': 'collapse',
                         }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event in OB TI
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True, ew_terms=self.ew_terms)

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: Horse Racing landing page is opened
        """
        self.navigate_to_page(name='horse-racing')

    def test_002_scroll_down_to_extra_places_module(self):
        """
        DESCRIPTION: Scroll down to 'Extra Places' module
        EXPECTED: 'Extra Places' module is shown as carousel
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.enhanced_races_name, sections,
                      msg=f'"{self.enhanced_races_name}" not found in "{list(sections.keys())}"')
        self.__class__.enhanced_races_section = sections[self.enhanced_races_name]
        self.assertTrue(self.enhanced_races_section.is_expanded(),
                        msg=f'"{self.enhanced_races_name}" section is not expanded by default')

    def test_003_collapse_the_extra_places_module(self):
        """
        DESCRIPTION: Collapse the 'Extra Places' module
        EXPECTED: Module is collapsed
        """
        self.enhanced_races_section.collapse()
        self.assertFalse(self.enhanced_races_section.is_expanded(),
                         msg=f'"{self.enhanced_races_name}" section is still expanded after collapsing')

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='extra place')
        self.compare_json_response(actual_response, self.expected_response)

    def test_005_expands_and_collapses_the_extra_place_module_one_more_time(self):
        """
        DESCRIPTION: Expands and collapses the Extra place module one more time
        EXPECTED: Module is collapsed
        """
        self.enhanced_races_section.expand()
        self.assertTrue(self.enhanced_races_section.is_expanded(),
                        msg=f'"{self.enhanced_races_name}": section is not expanded after expanding it')
        self.test_003_collapse_the_extra_places_module()

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event is **NOT** present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        objects_count = self.get_data_layer_objects_count(object_key='eventAction', object_value='extra place')
        self.assertEqual(objects_count, 1,
                         msg=f'Event "{self.expected_response}" should be present in datalayer once, '
                         f'but found "{objects_count}"')

    def test_007_leave_the_page_and_come_back_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Leave the page and come back to the 'Horse Racing' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state('HomePage', timeout=5)
        self.test_001_navigate_to_horse_racing_landing_page()

    def test_008_collapse_the_extra_places_module(self):
        """
        DESCRIPTION: Collapse the 'Extra Places' module
        EXPECTED: Module is collapsed
        """
        self.test_002_scroll_down_to_extra_places_module()
        self.test_003_collapse_the_extra_places_module()

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place',
        EXPECTED: 'eventLabel' : 'collapse'
        """
        objects_count = self.get_data_layer_objects_count(object_key='eventAction', object_value='extra place')
        self.assertEqual(objects_count, 1,
                         msg=f'Event "{self.expected_response}" should be present in datalayer once, '
                         f'but found "{objects_count}"')
