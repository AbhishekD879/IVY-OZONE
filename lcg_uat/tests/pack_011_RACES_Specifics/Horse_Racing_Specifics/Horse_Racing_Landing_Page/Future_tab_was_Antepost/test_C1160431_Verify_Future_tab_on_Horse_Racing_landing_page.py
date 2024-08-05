from collections import OrderedDict
from datetime import datetime
from typing import List

import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string, strftime_add_day_suffix
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from dateutil.parser import parse

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.racing_antepost
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.medium
@vtest
class Test_C1160431_Verify_Future_tab_on_Horse_Racing_landing_page(BaseRacing):
    """
    TR_ID: C1160431
    NAME: Verify Future tab on Horse Racing landing page
    DESCRIPTION: This test case verifies Future tab on Horse Racing landing page
    PRECONDITIONS: 1) In order to create HR Future event use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: - 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: 2) For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    """
    keep_browser_open = True
    event_times = None

    def format_date_to_ui_correspondence(self, event_date_time):
        date_time_obj = parse(event_date_time)
        time_format = '%d-%m-%Y | %H:%M' if self.brand != 'ladbrokes' else '%A %d %B %Y - %H:%M'
        formatted_date = get_date_time_as_string(time_format=time_format, date_time_obj=date_time_obj)
        self._logger.info(f'*** Got formatted date "{formatted_date}" from "{event_date_time}"')
        return formatted_date

    def sort_event_dates_by_ascending(self, event_dates):
        events_datetime = [parse(event.replace('|', ''), dayfirst=True) for event in event_dates]
        events_datetime.sort()
        if self.brand == 'ladbrokes' and self.device_type != 'desktop':
            event_dates = [get_date_time_as_string(time_format='%A %d %B %Y - %H:%M', date_time_obj=event) for event in events_datetime]
            sorted_events = [strftime_add_day_suffix(datetime_string=event,
                                                     format_pattern='%A %d %B %Y - %H:%M') for event in event_dates]
            sorted_events = self.remove_first_zero(sorted_events)
        else:
            sorted_events = [get_date_time_as_string(time_format='%d-%m-%Y | %H:%M', date_time_obj=event) for event
                             in events_datetime]
        return sorted_events

    def remove_first_zero(self, event_dates: List[str]):
        """
        Method verifies and removes first '0' for dates like '05th'.
            Example:
                - 'Saturday 05th October 2019 - 14:07' => 'Saturday 5th October 2019 - 14:07'
        :param event_dates: List with event dates
        :return: List with dates without '0' for days
        """
        result = []
        for date in event_dates:
            sub_dates = date.split(' ')
            number = sub_dates[1]
            if number.startswith('0'):
                number = number[1:]
            sub_dates[1] = number
            final_date = ' '.join(sub_dates)
            result.append(final_date)
        return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create antepost events (which are expected to be displayed on Future tab on HR EDP).
        """
        self.__class__.event_times = zip(vec.racing.RACING_ANTEPOST_SWITCHERS,
                                         [self.format_date_to_ui_correspondence(
                                             self.ob_config.add_UK_racing_event(number_of_runners=1, is_flat=True,
                                                                                start_time=self.get_date_time_formatted_string(
                                                                                    days=2)).event_date_time),
                                             self.format_date_to_ui_correspondence(
                                                 self.ob_config.add_UK_racing_event(number_of_runners=1, is_flat=True,
                                                                                    start_time=self.get_date_time_formatted_string(
                                                                                        days=2)).event_date_time),
                                          self.format_date_to_ui_correspondence(
                                              self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                                                 is_national_hunt=True,
                                                                                 start_time=self.get_date_time_formatted_string(
                                                                                     days=2)).event_date_time),
                                          self.format_date_to_ui_correspondence(
                                              self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                                                 is_international=True,
                                                                                 start_time=self.get_date_time_formatted_string(
                                                                                     days=2)).event_date_time)])

        self.ob_config.add_international_racing_event(number_of_runners=1, is_flat=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))
        self.ob_config.add_international_racing_event(number_of_runners=1, is_national_hunt=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))
        self.ob_config.add_international_racing_event(number_of_runners=1, is_international=True,
                                                      start_time=self.get_date_time_formatted_string(days=2))

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: Horse Racing landing page is opened
        EXPECTED: 'Featured' tab is opened by default
        EXPECTED: 'Future' tab is available and located right after 'Featured' tab
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tabs found on Horse racing page')
        tab_names = list(tabs.keys())
        self.assertIn(vec.racing.RACING_FUTURE_TAB_NAME, tab_names,
                      msg=f'Tab "{vec.racing.RACING_FUTURE_TAB_NAME} "should be displayed in tabs list "{tab_names}"')

        if self.brand != 'ladbrokes':
            self.assertTrue(tab_names.index(vec.racing.RACING_DEFAULT_TAB_NAME) + 1 == tab_names.index(vec.racing.RACING_FUTURE_TAB_NAME),
                            msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not located right after "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_002_tap_on_future_tab(self):
        """
        DESCRIPTION: Tap on 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: Switchers are displayed: 'Flat Races', 'National Hunt' and 'International'
        EXPECTED: If no events are available: "No events found" text is shown
        """
        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_FUTURE_TAB_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not selected after click')
        switchers = self.site.horse_racing.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(switchers, msg='No switchers present on page')
        self.assertListEqual(list(switchers.keys()), vec.racing.RACING_ANTEPOST_SWITCHERS)

    def test_003_navigate_between_available_switchers_eg_flat_races_national_hunt_international(self):
        """
        DESCRIPTION: Navigate between available switchers (e.g 'Flat Races', 'National Hunt', 'International')
        EXPECTED: - Corresponding events (that meet Preconditions are available) are displayed within one of the switchers (e.g 'Flat Races', 'National Hunt', 'International')
        EXPECTED: Events are grouped by 'Type'
        EXPECTED: Accordions are ordered by 'dispTypeOrder' (from SS)
        EXPECTED: Title of each accordion corresponds to 'typeName' from SS response
        EXPECTED: First accordion is expanded by default, other ones are collapsed
        EXPECTED: All accordions are collapsed/expanded once tapped
        """
        start_date = f'{get_date_time_as_string(days=2)}'
        query = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, self.ob_config.backend.ti.horse_racing.category_id)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                      OPERATORS.INTERSECTS, 'EVFLAG_FT,EVFLAG_IT,EVFLAG_NH')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.CONTAINS, 'EVFLAG_AP'))
        events = self.ss_req.ss_event_to_outcome_for_class(query_builder=query)

        events.sort(key=lambda x: int(x['event']['typeDisplayOrder']))

        national_hunt_types = list(OrderedDict.fromkeys([event['event']['typeName'].upper() for event in events
                                                         if 'EVFLAG_NH' in event['event']['drilldownTagNames']]))
        flat_types = list(OrderedDict.fromkeys([event['event']['typeName'].upper() for event in events
                                                if 'EVFLAG_FT' in event['event']['drilldownTagNames']]))
        international_types = list(OrderedDict.fromkeys([event['event']['typeName'].upper() for event in events
                                                         if 'EVFLAG_IT' in event['event']['drilldownTagNames']]))
        expected_types = {'FLAT': flat_types, 'NATIONAL HUNT': national_hunt_types, 'INTERNATIONAL': international_types}
        grouping_buttons = self.site.horse_racing.tab_content.grouping_buttons
        for switcher_name in vec.racing.RACING_ANTEPOST_SWITCHERS:
            self._logger.debug(f'*** Verifying "{switcher_name}"')
            is_switcher_tab_opened = grouping_buttons.click_button(button_name=switcher_name)
            self.assertTrue(is_switcher_tab_opened, msg=f'"{switcher_name}" switcher tab is not opened')

            type_sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(type_sections, msg='No type sections are present')

            self.assertListEqual(list(type_sections.keys()), expected_types.get(switcher_name),
                                 msg=f'Actual sections titles \n"{list(type_sections.keys())}"  are not the same as '
                                 f'expected \n"{expected_types.get(switcher_name)}"')

            first_section_name, first_section = list(type_sections.items())[0]
            self.assertTrue(first_section.is_expanded(),
                            msg=f'First section "{first_section_name}" is not expanded by default')
            [self.assertFalse(section.is_expanded(expected_result=False),
                              msg=f'Section "{section.name}" is not collapsed by default')
             for section_name, section in list(type_sections.items())[1:]]

            for section_name, section in type_sections.items():
                section.collapse()
                self.assertFalse(section.is_expanded(expected_result=False),
                                 msg=f'"{section_name}" is not collapsed after click')

                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded after click')

    def test_004_verify_events_within_a_type_accordion(self):
        """
        DESCRIPTION: Verify events within a 'Type' accordion
        EXPECTED: - Events within the same 'Type' accordion are ordered by 'startTime' in asc order
        EXPECTED: - Each event contains:
        EXPECTED: *** DD-MM-YYYY|HH:MM (corresponds to 'startDate' in SS response)
        EXPECTED: *** 'typeName' from SS response e.g. ASCOT
        EXPECTED: *** Event 'name' (corresponds to 'name' of the event in SS response)
        EXPECTED: - Each event area is clickable
        EXPECTED: On tablet:
        EXPECTED: - Events are displayed in two columns within an accordion
        EXPECTED: On desktop:
        EXPECTED: - Events are displayed in three columns within an accordion
        """
        horseracing_autotest_uk_name_pattern = self.horseracing_autotest_uk_name_pattern.upper()
        horseracing_autotest_uk_name_pattern_event = self.horseracing_autotest_uk_name_pattern.upper() if self.brand != 'ladbrokes' \
            else self.horseracing_autotest_uk_name_pattern
        type_sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(type_sections, msg='No type sections are present')
        for switcher, event_date in self.event_times:
            self.site.horse_racing.tab_content.grouping_buttons.click_button(button_name=switcher)

            type_sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(type_sections, msg='No type sections are present')
            section = type_sections.get(horseracing_autotest_uk_name_pattern)
            self.assertTrue(section, msg=f'Cannot found "{horseracing_autotest_uk_name_pattern}" section in "{type_sections.keys()}"')
            section.expand()
            events = section.items_as_ordered_dict
            self.assertTrue(events,
                            msg=f'No event found for "{horseracing_autotest_uk_name_pattern}" section in "{switcher}" tab')

            event_pattern = self.horseracing_autotest_uk_name_pattern if self.device_type == 'desktop' else horseracing_autotest_uk_name_pattern

            event_dates = [event.replace(event_pattern, '').strip() for event in events]
            sorted_dates = self.sort_event_dates_by_ascending(event_dates=event_dates)
            self.assertListEqual(event_dates, sorted_dates,
                                 msg=f'Events on UI \n[{", ".join(event_dates)}] \nare not ordered by "startTime" '
                                 f'in asc order \n[{", ".join(sorted_dates)}]')

            pattern = '%d-%m-%Y | %H:%M' if self.brand != 'ladbrokes' else '%A %d %B %Y - %H:%M'
            event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=pattern,
                                                                   date_time_str=event_date,
                                                                   future_datetime_format=pattern
                                                                   )  # need convert to local time (BMA-46066)

            if self.brand != 'ladbrokes':
                created_event_name = f'{event_time_resp_converted} {event_pattern}'
            else:
                created_event_name = datetime.strptime(event_time_resp_converted, '%A %d %B %Y - %H:%M').strftime('%d-%m-%Y | %H:%M ') + horseracing_autotest_uk_name_pattern_event \
                    if self.device_type == 'desktop' else strftime_add_day_suffix(datetime_string=event_time_resp_converted,
                                                                                  format_pattern='%A %d %B %Y - %H:%M')

            if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                created_event_name = self.remove_first_zero([created_event_name])[0]
            event = events.get(created_event_name)
            self.assertTrue(event,
                            msg=f'Created event "{created_event_name}" was not found in [{", ".join(events.keys())}]')

            self.assertEqual(event.type_name, self.horseracing_autotest_uk_name_pattern,
                             msg=f'"{event.type_name}" is not equal to "{self.horseracing_autotest_uk_name_pattern}"')
            self.assertTrue(event.link.href, msg=f'No link present for event "{created_event_name}"')
