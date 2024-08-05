import re
from datetime import datetime, timedelta
from tzlocal import get_localzone
from json import JSONDecodeError
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result, wait_for_haul


def clean_string(name):
    # Use regular expression to remove special characters and extra spaces
    cleaned_string = re.sub(r'[^A-Za-z0-9: ]', '', name)
    return ' '.join(cleaned_string.split())


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@vtest
class Test_C65940559_MRT__Verify_the_Next_races_tab_display_and_price_updates_in_next_races(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C65940559
    NAME: MRT - Verify the Next races tab display and price updates in next races
    DESCRIPTION: This test case is to verify the Next races with price updates

    """
    enable_bs_performance_log = True
    keep_browser_open = True
    int_filter_name = "International"
    uk_filter_name = "UK&IRE"
    vr_filter_name = "VIRTUALS"
    timezone = str(get_localzone())
    runner_names = []
    uk_filter = False
    international_filter = False
    virtual_filter = False

    def add_to_quick_bet(self, runners):
        runner_name, runner = list(runners.items())[0]
        self.__class__.runner_names.append(runner_name)
        self._logger.info(f'*** Selected first runner: "{runner_name}"')
        runner.scroll_to()
        self.device.driver.implicitly_wait(5)
        runner.bet_button.click()
        if self.device_type == 'mobile':
            if len(self.runner_names) == 1:
                self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True),
                                msg='Quick Bet is not present')
                self.site.quick_bet_panel.add_to_betslip_button.click()
                self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False, timeout=6),
                                 msg='Quick Bet is not closed')
            else:
                self.assertTrue(runner.bet_button.is_selected(),
                                msg=f'Button is not selected for runner')

    def formate_time(self, date_time):
        # Convert the string to a datetime object
        dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        current_time = get_date_time_as_string(time_format='%H:%M', url_encode=False)
        current_time = datetime.strptime(current_time, '%H:%M')
        # If the timezone is UTC, adjust the current time by 60 minutes
        europe_london = get_date_time_as_string(time_format='%H:%M', url_encode=False, tz_region='EUROPE/LONDON')
        europe_london = datetime.strptime(europe_london, '%H:%M')
        time_difference = abs(current_time - europe_london)
        if time_difference.total_seconds() / 3600 >= 1:
            dt_plus_one_hour = dt + timedelta(hours=1)
            return dt_plus_one_hour.strftime('%H:%M')
        # Extract the time as a string in HH:MM format from the new datetime
        return dt.strftime('%H:%M')

    from json.decoder import JSONDecodeError

    def get_response_url(self, url):
        """
        Get the complete URL from the performance logs matching the provided URL.

        :param url: The URL to search for in the performance logs.
        :return: The complete URL if found, else None.
        """
        perflog = self.device.get_performance_log()

        # Reverse the log list to start from the most recent logs
        for log in reversed(perflog):
            try:
                # Extract request information from the log
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']

                # Check if the provided URL is in the request URL
                if url in request_url:
                    return request_url

            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

        # If the URL is not found in any log, return None
        return None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: This test checks various preconditions before the main test.
        1) User should have oxygen CMS access.
        2) Configuration for module ribbon tab in the CMS.
        3) Click on the "Module Ribbon Tab" option from the left menu in the Main navigation.
        4) Click on "+ Create Module Ribbon Tab" button to create a new MRT.
        5) Enter all mandatory fields and click on the save button:
           - Module ribbon tab title as Next races
           - Directive name option from the dropdown as Next races
           - ID as tab-next-races
           - URL as /home/next-races
           - Click on "Create" CTA button.
        6) Check and select the following required fields in module ribbon tab configuration:
           - Active
           - iOS
           - Android
           - Windows Phone
           - Select Show tab on option from the dropdown like Both, Desktop, Mobile/tablet.
           - Select the radio button either Universal or segment(s) inclusion.
           - Click on "Save changes" button.
        """
        # Check if the 'NextRaces' module exists in the CMS.
        next_races_tab = self.get_module_data_by_directive_name_from_cms(directiveName='NextRaces')

        # If it doesn't exist, create it.
        if not next_races_tab:
            next_races_tab = self.cms_config.module_ribbon_tabs.create_tab(
                directive_name='NextRaces',
                internal_id="tab-next-races",
                title='AutoNextRaces',
                display_date=True,
                devices_wp=False
            )
            # Store the tab name for future reference.
            self.__class__.next_races_tab_name = next_races_tab.get('title').upper()
        else:
            # The tab already exists, so store its name.
            self.__class__.next_races_tab_name = next_races_tab[0].get('title').upper()

        # Retrieve the initial system configuration data for 'NextRaces'.
        next_races_config = self.get_initial_data_system_configuration().get('NextRaces')

        # Store the number of events and selections based on the configuration.
        self.__class__.number_of_events = int(next_races_config.get('numberOfEvents'))
        self.__class__.number_of_selections = int(next_races_config.get('numberOfSelections'))

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Ladscoral application and verify the homepage.
        EXPECTED: Home Page should be loaded successfully.
        """
        # Log in to the site.
        self.site.login()

        # Wait for the homepage content to load successfully.
        self.site.wait_content_state("homepage")

    def test_002_verify_next_races_tab_present_in_mrt(self):
        """
        DESCRIPTION: Verify that the 'Next Races' tab is present in the Module Ribbon Tab (MRT).
        EXPECTED: The 'Next Races' tab should be present in the MRT.
        """
        for i in range(20):
            # Get the current Module Ribbon Tabs from the site.
            module_ribbon_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            # Check if the 'Next Races' tab is present.
            tab_name = next((tab for tab in module_ribbon_tabs if tab.upper() == self.next_races_tab_name),
                            None)
            if tab_name:
                # If the tab is found, break out of the loop.
                break
            else:
                # If the tab is not found, refresh the page and wait for content state change.
                self.device.refresh_page()
                self.site.wait_content_state_changed()

        # Click on the 'Next Races' module ribbon tab.
        next_module_ribbon_tab = module_ribbon_tabs.get(tab_name)
        next_module_ribbon_tab.click()
        self.site.wait_content_state_changed()

    def test_003_click_on_next_races_tab(self):
        """
        DESCRIPTION: click on Next races tab
        EXPECTED: 1 user should be able to see Next races tab
        EXPECTED: 2 Coral-Two extra place event should be displayed at the top.
        EXPECTED: Ladbrokes-one extra place event should be displayed at the top.
        EXPECTED: 3 Horse race events which starts in next 45 mins should be displayed
        EXPECTED: 4: The following details should be displayed
        EXPECTED: 4a:Event Time
        EXPECTED: 4b:Meeting name
        EXPECTED: 4c:countdown timer
        EXPECTED: 4d:'MORE' links in event header
        """
        # Get the URL for fetching event data
        self.__class__.actual_url = self.get_response_url('/NextNEventToOutcomeForClass')

        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.site.wait_content_state_changed()
            self.__class__.actual_url = self.get_response_url('/NextNEventToOutcomeForClass')

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
        # Verify the presence of the 'Extra Place' module
        self.assertTrue(self.site.home.tab_content.has_extra_place_module(),
                        msg="Extra place module not found in next races tab")
        # Get the extra place events
        extra_place_events = self.site.home.tab_content.extra_place_module.items_as_ordered_dict
        # Define the number of expected extra place events based on the brand
        no_extra_place_events = 2 if self.brand == 'bma' else 1
        # Verify the number of extra place events
        self.assertEqual(no_extra_place_events, len(extra_place_events),
                         msg=f"Expected {no_extra_place_events} extra place events, but found {len(extra_place_events)}")
        # Get the list of events
        meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        # Ensure that the number of events displayed is not more than the configured number of events
        self.assertLessEqual(len(meetings), self.number_of_events,
                             msg="Number of events displayed is more than the configured events")
        # Create a list to store actual event times
        actual_time_list = []
        # Loop through the events in the 'meetings' dictionary
        for event_name, event in meetings.items():
            # Extract the time from the 'event_name' and prepare it for comparison
            time = event_name.split(" ")[0]
            # Verify the countdown timer for events starting in less than 45 minutes
            current_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%H:%M', url_encode=False)
            # If the timezone is UTC, adjust the current time by 60 minutes
            if self.timezone.upper() == "UTC":
                current_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%H:%M',
                                                       url_encode=False, minutes=60)
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
                if cleaned_event_name in self.event_name_dict.values():
                    self.assertIn(cleaned_event_name, list(self.event_name_dict.values()),
                                  msg=f'actual event "{cleaned_event_name}" is not in the expected list {self.event_name_dict.values()} in timezone {self.timezone}')
                else:
                    self.assertIn(cleaned_event_name, list(self.event_name_dict.keys()),
                                  msg=f'actual event "{cleaned_event_name}" is not in the expected list {self.event_name_dict.keys()} in timezone {self.timezone}')
                # Check if the 'cleaned_event_name' exists in various dictionaries
                if cleaned_event_name in self.international_events_dict:
                    self.__class__.international_filter = True
                if cleaned_event_name in self.uk_events_dict:
                    self.__class__.uk_filter = True
                if cleaned_event_name in self.virtual_events_dict:
                    self.__class__.virtual_filter = True
                # Scroll to the event and check if it has a timer
                event.scroll_to()
                self.assertTrue(event.has_timer(),
                                msg=f'actual event {event_name.upper()} doesn"t have a timer even though the event is less than 45 minutes{minutes_difference}{self.timezone}')
            # Check if the event starts in more than 45 minutes
            elif minutes_difference > 45:
                # Ensure the event doesn't have a timer
                self.assertFalse(event.has_timer(),
                                 msg=f'actual event {event_name.upper()} has a timer even though the event is more than 45 minutes {minutes_difference}{self.timezone}')
        # Sort the 'actual_time_list' and compare it with the expected sorted list
        expected_sort_list = sorted(actual_time_list)
        self.assertEqual(actual_time_list, expected_sort_list,
                         msg=f'Actual list: "{actual_time_list}" is not equal to the expected list: "{expected_sort_list}"')
        # Get details of the first meeting in 'meetings'
        meetings_details = list(meetings.values())[0]
        # Verify the actual length of runners' item names
        actual_length = len(meetings_details.runners.items_names)
        self.assertLessEqual(actual_length, self.number_of_selections,
                             msg=f'Actual length: "{actual_length}" is not equal to the expected length: "{self.number_of_selections}"')
        # Validate the 'View Full Race Card' and navigate back
        for i in range(1, 3):
            meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            meetings_details = list(meetings.values())[len(meetings) - i]

            # Check if the meeting is displayed
            self.assertTrue(meetings_details, msg=f'Meeting is not displayed')
            # Check if the 'Full race card' is displayed for the current meeting
            self.assertTrue(meetings_details.has_view_full_race_card(),
                            msg=f'Full race card is not displayed for the current meeting')
            # If 'VIRTUAL' is not in the name, click on 'Full race card' and navigate back
            if 'VIRTUAL' not in meetings_details.name.upper():
                meetings_details.full_race_card.click()
                self.site.wait_content_state_changed()
                # self.site.back_button.click()
                self.device.go_back()
                wait_for_haul(3)

    def test_004_verify_the_next_races_filters_like_ukamp_irish_international_amp_virtual_racing(self):
        """
        DESCRIPTION: Verify the next races filters like UK&amp; Irish, International &amp; Virtual Racing.
        EXPECTED: User should be able to select and unselect filter and next races events should be displayed according to filter
        """
        # Ensure that the filters for Next Races are enabled
        next_races_filters_horse_racing = self.cms_config.get_system_configuration_item("NextRacesFiltersHorseRacing")
        if not next_races_filters_horse_racing.get('EnableFilters'):
            self.cms_config.update_system_configuration_structure(config_item='NextRacesFiltersHorseRacing',
                                                                  field_name='enabled',
                                                                  field_value=True)
        filters = self.site.home.tab_content.filters_list.items_as_ordered_dict
        # Check if there are International Racing events, and if the International Racing filter is enabled in the configuration
        if len(self.international_events_dict) > 0 and next_races_filters_horse_racing.get(
                'INT') and self.international_filter:
            # Get the filter name for International Racing, specifically the one matching the current filter name
            international_filters = next(
                (filter_name for filter_name in filters.keys() if filter_name.upper() == self.int_filter_name.upper()),None)
            self.assertTrue(international_filters,
                            msg="International filter is not shown even if there are events present")
            # Select the International Racing filter
            filters.get(international_filters).click()

            # Check if events are displayed under the International Racing filter
            meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(meetings, msg="There are no events present under the International Racing filter")

        # Check if there are UK&IRE events, and if the filter is enabled in the configuration
        if len(self.uk_events_dict) > 0 and next_races_filters_horse_racing.get('UK&IRE') and self.uk_filter:
            # Get the filter name for UK&IRE, excluding the current filter name if it's present
            self.uk_filter_name = 'UK & Irish' if self.brand != 'bma' else self.uk_filter_name
            uk_filters = next((filter_name for filter_name in filters.keys() if
                               (filter_name.upper() == self.uk_filter_name.upper())), None)
            self.assertTrue(uk_filters, msg="Uk&IRE filter is not shown even if there are events present")
            # Select the UK&IRE filter
            filters.get(uk_filters).click()
            # Check if events are displayed under the UK&IRE filter
            meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(meetings, msg="There are no events present under the UK&IRE filter")
        # Check if there are Virtual Racing events, and if the Virtual Racing filter is enabled in the configuration
        if len(self.virtual_events_dict) > 0 and next_races_filters_horse_racing.get('VR') and self.virtual_filter:
            # Get the filter name for Virtual Racing, excluding the current filter name if it's present
            virtual_filter = next(
                (filter_name for filter_name in filters.keys() if filter_name.upper() == self.vr_filter_name.upper()),
                None)
            self.assertTrue(virtual_filter, msg="Virtual Racing filter is not shown even if there are events present")
            # Select the Virtual Racing filter
            filters.get(virtual_filter).click()
            # Check if events are displayed under the Virtual Racing filter
            meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(meetings, msg="There are no events present under the Virtual Racing filter")

    def test_005_verify_the_price_updates_in_next_races(self):
        """
        DESCRIPTION: verify the price updates in next races
        EXPECTED: Price updates should be displayed in next races
        """
        # Get the filters available on the webpage
        filters = self.site.home.tab_content.filters_list.items_as_ordered_dict
        # Find the filter that is not the "All" filter and not the "Virtual Racing" filter
        filter = next((filter_name for filter_name in filters.keys() if
                       filter_name.upper() != self.vr_filter_name.upper() and filter_name.upper() != "ALL"), None)
        # If such a filter is found, click on it
        if filter:
            filters[filter].click()
            # Get the list of events on the page
            events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            # Get the first event on the page
            first_event_name, first_event = list(events.items())[0]
            # Scroll to the first event
            first_event.scroll_to()
            # Get the selections (runners) for the first event
            selections = first_event.runners.items_as_ordered_dict
            # Check if there are selections (runners) for the first event
            self.assertTrue(selections, msg=F"There are selections for the first event: {first_event}")
            # Get the first selection (runner)
            selection_name, selection = list(selections.items())[0]
            # Check if the first selection has a previous price
            has_previous_price = selection.has_previous_price()
            # If there's no previous price, wait for a specific duration and check again
            if not has_previous_price:
                wait_for_haul(10)
                has_previous_price = list(selections.items())[0].has_previous_price()
                # Try to assert whether the selection has a previous price
                try:
                    self.assertTrue(has_previous_price, msg="Events don't have a previous price")
                except:
                    self._logger.info("Events don't have a previous price")

    def test_006_verify_bet_placement_for_single_bet_in_quick_bet_and_betslip(self):
        """
        DESCRIPTION: verify bet placement for single bet in Quick bet and betslip
        EXPECTED: Bet should be placed successfully
        """
        # Get a list of events on the webpage
        events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        # Get the last event in the list
        event_name, event = list(events.items())[-1]
        # Get the list of runners for the selected event
        runners = event.runners.items_as_ordered_dict
        # Check if there are runners for the selected event
        self.assertTrue(runners, msg=f'No runners found in racing card "{event_name}"')
        # Get the first runner in the list
        runner_name, runner = list(runners.items())[0]
        # Scroll to the runner
        runner.scroll_to()
        # Click on the bet button for the runner
        runner.bet_button.click()
        # Wait for the Quick Bet panel to be displayed
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True),
                        msg='Quick Bet is not present')
        # Get the Quick Bet panel's content
        quick_bet = self.site.quick_bet_panel.selection.content
        # Set the bet amount in the Quick Bet panel
        quick_bet.amount_form.input.value = self.bet_amount
        # Place the bet using the Quick Bet panel
        self.site.quick_bet_panel.place_bet.click()
        # Wait for the bet receipt to be displayed
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
        # Close the Quick Bet panel
        self.site.quick_bet_panel.close()

    def test_007_verify_bet_placement_for_multiple_and_complex_bet(self):
        """
        DESCRIPTION: Verify bet placement for multiple and complex bet
        EXPECTED: Bet should be placed successfully
        """
        # Get a dictionary of filters from the 'filters_list' on the site's home tab content
        filters = self.site.home.tab_content.filters_list.items_as_ordered_dict
        # Find the filter named "ALL" (case-insensitive) and assign it to 'events_filter'
        events_filter = next((filter_name for filter_name in filters.keys() if filter_name.upper() == "ALL"), None)
        # If 'events_filter' is found, click on it
        if events_filter:
            filters[events_filter].click()
        # Get a dictionary of events from the 'accordions_list' on the site's home tab content
        events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        # Loop through events in reverse order
        for event_name, event in reversed(events.items()):
            # Check if "VIRTUAL" is not in the 'event_name'
            if "VIRTUAL" not in event_name.upper():
                runners = event.runners.items_as_ordered_dict
                # Ensure that runners exist for this event
                self.assertTrue(runners, msg=f'No runners found in racing card "{event_name}"')
                # Get the first runner and its name
                runner_name, runner = list(runners.items())[0]
                runner.scroll_to()
                # Check if the runner's bet button is enabled
                if not runner.bet_button.is_enabled(expected_result=False):
                    continue
                # Add the runner to the quick bet
                self.add_to_quick_bet(runners=runners)
                # If there are three or more runner names in the list, exit the loop
                if len(self.runner_names) >= 3:
                    break
        # If there is more than one runner name in the list
        if len(self.runner_names) > 1:
            # Verify that the bet slip counter changes to the number of runners
            self.verify_betslip_counter_change(expected_value=len(self.runner_names))
            # Click on the bet slip counter in the site's header
            self.site.header.bet_slip_counter.click()
            # Place bets on all available stakes with each-way option
            self.__class__.bet_info = self.place_bet_on_all_available_stakes(each_way=True)
            # Check if the bet receipt is displayed
            self.check_bet_receipt_is_displayed()
