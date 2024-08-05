import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.user_journey_single_horse_race
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.low
@pytest.mark.next_races
@pytest.mark.races
@vtest
class Test_C1049081_Verify_Navigation_to_the_Event_Details_Page(BaseRacing):
    """
    TR_ID: C1049081
    VOL_ID: C9698386
    NAME: Verify Navigation to the Event Details Page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events in TI
        """
        # This cms switcher added to display all events, not only with LP prices
        self.cms_config.next_races_price_switcher(show_priced_only=False)
        self.setup_cms_next_races_number_of_events()
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesComponentEnabled'):
            self._logger.warning('*** "NextRacesToggle -> nextRacesComponentEnabled" component is disabled. Needs to be enabled')
            self.cms_config.set_next_races_toggle_component_status(next_races_component_status=True)

        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        params_5min = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=5)
        self.__class__.event_name_5min = f'{params_5min.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_off_time_5min = params_5min.event_off_time

        params_20min = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=20)
        self.__class__.event_name_20min = f'{params_20min.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_off_time_20min = params_20min.event_off_time

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=2)
        start_time_tomorrow2 = self.get_date_time_formatted_string(days=1, hours=3)

        params_t = self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=start_time_tomorrow)
        self.__class__.event_name_tomorrow = f'{params_t.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_off_time_tomorrow = params_t.event_off_time

        params_t2 = self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=start_time_tomorrow2)
        self.__class__.event_name_tomorrow2 = f'{params_t2.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_off_time_tomorrow2 = params_t2.event_off_time

        self.__class__.meeting_name = self.horseracing_autotest_uk_name_pattern if self.brand == 'ladbrokes' else self.horseracing_autotest_uk_name_pattern.upper()

    def test_001_tap_on_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: * 'Horse Racing' landing page is opened.
        EXPECTED: * Featured tab is opened by default
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_002_go_to_the_event_details_page_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the Event details page by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=self.meeting_name,
                                       event_off_time=self.event_off_time_5min)

        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name_5min,
                         msg=f'Current event name: "{event_title}" '
                             f'does not match with expected: "{self.event_name_5min}"')

    def test_003_go_to_the_event_details_page_from_the_next_4_module_by_tapping_view_full_race_card_link(self):
        """
        DESCRIPTION: Go to the event details page from the 'Next 4' module by tapping 'View Full race Card' link
        EXPECTED: Event details page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        expected_next_races_name = self.next_races_title

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        next_races = sections.get(expected_next_races_name)
        self.assertTrue(next_races, msg=f'There is no "{expected_next_races_name}" section')

        events = next_races.items_as_ordered_dict
        self.assertIn(self.event_name_5min.upper(), events.keys(),
                      msg=f'Event {self.event_name_5min.upper()} was not found '
                          f'in {expected_next_races_name} section events {events.keys()}')

        autotest_event = events[self.event_name_5min.upper()]
        autotest_event.click()

        self.site.wait_content_state(state_name='RacingEventDetails')

        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name_5min,
                         msg=f'Current event name: "{event_title}" '
                             f'does not match with expected: "{self.event_name_5min}"')

    def test_004_on_event_details_page_tap_another_event_off_time(self):
        """
        DESCRIPTION: On event details page tap another event off time
        EXPECTED: Event details page for other event is opened
        """
        self.site.racing_event_details.tab_content.event_off_times_list.select_off_time(
            off_time=self.event_off_time_20min)

        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name_20min,
                         msg=f'Current event name: "{event_title}" '
                             f'does not match with expected: "{self.event_name_20min}"')

    def test_005_go_back_to_landing_page__scroll_down_to_race_grid_accordions_where_day_switchers_available(self):
        """
        DESCRIPTION: Go back to landing page > scroll down to Race Grid accordions where Day switchers available
        EXPECTED: Day switcher name is day of the week
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        uk_ire = sections.get(self.uk_and_ire_type_name)
        self.assertTrue(uk_ire, msg=f'There is no "{self.uk_and_ire_type_name}" section')

        uk_ire.expand()
        date_tabs = uk_ire.date_tab.items_as_ordered_dict
        self.assertTrue(date_tabs, msg=f'Date tabs are not found')

        for date_tab_name, _ in date_tabs.items():
            self.assertIn(date_tab_name.upper(), vec.racing.DAYS,
                          msg=f'Day tab header "{date_tab_name}" is not in {vec.racing.DAYS}')

        date_tab_name, date_tab = list(date_tabs.items())[1]
        date_tab.click()

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        uk_ire = sections.get(self.uk_and_ire_type_name)
        self.assertTrue(uk_ire, msg=f'There is no "{self.uk_and_ire_type_name}" section')

        uk_ire.expand()
        meetings = uk_ire.items_as_ordered_dict
        horse_event_name = self.horseracing_autotest_uk_name_pattern if self.brand == 'ladbrokes' else self.horseracing_autotest_uk_name_pattern.upper()
        self.assertIn(horse_event_name, meetings.keys(),
                      msg=f'{horse_event_name} meeting is not found found on "{date_tab_name.upper()}"'
                      f'tab in the list of "{meetings.keys()}"')

        autotest_meeting = meetings.get(horse_event_name)

        events = autotest_meeting.items_as_ordered_dict
        self.assertIn(self.event_off_time_tomorrow, events,
                      msg=f'Event "{self.event_off_time_tomorrow}" was not found in "{events}"')
        event = events.get(self.event_off_time_tomorrow)
        event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')

        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name_tomorrow,
                         msg=f'Current event name: "{event_title}" '
                             f'does not match with expected: "{self.event_name_tomorrow}"')

    def test_006_go_to_the_event_details_page_from_next_day_switcher_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the Event details page from next Day switcher by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        self.site.racing_event_details.tab_content.event_off_times_list.select_off_time(
            off_time=self.event_off_time_tomorrow2)

        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name_tomorrow2,
                         msg=f'Current event name: "{event_title}" '
                             f'does not match with expected: "{self.event_name_tomorrow2}"')
