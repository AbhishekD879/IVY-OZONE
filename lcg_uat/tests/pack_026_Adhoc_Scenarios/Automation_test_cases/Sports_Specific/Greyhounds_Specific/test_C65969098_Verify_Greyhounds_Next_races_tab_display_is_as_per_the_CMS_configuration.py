import re
from datetime import datetime, timedelta
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
import voltron.environments.constants as vec
from tzlocal import get_localzone
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import do_request, get_response_url


def clean_string(name):
    # Use regular expression to remove special characters and extra spaces
    cleaned_string = re.sub(r'[^A-Za-z0-9: ]', '', name)
    return ' '.join(cleaned_string.split())


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.greyhounds
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969098_Verify_Greyhounds_Next_races_tab_display_is_as_per_the_CMS_configuration(Common):
    """
    TR_ID: C65969098
    NAME: Verify Greyhounds Next races tab display is as per the CMS configuration.
    DESCRIPTION: This test case validates the data in Greyhounds Next Races tab is as per the CMS configuration.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    timezone = str(get_localzone())

    def formate_time(self, date_time):
        # Convert the string to a datetime object
        dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        # Add one hour to the datetime
        if self.timezone.upper() == 'EUROPE/LONDON':
            utc = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%H:%M', url_encode=False)
            europe_london = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%H:%M', url_encode=False,
                                                    tz_region='EUROPE/LONDON')
            europe_london = datetime.strptime(europe_london, '%H:%M')
            utc_time = datetime.strptime(utc, '%H:%M')
            time_difference = utc_time - europe_london
            if time_difference.total_seconds() / 3600 >= 1:
                dt_plus_one_hour = dt + timedelta(hours=1)
                return dt_plus_one_hour.strftime('%H:%M')
        # Extract the time as a string in HH:MM format from the new datetime
        return dt.strftime('%H:%M')

    def get_ss_next_races_event(self):
        event_dict = {
            "ALL": {},
            "VIRTUAL": {},
            "UK&IRISH": {},
            "INTERNATIONAL": {}
        }
        # Get the URL for fetching event data
        actual_url = get_response_url(self, url='/NextNEventToOutcomeForClass')
        # If the URL is not available, refresh the page and try again
        if not actual_url:
            self.device.refresh_page()
            self.site.wait_content_state('Greyhound')
            actual_url = get_response_url(self, url='/NextNEventToOutcomeForClass')

        self.assertTrue(actual_url, 'Next Races SS URL is not present in performance log(from network call)')
        # Initialize dictionaries to store event details
        event_name_dict = {}
        uk_events_dict = {}
        international_events_dict = {}
        virtual_events_dict = {}
        # Fetch event data from the URL response
        response = do_request(method='GET', url=actual_url)
        # Process event data and populate dictionaries
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            # Check if the event should be shown in next races or if it's a special event (classId is 226)
            if 'NE' in event['event']['typeFlagCodes'] or '226' not in event['event']['classId']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                event_name_dict[event_name] = {
                    'name': clean_string(event['event']['name']).upper().strip(),
                    'ss_name': event['event']['name'],
                    "event": event['event']
                }
            # Check for UK events that are not special (typeFlagCodes does not contain 'SP')
            if 'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                uk_events_dict[event_name] = {
                    'name': clean_string(event['event']['name']).upper().strip(),
                    'ss_name': event['event']['name'],
                    "event": event['event']
                }
            # Check for international events
            if 'INT' in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName']).strip()}".upper()
                international_events_dict[event_name] = {
                    'name': clean_string(event['event']['name']).upper().strip(),
                    'ss_name': event['event']['name'],
                    "event": event['event']
                }
            # Check for virtual events
            if 'VR' in event['event']['typeFlagCodes']:
                event_name = f"{self.formate_time(event['event']['startTime']).strip()} {clean_string(event['event']['typeName'])}".upper().strip()
                virtual_events_dict[event_name] = {
                    'name': clean_string(event['event']['name']).upper().strip(),
                    'ss_name': event['event']['name'],
                    "event": event['event']
                }
        event_dict['ALL'] = event_name_dict
        event_dict['VIRTUAL'] = virtual_events_dict
        event_dict['UK&IRISH'] = uk_events_dict
        event_dict['INTERNATIONAL'] = international_events_dict
        return event_dict

    # C65949620
    @property
    def device_width(self) -> int:
        return int(self.device.driver.execute_script("return window.innerWidth"))

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" tab should be enabled in CMS (CMS -&gt; System Configuration -&gt; Structure -&gt; GreyhoundNextRacesToggle-&gt; nextRacesTabEnabled)
        PRECONDITIONS: In '**numberOfEvents**' (for Greyhound)enter some number -&gt; Press 'Submit'
        PRECONDITIONS: In '**Number of Selections**' (for Greyhound)enter some number -&gt; Press 'Submit'
        PRECONDITIONS: ('8' option should be set by default)
        PRECONDITIONS: Load Oxygen application.
        PRECONDITIONS: Race events are available for the current day.
        PRECONDITIONS: Navigate to Greyhounds page.
        """
        if tests.settings.brand == "bma":
            self.cms_config.update_system_configuration_structure(config_item='NextRacesToggle',
                                                                  field_name='nextRacesTabEnabled',
                                                                  field_value=True)
            self.cms_config.update_system_configuration_structure(config_item='NextRacesToggle',
                                                                  field_name='nextRacesComponentEnabled',
                                                                  field_value=True)
        else:
            self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRacesToggle',
                                                                  field_name='nextRacesTabEnabled',
                                                                  field_value=True)
            self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRacesToggle',
                                                                  field_name='nextRacesComponentEnabled',
                                                                  field_value=True)
        self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                              field_name='numberOfEvents',
                                                              field_value=12)
        self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                              field_name='numberOfSelections',
                                                              field_value=3)

    def test_001_load_the_oxygen_app_page_and_verify_the_availability_of_the_next_races_tab_on_greyhounds(self):
        """
        DESCRIPTION: Load the Oxygen app page and verify the availability of the "Next Races" tab on Greyhounds.
        EXPECTED: LADBROKES
        EXPECTED: "Next Races" tab is displayed on Greyhounds
        EXPECTED: CORAL
        EXPECTED: "Next Races" tab is not displayed on Greyhounds
        EXPECTED: Instead Next Races Module is seen in "Today" Tab
        """
        self.site.login()
        self.site.open_sport("Greyhounds")
        self.__class__.next_race_module = vec.racing.NEXT_RACES if self.brand == 'bma' and self.device_type == 'desktop' else vec.racing.NEXT_RACES.upper()
        if tests.settings.brand == "bma":
            if self.device_type == "mobile":
                tabs = self.site.greyhound.tabs_menu.items_as_ordered_dict
                self.assertIn("TODAY", tabs.keys(), msg="Next Races tab is not available on Greyhounds SLP")
                tabs.get("TODAY").click()

                sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                self.assertIn(self.next_race_module, sections.keys(), msg=f"{self.next_race_module} tab is not available on Greyhounds SLP")
            else:
                el = self.site.greyhound.tab_content.accordions_list
                if self.device_width <= 1280:
                    display_property = el.css_property_value('display')
                    self.assertEqual(display_property, "block",
                                     msg="Next races Section is not displayed below 'Today's' tab")
                else:
                    display_property = el.css_property_value('display')
                    self.assertEqual(display_property, "flex",
                                     msg="Next races Section is not displayed Beside 'Today's' tab")
                sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                self.assertIn("Next Races", sections.keys(),
                              msg="Next Races tab is not available on Greyhounds SLP")
        else:
            greyhound_tabs = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertIn(self.next_race_module, greyhound_tabs.keys(), msg="Next Races tab is not available on Greyhounds SLP")

    def test_002_in_ladbrokes_tap_on_next_races_tabin_coral_tap_on_today_tab(self):
        """
        DESCRIPTION: In LADBROKES: Tap on "Next Races" tab
        DESCRIPTION: In CORAL: Tap on "TODAY" Tab
        EXPECTED: LADBROKES
        EXPECTED: "Next Races" tab is selected and highlighted
        EXPECTED: Data is loaded successfully.
        EXPECTED: CORAL
        EXPECTED: "Next Races" Module is loaded in "TODAY" Tab
        """
        # Covered in Step 1

    def test_003_in_ladbrokes_verify_next_races_tab_layoutin_coral_verify_next_races_module_layout(self):
        """
        DESCRIPTION: In LADBROKES: Verify "Next Races" tab layout
        DESCRIPTION: In CORAL: Verify "Next Races" Module layout
        EXPECTED: LADBROKES
        EXPECTED: Event cards are displayed one by one as the list (The number of events depends on CMS configurations)
        EXPECTED: CORAL
        EXPECTED: For Mobile and Tablet, 'Next Races' module is displayed below 'Today's' tab &amp;gt; 'By meeting' switcher.
        EXPECTED: For Desktop :
        EXPECTED: For screen width &amp;gt; 970 px, 1025px, Next Races module is shown in line with Races Grids in the main display area.
        EXPECTED: For screen width 1280px, 1600px, Next Races module is displayed on the second column of the display area.
        """
        # Covered in Step 1

    def test_004_verify_event_cards_layout(self):
        """
        DESCRIPTION: Verify 'Event Cards' layout
        EXPECTED: Event cards are displayed one by one as the list
        EXPECTED: 'Event Card' consists of:
        EXPECTED: Header
        EXPECTED: Subheader
        EXPECTED: Event card main body
        """
        # Covered in Step 8

    def test_005_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: 'Event Card' header consists of:
        EXPECTED: Event name in the next format: 'HH:MM typeName'(corresponds to 'typeName' and 'startTime' in SS response)
        EXPECTED: 'More' link with chevron
        """
        # Covered in Step 8

    def test_006_verify_event_card_subheader_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout
        EXPECTED: 'Event Card' subheader consists of:
        EXPECTED: 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (taken from SS response and correspond to 'eachWayFactorNum', 'eachWayFactorDen' and 'eachWayPlaces' attributes )
        EXPECTED: 'Signposting Promotion' icon (if one or all of 'drilldownTagNames="EVFLAGEPR,EVFLAGFI,EVFLAGMB,EVFLAGBBL" attributes are received in SS response)
        EXPECTED: 'CashOut' icon is shown on the right (if the event has 'cashoutAvail'='Y' in SS response)
        EXPECTED: 'WATCH' icon
        """
        # Covered in Step 8

    def test_007_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: 'Event Card' body consists of:
        EXPECTED: 1.Runner Number (taken from 'runnerNumber' section in SS response)
        EXPECTED: 2.Silk (depends on runner number)
        EXPECTED: 3.Greyhounds Name (taken from 'name' section in SS response)
        EXPECTED: 4.Trainer Name
        EXPECTED: 5.Form Data
        EXPECTED: 6.'Price/Odds' button
        """
        # Covered in Step 8

    def test_008_in_desktop_verify_more_link_is_displayedin_mobile__verify_see_all_link_is_displayed(self):
        """
        DESCRIPTION: In Desktop: Verify 'More' link is displayed.
        DESCRIPTION: In Mobile:  Verify 'See All' link is displayed.
        EXPECTED: Link is displayed at the 'Event Card' header.
        EXPECTED: Link is displayed for each event in the 'Next Races' module.
        EXPECTED: Link is aligned to the right.
        """
        self.device.refresh_page()
        event_dict = self.get_ss_next_races_event()
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, 'Accordions are not available')
        next_races = sections.get(self.next_race_module)
        self.assertTrue(next_races, 'NEXT RACES is not available')
        race_cards = next_races.items_as_ordered_dict
        self.assertTrue(race_cards, 'RACE CARDS are not available')
        first_race_card_name, first_race_card = race_cards.popitem()
        required_event_name, required_event = next(
            ((key, value) for key, value in event_dict['ALL'].items() if
             value['ss_name'].upper() == first_race_card_name.upper() or key == first_race_card_name.upper()),
            (None, None))

        if not required_event:
            self.test_008_in_desktop_verify_more_link_is_displayedin_mobile__verify_see_all_link_is_displayed()

        # Header Verification
        self.assertIn(first_race_card_name.upper(), [required_event.get("ss_name").upper(), required_event_name],
                      msg="Race Card Name Does Not"
                          f"Match Actual:"
                          f"{first_race_card_name.upper()} "
                          f"Expected:{required_event.get('ss_name').upper()}")

        if "VR" in required_event.get('event').get('typeFlagCodes').upper():
            first_race_card.scroll_to()
            self.assertTrue(first_race_card.is_virtual,
                            msg="Virtual Logo is not Shown Even though required event typeFlagCodes is 'VR"
                                f" Actual ss typeFlagCode {required_event.get('event').get('typeFlagCodes').upper()}")

        # SubHeader Verification
        if self.device_type == "mobile":
            required_event_market = required_event.get('event').get('children')[0]['market']

            # Each Way Term
            is_each_way_available = required_event_market.get('isEachWayAvailable')
            if is_each_way_available == "true":
                numerator = required_event_market.get('eachWayFactorNum')
                denominator = required_event_market.get('eachWayFactorDen')
                each_way_places = int(required_event_market.get('eachWayPlaces'))
                is_each_term = first_race_card.has_each_way_terms()
                self.assertTrue(is_each_term,
                                msg="Each Way Term Not Displayed Even though isEachWayAvailable Flag is True")
                actual_each_way_term = first_race_card.each_way_terms
                expected_each_way_term = f'EW: {numerator}/{denominator} Odds - Places {"-".join([str(i) for i in range(1, each_way_places + 1)])}'
                self.assertEqual(actual_each_way_term.upper(), expected_each_way_term.upper(),
                                 msg=f"{actual_each_way_term} does not match expected {expected_each_way_term}")
            # CashOut
            is_cashout_available = required_event_market.get('cashoutAvail')
            if is_cashout_available == 'Y':
                has_cashout_label = first_race_card.has_cashout_label()
                self.assertTrue(has_cashout_label,
                                msg="Cashout label is not found even though cashout Avail Flag is True")

        # Event Card Verification
        all_selection = first_race_card.items_as_ordered_dict
        expected_selection = {outcome['outcome']['name']: outcome['outcome'] for outcome in
                              required_event['event']['children'][0]['market']['children']}
        for selection_name, selection in all_selection.items():
            ss_outcome = expected_selection.get(selection_name, None)
            selection.scroll_to()
            if ss_outcome:
                # Price odd validation
                try:
                    price = ss_outcome.get('children')[0].get('price')
                    dec = price.get('priceDec')
                    fact = f"{price.get('priceNum')}/{price.get('priceDen')}"
                    actual_price = selection.bet_button.outcome_price_text
                    self.assertIn(actual_price, [dec, fact], msg=f"Prices Does Not Match For Selection {selection_name}"
                                                                 f" Actual Odds {actual_price}, "
                                                                 f"expected odds {[dec, fact]}")
                except TypeError:
                    price = "SP"
                    actual_price = selection.bet_button.outcome_price_text
                    self.assertEqual(actual_price, price, msg=f"Prices Does Not Match For Selection {selection_name}"
                                                              f" Actual Odds {actual_price}, expected odds {price}")

                # RunnerInfo Validation
                runner_info = selection.runner_info
                runner_name = runner_info.name_section.horse_name
                self.assertEqual(runner_name, ss_outcome.get('name'), msg=f"Runner Hound Name {runner_name}"
                                                                          f" does not match "
                                                                          f"ss_outcome name {ss_outcome.get('name')}")

        # More Link Verification
        # if len(expected_selection) > 3:
        more_link = first_race_card.more_link
        self.assertTrue(more_link, msg=f"More Link Is Not Present even though "
                                       f"more than 3 selection present"
                                       f"Selections : {expected_selection}")
        more_link.scroll_to()
        more_link.click()

        if "VR" in required_event.get('event').get('typeFlagCodes').upper():
            self.site.wait_content_state(state_name="virtual-sports")
        else:
            self.site.wait_content_state(state_name='GREYHOUNDEVENTDETAILS')

        if self.device_type != "mobile":
            self.site.sports_page.back_button_click()
        else:
            self.site.back_button_click()

        self.site.wait_content_state(state_name="GREYHOUNDS")

    def test_009_tap_on_more_link(self):
        """
        DESCRIPTION: Tap on 'More' link.
        EXPECTED: The user is taken to the particular event details page.
        """
        # Covered in Step 8

    def test_010_tap_on_the_back_button(self):
        """
        DESCRIPTION: Tap on the 'Back' button.
        EXPECTED: The previously visited page is opened.
        """
        # Covered in Step 8
