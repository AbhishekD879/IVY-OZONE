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
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.low
@pytest.mark.mobile_only  # applicable for tablet as well
@vtest
class Test_C1232397_Tracking_of_click_on_Extra_Places_card(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232397
    VOL_ID: C9697920
    NAME: Tracking of click on Extra Places card
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of click on 'Extra Places' card on the Extra places Carousel module
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True
    event = None
    expected_response = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event in OB TI
        """
        params = self.ob_config.add_UK_racing_event(market_extra_place_race=True, ew_terms=self.ew_terms, number_of_runners=1, featured_racing_types=True)
        self.__class__.event_off_time = params.event_off_time
        self.__class__.created_event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}' \
            if self.brand != 'ladbrokes' else f'{self.event_off_time} Auto'

        self.__class__.expected_response = {'event': 'trackEvent',
                                            'eventCategory': 'horse racing',
                                            'eventAction': 'extra place',
                                            'eventLabel': f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}'}

    def test_001_navigate_to_the_horse_race_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Race' page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page(name='horse-racing')

    def test_002_scroll_down_to_extra_places_module(self):
        """
        DESCRIPTION: Scroll down to 'Extra Places' module
        EXPECTED: 'Extra Places' module is shown as carousel
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.enhanced_races_name, sections, msg=f'No "{self.enhanced_races_name}" in "{sections.keys()}"')
        enhanced_races_section = sections[self.enhanced_races_name].extra_place_offer_module
        events = enhanced_races_section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.enhanced_races_name}" section')
        self.assertIn(self.created_event_name, events, msg=f'No "{self.created_event_name}" in "{events.keys()}"')
        self.__class__.event = events[self.created_event_name]

    def test_003_click_on_extra_place_card(self):
        """
        DESCRIPTION: Click on Extra place card
        EXPECTED: User is redirected to the event details page
        """
        self.event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='extra place')
        self.compare_json_response(actual_response, self.expected_response)
