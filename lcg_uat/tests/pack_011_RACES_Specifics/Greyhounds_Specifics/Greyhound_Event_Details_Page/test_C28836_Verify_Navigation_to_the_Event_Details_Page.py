import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.low
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28836_Verify_Navigation_to_the_Event_Details_Page(BaseGreyhound):
    """
    TR_ID: C28836
    VOL_ID: C9697938
    NAME: Verify Navigation to the Event Details Page
    """
    keep_browser_open = True

    @classmethod
    def custom_setUp(cls):
        if tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            cls.get_ss_config()
            cls.suspend_old_events(class_ids=ob_config.backend.ti.greyhound_racing.class_ids)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        if self.brand == 'ladbrokes':
            self.__class__.today = vec.sb.TABS_NAME_TODAY
            self.__class__.tomorrow = vec.sb.TABS_NAME_TOMORROW
            self.__class__.meeting_name = self.greyhound_autotest_name_pattern if self.device_type == 'mobile' \
                else self.greyhound_autotest_name_pattern.upper()
        else:
            self.__class__.today = vec.sb.SPORT_DAY_TABS.today
            self.__class__.tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
            self.__class__.meeting_name = self.greyhound_autotest_name_pattern.upper()

        params_5min = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, time_to_start=5)
        self.__class__.event_name_5min = f'{params_5min.event_off_time} {self.greyhound_autotest_name_pattern}'
        self.__class__.event_off_time_5min = params_5min.event_off_time

        params_20min = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, time_to_start=20)
        self.__class__.event_name_20min = f'{params_20min.event_off_time} {self.greyhound_autotest_name_pattern}'
        self.__class__.event_off_time_20min = params_20min.event_off_time

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=2)
        start_time_tomorrow2 = self.get_date_time_formatted_string(days=1, hours=3)

        params_t = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time_tomorrow)
        self.__class__.event_name_tomorrow = f'{params_t.event_off_time} {self.greyhound_autotest_name_pattern}'
        self.__class__.event_off_time_tomorrow = params_t.event_off_time

        params_t2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time_tomorrow2)
        self.__class__.event_name_tomorrow2 = f'{params_t2.event_off_time} {self.greyhound_autotest_name_pattern}'
        self.__class__.event_off_time_tomorrow2 = params_t2.event_off_time

    def test_001_tap_greyhound_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' the landing page is opened
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_002_select_today_tab_by_meeting_sorting_type(self, tab=None):
        """
        DESCRIPTION: Select 'Today' tab, 'By Meeting' sorting type
        EXPECTED: 'Today' tab is selected
        """
        tab = self.today if not tab else tab

        self.site.greyhound.tabs_menu.click_button(tab)

        self.assertEqual(self.site.greyhound.tabs_menu.current, tab,
                         msg=f'Opened grouping button "{self.site.greyhound.tabs_menu.current}" '
                         f'is not the same as expected "{tab}"')

        if self.brand != 'ladbrokes' and self.device_type == 'desktop':
            self.site.greyhound.tab_content.grouping_buttons.click_button(vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING)
            self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                             vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING,
                             msg=f'Opened tab "{self.site.greyhound.tab_content.current}" is not '
                             f'the same as expected "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_003_go_to_event_details_page_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the event details page by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=self.meeting_name,
                                       event_off_time=self.event_off_time_5min,
                                       page_name='greyhound-racing')

    def test_004_on_event_details_page_tap_another_event_off_time(self):
        """
        DESCRIPTION: On event details page tap another event off time
        EXPECTED: Event details page for other event is opened
        """
        self.site.greyhound_event_details.tab_content.event_off_times_list.select_off_time(
            off_time=self.event_off_time_20min)
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_005_select_today_tab_by_time_sorting_type(self, tab=None):
        """
        DESCRIPTION: Select 'Today' tab, 'By Time' sorting type
        EXPECTED: 'By Time' sorting type is selected
        """
        tab = self.today if not tab else tab

        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

        self.site.greyhound.tabs_menu.click_button(tab)

        self.assertEqual(self.site.greyhound.tabs_menu.current, tab,
                         msg=f'Opened grouping button "{self.site.greyhound.tabs_menu.current}" '
                         f'is not the same as expected "{tab}"')

        self.site.greyhound.tab_content.grouping_buttons.click_button(vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1])
        self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                         vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1],
                         msg=f'Opened grouping button "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                         f'is not the same as expected "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1]}"')

    def test_006_go_to_event_details_page_by_tapping_event_name(self):
        """
        DESCRIPTION: Go to the event details page by tapping event name
        EXPECTED: Event details page is opened
        """
        if self.brand == 'ladbrokes':
            self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                           meeting_name=self.meeting_name,
                                           event_off_time=self.event_off_time_5min,
                                           page_name='greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            section_name = vec.sb.EVENTS.upper() if self.device_type == 'mobile' else vec.sb.EVENTS
            self.assertIn(section_name, sections,
                          msg=f'"{section_name}" section was not found in "{sections}"')

            events_section = sections.get(section_name)
            events = events_section.items_as_ordered_dict
            while self.event_name_5min not in events:
                self.assertTrue(events_section.has_show_more_button(),
                                msg=f'Event "{self.event_name_5min}" is not found and there is no "Show More" button')
                events_section.show_more_button.click()
                events = events_section.items_as_ordered_dict

            self.assertIn(self.event_name_5min, events,
                          msg=f'Event "{self.event_name_5min}" is not in "{events.keys()}"')

            event = events.get(self.event_name_5min)
            event.click()
            self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_007_verify_steps_3_7_for_tomorrow_tab(self):
        """
        DESCRIPTION: Verify steps # 3 - 7 for 'Tomorrow' tab
        EXPECTED: Step #5 should be skipped for 'Tomorrow' tab
        """
        self.test_001_tap_greyhound_icon_from_the_sports_menu_ribbon()
        self.test_002_select_today_tab_by_meeting_sorting_type(tab=self.tomorrow)

        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=self.meeting_name,
                                       event_off_time=self.event_off_time_tomorrow,
                                       page_name='greyhound-racing')
        self.site.greyhound_event_details.tab_content.event_off_times_list.select_off_time(
            off_time=self.event_off_time_tomorrow2)
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

        self.test_005_select_today_tab_by_time_sorting_type(tab=self.tomorrow)

        if self.brand == 'ladbrokes':
            self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                           meeting_name=self.meeting_name,
                                           event_off_time=self.event_off_time_tomorrow,
                                           page_name='greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            section_name = vec.sb.EVENTS.upper() if self.device_type == 'mobile' else vec.sb.EVENTS
            self.assertIn(section_name, sections, msg=f'"{section_name}" section was not found in "{sections}"')

            events_section = sections.get(section_name)
            events = events_section.items_as_ordered_dict
            self.assertIn(self.event_name_tomorrow, events,
                          msg=f'Event "{self.event_off_time_tomorrow}" is not in "{events.keys()}"')

            event = events.get(self.event_name_tomorrow)
            event.click()
            self.site.wait_content_state(state_name='GreyHoundEventDetails')
