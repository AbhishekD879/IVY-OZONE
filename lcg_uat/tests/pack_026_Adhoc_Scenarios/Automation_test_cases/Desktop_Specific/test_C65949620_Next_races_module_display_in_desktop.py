import re
from datetime import datetime, timedelta
import voltron.environments.constants as vec
import tests
import pytest
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone
from tests.base_test import vtest
from voltron.utils.helpers import get_response_url, do_request
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


def clean_string(name):
    # Use regular expression to remove special characters and extra spaces
    cleaned_string = re.sub(r'[^A-Za-z0-9: ]', '', name)
    return ' '.join(cleaned_string.split())


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.adhoc_suite
@pytest.mark.desktop_only
@pytest.mark.desktop
@pytest.mark.desktop_specific
@vtest
class Test_C65949620_Next_races_module_display_in_desktop(BaseRacing):
    """
    TR_ID: C65949620
    NAME: Next races module display in desktop
    DESCRIPTION: This test case is to validate Next races module display in desktop
    """
    keep_browser_open = True
    timezone = str(get_localzone())
    int_filter_name = vec.racing.int_filter_name
    uk_filter_name = vec.racing.uk_filter_name
    vr_filter_name = vec.racing.vr_filter_name
    timezone = str(get_localzone())
    uk_filter = False
    international_filter = False
    virtual_filter = False
    device_name = tests.desktop_default
    enable_bs_performance_log = True

    def check_events(self, event_names):
        # Create a list to store actual event times
        actual_time_list = []
        next_races = self.next_races_section.accordions_list.items_as_ordered_dict
        self.assertTrue(next_races, msg='No one race found in Next Race section')
        for event_name, event in next_races.items():
            # Extract the time from the 'event_name' and prepare it for comparison
            time = event_name.split(" ")[0]
            # Verify the countdown timer for events starting in less than 45 minutes
            current_time = get_date_time_as_string(time_format='%H:%M', url_encode=False)
            current_time = datetime.strptime(current_time, '%H:%M')
            # If the timezone is UTC, adjust the current time by 60 minutes
            europe_london = get_date_time_as_string(time_format='%H:%M', url_encode=False, tz_region='EUROPE/LONDON')
            europe_london = datetime.strptime(europe_london, '%H:%M')
            time_difference = abs(current_time - europe_london)
            if time_difference.total_seconds() / 3600 >= 1:
                current_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%H:%M', url_encode=False,minutes=60)
            # Parse the time strings into datetime objects
            current_time = datetime.strptime(current_time, '%H:%M')
            time = datetime.strptime(time, '%H:%M')
            # Add the 'time' to a list for future reference
            actual_time_list.append(time)
            # Calculate the time difference in seconds
            time_difference = time - current_time
            # Convert the time difference to minutes
            minutes_difference = time_difference.total_seconds() / 60
            # Check if the event starts in 1 to 45 minutes
            if 1 < minutes_difference <= 45:
                # Clean the 'event_name' and check if it exists in the 'event_name_dict'
                cleaned_event_name = str(clean_string(event_name).upper().replace("VIRTUAL", '')).strip()
                if cleaned_event_name in event_names.values():
                    self.assertIn(cleaned_event_name, list(event_names.values()),
                                  msg=f'actual event "{cleaned_event_name}" is not in the expected list {self.event_name_dict.values()} in timezone {self.timezone}')
                else:
                    self.assertIn(cleaned_event_name, list(event_names.keys()),
                                  msg=f'actual event "{cleaned_event_name}" is not in the expected list {self.event_name_dict.keys()} in timezone {self.timezone}')
                # Check if the 'cleaned_event_name' exists in various dictionaries
                if cleaned_event_name in self.international_events_dict or cleaned_event_name in list(
                        self.international_events_dict.values()):
                    self.__class__.international_filter = True
                if cleaned_event_name in self.uk_events_dict or cleaned_event_name in list(
                        self.uk_events_dict.values()):
                    self.__class__.uk_filter = True
                if cleaned_event_name in self.virtual_events_dict or cleaned_event_name in list(
                        self.virtual_events_dict.values()):
                    self.__class__.virtual_filter = True
                # Scroll to the event and check if it has a timer
                event.scroll_to()
                self.assertTrue(event.has_timer(),
                                msg=f'actual event {event_name.upper()} doesn"t have a timer even though the event is less than 45 minutes timediff-{minutes_difference} timezone- {self.timezone}')
            # Check if the event starts in more than 45 minutes
            elif minutes_difference > 45:
                # Ensure the event doesn't have a timer
                self.assertFalse(event.has_timer(),
                                 msg=f'actual event {event_name.upper()} has a timer even though the event is more than 45 minutes  timediff-{minutes_difference} timezone- {self.timezone}')
        return actual_time_list

    def formate_time(self, date_time):
        # Convert the string to a datetime object
        dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        # Add one hour to the datetime
        utc = get_date_time_as_string(time_format='%H:%M', url_encode=False)
        europe_london = get_date_time_as_string(time_format='%H:%M', url_encode=False,
                                                tz_region='EUROPE/LONDON')
        europe_london = datetime.strptime(europe_london, '%H:%M')
        utc_time = datetime.strptime(utc, '%H:%M')
        time_difference = utc_time - europe_london
        if time_difference.total_seconds() / 3600 >= 1:
            dt_plus_one_hour = dt + timedelta(hours=1)
            return dt_plus_one_hour.strftime('%H:%M')
        # Extract the time as a string in HH:MM format from the new datetime
        return dt.strftime('%H:%M')

    def check_event_section(self):
        self.__class__.next_races = self.next_races_section.accordions_list.items_as_ordered_dict
        self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        for race_name, race in self.next_races.items():
            race.scroll_to()
            selections = race.items_as_ordered_dict
            self.assertTrue(selections, msg=f'No one selection found for race: "{race_name}"')
            self.assertLessEqual(len(selections), self.number_of_selections,
                                 msg=f'Actual race: "{race_name}" selections number: "{len(selections)}", '
                                     f'expected less or equals than CMS configured: '
                                     f'"{self.number_of_selections}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2. Login with valid credentials
        PRECONDITIONS: 3.Navigate to System Configuration>structure>
        PRECONDITIONS: ->NextRacesToggle
        PRECONDITIONS: 4.Under field nextRacesComponentEnabled check box should be in active state.
        """
        next_races_toggle_config = self.get_initial_data_system_configuration().get('NextRacesToggle')
        if not next_races_toggle_config:
            next_races_toggle_config = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle_config.get('nextRacesComponentEnabled'):
            raise CmsClientException('Next Races component disabled in CMS')
            # Retrieve the initial system configuration data for 'NextRaces'.
        next_races_config = self.get_initial_data_system_configuration().get('NextRaces')

        # Store the number of events and selections based on the configuration.
        self.__class__.number_of_events = int(next_races_config.get('numberOfEvents'))
        self.__class__.number_of_selections = int(next_races_config.get('numberOfSelections'))

    def test_001_launch_the__ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the  Ladbrokes/Coral application.
        EXPECTED: Application should be  Launched successfully.
        """
        self.navigate_to_page('/')

    def test_002_homepage_should_be_launched(self):
        """
        DESCRIPTION: Homepage should be launched
        EXPECTED: User able to see all modules
        """
        self.site.wait_content_state('homepage')

    def test_003_verify_the_next_races_carousel_in_home_page(self):
        """
        DESCRIPTION: Verify the Next races carousel in Home page
        EXPECTED: Next races  carousel should be available in Home page
        EXPECTED: Race Filters Component is displayed with the below filters: 'All' and 'UK&amp;IRE '
        """
        self.__class__.module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
        self.__class__.next_races_section = \
            self.site.home.get_module_content(module_name=self.module_name)
        self.assertTrue(self.next_races_section, msg=f'"{self.next_races_title}" not found on Home page')
        self.__class__.next_races_filters_horse_racing = self.cms_config.get_system_configuration_item("NextRacesFiltersHorseRacing")
        if not self.next_races_filters_horse_racing.get('EnableFilters'):
            self.cms_config.update_system_configuration_structure(config_item='NextRacesFiltersHorseRacing',
                                                                  field_name='enabled',
                                                                  field_value=True)
        filters = self.next_races_section.filters_list.items_as_ordered_dict
        self.assertTrue(filters, msg="filters are not available even after it's enabled in cms")

    def test_004_verify_the_page_when_all_filter_is_selected_by_default(self):
        """
        DESCRIPTION: Verify the page when 'All' filter is selected by default
        EXPECTED: All' Filter is selected by default
        EXPECTED: All the available races will be displayed
        """
        # Get the URL for fetching event data
        self.__class__.actual_url = get_response_url(self, url='/NextNEventToOutcomeForClass')
        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.site.wait_content_state('homepage')
            self.__class__.actual_url = get_response_url(self, url='/NextNEventToOutcomeForClass')

        self.assertTrue(self.actual_url, 'Next Races SS URL is not present in performance log(from network call)')
        # Initialize dictionaries to store event details
        self.__class__.event_name_dict = {}
        self.__class__.uk_events_dict = {}
        self.__class__.international_events_dict = {}
        self.__class__.virtual_events_dict = {}
        # Fetch event data from the URL response
        response = do_request(method='GET', url=self.actual_url)
        # Process event data and populate dictionaries
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            # Check if the event should be shown in next races or if it's a special event (classId is 226)
            if 'NE' in event['event']['typeFlagCodes'] or '226' not in event['event']['classId']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                self.__class__.event_name_dict[event_name] = clean_string(event['event']['name']).upper().strip()
            # Check for UK events that are not special (typeFlagCodes does not contain 'SP')
            if 'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                self.__class__.uk_events_dict[event_name] = clean_string(event['event']['name']).upper().strip()
            # Check for international events
            if 'INT' in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                self.__class__.international_events_dict[event_name] = clean_string(
                    event['event']['name']).upper().strip()
            # Check for virtual events
            if 'VR' in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName'])}".upper().strip()
                self.__class__.virtual_events_dict[event_name] = clean_string(event['event']['name']).upper().strip()
        # Refresh the page for further verifications
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        # Get the list of events
        meetings = self.next_races_section.accordions_list.items_as_ordered_dict
        # Ensure that the number of events displayed is not more than the configured number of events
        self.assertLessEqual(len(meetings), self.number_of_events,
                             msg="Number of events displayed is more than the configured events")
        actual_time_list = self.check_events(event_names=self.event_name_dict)
        # Sort the 'actual_time_list' and compare it with the expected sorted list
        expected_sort_list = sorted(actual_time_list)
        self.assertEqual(actual_time_list, expected_sort_list,
                         msg=f'Actual list: "{actual_time_list}" is not equal to the expected list: "{expected_sort_list}"')
        # Get details of the first meeting in 'meetings'
        self.check_event_section()

    def test_005_select_ukampire__filter(self):
        """
        DESCRIPTION: Select 'UK&amp;IRE ' filter
        EXPECTED: Newly selected Race Filter UK&amp;IRE race filter is highlighted and respective events should load.
        EXPECTED: Events are sorted by Start Time
        """
        filters = self.next_races_section.filters_list.items_as_ordered_dict
        self.assertTrue(filters, msg="filters are not available even after it's enabled in cms")
        # Check if there are International Racing events, and if the International Racing filter is enabled in the configuration
        if len(self.international_events_dict) > 0 and self.next_races_filters_horse_racing.get(
                'INT') and self.international_filter:
            # Get the filter name for International Racing, specifically the one matching the current filter name
            international_filters = next(
                (filter_name for filter_name in filters.keys() if filter_name.upper() == self.int_filter_name.upper()),
                None)
            self.assertTrue(international_filters,
                            msg="International filter is not shown even if there are events present")
            # Select the International Racing filter
            filters.get(international_filters).click()
            actual_time_list = self.check_events(event_names=self.international_events_dict)
            # Sort the 'actual_time_list' and compare it with the expected sorted list
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual list: "{actual_time_list}" is not equal to the expected list: "{expected_sort_list}"')
            # Get details of the first meeting in 'meetings'
            self.check_event_section()

        # Check if there are UK&IRE events, and if the filter is enabled in the configuration
        if len(self.uk_events_dict) > 0 and self.next_races_filters_horse_racing.get('UK&IRE') and self.uk_filter:
            # Get the filter name for UK&IRE, excluding the current filter name if it's present
            self.uk_filter_name = 'UK & Irish' if self.brand != 'bma' else self.uk_filter_name
            uk_filters = next((filter_name for filter_name in filters.keys() if
                               (filter_name.upper() == self.uk_filter_name.upper())), None)
            self.assertTrue(uk_filters, msg=f"{self.uk_filter_name} filter is not shown even if there are events present")
            # Select the UK&IRE filter
            filters.get(uk_filters).click()
            actual_time_list = self.check_events(event_names=self.uk_events_dict)
            # Sort the 'actual_time_list' and compare it with the expected sorted list
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual list: "{actual_time_list}" is not equal to the expected list: "{expected_sort_list}"')
            # Get details of the first meeting in 'meetings'
            self.check_event_section()
        # Check if there are Virtual Racing events, and if the Virtual Racing filter is enabled in the configuration
        if len(self.virtual_events_dict) > 0 and self.next_races_filters_horse_racing.get('VR') and self.virtual_filter:
            # Get the filter name for Virtual Racing, excluding the current filter name if it's present
            virtual_filter = next(
                (filter_name for filter_name in filters.keys() if filter_name.upper() == self.vr_filter_name.upper()),
                None)
            self.assertTrue(virtual_filter, msg="Virtual Racing filter is not shown even if there are events present")
            # Select the Virtual Racing filter
            filters.get(virtual_filter).click()
            actual_time_list = self.check_events(event_names=self.virtual_events_dict)
            # Sort the 'actual_time_list' and compare it with the expected sorted list
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual list: "{actual_time_list}" is not equal to the expected list: "{expected_sort_list}"')
            # Get details of the first meeting in 'meetings'
            self.check_event_section()

    def test_006_verify_right_scroll_bar_is_displayed_when_there_are_more_no_of_events(self):
        """
        DESCRIPTION: Verify Right scroll bar is displayed when there are more no. of events
        EXPECTED: Right scroll bar is seen and able to scroll right side
        EXPECTED: Events on the right side will be displayed
        """
        next_races = self.next_races_section.accordions_list.items_as_ordered_dict
        self.assertTrue(next_races, msg='No one race found in Next Race section')
        # need scroll to first race section to correct perform next validations
        list(self.next_races.values())[0].scroll_to()
        for i, (race_name, race) in enumerate(next_races.items()):
            if i > 0 and i % 2 != 0:
                self.next_races_section.click_next_arrow()
            # need to add small sleep to make test run more stable after click with java script
            self.device.driver.implicitly_wait(1)
            next_race_name, next_race = list(
                self.next_races.items())[i + 1] if i < (len(self.next_races.items()) - 1) else (race_name, race)
            self.assertTrue(next_race.is_displayed(scroll_to=False),
                            msg=f'Next race: "{next_race_name}" not displayed after scrolling to')
            if i > 1:
                prev_race_name, prev_race = list(self.next_races.items())[i - 2]
                self.assertFalse(prev_race.is_displayed(expected_result=False, scroll_to=False),
                                 msg=f'Previous race: "{prev_race_name}" still displayed after scrolling to next')

    def test_007_verify_left_scroll_bars_are_displayed_when_there_are_more_no_of_events(self):
        """
        DESCRIPTION: Verify Left scroll bars are displayed when there are more no. of events
        EXPECTED: Left scroll bar is seen and able to scroll Left side
        EXPECTED: Events on the Left side will be displayed
        """
        next_races = self.next_races_section.accordions_list.items_as_ordered_dict
        self.assertTrue(next_races, msg='No one race found in Next Race section')
        # need scroll to last race section to correct perform next validations
        list(self.next_races.values())[-1].scroll_to()
        for i, (race_name, race) in enumerate(list(next_races.items())[::-1]):
            if i % 2 == 0:
                self.next_races_section.click_prev_arrow()
            # need to add small sleep to make test run more stable after click with java script
            self.device.driver.implicitly_wait(1)
            prev_race_name, prev_race = list(
                self.next_races.items())[::-1][i + 1] if i < (len(self.next_races.items()) - 1) else \
                (race_name, race)
            self.assertTrue(prev_race.is_displayed(scroll_to=False),
                            msg=f'Previous race: "{prev_race_name}" not displayed after scrolling to')
            if 1 < i < (len(self.next_races.items()) - 2):
                next_race_name, next_race = list(self.next_races.items())[::-1][i - 3]
                self.assertFalse(next_race.is_displayed(expected_result=False, scroll_to=False),
                                 msg=f'Next race: "{next_race_name}" still displayed after scrolling to previous')

    def test_008_verify_footer_link_on_next_races_module_is_displayed(self):
        """
        DESCRIPTION: Verify Footer link on Next Races module is displayed
        EXPECTED: Clicking on "View all horse Racing Events" Horse racing page is displayed
        """
        self.assertTrue(self.next_races_section.has_show_more_link(),
                        msg=f'Link not found under the: "{self.next_races_title}" module')
        self.next_races_section.show_more_link.click()
        self.site.wait_content_state(state_name='HorseRacing')
        self.site.horse_racing.header_line.back_button.click()
        self.site.wait_content_state(state_name='HomePage')
        next_races_section = self.site.home.get_module_content(module_name=self.module_name).accordions_list
        self.assertTrue(next_races_section, msg=f'"{self.next_races_title}" not found on Home page')
