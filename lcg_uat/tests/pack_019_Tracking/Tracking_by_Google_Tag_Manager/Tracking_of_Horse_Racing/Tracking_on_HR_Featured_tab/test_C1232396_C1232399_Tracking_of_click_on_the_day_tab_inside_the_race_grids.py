import pytest
from dateutil import parser

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
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1232396_C1232399_Tracking_of_click_on_the_day_tab_inside_the_race_grids(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232396
    TR_ID: C1232399
    VOL_ID: C9698001
    NAME: Tracking of click on the day tab inside the race grids
    DESCRIPTION: This test case verifies GA tracking of day tabs click on the UK & IRE, International, Virtuals race grids
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Day tabs on the racing grids should be available. If there is only one tab, create additional tabs in TI:
    PRECONDITIONS: 1. Navigate to category Horse Racing (id =21) > class Horse Racing - Live
    PRECONDITIONS: 2. The type should have one of the following check boxes selected: UK, IRE, Is International or Virtual Racing in order to appear in  UK&IRE, International, Virtual grids
    PRECONDITIONS: 3. Open the event under the type and set a start time date matching the day of the week to display on a day tab
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def verify_tracking_of_collapse_expand(self, event_action, event_label, find_action=None):
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=event_label, eventAction=find_action)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': event_action,
                             'eventLabel': event_label
                             }
        self.compare_json_response(actual_response, expected_response)

    def verify_tracking_of_current_tab_according_to_section(self, event_action, event_label):
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='horse racing')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': event_action,
                             'eventLabel': 'select day - ' + parser.parse(event_label).strftime('%A')
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        today = self.get_date_time_formatted_string(hours=2)
        tomorrow = self.get_date_time_formatted_string(days=1)

        self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=today)
        self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=tomorrow)

        self.ob_config.add_international_racing_event(number_of_runners=1, start_time=today)
        self.ob_config.add_international_racing_event(number_of_runners=1, start_time=tomorrow)

        self.ob_config.add_virtual_racing_event(number_of_runners=1, start_time=today)
        self.ob_config.add_virtual_racing_event(number_of_runners=1, start_time=tomorrow)

    def test_001_navigate_to_horse_racing(self):
        """
        DESCRIPTION: Navigate to HR -> Featured tab
        """
        self.navigate_to_page(name='horse-racing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab "%s" is not the same as expected "%s"'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Can not find any sections')

    def test_002_scroll_till_the_uk_ire_race_grid_click_on_the_several_day_tabs(self):
        """
        DESCRIPTION: Scroll till the UK & IRE race grid. Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'UK & IRE',
        EXPECTED: 'eventLabel' : '<< DAY TAB >>'
        EXPECTED: })
        """
        self.__class__.section = self.sections.get(self.uk_and_ire_type_name)
        self.assertTrue(self.section, msg='Can not find section: "%s"' % self.uk_and_ire_type_name)
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(), msg='Section "%s" is expanded' % self.uk_and_ire_type_name)
        self.verify_tracking_of_collapse_expand(event_action=self.uk_and_ire_type_name, event_label='collapse', find_action=self.uk_and_ire_type_name)
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg='Section "%s" is not expanded' % self.uk_and_ire_type_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        current_date_tab_name, current_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[0]
        current_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='UK & IRE',
                                                                 event_label=current_date_tab_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        next_date_tab_name, next_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[1]
        next_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='UK & IRE',
                                                                 event_label=next_date_tab_name)

    def test_003_scroll_till_the_international_race_grid_click_on_the_several_day_tabs(self):
        """
        DESCRIPTION: Scroll till the International race grid. Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'Other International',
        EXPECTED: 'eventLabel' : '<< DAY TAB >>'
        EXPECTED: })
        """
        self.__class__.section = self.sections.get(self.international_type_name)
        self.assertTrue(self.section, msg='Can not find section: "%s"' % self.international_type_name)
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(), msg='Section "%s" is expanded' % self.international_type_name)
        section = 'Other International' if self.brand != 'ladbrokes' else 'International Races'
        self.verify_tracking_of_collapse_expand(event_action=section, event_label='collapse', find_action=section)
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg='Section "%s" is not expanded' % self.international_type_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        current_date_tab_name, current_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[0]
        current_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='Other International',
                                                                 event_label=current_date_tab_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        next_date_tab_name, next_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[1]
        next_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='Other International',
                                                                 event_label=next_date_tab_name)

    def test_004_scroll_till_the_virtual_race_grid_click_on_the_several_day_tabs(self):
        """
        DESCRIPTION: Scroll till the Virtual race grid. Click on the several day tabs one after another.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'Virtual',
        EXPECTED: 'eventLabel' : '<< DAY TAB >>'
        EXPECTED: })
        """
        self.__class__.section = self.sections.get(self.legends_type_name)
        self.assertTrue(self.section, msg='Can not find section: "%s"' % self.legends_type_name)
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(), msg='Section "%s" is expanded' % self.legends_type_name)
        section = 'Virtual' if self.brand != 'ladbrokes' else 'Virtual Races'
        self.verify_tracking_of_collapse_expand(event_action=section, event_label='collapse', find_action=section)
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg='Section "%s" is not expanded' % self.legends_type_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        current_date_tab_name, current_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[0]
        current_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='Virtual',
                                                                 event_label=current_date_tab_name)

        self.assertTrue(self.section.date_tab.items_as_ordered_dict.items(), msg='Can not find items in section')
        next_date_tab_name, next_date_tab = list(self.section.date_tab.items_as_ordered_dict.items())[1]
        next_date_tab.click()
        self.verify_tracking_of_current_tab_according_to_section(event_action='Virtual',
                                                                 event_label=next_date_tab_name)

    def test_005_navigate_to_the_different_page_and_come_back_to_horse_race_page_repeat_steps_1_3(self):
        """
        DESCRIPTION: Navigate to the different page and come back to Horse Race page.
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: A relevant event is created after collapsing each grid
        """
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')
        self.navigate_to_page(name='horse-racing')
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Can not find any sections')
        self.test_002_scroll_till_the_uk_ire_race_grid_click_on_the_several_day_tabs()
        self.test_003_scroll_till_the_international_race_grid_click_on_the_several_day_tabs()
        self.test_004_scroll_till_the_virtual_race_grid_click_on_the_several_day_tabs()
