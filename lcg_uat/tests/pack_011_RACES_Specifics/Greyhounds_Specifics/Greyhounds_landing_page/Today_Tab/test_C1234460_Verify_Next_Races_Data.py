import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from json import JSONDecodeError
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.reg156_fix
@vtest
class Test_C1234460_Verify_Next_Races_Data(BaseFeaturedTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C1234460
    NAME: Verify 'Next Races' Data
    DESCRIPTION: This test case is for checking the data which is displayed in 'Next Races' module for greyhounds.
    PRECONDITIONS: 1) To get class IDs for <Race> sport user a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id =19, Horse Racing category id = 21
    PRECONDITIONS: 2) To get a list of events "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event time and local time
    PRECONDITIONS: - **'typeFlagCodes' **to check event group
    PRECONDITIONS: - **'eventStatusCode'** to check whether event is active or suspended
    PRECONDITIONS: - **'marketStatusCode' **to see market status
    PRECONDITIONS: - **'outcomeStatusCode'** to see outcome status
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    is_filters_available = False

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        if cls.virtual_races_enabled == 'Yes':
            cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                             field_name='isVirtualRacesEnabled',
                                                             field_value='Yes')

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url

            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: --
        """
        next_races_config = self.get_initial_data_system_configuration().get('NextRaces')
        self.__class__.number_of_events = int(next_races_config.get('numberOfEvents'))
        self.site.wait_content_state(state_name='HomePage')

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: - 'Greyhounds' landing page is opened
        EXPECTED: - 'Today' tab is opened
        """
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=30)
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not present')

    def test_003_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: 'Next Races' module is shown
        """
        self.__class__.virtual_races_enabled =self.cms_config.get_system_configuration_structure()['GreyhoundNextRaces']['isVirtualRacesEnabled']
        if self.brand == 'ladbrokes':
            self.__class__.next_races_tab = self.site.greyhound.tabs_menu.click_button(
                button_name=vec.racing.RACING_NEXT_RACES_NAME)
            self.assertTrue(self.next_races_tab,
                            msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
        greyhound_next_races_filter = self.cms_config.get_system_configuration_item("NextRacesFiltersGreyHounds")
        if greyhound_next_races_filter.get('EnableFilters'):
            filters = self.site.greyhound.tab_content.filters_list.items_as_ordered_dict
            self.__class__.is_filters_available = True
            filter_name = next((filter_name for filter_name in filters.keys() if
                                (filter_name.upper() != "VIRTUALS" and filter_name.upper() != "ALL")), None)
            if filter_name:
                filters.get(filter_name).click()
            else:
                self.__class__.virtual_races_enabled = \
                    self.cms_config.get_system_configuration_structure()['GreyhoundNextRaces']['isVirtualRacesEnabled']
                if self.virtual_races_enabled == 'Yes':
                    self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                                          field_name='isVirtualRacesEnabled',
                                                                          field_value='No')
                    wait_for_haul(60)
                    self.device.refresh_page()
        self.__class__.sections = self.get_sections('greyhound-racing')
        self.assertTrue(self.sections, msg='No race sections are found in next races')

    def test_004_verify_data_in_next_races_module(self):
        """
        DESCRIPTION: Verify data in 'Next Races' module
        EXPECTED: - The next available races in terms of OpenBet event off time are shown.
        EXPECTED: - Data corresponds to the Site Server response. See attribute **'name'**.
        EXPECTED: - Events are sorted in the following order: the first event to start is shown first.
        """
        no_of_sel_on_widget = self.get_greyhound_next_races_selections_number_from_cms()
        actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
        response = do_request(method='GET', url=actual_url)
        self.__class__.event_name_dict = {}
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            self.__class__.event_name_dict[
                f"{event['event']['name'].split()[0]} {event['event']['typeName']}".upper()] = event['event'][
                'name'].upper()
        if self.brand == 'ladbrokes':
            meetings = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(meetings, msg='Meetings are not displayed')
            meetings_names = list(meetings.keys())
            actual_time_list = []
            for times in meetings_names:
                time = times.split(" ")[0]
                actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(sorted(actual_time_list), expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')
            meetings_details = list(meetings.values())[0]
            actual_length = len(meetings_details.runners.items_names)
            self.assertLessEqual(actual_length, no_of_sel_on_widget,
                             msg=f'Actual text: "{actual_length}" is not equal with the '
                                 f'Expected text: "{no_of_sel_on_widget}"')

            meetings = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            non_virtual_events = [meeting_name for meeting_name, meetings_details in meetings.items() if not meetings_details.is_virtual]

            for meeting_name in non_virtual_events[:3]:
                meetings = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                meetings_details = meetings.get(meeting_name)

                self.assertTrue(meetings_details, msg=f'meeting is not displayed')
                self.assertTrue(meetings_details.header.full_race_card,
                                msg=f'Full race card is not displayed for the current meeting')
                expected_meeting_name = meetings_details.name.upper()
                meetings_details.header.full_race_card.click()
                self.site.wait_splash_to_hide(5)

                actual_meeting_name = self.site.greyhound_event_details.event_name.upper()

                self.assertEqual(actual_meeting_name.upper(), expected_meeting_name.upper(),
                                 msg=f'Actual text: "{actual_meeting_name}" is not equal with the '
                                     f'Expected text: "{expected_meeting_name}"')
                self.device.go_back()
                self.assertTrue(self.site.greyhound.is_displayed(), msg=f'Greyhound page is not displayed')
        else:
            if self.device_type == 'mobile':
                next_race_name, next_race_tab = \
                    list(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.items())[0]
                self.assertEqual(next_race_name, vec.racing.NEXT_RACES.upper(),
                                 msg=f'Currently opened tab is "{next_race_name}" '
                                     f'instead of "{vec.racing.NEXT_RACES.upper()}"')
            else:
                next_race_tab = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict[self.next_races_title]
                self.assertEqual(next_race_tab.name, vec.racing.NEXT_RACES,
                                 msg=f'Currently opened tab is "{next_race_tab.name}" '
                                     f'instead of "{vec.racing.NEXT_RACES}"')

            meetings = next_race_tab.items_as_ordered_dict
            self.assertTrue(meetings, msg='Meetings are not displayed')
            meetings_names = list(meetings.keys())
            actual_time_list = []
            for times in meetings_names:
                time = times.split(" ")[0]
                actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

            meetings_details = meetings.values()
            for selection in meetings_details:
                actual_length = len(selection.items_names)
                self.assertLessEqual(actual_length, no_of_sel_on_widget,
                                     msg=f'Actual text: "{actual_length}" is not equal with the'
                                         f'Expected text: "{no_of_sel_on_widget}"')

            for i in range((len(meetings))):
                if self.device_type == 'mobile':
                    next_race_name, next_race_tab = \
                        wait_for_result(lambda: list(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.items())[0])
                else:
                    next_race_tab = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict[self.next_races_title]
                event = list(next_race_tab.items_as_ordered_dict.values())[i]
                expected_meeting_name = event.event_name
                self.assertTrue(event, msg=f'"{expected_meeting_name}" event is not displayed')
                self.assertTrue(event.full_race_card,
                                msg=f'Full race card is not displayed for "{expected_meeting_name}" event')

    def test_005_verify_events_which_are_displayed_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify events which are displayed in the 'Next Races' module
        EXPECTED: *   Only events with attribute **'typeFlagCodes'="NE"**  [Next Events flag] from the Site Server response are shown.
        EXPECTED: *   Only active events are displayed in the 'Next Races' module (for those events attribute **'eventStatusCode'**='A' in the Site Server response)
        EXPECTED: *   Only events with active markets are shown in the 'Next Races' module (**'marketStatusCode'**='A')
        EXPECTED: *   'Next Races' module is not shown if no events with **'typeFlagCodes'="NE"**are available
        """
        if self.is_filters_available:
            filters = self.site.greyhound.tab_content.filters_list.items_as_ordered_dict
            all_filter = next(filter_obj for name, filter_obj in filters.items() if name.upper() == "ALL")
            all_filter.click()
            wait_for_haul(2)

        event_name_ss_time_event_name = list(self.event_name_dict.values())
        event_name_ss_time_type_name = list(self.event_name_dict.keys())
        if self.brand == 'ladbrokes':
            actual_event_list = list(self.sections.keys())
        else:
            actual_event_list = list(self.sections[self.next_races_title].items_as_ordered_dict.keys())
        actual_event_list = [event.upper() for event in actual_event_list]
        if self.device_type == 'desktop':
            self.assertTrue((sorted(actual_event_list) == sorted(event_name_ss_time_event_name)[:self.number_of_events]) or (sorted(actual_event_list) == sorted(event_name_ss_time_type_name)[:self.number_of_events]),
                                 msg=f'Outcome name "{sorted(actual_event_list)}" is not '
                                     f'the same as expected "{sorted(event_name_ss_time_event_name)[:self.number_of_events]}" or "{sorted(event_name_ss_time_type_name)[:self.number_of_events]}"')
        else:
            for index in sorted(actual_event_list):
                current_time = self.get_date_time_formatted_string(time_format='%H:%M')
                if current_time > index.split()[0]:
                    continue
                self.assertTrue((index in event_name_ss_time_event_name) or (index in event_name_ss_time_type_name),
                              msg=f'Event name "{index}" is not in '
                                  f'expected events "{event_name_ss_time_event_name}" or "{event_name_ss_time_type_name}"')

    def test_006_verify_event_sectionsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofselections(
            self):
        """
        DESCRIPTION: Verify event sections
        DESCRIPTION: Quantity of the events sets in the CMS (CMS -> systemConfiguration ->GreyhoundNextRaces -> numberOfSelections)
        EXPECTED: 1. Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: 2. If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: 3. - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        EXPECTED: 4. Only active selections are shown (**'outcomeStatusCode'**='A')
        """
        unnamed_favourite = vec.racing.UNNAMED_FAVORITE
        meetings = list(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        if self.brand == 'ladbrokes':
            last_runner = list(meetings.runners.items_as_ordered_dict.keys())[-1]
        else:
            last_runner = list(list(meetings.items_as_ordered_dict.values())[0].items_as_ordered_dict.keys())[-1]
        self.assertTrue(last_runner, msg='No outcomes found')
        self.assertNotEqual(unnamed_favourite, last_runner,
                            msg=f'Actual runner :"{last_runner}" is same as '
                                f'Expected : "{unnamed_favourite}".')

    def test_007_verify_selection_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify selection in the 'Next Races' module
        EXPECTED: Selections ONLY from 'Win or Each Way' market are displayed in the 'Next Races' module
        """
        if self.brand == 'ladbrokes':
            meetings = list(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.values())
            for index in meetings:
                e_w_text = index.sub_header.e_w_and_places.text
                self.check_each_way_terms_format(each_way_terms=e_w_text,
                                                 format=vec.regex.EXPECTED_EACH_WAY_FORMAT_DESKTOP_FUTURE)
